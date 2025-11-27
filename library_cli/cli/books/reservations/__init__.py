import typer
from .reservation import reserve, cancel_reserve, get, get_all

app = typer.Typer(help="Crud operations for reservation")

app.command("reserve")(reserve)
app.command("cancel")(cancel_reserve)
app.command("get")(get)
app.command("get-all")(get_all)
