import pandas as pd
from rich.console import Console
from rich.table import Table
import shutil



def print_table(df: pd.DataFrame):
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("Metric", style="cyan")
    for col in df.columns:
        table.add_column(str(col), overflow="fold")

    for idx, row in df.iterrows():
        table.add_row(str(idx), *[str(v) if pd.notna(v) else "" for v in row])


    Console().print(table)



# def check_transpose(df_preview: pd.DataFrame, full_df: pd.DataFrame) -> pd.DataFrame:
#     terminal_width = shutil.get_terminal_size((100, 20)).columns

#     col_widths = [
#         max(len(str(col)), full_df[col].astype(str).str.len().max())
#         for col in full_df.columns
#     ]

#     padding_per_column = 3
#     border_padding = 4

#     total_width = sum(col_widths) + (len(col_widths) * padding_per_column) + border_padding

#     print(f"📏 Terminal width: {terminal_width}")
#     print(f"📐 Total table width: {total_width}")

#     return df_preview.transpose() if total_width > terminal_width else df_preview

