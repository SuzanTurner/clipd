import pandas as pd
from clipd.core.session import load_session
from clipd.core.log_utils import log_command
from clipd.core.load import load
from clipd.core.table import print_table
from pathlib import Path
import typer

app = typer.Typer()

# class Describe():
#     @staticmethod
#     def describe(
#         all: bool = typer.Option(False, "--all", help="Include non-numeric columns"),
#         null: bool = typer.Option(False, "--null", help="Show null value counts"),
#         unique: bool = typer.Option(False, "--unique", help="Show unique value counts"),
#         dtypes: bool = typer.Option(False, "--dtypes", help="Show column data types"),
#         msg: str = typer.Option("", "--msg", help="Optional log message"),
#         head: bool = typer.Option(False, "--head", help = "Show top n row [df.head()] "),
#         lines: int = 5,
#     ) -> None:
#         msg = msg.strip()
#         command_msg = "describe" + (" --msg" if msg else "") + (" --all" if all else "") + (" --null" if null else "") + (" --unique" if unique else "") + (" --dtypes" if dtypes else "") + (" --head" if head else "" + "lines" if lines != 5 else "")
#         try:
#             file = load_session()

#             path = Path(file)
#             df = load(path)

#             typer.secho(f"Analyzing: {path.name}", fg=typer.colors.BLUE)

#             if all or null or dtypes or unique or head:

#                 if dtypes:
#                     typer.secho("\nColumn Data Types:", fg=typer.colors.CYAN)
#                     typer.echo(df.dtypes.to_string())

#                 if null:
#                     typer.secho("\nNull Value Counts:", fg=typer.colors.CYAN)
#                     typer.echo(df.isnull().sum().to_string())

#                 if unique:
#                     typer.secho("\nUnique Value Counts:", fg=typer.colors.CYAN)
#                     typer.echo(df.nunique().to_string())

#                 if head:
#                     typer.secho("\nDataFrame head:", fg=typer.colors.CYAN)
#                     typer.echo(df.head(lines).to_string())

#                 # if all or not (dtypes or null or unique):
#                 if all:
#                     typer.secho("\nDataFrame Description:", fg=typer.colors.CYAN)
#                     describe_df = df.describe(include="all") 
#                     typer.echo(describe_df.to_string())
#             else:
#                 typer.secho("\nDataFrame Description:", fg=typer.colors.CYAN)
#                 typer.echo(df.describe().to_string())

#             log_command(
#                 command = command_msg,
#                 detail = "Described file",
#                 status = "Completed",
#                 msg = msg
#             )

#         except Exception as e:
#             typer.secho(f"Error: {e}", fg=typer.colors.RED)
#             log_command(
#                 command = command_msg,
#                 detail = f"Could not describe file due to {e}",
#                 status = "Failed",
#                 msg = msg
#             )

#             raise typer.Exit(code=1)


# class Describe:
#     @staticmethod
#     def describe(
#         all: bool = typer.Option(False, "--all"),
#         null: bool = typer.Option(False, "--null"),
#         unique: bool = typer.Option(False, "--unique"),
#         dtypes: bool = typer.Option(False, "--dtypes"),
#         msg: str = typer.Option("", "--msg"),
#         head: bool = typer.Option(False, "--head"),
#         lines: int = 5,
#     ):
#         # ... load df exactly as before ...

#         msg = msg.strip()
#         command_msg = (
#             "describe"
#             + (" --msg" if msg else "")
#             + (" --all" if all else "")
#             + (" --null" if null else "")
#             + (" --unique" if unique else "")
#             + (" --dtypes" if dtypes else "")
#             + (" --head" if head else "")
#             + (f" --lines {lines}" if lines != 5 else "")
#         )

#         try:
#             file = load_session()
#             path = Path(file)
#             df = load(path)

#             typer.secho(f"Analyzing: {path.name}\n", fg=typer.colors.BLUE)
        
#             rows_to_add: dict[str, list[str]] = {}

#             if dtypes:
#                 rows_to_add["dtype"]  = [str(df[col].dtype)       for col in df.columns]
#             if null:
#                 rows_to_add["nulls"]  = [str(df[col].isnull().sum()) for col in df.columns]
#             if unique:
#                 rows_to_add["unique"] = [str(df[col].nunique())   for col in df.columns]
#             if all:
#                 desc = df.describe(include="all")
#             elif not rows_to_add:        # default case – no flags chosen
#                 desc = df.describe()
#             else:
#                 desc = None

