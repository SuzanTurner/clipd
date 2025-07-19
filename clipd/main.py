from clipd.commands import log
from clipd.core.suggestions import SuggestGroup
from clipd.base import base  
from clipd.commands import log
import typer

app = typer.Typer(cls=SuggestGroup, help="Command Line Interface for Pandas")


app.add_typer(base.get_base_app())
app.add_typer(log.app, name="log")


def main():
    app()

if __name__ == "__main__":
    main()
