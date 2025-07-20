from rich import print
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from typer import Typer
import typer


class Thankyou():  
    @staticmethod
    def thank_you():
        """
        Gratitude function 
        No args
        No flags

        Eg:
            clipd thankyou

        Output:
            Thank you @tiangolo, creator of Typer and FastAPI
        
        """
        print("Thank you [bold yellow]@tiangolo[/bold yellow], creator of [bold blue]Typer[/bold blue] and [bold green]FastAPI[/bold green]")

class Why():
    @staticmethod
    def why(long : bool = typer.Option(False, "--long", help = "Long Story not short")):
        if long:
            print("[bold cyan]📜 The Origin of Clipd[/bold cyan]\n")
            print("I was this backend guy at this **** company that paid me lesser than my self-confidance")
            print("Wrangling CSVs and APIs and DBs ")

            print("The data cleaning felt like torture")
            print("[yellow]All I wanted was something faster. Slicker. Cleaner. Lighter.[/yellow]")
            print("[green]Something that saved my time[/green]\n")

            print("[italic]So one afternoon... I put my brains to work[/italic]")
            print("[italic dim]And here we are...[/italic dim]")
        
            print("[bold yellow]Welcome to Clipd! [/bold yellow]")
        else:
            print("[bold yellow]Long story short [/bold yellow]")
            print("I was bored one afternoon")

console = Console()
selfdestruct_app = Typer()

class SelfDestruct():
    @staticmethod
    def self_destruct():
        
    
        console.clear()

        console.print(Panel.fit("[bold red]⚠️INITIATING SELF-DESTRUCT SEQUENCE[/bold red]", border_style="bold red"))

        countdown = [5, 4, 3, 2, 1]

        for i in countdown:
            console.print(f"[bold yellow]T-minus {i}...[/bold yellow]", justify="center")
            time.sleep(1)

        console.print("[bold red]💥 Detonating core modules...[/bold red]", justify="center")
        time.sleep(1)

        for _ in track(range(30), description="[red]Wiping pandas traces...[/red]"):
            time.sleep(0.05)

        messages = [
            "Deleting all CSVs...",
            "Deleting all .py files",
            "Deleting system.exe"
        ]

        for msg in messages:
            console.print(f"[italic red]{msg}[/italic red]")
            time.sleep(0.6)

        console.print("\n[bold red]💀 SYSTEM FAILURE IMMINENT 💀[/bold red]", justify="center")
        time.sleep(2)

        console.clear()
        console.print(
            Panel.fit(
                Text("clipd CHECKPOINT to the rescue", style="bold green"),
                title="[bold red]Abort Mission[/bold red]",
                subtitle="clipd eggs",
                border_style="bold red"
            )
        )
