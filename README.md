# 🐍 ScanacondaNmap

**Author:** Simon Buckler  
**Purpose:** Internal network TCP port scanner with real-time reporting and JSON logging.  
**Development:** Began November 30, 2025 – Ended December 5, 2025.

ScanacondaNmap 🐍🔍
A Python-based port scanning tool designed for internal network security testing and public URL analysis.
This script helps identify open and filtered ports, logs results in JSON format, and provides real-time feedback in the CLI.

Installation
No external libraries are required — the scanner uses built‑in Python modules only.
ANSI escape codes are used for colored CLI output, which work in most modern terminals (Windows 10/11, macOS, Linux).
Usage
Run the scanner with:


🚀 Features
Distinguishes between open, closed, and filtered ports for clearer results.
• 	Color‑Coded CLI Output
• 	🔴 Open ports flagged in red (only seen where connection refusal is explicitly returned by target)
• 	🟢 Closed ports flagged in green
• 	🟡 Filtered ports flagged in yellow (in many cases this includes closed ports see Note: Limitations below)
• 	JSON Logging

⚡ Scan Modes
This scanner supports two distinct modes to balance speed and accuracy:
🔴 Fast Scan
• 	Timeout: 0.5 seconds per port
• 	Classification:
• 	Open (red) → connection succeeds immediately
• 	Closed (green) → connection actively refused ( on Windows /  on Linux)
• 	All other cases are treated as closed for simplicity
• 	Use case: Quick sweeps when you only need to know which ports are open vs closed.
🟡 Slow Scan
• 	Two‑stage probe:
1. 	Quick check (0.4s):
• 	Immediate  → open
• 	Immediate  → closed
2. 	Extended wait (4.5s):
• 	If no error in the quick check, the scanner waits longer for a response.
• 	Open (red) → connection succeeds during wait
• 	Closed (green) → confirmed refusal () during wait
• 	Filtered (yellow) → no response after 4.5s (likely dropped by firewall)
• 	Use case: More accurate classification when you want to distinguish between closed and filtered ports.

⚠️ Technical Note
Because this tool uses Python’s  (a TCP connect scan), results depend on how the target host and operating system respond:
• 	On Windows localhost, many closed ports behave like filtered (no clear refusal).
• 	On public hosts (e.g. ), most non‑open ports are dropped silently and appear filtered.
• 	Professional tools like Nmap use raw SYN scans to distinguish these states more reliably.
For this project, results should be interpreted as:
• 	Fast mode: open vs closed only
• 	Slow mode: open, closed (confirmed refusal), filtered (no response after extended wait)
• 	Fast & Slow Scan Modes
Choose between quick scans (0.5s timeout) for rapid discovery or slower scans (5s timeout) for more thorough detection of filtered ports.
• 	Three‑Way Port Classification


Results are saved to a structured log file for later review or integration with other tools.
• 	Summary Report
At the end of each scan, a concise summary shows the number of open, closed, and filtered ports, along with the timestamp and log file location.
• 	Cross‑Platform Support
Runs on Python 3 with no external dependencies — works on Windows, macOS, and Linux terminals.

⚠️ Limitations of TCP Connect Scans
This tool uses Python’s  to perform a TCP connect scan. While this method reliably detects open ports, it cannot always distinguish between closed and filtered ports:
• 	Open ports → return  (connection succeeds).
• 	Closed ports → ideally return  (connection actively refused).
• 	Filtered ports → no response or timeout (packets dropped by firewall).
On Windows and some hosts (e.g. , , ), closed ports often behave like filtered ports — they don’t send back a clear refusal, so both cases appear as “filtered.”
Professional tools like Nmap use raw SYN scans (requires admin/root privileges) to distinguish these states more accurately. Our scanner intentionally avoids raw sockets for portability and simplicity, so results should be interpreted as:
• 	Open → confirmed open
• 	Filtered → includes both closed and firewalled ports


⚠️ Acceptable Use
This tool is intended only for internal network scanning.
Do not use it on external networks without explicit authorization.
Unauthorized port scanning may violate laws or organizational policies.

📈 Potential Future Enhancements
• 	Support for UDP scanning
• 	Save/load scan profiles
• 	Service detection and banner grabbing
• 	Integration with SIEM/logging systems

---

## ⚙️ Requirements:
- Python 3.10+

Install dependencies:
```bash
pip install -r requirements.txt

Project Folder/File Structure:
ScanacondaNmap/
│
├── scanacondaNmap.py        # Main script (CLI orchestration)
├── README.md                # Usage, scope, acceptable use notes
├── requirements.txt         # Dependencies (e.g., socket, colorama)
├── Data/                    # Output JSON logs
│   └── results.json
└── utils/                   # Helper modules
    ├── input_validation.py  # **Validate:** IP/hostname & port ranges
    ├── scanner.py           # **Scan:** Single-threaded TCP connect logic, timeouts, result classification
    ├── logger.py            # **Log:** Append JSON results to Data/results.json
    ├── cli_colors.py        # **Colors:** Green (open), yellow (filtered)
    └── constants.py         # **Defaults:** Common ports list for empty input

🐍═══════════════════════════════════════════════════════════════════════🐍
