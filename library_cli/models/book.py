from sqlalchemy import Integer, String, Enum, DateTime, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from datetime import date
from typing import List

from library_cli.static import Language

from library_cli.config.sqlalchemy import Base, TimestampMixin, book_authors
from library_cli.database.mixin import BaseMixin, InstanceMixin


class Book(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    subtitle: Mapped[str] = mapped_column(String, nullable=True)
    isbn: Mapped[str] = mapped_column(String, nullable=True)
    edition: Mapped[str] = mapped_column(String(50), nullable=True)
    genre_id: Mapped[int] = mapped_column(ForeignKey("genres.id"))
    publisher_id: Mapped[int] = mapped_column(ForeignKey("publisher.id"))
    published_year: Mapped[date] = mapped_column(Date, nullable=True)
    pages: Mapped[int] = mapped_column(Integer, nullable=True)

    genre: Mapped["Genre"] = relationship("Genre", back_populates="books")
    publisher: Mapped["Publisher"] = relationship("Publisher", back_populates="books")
    copies: Mapped[List["Copy"]] = relationship("Copy", back_populates="book", init=False)
    authors: Mapped[List["Author"]] = relationship(
        secondary=book_authors,
        back_populates="books", init=False
    )
    logs: Mapped[List["InventoryLog"]] = relationship("InventoryLog", back_populates="book", init=False)

    language: Mapped[str] = mapped_column(Enum(Language), default=Language.PERSIAN)

    Schema = None

    def __repr__(self) -> str:
        return f"Book(id={self.id}, title={self.title}, pages={self.pages})"
