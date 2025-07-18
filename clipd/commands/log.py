import typer
from clipd.core.log_utils import clear_history, get_log, log_command

app = typer.Typer(help = "Clearing Logs", invoke_without_command=True)

@app.callback()
def show_logs(ctx: typer.Context, lines: int = 10, msg: str = typer.Option("", "--msg", help="Optional log message")):
    if ctx.invoked_subcommand is None:
        history = get_log(lines)
        if not history:
            typer.echo("No logs yet.")
        else:
            for line in history:
                typer.echo(line.strip())
        log_command(f"Viewed last {lines} log entries", msg = msg)

@app.command("clear")
def clear_logs(msg: str = typer.Option("", "--msg", help="Optional log message")):
    clear_history()
    log_command(f"History cleared", msg = msg)