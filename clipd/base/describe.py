import pandas as pd
from clipd.core.session import load_session
from clipd.core.export import perform_export
from clipd.core.log_utils import log_command
from clipd.core.load import load
from clipd.core.table import print_table
from scipy.stats import entropy
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
        zero: bool = typer.Option(False, "--zero", "-z", help="Show number of zeros in columns"),
        dupes: bool = typer.Option(False, "--dupes", help = "Shows duplicated values in col"),
        emptystr: bool = typer.Option(False, "--empty", help = "Shows column with empty strings"),
        topval: bool = typer.Option(False, "--top", help = "Shows most frequently used value in column"),
        maxlen: bool = typer.Option(False, "--maxlen", help = "Shows maximum length of string in column"),
        nans: bool = typer.Option(False, "--nan", help = "Shows sum of nans in column"),
        const: bool = typer.Option(False, "--const"),
        entropy_flag: bool = typer.Option(False, "--entropy", help="Show entropy (measure of randomness) per column"),
        std: bool = typer.Option(False, "--std", help="Show standard deviation for numeric columns"),
        var: bool = typer.Option(False, "--var", help="Show variance for numeric columns"),
        skew: bool = typer.Option(False, "--skew", help="Show skewness (asymmetry) of distributions"),
        kurt: bool = typer.Option(False, "--kurt", help="Show kurtosis (tailedness) of distributions"),
        mode: bool = typer.Option(False, "--mode", help="Show most frequent value(s) per column"),
        idxmax: bool = typer.Option(False, "--max", help="Show index of maximum value per column"),
        idxmin: bool = typer.Option(False, "--min", help="Show index of minimum value per column"),
        corr: bool = typer.Option(False, "--corr", help="Show correlation matrix between numeric columns"),
        cov: bool = typer.Option(False, "--cov", help="Show covariance matrix between numeric columns"),
        minmax_range: bool = typer.Option(False, "--range"),
        is_monotonic : bool = typer.Option(False, "--mono"),
        export : bool = typer.Option(False, "--export"),
        csv: bool = typer.Option(False, "--json", help="Export in JSON format"),
        xlsx: bool = typer.Option(False, "--xlsx", help="Export in Excel (.xlsx) format"),
        filename: str = typer.Option("described_from_clipd", "--filename", "-f", help="Custom filename (without extension)"),
        dir: str = typer.Option("clipd_outputs", "--dir", help="Directory to export the file to"),
        force: bool = typer.Option(False, "--force", "-F", help="Overwrite file if it exists"),
        preview: bool = typer.Option(False, "--preview", help="Show the full export path and format without writing file"),
        
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
            + (f" --empty" if emptystr else "")
            + (f" --top" if topval else "")
            + (f" --maxlen" if maxlen else "")
            + (f" --nan" if nans else "")
            + (f" --const" if const else "")
            + (" --entropy" if entropy_flag else "")
            + (" --std" if std else "")
            + (" --var" if var else "")
            + (" --skew" if skew else "")
            + (" --kurt" if kurt else "")
            + (" --mode" if mode else "")
            + (" --max" if idxmax else "")
            + (" --min" if idxmin else "")
            + (" --corr" if corr else "")
            + (" --cov" if cov else "")
            + (" --mono" if is_monotonic else "")
            + (" --range" if minmax_range else "")
            
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

            
            if not (dtypes or null or unique or dupes or zero or topval  or emptystr or nans or const or maxlen or
                    nans or const or topval or entropy_flag or std or var or skew or kurt or mode or idxmax or idxmin or 
                    corr or cov or is_monotonic or minmax_range):
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

                if emptystr:
                    rows_to_add["empty_str"] = [str((df[col] == "").sum()) if df[col].dtype == object else "-" for col in df.columns]

                if nans:
                    rows_to_add["NaNs"] = [str(df[col].isna().sum()) for col in df.columns]

                if const:
                    rows_to_add["is_constant"] = [str(df[col].nunique() == 1) for col in df.columns]

                if topval:
                    rows_to_add["top_value"] = [
                        str(df[col].mode().iloc[0]) if not df[col].mode().empty else "-"
                        for col in df.columns
                    ]

                if maxlen:
                    rows_to_add["max_len"] = [
                        str(df[col].astype(str).map(len).max()) if df[col].dtype == object else "-"
                        for col in df.columns
                    ]

                if entropy_flag:
                    rows_to_add["entropy"] = [
                        str(round(entropy(df[col].value_counts(normalize=True)), 4)) if df[col].dtype == object else "-"
                        for col in df.columns
                    ]


                if std:
                    rows_to_add["std_dev"] = [str(df[col].std()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                if var:
                    rows_to_add["variance"] = [str(df[col].var()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                if skew:
                    rows_to_add["skewness"] = [str(df[col].skew()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                if kurt:
                    rows_to_add["kurtosis"] = [str(df[col].kurt()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                if mode:
                    rows_to_add["mode"] = [str(df[col].mode().iloc[0]) if not df[col].mode().empty else "-" for col in df.columns]

                if idxmax:
                    rows_to_add["idx_max"] = [str(df[col].idxmax()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                if idxmin:
                    rows_to_add["idx_min"] = [str(df[col].idxmin()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                # if minmax_range:
                #     rows_to_add["range"] = [str(df[col].max() - df[col].min()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]
                if minmax_range:
                    rows_to_add["range"] = [
                        f"{df[col].min()} - {df[col].max()}"
                        if pd.api.types.is_numeric_dtype(df[col]) else "-"
                        for col in df.columns
                    ]
                
                if is_monotonic:
                    rows_to_add["monotonic"] = [str(df[col].is_monotonic_increasing or df[col].is_monotonic_decreasing) for col in df.columns]

                if zero:
                    rows_to_add["zeros"] = [str((df[col] == 0).sum()) if pd.api.types.is_numeric_dtype(df[col]) else "-" for col in df.columns]

                if rows_to_add:
                    df_rows = pd.DataFrame(rows_to_add, index=df.columns)
                    if cols < 17:
                        print_table(df_rows.transpose())
                    else:
                        print_table(df_rows)

                summary_df = pd.DataFrame(rows_to_add, index=df.columns)
                summary_df.index.name = "Metric"
                summary_df.reset_index(inplace=True)

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

            if corr:
                print("\nCorrelation Matrix:")
                print_table(df.corr())

            if cov:
                print("\nCovariance Matrix:")
                print_table(df.cov())

            if export:
                export_format = "json"
                if csv:
                    export_format = "json"
                elif xlsx:
                    export_format = "xlsx"

                perform_export(
                    df=summary_df,
                    export_format=export_format,
                    filename=filename,
                    dir=dir,
                    force=force,
                    preview=preview,
                    msg=msg,
                    command = command_msg,
                )


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
