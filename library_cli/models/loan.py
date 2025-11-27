from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import Optional

from library_cli.config.sqlalchemy import Base, TimestampMixin
from library_cli.database.mixin import BaseMixin, InstanceMixin


class Loan(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "loan"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    returned_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    copy_id: Mapped[int] = mapped_column(ForeignKey("copy.id"), nullable=False)
    copy: Mapped["Copy"] = relationship("Copy", back_populates="loans")

    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), nullable=False)
    member: Mapped["Member"] = relationship("Member", back_populates="loans")

    borrowed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    Schema = None

    def __repr__(self) -> str:
        return f"Loan(id={self.id}, returned_at={self.returned_at}, borrowed_at={self.borrowed_at})"
