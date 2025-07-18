import pandas as pd
from clipd.core.session import save_session, load_session
from clipd.core.log_utils import get_log, log_command
from clipd.commands import log
import typer

app = typer.Typer(help="Command Line Interface for Pandas")

app.add_typer(log.app, name = "log")

@app.command("init", help = "Start command")
def init( msg: str = typer.Option("", "--msg", help="Optional log message")):
    typer.echo("CLI Initialized")
    log_command(f"CLi Initialised", msg = msg)


@app.command("connect", help = "Connects to excel/csv/db file")
def connect(file: str, msg: str = typer.Option("", "--msg", help="Optional log message")):
    typer.echo(f"Connecting to {file}...")
    save_session(file) 
    try:
        df = pd.read_csv(file)
        typer.echo(f"Loaded {len(df)} rows.")
        log_command(f"Connected {file.name}", msg= msg)
    except Exception as e:
        typer.echo(f"Error: {e}")
        log_command(f"Failed to connect {file.name}", msg = msg)


@app.command("describe")
def describe(msg: str = typer.Option("", "--msg", help="Optional log message")):
    try:
        file = load_session()  
        df = pd.read_csv(file)
        typer.echo(df.describe().to_string())
        log_command(f"Described {file.name}", msg = msg)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}")
        log_command(f"Failed to describe {file.name} due to {e}", msg = msg)
    except Exception as e:
        typer.echo(f"Error: {e}")
        log_command(f"Failed to describe {file.name} due to {e}", msg = msg)


def main():
    app()

if __name__ == "__main__":
    main()
