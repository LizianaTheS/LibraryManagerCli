import typer
from .genres import app as genre_app
from .loans import app as loan_app
from .reservations import app as res_app
from .book import create_book, update_book, delete_book, get_authors, get_copies, get_all,get
from .copies import app as copies_app

app = typer.Typer(help="Genre Crud | Book Crud | Loan Crud | Reservation Crud")

app.add_typer(genre_app, name="genres")
app.add_typer(loan_app, name="loans")
app.add_typer(res_app, name="reservations")
app.add_typer(copies_app, name="copies")

app.command("create")(create_book)
app.command("update")(update_book)
app.command("delete")(delete_book)
app.command("get-authors")(get_authors)
app.command("get-copies")(get_copies)
app.command("get-all")(get_all)
app.command("get")(get)
