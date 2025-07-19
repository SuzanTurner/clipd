import pandas as pd
from clipd.core.session import save_session
from clipd.core.log_utils import log_command
from rich import print
from pathlib import Path
import typer 


class Connect:
    @staticmethod
    def connect(file: str, msg: str = typer.Option("", "--msg", help="Optional log message")):

        """
        Connect to a CSV file and load it into a DataFrame.
        Logs the command and optionally takes a custom log message.

        Args:
            file (str): Path to the CSV file.
            msg (str, optional): Optional log message.

        Example:
            $ clipd connect data.csv --msg "here's a msg"
            Connecting to data.csv...
            Loaded 2 rows.

        Returns:
            pd.DataFrame: Loaded DataFrame.
        """

        msg = msg.strip()
        command_str = "connect " + file + (" --msg" if msg else "")

        if not Path(file).exists():
            typer.secho(f"File not found: {file}", fg=typer.colors.RED, bold=True)
            log_command(command=command_str, detail=f"File not found: {file}", status="Failed", msg=msg)
            raise typer.Exit(code=1)

        print(f"[bold yellow]Connecting to {file}...[/bold yellow]")
        save_session(Path(file).resolve())
        try:
            df = pd.read_csv(file, on_bad_lines="error", engine="python")
            typer.secho(f"Loaded {len(df)} rows.", fg=typer.colors.GREEN)
            log_command(command=command_str, detail=f"Connected to {file}", status="Completed", msg=msg)
            return df
        except pd.errors.EmptyDataError:
            typer.secho("The file is empty.", fg=typer.colors.RED)
            log_command(command=command_str, detail="CSV file is empty ", status="Failed", msg=msg)
            raise typer.Exit(code=1)
        except pd.errors.ParserError as e:
            typer.secho(f"Malformed CSV: {e}", fg=typer.colors.RED)
            log_command(command=command_str, detail=f"Malformed CSV: {e}", status="Failed", msg=msg)
            raise typer.Exit(code=1)
        except Exception as e:
            typer.secho(f"Error reading file: {e}", fg=typer.colors.RED)
            log_command(command=command_str, detail=f"Unable to connect to {file} due to {e}", status="Failed", msg=msg)
            raise typer.Exit(code=1)