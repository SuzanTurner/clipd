
from clipd.commands import log
from clipd.base.base import Base

import typer

app = typer.Typer(help="Command Line Interface for Pandas")

app.add_typer(log.app, name = "log")
app.command("init", help="Start command")(Base.init)
app.command("connect", help = "Connects to excel/csv/ file")(Base.connect)
app.command("describe")(Base.describe)
app.command("status", help = "Displays current active file")(Base.show_connected_file)


def main():
    app()

if __name__ == "__main__":
    main()
