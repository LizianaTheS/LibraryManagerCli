import typer

from library_cli.service.copy_service import CopyService
from library_cli.service.member_service import MemberService
from library_cli.service.reservation_service import ReservationService
from library_cli.database.session_manager import SessionManager

session_manager = SessionManager()


def reserve(copy_id: int = typer.Option(..., prompt="CopyID", help="The id of the copy version you want to reserve"),
            member_id: int = typer.Option(..., prompt="MemberID",
                                          help="The id of the member you want to reserve for")):
    with session_manager.session_scope() as session:
        member_service = MemberService(session)
        copy_service = CopyService(session)
        reservation_service = ReservationService(session)
        copy = copy_service.get(copy_id)
        member = member_service.get(member_id)
        reservation = reservation_service.reserve(copy, member)
        typer.echo(reservation_service.get_schema().dump(reservation))


def cancel_reserve(
        res_id: int = typer.Option(..., prompt="ReservationID", help="The reservation id you want to cancel")):
    with session_manager.session_scope() as session:
        reservation_service = ReservationService(session)
        reservation_service.cancel_reservation(res_id)
        typer.echo("Reservation time got cancelled")


def get(copy_id: int = typer.Option(..., prompt="CopyID", help="The id of the copy version you want to reserve"),
        member_id: int = typer.Option(..., prompt="MemberID",
                                      help="The id of the member you want to reserve for"),
        reserved: bool = None,
        expired: bool = None,
        status: str = None,
        dumped: bool = True,
        many: bool = False):
    with session_manager.session_scope() as session:
        reservation_service = ReservationService(session)
        reservation = reservation_service.get_x_reservation(copy_id, member_id, reserved, expired,
                                                            status, dumped,
                                                            many)
        typer.echo(reservation)


def get_all(reserved: bool = typer.Option(..., prompt="Reserved", help="You wanna see reserved contracts ?"),
            expired: bool = typer.Option(..., prompt="Expired", help="You wanna see reserved contracts ?"),
            status: str = typer.Option(..., prompt="Status", help="Status of contract"),
            many: bool = typer.Option(..., prompt="Many", help="You wanna see a list ?")):
    with session_manager.session_scope() as session:
        reservation_service = ReservationService(session)
        reservation = reservation_service.get_all(reserved, expired,
                                                  status,
                                                  True, many)
        typer.echo(reservation)
