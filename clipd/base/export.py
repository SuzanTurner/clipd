import pandas as pd
from clipd.core.session import active_file
from clipd.core.log_utils import log_command
from rich import print
from pathlib import Path
import typer 
from pathlib import Path
from datetime import datetime


def write_file(df, file_path, export_format):
    if export_format == "csv":
        df.to_csv(file_path, index=False)
    elif export_format == "json":
        df.to_json(file_path, orient="records", indent=2)
    elif export_format == "xlsx":
        df.to_excel(file_path, index=False)

class Export:
    @staticmethod
    def export(
        json: bool = typer.Option(False, "--json", help="Export in JSON format"),
        xlsx: bool = typer.Option(False, "--xlsx", help="Export in Excel (.xlsx) format"),
        msg: str = typer.Option("", "--msg", help="Optional log message"),
        filename: str = typer.Option("exported_from_clipd", "--filename", "-f", help="Custom filename (without extension)"),
        dir: str = typer.Option(".", "--dir", help="Directory to export the file to"),
        force: bool = typer.Option(False, "--force", "-F", help="Overwrite file if it exists"),
        preview: bool = typer.Option(False, "--preview", help="Show the full export path and format without writing file"),
    ):
        """
        Export the current DataFrame to the specified format and directory.

        Args:
            --json (bool): Export as JSON. Default is CSV.
            --xlsx (bool): Export as Excel (.xlsx). Default is CSV.
            --msg (str): Optional log message to include in the terminal output.
            --filename (str): Name of the exported file (without extension). Default is 'exported_data'.
            --dir (str): Directory where the file should be saved. Default is the current directory.
            --force (bool): Overwrite file if it already exists. Default is False.
            --preview (bool): Show the export path and format without actually writing the file.

        Example:
            $ clipd export --json --filename my_data --dir ./exports --msg "Backup export"

        Returns:
            None
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = msg.strip()
        command_str = "export" + (" --msg" if msg else "") + (" --json" if json else "") + (" --xlsx" if xlsx else "") + (" --filename" if filename else "") + (" --dir" if dir else "") + (" --force" if force else "") + (" --preview" if preview else "")

        file_path = active_file()
        df = pd.read_csv(file_path)

        if df.empty:
            print("[bold red]No data to export.[/bold red] Please connect a file or process a DataFrame first.")
            log_command(
                command=command_str,
                detail=f"No data",
                status="Failed",
                msg=msg
            )
            raise typer.Exit(code=1)
        
        export_format = "csv"
        if json:
            export_format = "json"
        elif xlsx:
            export_format = "xlsx"

        export_path = Path(dir).resolve() / f"{filename}.{export_format}"
        export_path.parent.mkdir(parents=True, exist_ok=True)

        write_file(df, export_path, export_format)
        

        if preview:
            typer.secho(f"Would export as {export_format.upper()} to → {file_path}", fg=typer.colors.YELLOW)
            log_command(
                command=command_str,
                detail=f"Would export as {export_format.upper()} to → {file_path}",
                status="Completed",
                msg=msg
            )
            raise typer.Exit()

        if file_path.exists() and not force:
            typer.secho(f"File already exists at {file_path}. Use --force to overwrite.", fg=typer.colors.RED)
            log_command(
                command=command_str,
                detail=f"File already exists at {file_path}. Use --force to overwrite.",
                status="Failed",
                msg=msg
            )
            raise typer.Exit(code=1)

        try:
            write_file(df, file_path, export_format)
            typer.secho(f"{timestamp} | Exported as {export_format.upper()} → {file_path}", fg=typer.colors.YELLOW)
            log_command(
                command=command_str,
                detail=f"Would export as {export_format.upper()} to → {file_path}",
                status="Completed",
                msg=msg
            )

        except Exception as e:
            typer.secho(f"Export failed: {e}", fg=typer.colors.RED)
            log_command(
                command=command_str,
                detail=f"Failed to export due to {e}",
                status="Failed",
                msg=msg
            )

            raise typer.Exit(code=1)
