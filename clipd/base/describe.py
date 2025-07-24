import pandas as pd
from clipd.core.session import load_session
from clipd.core.log_utils import log_command
from clipd.core.load import load
from clipd.core.table import print_table
from typing import List
from rich import print
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


class Describe():
    @staticmethod
    def describe(
        all: bool = typer.Option(False, "--all", help="Include non-numeric columns"),
        null: bool = typer.Option(False, "--null", "-n", help="Show null value counts"),
        unique: bool = typer.Option(False, "--unique", "-u", help="Show unique value counts"),
        dtypes: bool = typer.Option(False, "--dtypes", "-d", help="Show column data types"),
        msg: str = typer.Option("", "--msg", help="Optional log message"),
        head: bool = typer.Option(False, "--head", help="Show top n row [df.head()]"),
        tail:bool = typer.Option(False, "--tail", help = "Show bottom n rows [df.tail()]"),
        lines: int = 5,
        percent : str = typer.Option(None, "--percent", help = "Comma-separated percentiles like: 0.1,0.2,0.3"),
        # exclude : str = typer.Option(None, "--exclude", help = "Excludes selected datatype [df.describe(exclude = 'object')]"),
        exclude: List[str] = typer.Option(None, "--exclude", help="Exclude data types", show_default=False),
        zero: bool = typer.Option(False, "--zeros", "-z", help="Show number of zeros in columns"),
        dupes: bool = typer.Option(False, "--dupes", help = "Shows duplicated values in col"),

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
            + (f" --percent {percent}" if percent else "")
            + (f" --dupes" if dupes else "")
            
        )


        try:
            file = load_session()
            path = Path(file)
            df = load(path)
            cols = df.shape[1]

            typer.secho(f"Analyzing: {path.name}\n", fg=typer.colors.BLUE)
            # console = Console()

            # if not percent:
            #     if all:
            #         describe_df = df.describe(include="all").transpose()
            #         print_table(describe_df)

            #     # elif exclude and object:
            #     #     describe_df = df.describe(exclude= f"{object}").transpose()
            #     #     print_table(describe_df)

            #     elif exclude:
            #         describe_df = df.describe(exclude=exclude).transpose()
            #         print_table(describe_df)

            #     elif not any([dtypes, null, unique, head]):
            #         describe_df = df.describe().transpose()
            #         print_table(describe_df)
            #         typer.secho(f"Rows : {df.shape[0]}",fg=typer.colors.BLUE)
            #         typer.secho(f"Columns : {df.shape[1]}", fg=typer.colors.BLUE)
            # else:
            #     percent_list = [float(p.strip()) for p in percent.split(",")]
            #     percent_list = [p if p < 1 else p / 100 for p in percent_list]
            #     describe_df = df.describe(percentiles= percent_list).transpose()
            #     print_table(describe_df)

            describe_kwargs = {}

            if all:
                describe_kwargs["include"] = "all"
            if exclude:
                describe_kwargs["exclude"] = exclude
            if percent:
                percent_list = [float(p.strip()) for p in percent.split(",")]
                percent_list = [p if p < 1 else p / 100 for p in percent_list]
                describe_kwargs["percentiles"] = percent_list

            
            if not (dtypes or null or unique or dupes or zero):
                describe_df = df.describe(**describe_kwargs).transpose()
                print_table(describe_df)
                typer.secho(f"\nRows : {df.shape[0]}", fg=typer.colors.BLUE)
                typer.secho(f"Columns : {df.shape[1]}", fg=typer.colors.BLUE)
                
            
            else:
                rows_to_add = {}

                if dtypes:
                    rows_to_add["dtype"] = [str(df[col].dtype) for col in df.columns]

                if null:
                    rows_to_add["nulls"] = [str(df[col].isnull().sum()) for col in df.columns]

                if unique:
                    rows_to_add["unique"] = [str(df[col].nunique()) for col in df.columns]

                if dupes:
                    rows_to_add["duplicates"] = [str(df[col].duplicated().sum()) for col in df.columns]

                if zero:
                    rows_to_add["zeros"] = [str((df[col] == 0).sum()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                if rows_to_add:
                    df_rows = pd.DataFrame(rows_to_add, index=df.columns)
                    if cols < 17:
                        print_table(df_rows.transpose())
                    else:
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
