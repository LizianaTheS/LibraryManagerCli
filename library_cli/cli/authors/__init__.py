import typer
from .author import create, update, get, get_all, delete

app = typer.Typer(help="Author Crud Operations")

app.command("create")(create)
app.command("update")(update)
app.command("get")(get)
app.command("get-all")(get_all)
app.command("delete")(delete)
