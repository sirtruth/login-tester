import sys
import argparse
import requests
from rich.console import Console
from rich.table import Table

console = Console()

# Common default credentials to test
DEFAULT_CREDS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("root", "root"),
    ("administrator", "password"),
    ("test", "test")
]

def test_credentials(target_url, credentials):
    """Tests pairs of usernames and passwords and checks response content for success indicators."""
    results = []
    
    for username, password in credentials:
        payload = {
            "user_login": username,
            "login_password": password
        }
        
        try:
            # allow_redirects=True to follow potential login redirection chains
            response = requests.post(target_url, data=payload, timeout=5, allow_redirects=True)
            status_code = response.status_code
            
            # Check response body text for common failure vs success strings
            response_text_lower = response.text.lower()
            
            # Heuristic check: if failure strings are missing, it might be a success
            failure_indicators = ["invalid", "failed", "incorrect", "wrong", "error", "denied"]
            is_failed = any(indicator in response_text_lower for indicator in failure_indicators)
            
            # Determine outcome status label
            if status_code == 200 and not is_failed:
                result_type = "SUCCESS (200)"
            elif status_code == 302:
                result_type = "REDIRECT (302)"
            elif is_failed:
                result_type = "FAILED (Invalid)"
            else:
                result_type = f"CHECK ({status_code})"
                
            results.append((username, password, status_code, result_type))
        except requests.exceptions.RequestException:
            results.append((username, password, "N/A", "CONNECTION ERROR"))
            
    return results

def main():
    parser = argparse.ArgumentParser(description="Smart Credential Tester with Response Content Analysis")
    parser.add_argument("url", help="Target login URL (e.g., http://zero.webappsecurity.com/login.html)")
    args = parser.parse_args()

    console.print(f"[bold cyan][+] Auditing target credentials on:[/bold cyan] {args.url}")

    with console.status("[bold green]Analyzing server responses..."):
        discovered = test_credentials(args.url, DEFAULT_CREDS)

    if discovered:
        table = Table(title="Enhanced Credential Audit Results")
        table.add_column("Username", style="bold cyan")
        table.add_column("Password", style="bold yellow")
        table.add_column("Status", style="bold")
        table.add_column("Verdict", style="bold")

        for user, pwd, status, verdict in discovered:
            if "SUCCESS" in verdict or "REDIRECT" in verdict:
                v_color = "green"
            elif "FAILED" in verdict:
                v_color = "red"
            else:
                v_color = "yellow"
                
            table.add_row(user, pwd, str(status), f"[{v_color}]{verdict}[/{v_color}]")

        console.print(table)
    else:
        console.print("[bold yellow][-] No responses received from target.[/bold yellow]")

if __name__ == "__main__":
    main()
