import typer

from library_cli.service.book_service import BookService
from library_cli.service.copy_service import CopyService
from library_cli.database.session_manager import SessionManager
from library_cli.service.loan_service import LoanService
from library_cli.service.reservation_service import ReservationService

session_manager = SessionManager()


def create(book_id: int = typer.Option(..., prompt="BookID", help="The book id you want to create copy for")):
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        book_service = BookService(session)
        book = book_service.get(book_id)
        copy = copy_service.create(book, {})
        typer.echo(copy_service.get_schema().dump(copy))


def mark_condition_as(copy_id: int = typer.Option(..., prompt="CopyID", help="The copy id you want to update"),
                      condition: str = typer.Option(..., prompt="Condition", help="The condition for your book")):
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        copy = copy_service.mark_condition_as(condition, copy_id)
        typer.echo(copy_service.get_schema().dump(copy))


def mark_action_as(copy_id: int = typer.Option(..., prompt="CopyID", help="The copy id you want to delete"),
                   action: str = typer.Option(..., prompt="Action", help="The action for your book")):
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        copy = copy_service.mark_action_as(action, copy_id)
        typer.echo(copy_service.get_schema().dump(copy))


def find_by(action: str = typer.Option(..., prompt="Action", help="The action for your book"),
            condition: str = typer.Option(..., prompt="Condition", help="The condition for your book"),
            many: bool = False,
            ):
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        fetched = copy_service.get_x_copy(action,
                                          condition, many, True)
        typer.echo(fetched)


def get_loans(copy_id: int = typer.Option(..., prompt="CopyID", help="The copy id you want to get loans")):
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        loan_service = LoanService(session)
        loans = copy_service.get_loans(copy_id)
        typer.echo(loan_service.get_schema().dump(loans, many=True))


def get_all():
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        copies = copy_service.get_all_copies(True)
        typer.echo(copies)


def get_reservations(
        copy_id: int = typer.Option(..., prompt="CopyID", help="The copy id you want to get reservations")):
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        res_service = ReservationService(session)
        reservations = copy_service.get_reservations(copy_id)
        typer.echo(res_service.get_schema().dump(reservations, many=True))
