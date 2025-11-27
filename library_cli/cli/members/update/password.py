import typer

from library_cli.service.member_service import MemberService
from library_cli.database.session_manager import SessionManager

session_manager = SessionManager()


def update_password(member_id: int = typer.Option(..., prompt="id", help="Your current member id"),
                    old_password: str = typer.Option(..., prompt="old_password", help="Enter your current password"),
                    new_password: str = typer.Option(..., prompt="new_password", help="Enter your new password")):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        member = member_service.update_password(member_id, old_password, new_password)
        typer.echo(member_service.get_schema().dump(member))
        typer.echo("password has been updated successfully")
