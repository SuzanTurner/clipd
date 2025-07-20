
from functools import wraps
from pathlib import Path
from clipd.core.session import active_file
from clipd.core.exceptions import NoActiveFileError

def requires_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        file_path = active_file()
        if not file_path or not Path(file_path).exists():
            raise NoActiveFileError()
        return func(*args, **kwargs)
    return wrapper
