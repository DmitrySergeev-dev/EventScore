from datetime import datetime

from sqlalchemy import (
    Text,
    func,
    DateTime,
    Enum as SQLAlchemyEnum,
    Column
)
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column
)

from src.domain.model import NewsStatus


class Base(DeclarativeBase):
    pass


class News(Base):
    """События"""
    __tablename__ = "news"
    __table_args__ = (
        {
            "schema": "news",
            "comment": "Новости",
        }
    )
    pk: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
        nullable=False,
        server_default=func.public.uuid_generate_v4()
    )
    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Описание новости"
    )
    deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Дедлайн для оценки новости"
    )
    status: Mapped[SQLAlchemyEnum] = mapped_column(
        SQLAlchemyEnum(NewsStatus),
        nullable=False,
        comment="Статус новости",
        default=NewsStatus.NOT_SCORED
    )
