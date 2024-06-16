from commands.commands import Commands
from colors.colors import Colors
from bs4 import BeautifulSoup
import requests
import time
import sys
import re

REGEX_EMAIL = r"[a-zA-Z0-9._+!#$&%]{1,64}@[a-zA-Z0-9.]*\.[a-zA-Z]{2,3}"

LOGO = (
    Colors.BRIGHT_RED                         +
    r" ___   ___ __ _ _ __ _ _ __  ___ _ _ " + "\n" +
    r"/ -_) (_-</ _| '_/ _` | '_ \/ -_) '_|" + "\n" +
    r"\___|_/__/\__|_| \__,_| .__/\___|_|  " + "\n" +
    r"   |___|              |_|            " + "\n" +
    Colors.RESET
)

def help_menu():
    print("Usage:\n<url> - website url")

def get_website_emails(website):
    req = requests.get(website)

    if req.status_code == 200:
        soup = BeautifulSoup(req.text, "html.parser")
        soup_text = soup.get_text()

        website_emails = re.findall(REGEX_EMAIL, soup_text)

        return website_emails

def main():
    args = sys.argv[1:]

    if len(args) != 1:
        help_menu()
        sys.exit(1)

    url = args[0]

    valid_url = url.startswith(("https://", "http://"))

    if not valid_url:
        print(Commands.Error("Url address is not correct! Enter a valid url like: https://example.com"))
        sys.exit(1)

    try:
        req = requests.get(url)
    except:
        print(Commands.Error("Error while trying to connect to the website!"))
        sys.exit(1)

    if req.status_code != 200:
        print(Commands.Error("Error while scraping the page!"))
        sys.exit(1)

    soup = BeautifulSoup(req.text, "html.parser")
    soup_text = soup.get_text()

    print(LOGO)

    url_protocol = url.split("://")[0]
    url_domain = url.split("://")[1].split("/")[0]

    websites = []
    for link in soup.find_all("a"):
        link_href = link.get("href")

        if link_href != None and link_href.startswith(f"{url_protocol}://{url_domain}"):
            if link_href != url and link_href not in websites:
                websites.append(link_href)

    print(f"{Colors.BOLD}{Colors.BRIGHT_RED}Websites:{Colors.RESET}")

    emails = []
    emails.extend(re.findall(REGEX_EMAIL, soup_text))

    for website in websites:
        try:
            website_emails = get_website_emails(website)

            emails.extend(website_emails)

            print(f"[{Colors.BOLD}{Colors.BRIGHT_RED}+{Colors.RESET}] {Colors.BRIGHT_RED}{website}{Colors.RESET}")
        except:
            continue

    emails = list(set(emails)) # to remove repeated email addresses

    print(f"\n{Colors.BOLD}{Colors.BRIGHT_BLUE}Emails:{Colors.RESET}")

    for i, email in enumerate(emails):
        print(f"[{Colors.BOLD}{Colors.BRIGHT_BLUE}{i + 1}{Colors.RESET}] {Colors.BRIGHT_BLUE}{email}{Colors.RESET}")

    print("\n" + Commands.Success(f"Scraped a total of {len(emails)} emails from {len(websites)} sites\n"))

    save_emails = input(Commands.Question("Save emails to file? (Y/n): "))

    if save_emails.lower() in ["y", "yes"]:
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%d-%m-%Y")

        with open(f"e_scraper({current_time}_{current_date}).txt", "w") as file:
            file.write(f"[{current_time}, {current_date}]\n\n")
            file.write(f"Emails ({len(emails)} total):\n\n")

            for email in emails:
                file.write(f"{email}\n")

if __name__ == "__main__":
    main()