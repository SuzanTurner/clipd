from rich import print
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import track
from typer import Typer


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
    def why():
        print("[bold cyan]📜 The Origin of Clipd[/bold cyan]\n")

        print("[italic dim]Once upon a deployment...[/italic dim]")
        print("I was the ETL guy. You know the one — duct-taping pipelines at 2 AM,")
        print("wrangling CSVs that looked like they'd survived a war,")
        print("living between [bold]pandas[/bold], [bold]Jupyter notebooks[/bold], and [bold]frustration[/bold].\n")

        print("Every task felt like déjà vu.")
        print("Same cleanup, same transform, same exports... different bugs.")
        print("[yellow]All I wanted was something faster. Slicker. Cleaner. Lighter.[/yellow]\n")

        print("But all I got was more boilerplate, more notebooks, more 😮‍💨 copy-paste.")
        print("So one day, I snapped. Not in a villain arc way, more like a [italic]main-character moment[/italic].\n")

        print("[bold green]And I wrote Clipd.[/bold green]")
        print("Not a framework. Not a library. A [bold magenta]vibe[/bold magenta].")
        print("A CLI-first, ETL-tuned, zero-bullshit tool that respects your time.")
        print("Built with [bold]Typer[/bold], styled with [bold]Rich[/bold], and [bold]Pandas[/bold] ofcourse [dim](Don't bother about the hipocrasy) [/dim], powered by every moment I said,")
        print("[italic]'There has to be a better way.'[/italic]\n")
        

        print("[blue]Clipd is for the misfits who automate their pain,[/blue]")
        print("[blue]the rebels who don’t want to live inside Jupyter forever,[/blue]")
        print("[blue]and the builders who think CLI should be a love letter — not a chore.[/blue]\n")

        print("[bold yellow]Welcome to Clipd! [/bold yellow]")

console = Console()
selfdestruct_app = Typer()

class SelfDestruct():
    @staticmethod
    def self_destruct():
        
    
        console.clear()

        console.print(Panel.fit("[bold red]⚠️ INITIATING SELF-DESTRUCT SEQUENCE[/bold red]", border_style="bold red"))

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
                Text("Just kidding.", style="bold green"),
                title="[bold red]Abort Mission[/bold red]",
                subtitle="clipd eggs",
                border_style="bold red"
            )
        )
