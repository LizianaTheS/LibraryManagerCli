from sqlalchemy.orm import Session, joinedload

from library_cli.models import Book
from library_cli.schemas import BookSchema
from library_cli.config.logging import get_logger
from sqlalchemy import select
from typing import List
from datetime import date, datetime

from library_cli.service.author_service import AuthorService
from library_cli.service.genre_service import GenreService
from library_cli.service.publisher_service import PublisherService
from library_cli.static import Language
from library_cli.utils.helper_func import to_enum


class BookService:
    def __init__(self, session: Session):
        self._model = Book
        self.logger = get_logger(self.__class__.__name__)
        self.session = session
        self.schema = BookSchema

    def get_schema(self, load_instance: bool = True):
        return self.schema()

    def create(self, data: dict):
        schema = self.get_schema()
        data["language"] = to_enum(Language, data.get("language"))
        data["published_year"] = datetime.strptime(data.get("published_year"), "%Y-%m-%d").date()
        publisher_service = PublisherService(self.session)
        genre_service = GenreService(self.session)
        publisher = publisher_service.get(data.get("publisher_id"))
        genre = genre_service.get(data.get("genre_id"))
        # data["genre"] = genre
        # data["publisher"] = publisher
        # book = schema.load(data=data, session=self.session)
        # exists = self.session.execute(
        #     select(Book).where(Book.title == book.title,
        #                        Book.edition == book.edition)).scalar_one_or_none()
        #
        # if exists:
        #     self.logger.warning("Warning: Duplicate value, Class: Book, Message: A book with %s and %s already exists.",
        #                         book.title, book.edition)
        #     raise ValueError(f"There is a book with same `{book.title}` and `{book.edition}` ")

        # new=Book(title=book.title, subtitle=book.subtitle, isbn=book.isbn, edition=book.edition,
        #            genre_id=genre.id, publisher_id=publisher.publisher_id, published_year=book.publisher_year,
        #            pages=book.pages, genre=genre, publisher=publisher, language=book.language)

        validated = schema.load(data, partial=True)
        book = Book(
            title=validated.get("title").title() if validated.get("title") else None,
            subtitle=validated.get("subtitle"),
            isbn=validated.get("isbn"),
            edition=validated.get("edition"),
            genre_id=validated.get("genre_id"),
            publisher_id=validated.get("publisher_id"),
            genre=genre,
            publisher=publisher,
            pages=validated.get("pages"),
            language=validated.get("language"),  # keep enum object
            published_year=validated.get("published_year")
        )

        self.session.add(book)

        self.logger.info("Book `%s` added to the database.", book.title.title())
        return book

    def update(self, book_id: int, data: dict):
        schema = self.get_schema(True)

        book = self.get(book_id)

        modified = schema.load(data=data, instance=book, session=self.session, partial=True)

        self.session.add(modified)
        self.logger.info("Book `%s` updated.",
                         modified.title)
        return schema.dump(modified)

    def get(self, book_id, dumped: bool = False):
        book = self.session.get(Book, book_id)
        if not book:
            self.logger.warning("Warning: Not Found, Class: Book, Message: No book found with id %s", book_id)
            raise ValueError(f"No book found with id {book_id}")
        return book if not dumped else self.get_schema().dump(book)

    def delete(self, book_id):
        book = self.get(book_id)
        self.session.delete(book)

    def list_books(self, limit: int = 5):
        schema = self.get_schema()
        return schema.dump(
            self.session.query(Book)
            .options(
                joinedload(Book.copies),
                joinedload(Book.authors),
                joinedload(Book.logs)
            )
            .limit(limit)
            .all(),
            many=True
        )

    def get_copies(self, book_id: int) -> List["Copy"]:
        book = (
            self.session.query(Book)
            .options(joinedload(Book.copies))
            .filter(Book.id == book_id)
            .first()
        )

        if not book:
            raise ValueError(f"No book found with id {book_id}")

        return book.copies

    def get_authors(self, book_id: int) -> List["Author"]:
        book = (
            self.session.query(Book)
            .options(joinedload(Book.authors))
            .filter(Book.id == book_id)
            .first()
        )

        if not book:
            raise ValueError(f"No book found with id {book_id}")

        return book.authors
