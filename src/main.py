from colors.colors import Colors
import requests
import time
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

print(f"{Colors.BOLD}{Colors.UNDERLINE}{Colors.BRIGHT_RED}<-< e_scraper >->{Colors.RESET}\n")

print(f"{Colors.BOLD}{Colors.BRIGHT_GREEN}<<< Website >>>{Colors.RESET}")

print(f"  ({Colors.BOLD}{Colors.BRIGHT_MAGENTA}+{Colors.RESET}) {Colors.BRIGHT_MAGENTA}{url}{Colors.RESET}")

data = req.text
emails = re.findall(REGEX, data)
emails = list(set(emails)) # to remove repeated email addresses 

print(f"\n{Colors.BOLD}{Colors.BRIGHT_GREEN}<<< Emails >>>{Colors.RESET}")

for i, email in enumerate(emails):
    print(f"  ({Colors.BOLD}{Colors.BRIGHT_BLUE}{i + 1}{Colors.RESET}) {Colors.BRIGHT_BLUE}{email}{Colors.RESET}")

save_emails = input(f"\nSave emails to file? (y/n): ")

if save_emails == "y":
    current_time = time.strftime("%H:%M:%S_%d-%m-%Y")

    with open(f"e_scraper({current_time}).txt", "w") as file:
        for email in emails:
            file.write(f"{email}\n")