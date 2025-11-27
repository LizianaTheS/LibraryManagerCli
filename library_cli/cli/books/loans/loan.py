import typer
from library_cli.database.session_manager import SessionManager
from library_cli.service.copy_service import CopyService
from library_cli.service.loan_service import LoanService
from library_cli.service.member_service import MemberService

session_manager = SessionManager()


def borrow_copy(copy_id: int = typer.Option(..., prompt="CopyID", help="The id of the copy version you want to borrow"),
                member_id: int = typer.Option(..., prompt="MemberID",
                                              help="The id of the member you want to borrow for"),
                ):
    with session_manager.session_scope() as session:
        loan_service = LoanService(session)
        member_service = MemberService(session)
        copy_service = CopyService(session)

        copy = copy_service.get(copy_id)
        member = member_service.get(member_id)
        loan = loan_service.borrow_copy(copy, member)
        typer.echo(loan_service.get_schema().dump(loan))


def return_copy(
        copy_id: int = typer.Option(..., prompt="CopyID", help="The id of the copy version you want to borrow")):
    with session_manager.session_scope() as session:
        copy_service = CopyService(session)
        loan_service = LoanService(session)
        copy = copy_service.get(copy_id)
        loan = loan_service.return_copy(copy)
        typer.echo(loan_service.get_schema().dump(loan))


def get(borrowing: bool = typer.Option(..., prompt="Borrowing", help="You wanna see borrowed loans"),
        returning: bool = typer.Option(..., prompt="Returning", help="You wanna see returned loans"),
        many: bool = typer.Option(..., prompt="many", help="get list of loans ?")):
    with session_manager.session_scope() as session:
        loan_service = LoanService(session)
        loans = loan_service.get_x_loan(borrowed_at=borrowing, returned_at=returning, many=many)
        typer.echo(loan_service.get_schema().dump(loans, many=many))