#             if desc is not None:
#                 for metric in desc.index:
#                     row = [str(desc[col]) if col in desc.columns else "" for col in df.columns]
#                     rows_to_add[metric] = row

#             # --- SINGLE unified table ---
#             if rows_to_add:
#                 combined_df = pd.DataFrame.from_dict(
#                     rows_to_add, orient="index", columns=df.columns
#                 )
#                 print_table(combined_df)

#             # Optional head preview
#             if head:
#                 typer.secho(f"\n🔹 Top {lines} rows:", fg=typer.colors.CYAN)
#                 Console().print(df.head(lines))
#                 log_command(
#                     command=command_msg,
#                     detail="Described file",
#                     status="Completed",
#                     msg=msg
#                 )

#         except Exception as e:
#             typer.secho(f"Error: {e}", fg=typer.colors.RED)
#             log_command(
#                 command=command_msg,
#                 detail=f"Could not describe file due to {e}",
#                 status="Failed",
#                 msg=msg
#             )
#             raise typer.Exit(code=1)



class Describe():
    @staticmethod
    def describe(
        all: bool = typer.Option(False, "--all", help="Include non-numeric columns"),
        null: bool = typer.Option(False, "--null", help="Show null value counts"),
        unique: bool = typer.Option(False, "--unique", help="Show unique value counts"),
        dtypes: bool = typer.Option(False, "--dtypes", help="Show column data types"),
        msg: str = typer.Option("", "--msg", help="Optional log message"),
        head: bool = typer.Option(False, "--head", help="Show top n row [df.head()]"),
        tail:bool = typer.Option(False, "--tail", help = "Show bottom n rows [df.tail()]"),
        lines: int = 5,
    ) -> None:

        msg = msg.strip()
        command_msg = (
            "describe"
            + (" --msg" if msg else "")
            + (" --all" if all else "")
            + (" --null" if null else "")
            + (" --unique" if unique else "")
            + (" --dtypes" if dtypes else "")
            + (" --head" if head else "")
            + (f" --lines {lines}" if lines != 5 else "")
        )

        try:
            file = load_session()
            path = Path(file)
            df = load(path)
            cols = df.shape[1]

            typer.secho(f"Analyzing: {path.name}\n", fg=typer.colors.BLUE)
            # console = Console()

            if all:
                describe_df = df.describe(include="all").transpose()
                print_table(describe_df)

            # Handle default describe when no other flags
            elif not any([dtypes, null, unique, head]):
                describe_df = df.describe().transpose()
                print_table(describe_df)
                typer.secho(f"Rows : {df.shape[0]}",fg=typer.colors.BLUE)
                typer.secho(f"Columns : {df.shape[1]}", fg=typer.colors.BLUE)

            rows_to_add = {}

            if dtypes:
                rows_to_add["dtype"] = [str(df[col].dtype) for col in df.columns]

            if null:
                rows_to_add["nulls"] = [str(df[col].isnull().sum()) for col in df.columns]

            if unique:
                rows_to_add["unique"] = [str(df[col].nunique()) for col in df.columns]

            if rows_to_add:
                df_rows = pd.DataFrame(rows_to_add, index=df.columns)
                df_rows = df_rows.reset_index(names="Metric")
                print_table(df_rows)

            if head:
                typer.secho(f"\n🔹 Top {lines} Rows:", fg=typer.colors.CYAN)
                if cols > 17:
                    print_table(df.head(lines).transpose())
                else:
                    print_table(df.head(lines))


            if tail:
                typer.secho(f"\n🔹 Top {lines} Rows:", fg=typer.colors.CYAN)
                if cols > 17:
                    print_table(df.tail(lines).transpose())
                else:
                    print_table(df.tail(lines))


            log_command(
                command=command_msg,
                detail="Described file",
                status="Completed",
                msg=msg
            )

        except Exception as e:
            typer.secho(f"Error: {e}", fg=typer.colors.RED)
            log_command(
                command=command_msg,
                detail=f"Could not describe file due to {e}",
                status="Failed",
                msg=msg
            )
            raise typer.Exit(code=1)
