from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import List

from library_cli.config.sqlalchemy import Base, TimestampMixin
from library_cli.database.mixin import BaseMixin, InstanceMixin


class Genre(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    books: Mapped[List["Book"]] = relationship("Book", back_populates="genre", init=False)
    Schema = None

    def __repr__(self) -> str:
        return f"Genre(id={self.id}, name={self.name})"
