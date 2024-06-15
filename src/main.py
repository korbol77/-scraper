from colors.colors import Colors
from bs4 import BeautifulSoup
import requests
import time
import sys
import re

REGEX_EMAIL = r"[a-zA-Z0-9._+!#$&%]{1,64}@[a-zA-Z0-9.]*\.[a-zA-Z]{2,3}"

def help_menu():
    print("Usage:\n<url> - website url")

def get_website_emails(website):
    req = requests.get(website)

    if req.status_code == 200:
        soup = BeautifulSoup(req.text, "html.parser")
        soup_text = soup.get_text()

        website_emails = re.findall(REGEX_EMAIL, soup_text)

        return website_emails

args = sys.argv[1:]

if len(args) != 1:
    help_menu()
    sys.exit(1)

url = args[0]

valid_url = url.startswith(("https://", "http://"))

if not valid_url:
    print(f"{Colors.BRIGHT_RED}Url address is not correct!\nEnter a valid url like: https://example.com{Colors.RESET}")
    sys.exit(1)

try:
    req = requests.get(url)
except:
    print(f"{Colors.BRIGHT_RED}Error while trying to connect to the website!{Colors.RESET}")
    sys.exit(1)

if req.status_code != 200:
    print(f"{Colors.BRIGHT_RED}Error while scraping the page!{Colors.RESET}")
    sys.exit(1)

soup = BeautifulSoup(req.text, "html.parser")
soup_text = soup.get_text()

print(f"{Colors.BOLD}{Colors.UNDERLINE}{Colors.BRIGHT_RED}[e_scraper]{Colors.RESET}\n")

url_protocol = url.split("://")[0]
url_domain = url.split("://")[1].split("/")[0]

websites = []
for link in soup.find_all("a"):
    link_href = link.get("href")

    if link_href != None and link_href.startswith(f"{url_protocol}://{url_domain}"):
        if link_href != url:
            websites.append(link_href)

websites = list(set(websites)) # to remove repeated websites

print(f"{Colors.BOLD}{Colors.BRIGHT_MAGENTA}Websites:{Colors.RESET}")

emails = []
emails.extend(re.findall(REGEX_EMAIL, soup_text))

for website in websites:
    try:
        website_emails = get_website_emails(website)

        emails.extend(website_emails)

        print(f"  ({Colors.BOLD}{Colors.BRIGHT_MAGENTA}+{Colors.RESET}) {Colors.BRIGHT_MAGENTA}{website}{Colors.RESET}")
    except:
        continue

emails = list(set(emails)) # to remove repeated email addresses

print(f"\n{Colors.BOLD}{Colors.BRIGHT_BLUE}Emails:{Colors.RESET}")

for i, email in enumerate(emails):
    print(f"  ({Colors.BOLD}{Colors.BRIGHT_BLUE}{i + 1}{Colors.RESET}) {Colors.BRIGHT_BLUE}{email}{Colors.RESET}")

save_emails = input("\nSave emails to file? (Y/n): ")

if save_emails.lower() in ["y", "yes"]:
    current_time = time.strftime("%H:%M:%S")
    current_date = time.strftime("%d-%m-%Y")

    with open(f"e_scraper({current_time}_{current_date}).txt", "w") as file:
        file.write(f"[{current_time}, {current_date}]\n\n")
        file.write(f"Emails ({len(emails)} total):\n\n")

        for email in emails:
            file.write(f"{email}\n")