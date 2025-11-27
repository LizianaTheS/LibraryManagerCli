import typer

from library_cli.service.loan_service import LoanService
from library_cli.service.member_service import MemberService
from library_cli.database.session_manager import SessionManager
from library_cli.service.reservation_service import ReservationService
from library_cli.static import Status

session_manager = SessionManager()


def login(username: str = typer.Option(..., prompt="Username", help="Enter your username"),
          password: str = typer.Option(..., prompt="Password", help="Enter your password")):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        member = member_service.login(username, password)
        typer.echo(member_service.get_schema().dump(member))


def list_members():
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        members = member_service.get_members(True)
        typer.echo(members)


def create_member(
        fullname: str = typer.Option(..., prompt=True, help="Full name of the members"),
        username: str = typer.Option(..., prompt=True, help="Username of the members"),
        email: str = typer.Option(..., prompt=True, help="Email address of the members"),
        password: str = typer.Option(..., prompt=True, help="Password of the members")
):
    data = {"fullname": fullname, "username": username, "email": email, "password": password, "status": "active"}
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        member = member_service.create(data)
        typer.echo(member_service.get_schema().dump(member))


def delete(member_id: int = typer.Option(..., prompt="MemberID", help="The member you want to delete ")):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        member = member_service.mark_status_as(Status.DELETED, member_id)
        typer.echo(member_service.get_schema().dump(member))


def get_active_reservations(
        member_id: int = typer.Option(..., prompt="MemberID", help="The member you want to delete ")):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        res_service = ReservationService(session)
        reservations = member_service.get_active_reservations(member_id)
        typer.echo(res_service.get_schema().dump(reservations, many=True))


def get_active_loans(
        member_id: int = typer.Option(..., prompt="MemberID", help="The member you want to delete ")):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        loan_service = LoanService(session)
        loans = member_service.get_active_loans(member_id)
        typer.echo(loan_service.get_schema().dump(loans, many=True))


def search_member(
        fullname: str = typer.Option(None, help="New full name of the members"),
        phone: str = typer.Option(None, help="Update your phone number")
):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        members = member_service.search_member(fullname, phone)
        typer.echo(member_service.get_schema().dump(members, many=True))


def get(member_id: int = typer.Option(..., prompt="MemberID", help="The member you want to get ")):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        member = member_service.get(member_id, True)
        return typer.echo(member)
