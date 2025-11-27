import typer
from .loan import return_copy, borrow_copy, get

app = typer.Typer(help="Crud operations for loan")

app.command("return-copy")(return_copy)
app.command("borrow-copy")(borrow_copy)
app.command("get")(get)
