import pandas as pd
from rich.console import Console
from rich.table import Table

def print_table(df: pd.DataFrame):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="cyan")
    for col in df.columns:
        table.add_column(str(col), overflow="fold")

    for idx, row in df.iterrows():
        table.add_row(str(idx), *[str(v) if pd.notna(v) else "" for v in row])

    Console().print(table)