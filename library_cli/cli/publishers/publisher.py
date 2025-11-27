import typer

from library_cli.service.publisher_service import PublisherService
from library_cli.database.session_manager import SessionManager

session_manager = SessionManager()


def create_publisher(name: str = typer.Option(..., prompt="Name", help="The publisher name"),
                     country: str = typer.Option(..., prompt="Country", help="The country the publisher is from"),
                     founded_year: str = typer.Option(..., prompt="FoundedYear",
                                                      help="When publisher has been founded")):
    with session_manager.session_scope() as session:
        publisher_service = PublisherService(session)
        publisher = publisher_service.create(name, country, founded_year)
        typer.echo(publisher_service.get_schema().dump(publisher))


def update(publisher_id: int = typer.Option(..., prompt="PublisherID", help="Publisher id to find"),
           name: str = typer.Option(..., prompt="Name", help="The publisher name"),
           country: str = typer.Option(..., prompt="Country", help="The country the publisher is from"),
           founded_year: str = typer.Option(..., prompt="FoundedYear",
                                            help="When publisher has been founded")
           ):
    with session_manager.session_scope() as session:
        publisher_service = PublisherService(session)
        publisher = publisher_service.update(publisher_id, name, country, founded_year)
        typer.echo(publisher_service.get_schema().dump(publisher))


def get_all():
    with session_manager.session_scope() as session:
        publisher_service = PublisherService(session)
        publishers = publisher_service.get_all(True)
        typer.echo(publishers)


def get(publisher_id: int = typer.Option(..., prompt="PublisherID", help="Publisher id to find")):
    with session_manager.session_scope() as session:
        publisher_service = PublisherService(session)
        publisher = publisher_service.get(publisher_id, True)
        typer.echo(publisher)


def delete(publisher_id: int = typer.Option(..., prompt="PublisherID", help="Publisher id to find")):
    with session_manager.session_scope() as session:
        publisher_service = PublisherService(session)
        publisher_service.delete(publisher_id)
        typer.echo("Publisher has been deleted")
