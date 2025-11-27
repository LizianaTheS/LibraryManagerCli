import typer
from library_cli.service.genre_service import GenreService
from library_cli.database.session_manager import SessionManager

session_manager = SessionManager()


def create(name: str = typer.Option(..., prompt="Name", help="The name of your genres")):
    with session_manager.session_scope() as session:
        genre_service = GenreService(session)
        genre = genre_service.create(name)
        typer.echo(genre_service.get_schema().dump(genre))


def update(genre_id: int = typer.Option(..., prompt="GenreID", help="The id of the genres you want to update"),
           name: str = typer.Option(..., prompt="Name", help="The name of your genres")):
    with session_manager.session_scope() as session:
        genre_service = GenreService(session)
        genre = genre_service.update(genre_id, name)
        typer.echo(genre_service.get_schema().dump(genre))


def delete(genre_id: int = typer.Option(..., prompt="GenreID", help="The id of the genres you want to delete")):
    with session_manager.session_scope() as session:
        genre_service = GenreService(session)
        genre_service.delete(genre_id)
        typer.echo("Genre has been deleted successfully")


def get(genre_id: int = typer.Option(..., prompt="GenreID", help="The id of the genres you want to get")):
    with session_manager.session_scope() as session:
        genre_service = GenreService(session)
        genres = genre_service.get(genre_id, True)
        typer.echo(genres)


def get_all():
    with session_manager.session_scope() as session:
        genre_service = GenreService(session)
        genres = genre_service.get_all_genres(True)
        typer.echo(genres)
