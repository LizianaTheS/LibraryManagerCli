from sqlalchemy import DateTime, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from library_cli.config.sqlalchemy import Base, TimestampMixin
from library_cli.static import Status
from library_cli.database.mixin import BaseMixin, InstanceMixin


class Reservation(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "reservation"
    id: Mapped[int] = mapped_column(primary_key=True,init=False)
    copy_id: Mapped[int] = mapped_column(ForeignKey("copy.id"))

    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    member: Mapped["Member"] = relationship("Member", back_populates="reservations")
    copy: Mapped["Copy"] = relationship("Copy", back_populates="reservations")

    status: Mapped[str] = mapped_column(Enum(Status), default=Status.ACTIVE)
    reserved_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    Schema = None

    def __repr__(self) -> str:
        return f"Reservation(id={self.id}, member_name={self.member.fullname}, book_name={self.book.title}, status={self.status})"
