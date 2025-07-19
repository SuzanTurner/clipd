
from clipd.core.log_utils import log_command
from clipd.core.session import SESSION_PATH
from rich import print
import typer

class Init:
    @staticmethod
    def init(msg: str = typer.Option("", "--msg", help="Optional log message")):

        """
        Initializes Clipd.

        Logs the initialization command and optionally records a custom log message.

        Args:
            msg (str, optional): Optional log message passed via --msg.

        Example:
            $ clipd init --msg "Here's a msg"
            Clipd Initialised!

        Returns:
            None
        """

        msg = msg.strip()
        command_str = "init" + (" --msg" if msg else "")
        try:
            if not SESSION_PATH.exists():
                typer.secho("Clipd Initialised!", fg=typer.colors.GREEN, bold=True)
                log_command(
                    command=command_str,
                    detail="Clipd Initialised",
                    status="Completed",
                    msg=msg
                )
            else:
                typer.secho("Clipd Reinitialised!", fg=typer.colors.GREEN, bold=True)
                print(f"[dim]Connected to session {SESSION_PATH}[/dim]")
                log_command(
                    command=command_str,
                    detail="Clipd Initialised",
                    status="Completed",
                    msg=msg
                )
        except Exception as e:
            log_command(
                command=command_str,
                detail=f"Failed to initialise clipd due to {e}",
                status="Failed",
                msg=msg
            )