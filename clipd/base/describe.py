import pandas as pd
from clipd.core.session import load_session
from clipd.core.log_utils import log_command
from pathlib import Path
import typer

app = typer.Typer()

class Describe():
    @staticmethod
    def describe(
        all: bool = typer.Option(False, "--all", help="Include non-numeric columns"),
        null: bool = typer.Option(False, "--null", help="Show null value counts"),
        unique: bool = typer.Option(False, "--unique", help="Show unique value counts"),
        dtypes: bool = typer.Option(False, "--dtypes", help="Show column data types"),
        msg: str = typer.Option("", "--msg", help="Optional log message"),
    ) -> None:
        msg = msg.strip()
        command_msg = "describe" + (" --msg" if msg else "") + (" --all" if all else "") + (" --null" if null else "") + (" --unique" if unique else "") + (" --dtypes" if dtypes else "")
        try:
            file = load_session()

            path = Path(file)
            df = pd.read_csv(path)

            typer.secho(f"Analyzing: {path.name}", fg=typer.colors.BLUE)

            if dtypes:
                typer.secho("\nColumn Data Types:", fg=typer.colors.CYAN)
                typer.echo(df.dtypes.to_string())

            if null:
                typer.secho("\nNull Value Counts:", fg=typer.colors.CYAN)
                typer.echo(df.isnull().sum().to_string())

            if unique:
                typer.secho("\nUnique Value Counts:", fg=typer.colors.CYAN)
                typer.echo(df.nunique().to_string())

            if all or not (dtypes or null or unique):
                typer.secho("\nDataFrame Description:", fg=typer.colors.CYAN)
                describe_df = df.describe(include="all") if all else df.describe()
                typer.echo(describe_df.to_string())

            log_command(
                command = command_msg,
                detail = "Described file",
                status = "Completed",
                msg = msg
            )

        except Exception as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED)
            log_command(
                command = command_msg,
                detail = f"Could not describe file due to {e}",
                status = "Failed",
                msg = msg
            )

            raise typer.Exit(code=1)

        
