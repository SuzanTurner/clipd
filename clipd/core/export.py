import pandas as pd
from clipd.core.log_utils import log_command
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


def perform_export(df: pd.DataFrame, export_format: str, filename: str, dir: str, force: bool, preview: bool, msg: str = "", command : str = ""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    export_path = Path(dir).resolve() / f"{filename}.{export_format}"
    export_path.parent.mkdir(parents=True, exist_ok=True)

    if preview:
        typer.secho(f"Would export as {export_format.upper()} to → {export_path}", fg=typer.colors.YELLOW)
        log_command(command = command, detail=f"Preview export as {export_format.upper()} to → {export_path}", status="Completed", msg=msg)
        return

    if export_path.exists() and not force:
        typer.secho(f"File already exists at {export_path}. Use --force to overwrite.", fg=typer.colors.RED)
        log_command(command = command, detail=f"File already exists at {export_path}", status="Failed", msg=msg)
        # raise typer.Exit(code=1)
        return

    try:
        write_file(df, export_path, export_format)
        typer.secho(f"{timestamp} | Exported as {export_format.upper()} → {export_path}", fg=typer.colors.GREEN)
        log_command(command = command, detail=f"Exported as {export_format.upper()} to {export_path}", status="Completed", msg=msg)
    except Exception as e:
        typer.secho(f"Export failed: {e}", fg=typer.colors.RED)
        log_command(command=command, detail=f"Failed to export due to {e}", status="Failed", msg=msg)
        raise typer.Exit(code=1)
