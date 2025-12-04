# utils/scanner.py

import socket
import errno
import select
from utils.cli_colors import print_open, print_closed, print_closed_fast, print_filtered, RED, RESET

def scan_tcp_port_fast(target, port, timeout=0.5):
    #Fast scan: only open/closed, no filtered classification.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    try:
        result = sock.connect_ex((target, port))
        sock.close()
        if result == 0:
            return "open"
        elif result in (errno.ECONNREFUSED, 10061):  # Windows closed
            return "closed"
        else:
            return "closed"  # lump everything not-open into closed
    except Exception:
        sock.close()
        return "closed"

def scan_tcp_port_slow(target, port, quick_timeout=0.4, wait_timeout=4.5):
    #Slow scan: quick probe first, then extended wait if inconclusive.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setblocking(False)
    sock.settimeout(quick_timeout)

    try:
        result = sock.connect_ex((target, port))

        # Immediate classification
        if result == 0:
            sock.close()
            return "open"
        elif result in (errno.ECONNREFUSED, 10061):
            sock.close()
            return "closed"

        # If inconclusive, wait longer
        ready = select.select([], [sock], [], wait_timeout)
        if ready[1]:
            err = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
            sock.close()
            if err == 0:
                return "open"
            elif err in (errno.ECONNREFUSED, 10061):
                return "closed"
            else:
                return "filtered"
        else:
            sock.close()
            return "filtered"

    except Exception:
        sock.close()
        return "filtered"


# utils/scanner.py
def perform_scan(targets, ports, speed="fast"):
    """
    Perform scan across targets and ports using fast or slow mode.
    Interrupt-aware: catches KeyboardInterrupt and returns partial results.
    """
    open_map, closed_map, filtered_map = {}, {}, {}

    try:
        for target in targets:
            open_map[target], closed_map[target], filtered_map[target] = [], [], []

            for port in ports:
                if speed == "fast": #fast scan
                    status = scan_tcp_port_fast(target, port)
                    if status == "open":
                        print_open(port, target)
                        open_map[target].append(port)
                    elif status == "closed":
                        print_closed_fast(port, target)
                        closed_map[target].append(port)

                else:  # slow scan
                    status = scan_tcp_port_slow(target, port)
                    if status == "open":
                        print_open(port, target)
                        open_map[target].append(port)
                    elif status == "closed":
                        print_closed(port, target)
                        closed_map[target].append(port)
                    elif status == "filtered":
                        print_filtered(port, target)
                        filtered_map[target].append(port)

    except KeyboardInterrupt:
        print(f"\n{RED}❌ {RESET}Scan interrupted during perform_scan. Returning partial results...")

    # single return at the end
    return open_map, closed_map, filtered_map