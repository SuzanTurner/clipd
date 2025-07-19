from pathlib import Path
from datetime import datetime
import typer
import json

app = typer.Typer(help = "Veiwing history")

HISTORY_PATH = Path.home() / ".clipd_history.txt"

def log_command(command: str, detail : str, status: str , msg: str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {
        "timestamp": timestamp,
        "command": command,
        "detail" : detail,
        "status": status,
        "msg": msg
    }
    with open(HISTORY_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

def format_logs_pretty(lines):
    formatted_lines = []
    for line in lines:
        try:
            entry = json.loads(line)
            timestamp = entry.get("timestamp", "")
            command = entry.get("command", "")
            status = entry.get("status", "")
            msg = entry.get("msg", "")

            pretty = f"[{timestamp}] {command} | {status}"
            if msg:
                pretty += f" | {msg}"
            formatted_lines.append(pretty)
        except json.JSONDecodeError:
            formatted_lines.append("Corrupted log line!")
    return formatted_lines[::-1]

def get_log(n: int = 10):
    if not HISTORY_PATH.exists():
        return []
    
    with open(HISTORY_PATH) as f:
        lines = f.readlines()
    
    if n == float('inf'):
        selected_lines = lines
    else:
        selected_lines = lines[-n:]
    
    formatted = format_logs_pretty(selected_lines)
    return formatted


def num_log():
    if not HISTORY_PATH.exists():
        return 0  

    with open(HISTORY_PATH) as f:
        lines = f.readlines()
        return len(lines)
        
    
def clear_history():
    if HISTORY_PATH.exists():
        HISTORY_PATH.unlink()
        print("History cleared.")
    else:
        print("No history to clear.")
    
def get_json_logs(lines: int = 10):
    with open(HISTORY_PATH, "r") as f:
        log_lines = f.readlines()[-lines:]

    json_logs = []
    for line in log_lines:
        try:
            json_logs.append(json.loads(line))
        except json.JSONDecodeError:
            # Optional: log it or skip silently
            continue

    return json_logs

