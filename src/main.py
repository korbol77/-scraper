from colors.colors import Colors
import requests
import sys
import re

REGEX = r"[a-zA-Z0-9._+!#$&%]{1,64}@[a-zA-Z0-9.]*\.[a-zA-Z]{2,3}"

def help_menu():
    print("Usage:\n<url> - website url")

args = sys.argv[1:]

if len(args) != 1:
    help_menu()
    sys.exit(1)

url = args[0]

req = requests.get(url)

if req.status_code != 200:
    print(f"{Colors.BRIGHT_RED}Error while scraping the page!{Colors.RESET}")
    sys.exit(1)

print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}[WEBSITE]{Colors.RESET}")

print(f"  [{Colors.BOLD}+{Colors.RESET}] {Colors.BRIGHT_MAGENTA}{url}{Colors.RESET}")

data = req.text
emails = re.findall(REGEX, data)
emails = list(set(emails)) # to remove repeated email addresses 

print(f"\n{Colors.BOLD}{Colors.BRIGHT_GREEN}[EMAILS]{Colors.RESET}")

for email in emails:
    print(f"  [{Colors.BOLD}+{Colors.RESET}] {Colors.BRIGHT_GREEN}{email}{Colors.RESET}")