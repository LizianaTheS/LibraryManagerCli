from sqlalchemy.orm import Mapped, mapped_column
from ..config.sqlalchemy import Base, TimestampMixin
from ..database.mixin import BaseMixin, InstanceMixin


class SystemSettings(BaseMixin, InstanceMixin, TimestampMixin, Base):
    __tablename__ = "system_settings"
    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(unique=True, nullable=False)
    value: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
