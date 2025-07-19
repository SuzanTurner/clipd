import typer
from clipd.core.log_utils import clear_history, get_log, log_command, get_json_logs, num_log
import json

log_app = typer.Typer(help="Display and manage logs", invoke_without_command=True)  

# TODO : Format Logs!! (" --msg" if msg else "")

@log_app.callback()
def show_logs(
    ctx: typer.Context,
    lines: int = 10,
    msg: str = typer.Option("", "--msg", help="Optional log message"),
    json_flag: bool = typer.Option(False, "--json", help="Show raw JSON logs"),
    all: bool = typer.Option(False, "--all", help="Show all logs")
):
    try:
        if ctx.invoked_subcommand is None:
            logs = get_json_logs(lines) if json_flag else get_log(float('inf') if all else lines)
            if json_flag:
                typer.echo(json.dumps(logs[::-1], indent=2))
            elif logs:
                for line in logs:
                    typer.echo(line.strip())
            else:
                print("Clean Slate")

            log_command(command="log", detail="Viewed logs", status="Completed", msg=msg)
    except Exception as e:
        log_command(command="log", detail=f"Could not view logs due to {e}", status="Failed", msg=msg)


@log_app.command("clear", help="Clears all logs from the current session")
def clear_logs(msg: str = typer.Option("", "--msg", help="Optional log message")):
    try:
        log_count = num_log()
        confirm = typer.confirm(f"Are you sure you want to delete {log_count} log{'s' if log_count != 1 else ''}?")

        if not confirm:
            typer.secho("Aborted. Logs not cleared.", fg=typer.colors.YELLOW)
            log_command(command="log clear", detail="User aborted log clear", status="Cancelled", msg=msg)
            return

        clear_history()
        typer.secho("Logs cleared.", fg=typer.colors.RED, bold=True)
        log_command(command="log clear", detail="Cleared logs", status="Completed", msg=msg)

    except Exception as e:
        typer.secho(f"Error: {e}", fg=typer.colors.RED)
        log_command(command="log clear", detail=f"Unable to clear logs due to {e}", status="Failed", msg=msg)
