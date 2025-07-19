import typer
from clipd.core.log_utils import clear_history, get_log, log_command, get_json_logs, num_log
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
            if logs:
                for line in logs:
                    typer.echo(line.strip())
            else:
                print("Clean Slate")

        log_command(command= "log", detail= f"Veiwed logs", status= "Completed", msg = msg) 

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


# @app.command("clear")
# def clear_logs(msg: str = typer.Option("", "--msg", help="Optional log message")):
#     try:
#         clear_history()
#         log_command(command= "log clear", detail= f"Cleared logs", status= "Completed", msg = msg) 
#     except Exception as e:
#         log_command(command= "log clear", detail= f"Unable to clear logs due to {e}", status= "Failed", msg = msg)

@app.command("clear")
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