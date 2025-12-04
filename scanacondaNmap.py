"""
File: scanaconda.py
Author: Simon Buckler
Purpose: Port scanning tool using Nmap in Python
Development: Began Nov 30, 2025 – Ended [December 4, 2025]
"""

from utils.scanner import perform_scan
from utils.logger import save_results_json, build_results_json
from utils.cli_colors import print_summary, timestamp_now, clear_screen, banner, good_bye, ORANGE
from utils.input_validation import get_user_inputs


def run_scan():
    """Run a single scan and save results."""
    config = get_user_inputs()
    start_time = timestamp_now()
    # Perform scan (interrupts handled inside perform_scan)
    open_map, closed_map, filtered_map = perform_scan(
        config["target"],
        config["port_list"],
        config["speed"]
    )
    # Build results JSON
    results = build_results_json(open_map, closed_map, filtered_map, start_time)
    path = save_results_json(results, filename=config["output"])
    # Print summary
    print_summary(open_map, closed_map, filtered_map, start_time, path)


def main():
    """Main loop: allow user to run multiple scans or exit."""
    while True:
        clear_screen()
        banner()
        run_scan()
        choice = input(f"{ORANGE}\nWould you like to perform another scan? (y/n): ").strip().lower()
        if choice not in ("y", "yes"):
            good_bye()
            break

if __name__ == "__main__":
    main()