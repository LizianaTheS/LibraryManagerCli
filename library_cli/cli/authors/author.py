import typer
from library_cli.service.author_service import AuthorService
from library_cli.database.session_manager import SessionManager

session_manager = SessionManager()


def create(fullname: str = typer.Option(..., prompt="Fullname", help="Fullname of the author"),
           birth_year: str = typer.Option(..., prompt="BirthYear", help="Birth year of the author"),
           death_year: str = None,
           nationality: str = typer.Option(..., prompt="Nationality", help="Nationality of the author")):
    with session_manager.session_scope() as session:
        author_service = AuthorService(session)
        author = author_service.create(fullname, birth_year, death_year,
                                       nationality)  # change this
        typer.echo(author_service.get_schema().dump(author))


def get(author_id: int = typer.Option(..., prompt="AuthorID", help="Author id to get")):
    with session_manager.session_scope() as session:
        author_service = AuthorService(session)
        author = author_service.get(author_id, True)
        typer.echo(author)


def get_all():
    with session_manager.session_scope() as session:
        author_service = AuthorService(session)
        author = author_service.get_all(True)
        typer.echo(author)


def update(author_id: int = typer.Option(..., prompt="AuthorID", help="Author id to get"),
           fullname: str = typer.Option(..., prompt="Fullname", help="Fullname of the author"),
           birth_year: str = typer.Option(..., prompt="BirthYear", help="Birth year of the author"),
           death_year: str = None,
           nationality: str = typer.Option(..., prompt="Nationality", help="Nationality of the author")
           ):
    with session_manager.session_scope() as session:
        author_service = AuthorService(session)
        author = author_service.update(author_id, fullname, birth_year, death_year, nationality)

        typer.echo(author_service.get_schema().dump(author))


def delete(author_id: int = typer.Option(..., prompt="AuthorID", help="Author id to get")):
    with session_manager.session_scope() as session:
        author_service = AuthorService(session)
        author_service.delete(author_id)
        typer.echo("author has been deleted successfully")
