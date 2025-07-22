from pathlib import Path
import json

CLIPD_DIR = Path.cwd() / ".clipd"
SESSION_PATH = CLIPD_DIR / "session.json"  

CLIPD_DIR.mkdir(parents=True, exist_ok=True)

def save_session(file_path: str):
    with open(SESSION_PATH, "w") as f:
        json.dump({"file": str(file_path)}, f)

def load_session() -> str:
    if not SESSION_PATH.exists():
        raise FileNotFoundError("No session found. \nRun `clipd connect <file>`")
    
    with open(SESSION_PATH) as f:
        return json.load(f)["file"]

def active_file() -> Path:
    if not SESSION_PATH.exists():
        raise FileNotFoundError("No active file. \nRun `clipd connect <file>` ")

    with open(SESSION_PATH) as f:
        raw_path = json.load(f)["file"]

    path = Path(raw_path)

    # Convert to absolute if needed
    if not path.is_absolute():
        path = Path.cwd() / path

    if not path.exists():
        raise FileNotFoundError(f"File not found at: {path}")

    return path

def filename(path: str) -> str:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File does not exist: {path}")
    return p.name

def disconnect_session():
    if SESSION_PATH.exists():
        with open(SESSION_PATH) as f:
            file_info = json.load(f).get("file", "")
        SESSION_PATH.unlink()
        return file_info
    return None
