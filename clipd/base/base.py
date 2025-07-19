import pandas as pd
from clipd.core.session import save_session, load_session
from clipd.core.log_utils import log_command
from rich import print
import typer

app = typer.Typer(help = "Base commands")

class Base:
    @staticmethod
    def init( msg: str = typer.Option("", "--msg", help="Optional log message")):
        typer.secho("Clipd Initialised!", fg=typer.colors.GREEN, bold=True)
        log_command(command= "init", detail= "Clipd Initialised", status= "Completed", msg = msg) #  ILEFT IT HERE!!! NOW DO PROPER LOGS FOR ALL!!

    @staticmethod
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

    @staticmethod
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

    @staticmethod
    def show_connected_file(msg: str = typer.Option("", "--msg", help="Optional log message")):
        try:
            filename = load_session()
            # typer.echo(f"Connected to: {filename}")
            print(f"Connected to: [bold yellow]{filename}[/bold yellow]")
            log_command(command= "status", detail= f"Current active file {filename}", status= "Completed", msg = msg)
        except FileNotFoundError as e:
            typer.echo("No file connected.")
            log_command(command= "status", detail= f"Failed to connect due to {e}", status= "Failed", msg = msg)