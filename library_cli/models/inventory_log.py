from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum

from library_cli.config.sqlalchemy import Base, TimestampMixin
from library_cli.static import Action
from library_cli.database.mixin import BaseMixin, InstanceMixin


class InventoryLog(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "inventory_log"

    id: Mapped[int] = mapped_column(primary_key=True,init=False)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=False)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    action: Mapped[Action] = mapped_column(Enum(Action), nullable=False)

    book: Mapped["Book"] = relationship("Book", back_populates="logs")
    member: Mapped["Member"] = relationship("Member", back_populates="logs")
    Schema = None

    def __repr__(self) -> str:
        return f"InventoryLog(id={self.id}, book_title={self.book.title}, action={self.action})"
