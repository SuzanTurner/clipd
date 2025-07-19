from clipd.core.suggestions import SuggestGroup
from clipd.base import base  
import typer

app = typer.Typer(cls=SuggestGroup,  help="Command Line Interface for Pandas")


app.add_typer(base.base())

def main():
    app()

if __name__ == "__main__":
    main()
