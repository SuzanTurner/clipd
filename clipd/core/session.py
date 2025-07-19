from pathlib import Path
import json

SESSION_PATH = Path.home() / ".clipd_session.json"

def save_session(file_path: str):
    with open(SESSION_PATH, "w") as f:
        # json.dump({"file": file_path}, f)
        json.dump({"file": str(file_path)}, f)

def load_session():
    if not SESSION_PATH.exists():
        raise FileNotFoundError("No session found. Run `clipd connect <file>` first.")
    with open(SESSION_PATH) as f:
        return json.load(f)["file"]
    
def rel_path():
    with open(SESSION_PATH) as f:
        raw_path = json.load(f)["file"]
    path = Path(raw_path)

    # If it's relative, make it absolute based on cwd
    if not path.is_absolute():
        path = Path.cwd() / path

    if not path.exists():
        raise FileNotFoundError(f"Session file not found at: {path}")

    return path

def active_file():
    if not SESSION_PATH.exists():
        raise FileNotFoundError("No session found. Run `clipd connect <file>` first.")
    
    with open(SESSION_PATH) as f:
        raw_path = json.load(f)["file"]
    
    path = Path(raw_path)

    if not path.is_absolute():
        path = Path.cwd() / path

    if not path.exists():
        raise FileNotFoundError(f"Session file not found at: {path}")

    return path

def disconnect_session():
    if SESSION_PATH.exists():
        file_name = SESSION_PATH.read_text().strip()
        SESSION_PATH.unlink()
        return file_name
    else:
        return None
