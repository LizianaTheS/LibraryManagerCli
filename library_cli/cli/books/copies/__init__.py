import typer
from .copy import create, mark_action_as, mark_condition_as, find_by, get_loans, get_reservations, get_all

app = typer.Typer(help="Copy Crud Operations")

app.command("create")(create)
app.command("mark-action-as")(mark_action_as)
app.command("mark-condition-as")(mark_condition_as)
app.command("find-by")(find_by)
app.command("get-loans")(get_loans)
app.command("get-reservations")(get_reservations)
app.command("get-all")(get_all)
