from functools import wraps
from pathlib import Path
from clipd.core.session import active_file
from clipd.core.exceptions import NoActiveFileError
from rich import print
from functools import wraps
from pathlib import Path
from clipd.core.session import active_file
from clipd.core.exceptions import NoActiveFileError
import typer


def requires_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            file_path = active_file()
            if not file_path or not Path(file_path).exists():
                raise NoActiveFileError()
        except (FileNotFoundError, NoActiveFileError) as e:
            print(f"[bold red]Error:[/bold red] {e}")
            raise typer.Exit(code=1)
        return func(*args, **kwargs)
    return wrapper

