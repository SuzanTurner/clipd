import pandas as pd
from clipd.core.session import load_session
from clipd.core.log_utils import log_command
from pathlib import Path
from enum import Enum
from typing import List
import typer


class DescribeMode(str, Enum):
    all = "all"         # df.describe(include="all")
    null = "null"       # df.isnull().sum()
    dtype = "dtypes"     # df.dtypes
    unique = "unique"


class Describe:
    @staticmethod
    def describe(
        msg: str = typer.Option("", "--msg", help="Optional log message"),
        mode: List[DescribeMode] = typer.Option(
            None, "--mode", "-m", help="Choose one or more describe modes: all, null, dtype, unique"
        ),
    ):
        """
        Describe the currently connected dataset using pandas utilities.

        Example:
            $ clipd describe --mode all --mode null --msg "Deep dive"
        """
        msg = msg.strip()
        mode = mode or []

        command_str = "describe " + " ".join(f"--mode {m}" for m in mode) + (f" --msg" if msg else "")

        try:
            file = load_session()
            if not Path(file).exists():
                raise FileNotFoundError(f"File not found: {file}")

            df = pd.read_csv(file)

            # Flags processing
            if DescribeMode.dtype in mode:
                typer.secho("Column Data Types:\n", fg=typer.colors.CYAN)
                typer.echo(df.dtypes.to_string())
                typer.echo(df.dtypes.value_counts())
                typer.echo()

            if DescribeMode.null in mode and DescribeMode.all not in mode:
                typer.secho("Null Values:\n", fg=typer.colors.CYAN)
                typer.echo(df.isnull().sum().to_string())
                typer.echo()

            if DescribeMode.unique in mode:
                typer.secho("Unique Value Counts:\n", fg=typer.colors.CYAN)
                typer.echo(df.nunique().to_string())
                typer.echo()

            if DescribeMode.all in mode or not mode:
                # default fallback to normal describe
                kwargs = {"include": "all"} if DescribeMode.all in mode else {}
                describe_df = df.describe(**kwargs)

                if DescribeMode.null in mode:
                    describe_df.loc["nulls"] = df.isnull().sum()

                typer.secho("DataFrame Description:\n", fg=typer.colors.CYAN)
                typer.echo(describe_df.to_string())

            log_command(
                command=command_str,
                detail=f"Described file: {Path(file).resolve()}",
                status="Completed",
                msg=msg,
            )

        except FileNotFoundError as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED)
            log_command(
                command=command_str,
                detail=f"File not found during describe: {e}",
                status="Failed",
                msg=msg,
            )
            raise typer.Exit(code=1)

        except Exception as e:
            typer.secho(f"Unexpected error: {e}", fg=typer.colors.RED)
            log_command(
                command=command_str,
                detail=f"Unexpected error during describe: {e}",
                status="Failed",
                msg=msg,
            )
            raise typer.Exit(code=1)
