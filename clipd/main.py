import pandas as pd
from clipd.core.session import save_session, load_session
from clipd.core.log_utils import log_command
from clipd.commands import log
from rich import print
import typer

app = typer.Typer(help="Command Line Interface for Pandas")

app.add_typer(log.app, name = "log")

@app.command("init", help = "Start command")
def init( msg: str = typer.Option("", "--msg", help="Optional log message")):
    typer.secho("Clipd Initialised!", fg=typer.colors.GREEN, bold=True)
    log_command(command= "init", detail= "Clipd Initialised", status= "Completed", msg = msg) #  ILEFT IT HERE!!! NOW DO PROPER LOGS FOR ALL!!


@app.command("connect", help = "Connects to excel/csv/ file")
def connect(file: str, msg: str = typer.Option("", "--msg", help="Optional log message")):
    # typer.echo(f"Connecting to {file}...")
    print(f"Connecting to [bold yellow]{file}[/bold yellow]...")
    save_session(file) 
    try:
        df = pd.read_csv(file)
        typer.echo(f"Loaded {len(df)} rows.")
        log_command(f"Connected to {file}", msg= msg)
    except Exception as e:
        typer.echo(f"Error: {e}")
        log_command(f"Failed to connect {file}", msg = msg)


@app.command("describe")
def describe(msg: str = typer.Option("", "--msg", help="Optional log message")):
    try:
        file = load_session()  
        df = pd.read_csv(file)
        typer.echo(df.describe().to_string())
        log_command(f"Described {file}", msg = msg)
    except FileNotFoundError as e:
        typer.echo(f"Error: {e}")
        log_command(f"Failed to describe {file} due to {e}", msg = msg)
    except Exception as e:
        typer.echo(f"Error: {e}")
        log_command(f"Failed to describe {file} due to {e}", msg = msg)


def main():
    app()

if __name__ == "__main__":
    main()
