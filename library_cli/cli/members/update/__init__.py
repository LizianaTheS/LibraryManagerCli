import typer
from .profile import update_profile
from .password import update_password

app = typer.Typer(help="Update member fields")

app.command("profile")(update_profile)
app.command("password")(update_password)
