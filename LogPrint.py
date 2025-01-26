from colorama import Fore, Style, Back


def print_green(message_type="INFO", text=""):
    print(f"{message_type} --> ", end="")
    print(Fore.GREEN + f"{text}")
    print(Style.RESET_ALL, end="")


def print_red(message_type="ERROR", text=""):
    print(f"{message_type} --> ", end="")
    print(Fore.RED + f"{text}")
    print(Style.RESET_ALL, end="")

def print_yellow(message_type="WARNING", text=""):
    print(f"{message_type} --> ", end="")
    print(Fore.YELLOW + f"{text}")
    print(Style.RESET_ALL, end="")


def print_uncolored(message_type, text):
    print(f"{message_type} --> {text}")


def print_cyan(message_type="WARNING", text="", text_colored=None, end="\n"):
    print(f"{message_type} --> ", end="")
    if text_colored is None:
        print(Fore.CYAN + f"{text}", end=end)
    else:
        print(text, end="")
        print(Fore.CYAN + f"{text_colored}", end=end)
    print(Style.RESET_ALL, end="")


def print_magenta(message_type, text):
    print(f"{message_type} --> ", end="")
    print(Fore.MAGENTA + f"{text}")
    print(Style.RESET_ALL, end="")

def print_blue(message_type, text):
    print(f"{message_type} --> ", end="")
    print(Fore.BLUE + f"{text}")
    print(Style.RESET_ALL, end="")

def print_blue_line():
    print(Back.BLUE + "")
    print(Style.RESET_ALL, end="")

def print_title(title):
    print(Fore.MAGENTA + f"{title}")
    print(Style.RESET_ALL, end="")
