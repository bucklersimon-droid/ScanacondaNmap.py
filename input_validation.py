# utils/input_validation.py

import ipaddress
import socket
from utils.constants import DEFAULT_COMMON_PORTS
from utils.cli_colors import RED, RESET, ORANGE

def expand_ip_range(ip_range_str):
    #Expand a numeric IP range string into a list of IP addresses.
    if "-" not in ip_range_str:
        return [ip_range_str.strip()]

    start_str, end_str = ip_range_str.split("-")
    start_ip = ipaddress.IPv4Address(start_str.strip())
    end_ip = ipaddress.IPv4Address(end_str.strip())

    if int(end_ip) < int(start_ip):
        raise ValueError("End IP must be greater than or equal to start IP")

    return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start_ip), int(end_ip) + 1)]


def get_targets_from_input(user_input):
    #Split comma-separated targets and expand ranges.
    targets = []
    for part in user_input.split(","):
        if part.strip():
            targets.extend(expand_ip_range(part.strip()))
    return targets


def validate_target(target: str) -> str:
    #Validate a single hostname or IP (IPv4/IPv6).
    try:
        socket.getaddrinfo(target, None)  # resolves IPv4/IPv6 or hostname
        return target
    except socket.gaierror:
        print(f"{RED}[ERROR]❌ {RESET}Invalid hostname/IP: {target}")
        return None


def validate_ports(port_input: str) -> list[int]:
    if not port_input.strip():
        return DEFAULT_COMMON_PORTS
    try:
        if "-" in port_input:
            start, end = port_input.split("-")
            start, end = int(start), int(end)
            if not (1 <= start <= 65535 and 1 <= end <= 65535 and start <= end):
                raise ValueError
            return list(range(start, end + 1))
        else:
            ports = int(port_input)
            if not (1 <= ports <= 65535):
                raise ValueError
            return [ports]
    except ValueError:
        print(f"{RED}[ERROR]❌ {RESET}Invalid port input: {port_input}")
        return None


def validate_speed(speed: str) -> str:
    # If blank, default to fast
    if not speed.strip():
        return "fast"
    if speed.lower() in ["fast", "slow"]:
        return speed.lower()
    print(f"{RED}[ERROR]❌ {RESET}Invalid speed option: {speed}")
    return None


def get_user_inputs():
    # Prompt user interactively for inputs and validate them.
    targets = None
    while not targets:
        target_input = input(f"{ORANGE}Enter target IP/hostname (supports ranges and commas): {RESET}").strip()
        try:
            expanded = get_targets_from_input(target_input)
            validated = []
            for t in expanded:
                vt = validate_target(t)
                if vt:
                    validated.append(vt)
            if validated:
                targets = validated
        except ValueError as e:
            print(f"{RED}[ERROR]❌ {RESET}{e}")
            targets = None

    ports = None
    while ports is None:
        port_input = input(f"{ORANGE}Enter port range (e.g. 22 or 1-1024, leave empty for common ports):{RESET} ")
        ports = validate_ports(port_input)

    speed = None
    while speed is None:
        print("Fast scan confirms Open ports, Reports non responding ports as Closed")
        print("Slow scan confirms Open and Closed ports, Reports non responding ports as Filtered")
        speed_input = input(f"{ORANGE}Select scan speed [fast/slow]: {RESET}").strip() or "fast"
        speed = validate_speed(speed_input)

    output_file = None
    while not output_file:
        output_file = input(f"{ORANGE}Enter output filename (default: results.json): ").strip()
        if not output_file:
            output_file = "results.json"
        if not output_file.endswith(".json"):
            print(f"{RED}[ERROR]❌ {RESET}Output filename must end with .json")
            output_file = None

    return {
        "target": targets,      # now a list of validated IPs/hostnames
        "port_list": ports,
        "speed": speed,
        "output": output_file
    }

"""
#input_validation.py

import ipaddress
import socket
import sys
from utils.constants import DEFAULT_COMMON_PORTS
from utils.cli_colors import RED, RESET, ORANGE


def expand_ip_range(ip_range_str): #expand range of IPs to a list of targets
    
    #Expand a numeric IP range string into a list of IP addresses.
    #Example: "192.168.1.10-192.168.1.20"
    
    if "-" not in ip_range_str:
        # single IP, just return it
        return [ip_range_str.strip()]

    start_str, end_str = ip_range_str.split("-")
    start_ip = ipaddress.IPv4Address(start_str.strip())
    end_ip = ipaddress.IPv4Address(end_str.strip())

    if int(end_ip) < int(start_ip):
        raise ValueError("End IP must be greater than or equal to start IP")
    return [str(ipaddress.IPv4Address(ip)) for ip in range(int(start_ip), int(end_ip) + 1)]


def get_targets_from_input(user_input): #seperates list of IPs with ','
    targets = []
    for part in user_input.split(","):
        targets.extend(expand_ip_range(part.strip()))
    return targets


def validate_target(target: str) -> str:
    #Validate hostname or IP (IPv4/IPv6).
    try:
        socket.getaddrinfo(target, None)  # resolves IPv4 
        return target
    except socket.gaierror:
        print(f"{RED}[ERROR]❌ {RESET}Invalid hostname/IP: {target}")
        return None

def validate_ports(port_input: str) -> list[int]:
    #Validate port range or return default common ports.
    if not port_input.strip():
        return DEFAULT_COMMON_PORTS
    try:
        if "-" in port_input: #range of ports
            start, end = port_input.split("-")
            start, end = int(start), int(end)
            if not (1 <= start <= 65535 and 1 <= end <= 65535 and start <= end):
                raise ValueError
            return list(range(start, end + 1))
        else: #single port selected
            ports = int(port_input)
            if not (1 <= ports <= 65535):
                raise ValueError
            return [ports]
    except ValueError:
        print(f"{RED}[ERROR]❌ {RESET}Invalid port input: {port_input}")
        return None #return None re-prompts user

def validate_speed(speed: str) -> str:
    #Validate scan speed option.
    if speed.lower() in ["fast", "slow"]:
        return speed.lower()
    print(f"{RED}[ERROR]❌ {RESET}Invalid speed option: {speed}")
    return None

def get_user_inputs():
    #Prompt user interactively for inputs and validate them.
    target = None
    while not target:
        target_input = input(f"{ORANGE}Enter target IP/hostname: ").strip()
        target = validate_target(target_input)

    ports = None
    while ports is None:
        port_input = input(f"{ORANGE}Enter port range (e.g. 22 or 1-1024, leave empty for common ports): ")
        ports = validate_ports(port_input)

    speed = None
    while speed is None:
        print("Fast scan confirms Open ports, Reports non responding ports as Closed")
        print("Slow scan confirms Open and Closed ports, Reports non responding ports as Filtered")
        speed_input = input(f"{ORANGE}Select scan speed [fast/slow]: ").strip() or "fast"
        speed = validate_speed(speed_input)

    output_file = None
    while not output_file:
        output_file = input(f"{ORANGE}Enter output filename (default: results.json): ").strip()
        if not output_file:
            output_file = "results.json"  # fallback default
        # basic validation: must end with .json
        if not output_file.endswith(".json"):
            print(f"{RED}[ERROR]❌ {RESET}Output filename must end with .json")
            output_file = None

    return {
        "target": target,
        "port_list": ports,
        "speed": speed,
        "output": output_file
    }
"""
    