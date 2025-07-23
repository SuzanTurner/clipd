from pathlib import Path
from clipd.core.session import disconnect_session
from clipd.core.log_utils import log_command
import typer 

class Disconnect():
    @staticmethod
    def disconnect(msg: str = typer.Option("", "--msg", help="Optional log message")) -> None:
        """
        Disconnect the current session and wipe memory of the linked file.

        Args: 
            --msg : Optional log msg

        Example:
            $ clipd disconnect --msg "Disconnecting"

        Returns:
            None
        """
        msg = msg.strip()
        command_str = "disconnect" + (" --msg" if msg else "")
        file = disconnect_session()
        try:
            if file:
                # file_name = str(Path(file).name)[:-2]
                file_name = str(Path(file).name)
                typer.secho(f"Disconnected from {file_name} ", fg=typer.colors.RED)
                log_command(command = command_str,
                            detail = f"Disconnected from {file_name}",
                            status = "Completed",
                            msg = msg)
            else:
                typer.secho(f"No active file. \nRun clipd connect <file>", fg=typer.colors.RED)
                log_command(command = command_str,
                            detail = f"No active file",
                            status = "Completed",
                            msg = msg)
        except Exception as e:
            log_command(command = command_str,
                        detail = f"Could not disconnect from {file_name} due to {e}",
                        status = "Failed",
                        msg = msg)
            raise typer.Exit(code=1)
