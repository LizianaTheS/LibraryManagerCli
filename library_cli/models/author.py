from sqlalchemy import Integer, String, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List

from library_cli.config.sqlalchemy import Base, TimestampMixin, book_authors
from library_cli.static import Country
from library_cli.database.mixin import BaseMixin, InstanceMixin


# from library_cli.schemas import AuthorSchema


class Author(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    fullname: Mapped[str] = mapped_column(String(100))
    birth_year: Mapped[date] = mapped_column(Date)
    death_year: Mapped[date] = mapped_column(Date, nullable=True)

    books: Mapped[List["Book"]] = relationship(
        secondary=book_authors,
        back_populates="authors", init=False
    )
    nationality: [str] = mapped_column(Enum(Country), default=Country.IRAN)

    Schema = None

    def __repr__(self) -> str:
        return f"Author(id={self.id}, fullname={self.fullname}, birth_year={self.birth_year}, death_year={self.death_year}, nationality={self.nationality})"
