import typer
from clipd.core.log_utils import clear_history, get_log, log_command, get_json_logs
import json

app = typer.Typer(help = "Clearing Logs", invoke_without_command=True)

# @app.callback()
# def show_logs(ctx: typer.Context, lines: int = 10, msg: str = typer.Option("", "--msg", help="Optional log message")):
#     if ctx.invoked_subcommand is None:
#         logs = get_log(lines)
#         if not logs:
#             typer.echo("No logs yet.")
#         else:
#             for log in logs:
#                 try:
#                     log_entry = json.loads(log)
#                     typer.echo(
#                         f"[{log_entry['timestamp']}] {log_entry['command']} "
#                         f"{log_entry['status']} "
#                         + (f"| {log_entry['msg']}" if log_entry.get("msg") else "")
#                     )
#                 except json.JSONDecodeError:
#                     typer.echo(f"(Unreadable log entry): {log.strip()}")
#         log_command(f"Viewed last {lines} log entries", msg=msg)

@app.callback()
def show_logs(
    ctx: typer.Context,
    lines: int = 10,
    msg: str = typer.Option("", "--msg", help="Optional log message"),
    json_flag: bool = typer.Option(False, "--json", help="Show raw JSON logs"),
):
    if ctx.invoked_subcommand is None:
        if json_flag:
            logs = get_json_logs(lines)
            typer.echo(json.dumps(logs, indent=2))
        else:
            logs = get_log(lines)
            for line in logs:
                typer.echo(line.strip())

        log_command(f"Viewed last {lines} log entries", msg=msg)

# @app.callback()
# def show_logs_json(
#     ctx: typer.Context,
#     lines: int = 10,
#     msg: str = typer.Option("", "--msg", help="Optional log message"),
#     json_flag: bool = typer.Option(False, "--json", help="Show raw JSON logs"),
# ):
#     if ctx.invoked_subcommand is None:
#         history = get_log(lines)
#         if not history:
#             typer.echo("No logs yet.")
#             return

#         if json_flag:
#             import json
#             json_logs = []
#             for line in history:
#                 try:
#                     json_logs.append(json.loads(line))
#                 except Exception:
#                     pass  # Skip if not valid JSON

#             typer.echo(json.dumps(json_logs, indent=2))
#         else:
#             for line in history:
#                 typer.echo(line.strip())

#         log_command(f"Viewed last {lines} log entries", msg=msg)


@app.command("clear")
def clear_logs(msg: str = typer.Option("", "--msg", help="Optional log message")):
    clear_history()
    log_command(f"History cleared", msg = msg)