from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker
from sqlalchemy import MetaData, create_engine

from sqlalchemy import Table, Column, ForeignKey
from .settings import settings

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone


class Base(DeclarativeBase, MappedAsDataclass):
    metadata = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import declarative_mixin


@declarative_mixin
class TimestampMixin:
    created: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc), init=False
    )
    updated: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        init=False,
    )


book_authors = Table(
    "book_authors",
    Base.metadata,
    Column("book_id", ForeignKey("book.id"), primary_key=True),
    Column("author_id", ForeignKey("author.id"), primary_key=True),
)

engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
