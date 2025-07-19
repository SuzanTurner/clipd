import pandas as pd
from clipd.core.session import load_session
from clipd.core.log_utils import log_command
from pathlib import Path
import typer

class Describe():
    @staticmethod
    def describe(msg: str = typer.Option("", "--msg", help="Optional log message")):
        """
        Describe the currently connected dataset using pandas' .describe().

        Args:
            msg (str, optional): Optional log message.

        Example:
            $ clipd describe --msg "Quick stats"
            (prints DataFrame summary stats)

        Return:
             None
        """
        msg = msg.strip()
        command_str = "describe" + (" --msg" if msg else "")

        try:
            file = load_session()
            if not Path(file).exists():
                raise FileNotFoundError(f"File not found: {file}")

            df = pd.read_csv(file)
            typer.secho(df.describe().to_string())
            log_command(
                command=command_str,
                detail=f"Described file: {file}",
                status="Completed",
                msg=msg
            )
        except FileNotFoundError as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED)
            log_command(
                command=command_str,
                detail=f"File not found during describe: {e}",
                status="Failed",
                msg=msg
            )
            raise typer.Exit(code=1)
        except Exception as e:
            typer.secho(f"Error describing file: {e}", fg=typer.colors.RED)
            log_command(
                command=command_str,
                detail=f"Unexpected error during describe: {e}",
                status="Failed",
                msg=msg
            )
            raise typer.Exit(code=1)