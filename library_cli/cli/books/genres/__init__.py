import typer
from .genre import create, delete, update, get, get_all

app = typer.Typer(help="Genre Crud operations")

app.command("create")(create)
app.command("update")(update)
app.command("get")(get)
app.command("get-all")(get)
app.command("delete")(delete)
