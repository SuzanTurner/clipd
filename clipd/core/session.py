from pathlib import Path
import json

SESSION_PATH = Path.home() / ".clipd_session.json"

def save_session(file_path: str):
    with open(SESSION_PATH, "w") as f:
        json.dump({"file": file_path}, f)

def load_session():
    if not SESSION_PATH.exists():
        raise FileNotFoundError("No session found. Run `clipd connect <file>` first.")
    with open(SESSION_PATH) as f:
        return json.load(f)["file"]