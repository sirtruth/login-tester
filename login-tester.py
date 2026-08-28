import sys
import argparse
import requests
from rich.console import Console
from rich.table import Table

console = Console()

DEFAULT_CREDS = [
    ("admin", "admin"),
    ("admin", "password"),
    ("root", "root"),
    ("administrator", "password"),
    ("test", "test")
]

def test_credentials(target_url, credentials):
    """Tests credentials, tracks attempted endpoints, and analyzes responses."""
    results = []
    
    for username, password in credentials:
        payload = {
            "user_login": username,
            "login_password": password
        }
        
        try:
            response = requests.post(target_url, data=payload, timeout=5, allow_redirects=True)
            status_code = response.status_code
            
            # Capture the exact final URL endpoint after any redirects
            attempted_endpoint = response.url
            
            response_text_lower = response.text.lower()
            failure_indicators = ["invalid", "failed", "incorrect", "wrong", "error", "denied"]
            is_failed = any(indicator in response_text_lower for indicator in failure_indicators)
            
            if status_code == 200 and not is_failed:
                result_type = "SUCCESS (200)"
            elif status_code == 302:
                result_type = "REDIRECT (302)"
            elif is_failed:
                result_type = "FAILED (Invalid)"
            else:
                result_type = f"CHECK ({status_code})"
                
            results.append((username, password, status_code, attempted_endpoint, result_type))
        except requests.exceptions.RequestException:
            results.append((username, password, "N/A", target_url, "CONNECTION ERROR"))
            
    return results

def main():
    parser = argparse.ArgumentParser(description="Smart Credential Tester with Endpoint Tracking")
    parser.add_argument("url", help="Target login URL (e.g., http://zero.webappsecurity.com/login.html)")
    args = parser.parse_args()

    console.print(f"[bold cyan][+] Auditing target credentials on:[/bold cyan] {args.url}")

    with console.status("[bold green]Tracking request endpoints..."):
        discovered = test_credentials(args.url, DEFAULT_CREDS)

    if discovered:
        table = Table(title="Credential Audit Results with Target Endpoints")
        table.add_column("Username", style="bold cyan")
        table.add_column("Password", style="bold yellow")
        table.add_column("Status", style="bold")
        table.add_column("Endpoint Hit", style="bold blue")
        table.add_column("Verdict", style="bold")

        for user, pwd, status, endpoint, verdict in discovered:
            if "SUCCESS" in verdict or "REDIRECT" in verdict:
                v_color = "green"
            elif "FAILED" in verdict:
                v_color = "red"
            else:
                v_color = "yellow"
                
            table.add_row(user, pwd, str(status), endpoint, f"[{v_color}]{verdict}[/{v_color}]")

        console.print(table)
    else:
        console.print("[bold yellow][-] No responses received from target.[/bold yellow]")

if __name__ == "__main__":
    main()
