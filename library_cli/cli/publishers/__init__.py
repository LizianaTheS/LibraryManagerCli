import typer
from .publisher import create_publisher, update, get, delete, get_all

app = typer.Typer(help="Publisher Crud Operations")

app.command("create")(create_publisher)
app.command("update")(update)
app.command("get")(get)
app.command("delete")(delete)
app.command("get-all")(get_all)
