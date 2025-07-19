from clipd.base.init import Init
from clipd.base.connect import Connect
from clipd.base.describe import Describe
from clipd.base.thankyou import Thankyou
import typer

def get_base_app():
    app = typer.Typer()

    app.command("init", help = "Initialising Clipd")(Init.init)
    app.command("connect", help = "Connects to excel/csv file")(Connect.connect)
    app.command("describe", help = "Pandas describe function")(Describe.describe)
    app.command("thankyou", help = "Gratitude message")(Thankyou.thank_you)

    return app
