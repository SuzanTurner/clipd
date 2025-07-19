from rich import print


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