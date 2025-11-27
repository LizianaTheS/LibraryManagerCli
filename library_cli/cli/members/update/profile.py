import typer

from library_cli.service.member_service import MemberService
from library_cli.database.session_manager import SessionManager

session_manager = SessionManager()


def update_profile(
        member_id: int = typer.Option(..., prompt="Member ID to update", help="The ID of the members to update"),
        fullname: str = typer.Option(prompt="Fullname", help="New full name of the members"),
        phone: str = typer.Option(prompt="Phone", help="New phone to update")

):
    """
    Update an existing members. Only provided fields will be updated.
    """
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        member = member_service.update(member_id, {"fullname": fullname, "phone": phone})
        typer.echo(member_service.get_schema().dump(member))
