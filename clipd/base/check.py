from clipd.core.session import active_file, filename, load_session
from clipd.core.decorators import requires_connection
from clipd.core.load import load
from clipd.core.log_utils import log_command
from rich import print
from scipy.stats import entropy
from clipd.core.table import print_table
from pathlib import Path
import typer 
import pandas as pd

# TODO : Also check if connected fie is clean

class Check():
    @requires_connection
    @staticmethod
    def check(msg: str = typer.Option("", "--msg", help="Optional log message"),
              ) -> None:
        """
        Checks current active file
        """

        msg = msg.strip()
        command_str = "check " + ("--msg" if msg else "")
        path = active_file()
        
        if filename(path):
            print(f"Connected to [bold green]{filename(path)}[/bold green]")
            log_command(
                command = command_str,
                detail = "Checking active file",
                status= "Completed",
                msg = command_str
            )
        else:
            log_command(
                command = command_str,
                detail = "Could not check active file",
                status= "Failed",
                msg = command_str
            )

       
