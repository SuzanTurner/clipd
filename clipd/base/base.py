from clipd.base.init import Init
from clipd.base.connect import Connect
from clipd.base.describe import Describe
from clipd.base.log import log_app
from clipd.base.eggs import Thankyou, Why, SelfDestruct
from clipd.base.export import Export
from clipd.base.disconnect import Disconnect
import typer

def base():
    app = typer.Typer()

    app.add_typer(log_app, name="log")

    app.command("init", help = "Initialising Clipd.")(Init.init)
    app.command("connect", help = "Connects to excel/csv file.")(Connect.connect)
    app.command("describe", help = "Pandas describe function. ")(Describe.describe)
    app.command("export", help = "Export the modified DataFrame to the current directory in csv.")(Export.export)
    app.command("disconnect", help = "Disconnects from active file")(Disconnect.disconnect)
    app.command("thankyou", help = "Gratitude message")(Thankyou.thank_you)
    app.command("why", help = "The origin of clipd")(Why.why)
    app.command("selfdestruct")(SelfDestruct.self_destruct)

    return app
