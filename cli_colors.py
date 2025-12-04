# utils/cli_colors.py

import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("\033[92m   ╔═════════════════════════════════════════════════════════════════════════╗\033[0m")
    print("\033[93m   ║ 🐍 ScanacondaNmap – Python-powered port scanning with a deadly squeeze. ║\033[0m")
    print("\033[92m   ╚═════════════════════════════════════════════════════════════════════════╝\033[0m\n")

def good_bye():
    print("\033[93m  🐍 Thank you for using ScanacondaNmap! Bye for now.\033[0m\n")

def end_scan_border():
    print("\033[92m  🐍════════════════════SCAN═══════COMPLETE═══════════════"
          "═══════🐍\033[0m\n")

# ANSI color codes
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
ORANGE = "\033[38;5;208m"
RESET = "\033[0m"

def print_open(port, target):
    print(f"{RED}[OPEN]{RESET} Port {port} on {target}")

def print_closed_fast(port, target):
    print(f"{GREEN}[CLOSED]{RESET} Port {port} on {target}")

def print_closed(port, target):
    print(f"{GREEN}[CONFIRMED CLOSED]{RESET} Port {port} on {target}")

def print_filtered(port, target):
    print(f"{YELLOW}[FILTERED or CLOSED]{RESET} Port {port} on {target}")

# utils/cli_colors.py

def print_summary(open_map, closed_map, filtered_map, start_time, path):
    print("\n=== Scan Summary ===")
    print(f"Started: {start_time}")
    for target in open_map:
        print(f"\nTarget: {target}")
        print(f"Open ports: {open_map[target]}")
        print(f"Closed ports: {closed_map[target]}")
        print(f"Filtered ports: {filtered_map[target]}")
    print(f"\n\t\t💥Results saved to: {path}💥")
    end_scan_border()


def timestamp_now():
    import datetime
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")