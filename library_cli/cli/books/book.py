import typer
from library_cli.database.session_manager import SessionManager
from library_cli.service.author_service import AuthorService
from library_cli.service.book_service import BookService
from library_cli.service.copy_service import CopyService
from library_cli.service.genre_service import GenreService
from library_cli.service.publisher_service import PublisherService

session_manager = SessionManager()


def create_book(title: str = typer.Option(..., prompt="Title", help="The title of your book"),
                genre_id: int = typer.Option(..., prompt="GenreId", help="The id your genres"),
                publisher_id: int = typer.Option(..., prompt="PublisherId", help="The id of your publisher"),
                subtitle: str = None,
                isbn: str = None,
                edition: str = None,
                published_year: str = typer.Option(..., prompt="PublishedYear", help="Published year of your book"),
                pages: int = None,
                language: str = typer.Option(..., prompt="Language", help="Your book language"),
                ):
    with session_manager.session_scope() as session:
        book_service = BookService(session)

        book = book_service.create(
            data={"title": title, "subtitle": subtitle, "isbn": isbn, "edition": edition,
                  "pages": pages,
                  "language": language,
                  "published_year": published_year,
                  "publisher_id": publisher_id,
                  "genre_id": genre_id
                  })
        typer.echo(book_service.get_schema().dump(book))


def update_book(book_id: int = typer.Option(..., prompt="BookID", help="The book id you want to update"),
                title: str = typer.Option(..., prompt="Title", help="The title of your book"),
                genre_id: int = typer.Option(..., prompt="GenreId", help="The id your genres"),
                publisher_id: int = typer.Option(..., prompt="PublisherId", help="The id of your publisher"),
                subtitle: str = None,
                isbn: str = None,
                edition: str = None,
                published_year: str = None,
                pages: int = None,
                language: str = None,
                author_ids: str = ""):
    authors = [int(a) for a in author_ids.split(",") if a]
    with session_manager.session_scope() as session:
        book_service = BookService(session)
        genre_service = GenreService(session)
        publisher_service = PublisherService(session)
        author_service = AuthorService(session)
        genre = genre_service.get(genre_id)
        publisher = publisher_service.get(publisher_id)
        authors_list = [author_service.get(author_id) for author_id in authors]
        data = {"title": title, "subtitle": subtitle, "isbn": isbn, "edition": edition,
                "published_year": published_year, "pages": pages, "authors": authors_list,
                "language": language, "publisher": publisher, "genre": genre}
        book = book_service.update(book_id, data)
        typer.echo(book_service.get_schema().dump(book))


def get_all(limit: int = 5):
    with session_manager.session_scope() as session:
        book_service = BookService(session)
        books = book_service.list_books(limit)
        typer.echo(books)


def get(book_id: int = typer.Option(..., prompt="BookID", help="The book id you want to update")):
    with session_manager.session_scope() as session:
        book_service = BookService(session)
        book = book_service.get(book_id, True)
        typer.echo(book)


def delete_book(book_id: int = typer.Option(..., prompt="BookID", help="The book id you want to delete")):
    with session_manager.session_scope() as session:
        book_service = BookService(session)
        book_service.delete(book_id)
        typer.echo("book has been deleted successfully")


def get_copies(book_id: int = typer.Option(..., prompt="BookID", help="The book id you want to get copies")):
    with session_manager.session_scope() as session:
        book_service = BookService(session)
        copy_service = CopyService(session)
        copies = book_service.get_copies(book_id)
        typer.echo(copy_service.get_schema().dump(copies, many=True))


def get_authors(book_id: int = typer.Option(..., prompt="BookID", help="The book id you want to get authors")):
    with session_manager.session_scope() as session:
        book_service = BookService(session)
        author_service = AuthorService(session)
        authors = book_service.get_authors(book_id)
        typer.echo(author_service.get_schema().dump(authors, many=True))
