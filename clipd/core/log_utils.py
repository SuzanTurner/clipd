from pathlib import Path
from datetime import datetime
import typer

app = typer.Typer(help = "Veiwing history")

HISTORY_PATH = Path.home() / ".clipd_history.txt"

def log_command(command: str, status: str = "Completed", msg: str = ""):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    note = f" | {msg}" if msg else ""
    with open(HISTORY_PATH, "a") as f:
        f.write(f"[{timestamp}] {command} {status} {note} \n")

def get_log(n: int = 10):
    if not HISTORY_PATH.exists():
        return []
    with open(HISTORY_PATH) as f:
        lines = f.readlines()
        return lines[-n:]
    
def clear_history():
    if HISTORY_PATH.exists():
        HISTORY_PATH.unlink()
        print("History cleared.")
    else:
        print("No history to clear.")
    

