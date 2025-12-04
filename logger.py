# utils/logger.py

import json
import os
from datetime import datetime

def build_results_json(open_map, closed_map, filtered_map, timestamp):
    """
    Build a JSON-friendly structure of scan results.
    Ensures all targets are included, even if lists are empty.
    """
    results = {
        "scan_started": timestamp,
        "targets": {}
    }

    # Union of all target keys across open, closed, and filtered maps
    all_targets = set(open_map.keys()) | set(closed_map.keys()) | set(filtered_map.keys())

    for target in all_targets:
        results["targets"][target] = {
            "open_ports": open_map.get(target, []),
            "closed_ports": closed_map.get(target, []),
            "filtered_ports": filtered_map.get(target, [])
        }

    return results

def save_results_json(results, filename="results.json"):
    """
    Save results to a JSON file inside the Data directory.
    """
    if not os.path.exists("Data"):
        os.makedirs("Data")
    path = os.path.join("Data", filename)
    with open(path, "w") as f:
        json.dump(results, f, indent=2)
    return path