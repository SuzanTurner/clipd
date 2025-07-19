import typer
import difflib
from typing import List
from typer.core import TyperGroup

class SuggestGroup(TyperGroup):
    def get_command(self, ctx, cmd_name):
        cmd = super().get_command(ctx, cmd_name)
        if cmd:
            return cmd
        available_commands: List[str] = self.commands.keys()
        suggestion = difflib.get_close_matches(cmd_name, available_commands, n=1)
        if suggestion:
            typer.secho(f"No such command '{cmd_name}'. Did you mean '{suggestion[0]}'?", fg=typer.colors.YELLOW)
        else:
            typer.secho(f"No such command '{cmd_name}'.", fg=typer.colors.RED)
        raise typer.Exit(1)