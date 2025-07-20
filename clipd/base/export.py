import pandas as pd
from clipd.core.session import active_file
from clipd.core.log_utils import log_command
from rich import print
from pathlib import Path
import typer 
from pathlib import Path
from datetime import datetime


def write_file(df, path: Path, format: str):
    if format == "csv":
        df.to_csv(path, index=False)
    elif format == "json":
        df.to_json(path, orient="records", indent=2)
    elif format == "xlsx":
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported format: {format}")



class Export:
    @staticmethod
    def export(
        json: bool = typer.Option(False, "--json", help="Export in JSON format"),
        xlsx: bool = typer.Option(False, "--xlsx", help="Export in Excel (.xlsx) format"),
        msg: str = typer.Option("", "--msg", help="Optional log message"),
        filename: str = typer.Option("exported_from_clipd", "--filename", "-f", help="Custom filename (without extension)"),
        dir: str = typer.Option("clipd_outputs", "--dir", help="Directory to export the file to"),
        force: bool = typer.Option(False, "--force", "-F", help="Overwrite file if it exists"),
        preview: bool = typer.Option(False, "--preview", help="Show the full export path and format without writing file"),
    ):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = msg.strip()
        command_str = "export" + (" --msg" if msg else "") + (" --json" if json else "") + (" --xlsx" if xlsx else "") + (" --filename" if filename else "") + (" --dir" if dir else "") + (" --force" if force else "") + (" --preview" if preview else "")

        try:
            file_path = active_file()
            df = pd.read_csv(file_path)
        except FileNotFoundError:
            print("[bold red]No file found \nRun clipd connect <file> [/bold red] ")
            raise typer.Exit(code = 1)
        

        if df.empty:
            print("[bold red]No data to export.[/bold red]")
            log_command(command=command_str, detail="No data", status="Failed", msg=msg)
            raise typer.Exit(code=1)

        # Determine export format
        export_format = "csv"
        if json:
            export_format = "json"
        elif xlsx:
            export_format = "xlsx"

        # Build export path
        export_path = Path(dir).resolve() / f"{filename}.{export_format}"
        export_path.parent.mkdir(parents=True, exist_ok=True)

        # Preview-only mode
        if preview:
            typer.secho(f"Would export as {export_format.upper()} to → {export_path}", fg=typer.colors.YELLOW)
            log_command(
                command=command_str,
                detail=f"Preview export as {export_format.upper()} to → {export_path}",
                status="Completed",
                msg=msg
            )
            raise typer.Exit()

        # File exists check
        if export_path.exists() and not force:
            typer.secho(f"File already exists at {export_path}. Use --force to overwrite.", fg=typer.colors.RED)
            log_command(
                command=command_str,
                detail=f"File already exists at {export_path}. Use --force to overwrite.",
                status="Failed",
                msg=msg
            )
            raise typer.Exit(code=1)

        # Export file
        try:
            write_file(df, export_path, export_format)
            typer.secho(f"{timestamp} | Exported as {export_format.upper()} → {export_path}", fg=typer.colors.GREEN)
            log_command(
                command=command_str,
                detail=f"Exported as {export_format.upper()} → {export_path}",
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
