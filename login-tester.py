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
    """Tests pairs of usernames and passwords against a target login form."""
    results = []
    
    for username, password in credentials:
        # Example payload dictionary (adjust form field names based on the target app)
        payload = {
            "user_login": username,
            "login_password": password
        }
        
        try:
            # allow_redirects=False lets us catch success redirects vs 200 re-renders
            response = requests.post(target_url, data=payload, timeout=5, allow_redirects=False)
            status_code = response.status_code
            
            # A 302 redirect often indicates a successful login shifting to a dashboard
            results.append((username, password, status_code))
        except requests.exceptions.RequestException:
            pass
            
    return results

def main():
    parser = argparse.ArgumentParser(description="Lightweight Credential Tester for Web Auditing")
    parser.add_argument("url", help="Target login URL (e.g., http://zero.webappsecurity.com/login.html)")
    args = parser.parse_args()

    console.print(f"[bold cyan][+] Testing default credentials against:[/bold cyan] {args.url}")

    with console.status("[bold green]Submitting login attempts..."):
        discovered = test_credentials(args.url, DEFAULT_CREDS)

    if discovered:
        table = Table(title="Credential Audit Results")
        table.add_column("Username", style="bold cyan")
        table.add_column("Password", style="bold yellow")
        table.add_column("Status Code", style="bold")

        for user, pwd, status in discovered:
            color = "green" if status == 302 else "red"
            table.add_row(user, pwd, f"[{color}]{status}[/{color}]")

        console.print(table)
    else:
        console.print("[bold yellow][-] No responses received from target.[/bold yellow]")

if __name__ == "__main__":
    main()
