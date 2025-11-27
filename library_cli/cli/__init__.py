import typer
from .members import app as members_app
from .publishers import app as publishers_app
from .books import app as books_app
from .authors import app as authors_app

app = typer.Typer()

app.add_typer(members_app, name="members")
app.add_typer(publishers_app, name="publishers")
app.add_typer(books_app, name="books")
app.add_typer(authors_app, name="authors")
