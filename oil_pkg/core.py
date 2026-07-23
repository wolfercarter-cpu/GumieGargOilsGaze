import json
import os
import csv
import sys
import tempfile
import subprocess


def oil_soak(file_path, data):
    """Saves data to a user-defined file path."""
    # Get the directory part of the path
    directory = os.path.dirname(file_path)
    
    # Only try to create the directory if it's not the current directory
    if directory:
        os.makedirs(directory, exist_ok=True)
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def oil_spill(file_path):
    """Reads data from a user-defined file path."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Return an empty dict if the file is missing or corrupted
        return {}

def oil_rag(file_path):
    """Wipes the persistent file clean (deletes it)."""
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def oil_read_csv(file_path: str):
    with open(file_path, mode='r', newline='') as f:
        reader = csv.reader(f)
        return list(reader)

def oil_join(content1: str, content2: str, mode: str = "vertical"):
    if mode == "vertical":
        return f"{content1}\n{content2}"
    elif mode == "horizontal":
        lines1 = content1.splitlines()
        lines2 = content2.splitlines()
        # Ensure equal height for side-by-side
        max_height = max(len(lines1), len(lines2))
        lines1 += [""] * (max_height - len(lines1))
        lines2 += [""] * (max_height - len(lines2))
        
        joined = [f"{l1:<30} {l2}" for l1, l2 in zip(lines1, lines2)]
        return "\n".join(joined)
    return content1


def get_piped_data() -> list:
    """Reads lines from stdin, then reconnects stdin to the terminal."""
    if not sys.stdin.isatty():
        # 1. Read the data coming from the pipe
        data = sys.stdin.read().splitlines()
        
        # 2. Reconnect standard input to the controlling terminal
        # This allows interactive prompts (like inquirer) to read keyboard input again
        try:
            sys.stdin = open('/dev/tty')
        except OSError:
            pass # Fallback if /dev/tty isn't available
            
        return data
    return []

def oil_pump(file_path: str, new_item: dict):
    """Pumps a fresh record straight into the JSON array file."""
    data = oil_spill(file_path)
    if not isinstance(data, list):
        data = []
    data.append(new_item)
    oil_soak(file_path, data)

def oil_skim(file_path: str, key: str, value):
    """Skims/removes unwanted records from the JSON array."""
    data = oil_spill(file_path)
    if isinstance(data, list):
        data = [item for item in data if item.get(key) != value]
        oil_soak(file_path, data)

def oil_tune(file_path: str, match_key: str, match_val, update_key: str, update_val):
    """Tunes a field or flag on matching records in the JSON array."""
    data = oil_spill(file_path)
    if isinstance(data, list):
        for item in data:
            if item.get(match_key) == match_val:
                item[update_key] = update_val
            elif update_key == "fav":  # Enforce exclusive toggle for favorites
                item[update_key] = False
        oil_soak(file_path, data)

def oil_spill_table(file_path: str):
    """Spills a JSON state file, converts it to CSV, and renders it using Charmbracelet's 'gum table'."""
    data = oil_spill(file_path)
    
    if not data:
        print(f"No data found or file is empty: {file_path}")
        return

    # Normalize single dict to a list of dicts
    if isinstance(data, dict):
        data = [data]

    if not isinstance(data, list) or len(data) == 0:
        print(f"Invalid table format in {file_path}")
        return

    # Extract headers
    headers = list(data[0].keys())

    # Write data to a temporary CSV file for gum table
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
        writer = csv.DictWriter(tmp, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        tmp_csv_path = tmp.name

    try:
        # Pass the CSV file using the required --file flag for gum table
        subprocess.run(["gum", "table", "--file", tmp_csv_path])
    except FileNotFoundError:
        print("Error: 'gum' is not installed or not found in your system PATH.")
    finally:
        # Clean up the temporary CSV file
        if os.path.exists(tmp_csv_path):
            os.remove(tmp_csv_path)
