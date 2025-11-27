from sqlalchemy.orm import Session

from library_cli.config.logging import get_logger
from library_cli.models.author import Author
from library_cli.schemas import AuthorSchema
from datetime import datetime

from library_cli.static import Country
from library_cli.utils.helper_func import to_enum


class AuthorService:
    def __init__(self, session: Session):
        self.session = session
        self._model = Author
        self.schema = AuthorSchema
        self.logger = get_logger(self.__class__.__name__)

    def get_schema(self, load_instance: bool = True):
        return self.schema(load_instance=load_instance, session=self.session)

    def get(self, author_id: int, dumped: bool = False):
        schema = self.get_schema()
        author = self.session.get(Author, author_id)
        if not author:
            # log here
            raise ValueError(f"No author found with id {author_id}")
        return schema.dump(author) if dumped else author

    def create(self, fullname: str, birth_year: str, death_year: str = None, nationality: str = None):
        existing = self.session.query(Author).filter(
            Author.fullname == fullname,
            Author.birth_year == birth_year,
            Author.death_year == death_year
        ).first()
        if existing:
            # log here
            raise ValueError("There is already a author with above data")
        by = datetime.strptime(birth_year, "%Y-%m-%d").date()
        dy = datetime.strptime(death_year, "%Y-%m-%d").date() if death_year else None
        schema = self.get_schema()
        author = schema.load(
            data={"fullname": fullname, "birth_year": by, "death_year": dy, "nationality": to_enum(Country,nationality)},
            session=self.session)
        self.session.add(author)
        return author

    def get_all(self, dumped: bool = False):
        schema = self.get_schema()
        authors = self.session.query(Author).all()
        return schema.dump(authors, many=True) if dumped else authors

    def update(self, author_id: int, fullname: str, birth_year: str, death_year: str = None, nationality: str = None):
        author = self.get(author_id)
        schema = self.get_schema()
        by = datetime.strptime(birth_year, "%Y-%m-%d").date()
        dy = datetime.strptime(death_year, "%Y-%m-%d").date() if death_year else None
        new = schema.load(data={"fullname": fullname, "birth_year": by, "death_year": dy, "nationality": to_enum(Country,nationality)},
                          session=self.session, instance=author)
        self.session.add(new)
        return new

    def delete(self, author_id: int):
        author = self.get(author_id)
        self.session.delete(author)
