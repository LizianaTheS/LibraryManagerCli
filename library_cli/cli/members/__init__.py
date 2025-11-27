import typer

from .member import login, list_members, create_member, delete, get_active_loans, get_active_reservations, \
    search_member, get
from .update import app as update_app

app = typer.Typer(help="Manage members")

app.command("create")(create_member)
app.command("login")(login)
app.command("delete")(delete)
app.command("get")(get)
app.command("get-active-loans")(get_active_loans)
app.command("get-active-reservations")(get_active_reservations)
app.command("search-member")(search_member)
app.command("list-members")(list_members)

app.add_typer(update_app, name="update")
