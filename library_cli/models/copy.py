from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library_cli.config.sqlalchemy import Base, TimestampMixin
from library_cli.database.mixin import BaseMixin, InstanceMixin
from library_cli.static import Condition, Action

from typing import List


class Copy(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "copy"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    barcode: Mapped[str] = mapped_column(String(50), unique=True)

    book: Mapped["Book"] = relationship("Book", back_populates="copies")
    loans: Mapped[List["Loan"]] = relationship("Loan", back_populates="copy", init=False)
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="copy", init=False)

    condition: Mapped[str] = mapped_column(Enum(Condition), default=Condition.GOOD)
    action: Mapped[str] = mapped_column(Enum(Action), default=Action.FREE)

    Schema = None

    def __repr__(self) -> str:
        return f"Copy(id={self.id}, condition={self.condition}, action={self.action}, book_authors={self.book.authors}, book_name={self.book.title})"
