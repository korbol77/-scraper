from colors.colors import Colors

class Commands:
    def Error(text):
        return f"[{Colors.BRIGHT_RED}!{Colors.RESET}] {Colors.BRIGHT_RED}{text}{Colors.RESET}"
    def Success(text):
        return f"[{Colors.BRIGHT_GREEN}+{Colors.RESET}] {Colors.BRIGHT_GREEN}{text}{Colors.RESET}"
    def Question(text):
        return f"[{Colors.BRIGHT_BLUE}?{Colors.RESET}] {text}"