from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from library_cli.config.sqlalchemy import Base, TimestampMixin
from library_cli.database.mixin import BaseMixin, InstanceMixin
from library_cli.static import Status
from typing import List, Optional


class Member(BaseMixin, InstanceMixin, TimestampMixin, Base):
    def __init__(self, fullname=None, email=None, password=None, username=None, **kwargs):
        super().__init__()
        self.fullname = fullname
        self.email = email
        self.password = password
        self.username = username
        for k, v in kwargs.items():
            setattr(self, k, v)

    __tablename__ = "members"
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    fullname: Mapped[str] = mapped_column(String(100))
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True)

    logs: Mapped[List["InventoryLog"]] = relationship("InventoryLog", back_populates="member", init=False)
    reservations: Mapped[List["Reservation"]] = relationship("Reservation", back_populates="member", init=False)
    loans: Mapped[List["Loan"]] = relationship("Loan", back_populates="member", init=False)
    phone: Mapped[Optional[str]] = mapped_column(String(15), nullable=True, default=None)
    status: Mapped[str] = mapped_column(Enum(Status), default=Status.ACTIVE)
    Schema = None

    def __repr__(self) -> str:
        return f"Member(id={self.id}, fullname={self.fullname}, email={self.email}, status={self.status})"
