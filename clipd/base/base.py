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
            log_command(command= "connect", detail= f"Connected to {file}", status= "Completed", msg = msg) 
        except Exception as e:
            typer.echo(f"Error: {e}")
            log_command(command= "connect", detail= f"Unable to connect {file}", status= "Failed", msg = msg) 

    @staticmethod
    def describe(msg: str = typer.Option("", "--msg", help="Optional log message")):
        try:
            file = load_session()  
            df = pd.read_csv(file)
            typer.echo(df.describe().to_string())
            log_command(command= "describe", detail= f"Described {file}", status= "Completed", msg = msg) 
        except FileNotFoundError as e:
            typer.echo(f"Error: {e}")
            log_command(command= "describe", detail= f"Unable to describe {file} due to {e}", status= "Failed", msg = msg) 
        except Exception as e:
            typer.echo(f"Error: {e}")
            log_command(command= "describe", detail= f"Unable to describe {file} due to {e}", status= "Failed", msg = msg) 

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

    @staticmethod
    def thank_you():
        print("Thank you [bold yellow]@tiangolo[/bold yellow], creator of [bold blue]Typer[/bold blue] and [bold green]FastAPI[/bold green]")