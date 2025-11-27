from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List
from sqlalchemy import Enum
from library_cli.config.sqlalchemy import Base, TimestampMixin
from library_cli.database.mixin import BaseMixin, InstanceMixin
from library_cli.static import Country


class Publisher(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "publisher"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str] = mapped_column(String(100))
    country: Mapped[str] = mapped_column(Enum(Country))
    founded_year: Mapped[date] = mapped_column(Date)
    books: Mapped[List["Book"]] = relationship("Book", back_populates="publisher", init=False)

    Schema = None

    def __repr__(self) -> str:
        return f"Publisher(id={self.id}, name={self.name}, country={self.country})"
