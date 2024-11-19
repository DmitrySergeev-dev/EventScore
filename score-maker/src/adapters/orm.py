from sqlalchemy import (
    Text,
    func,
    Integer,
    Boolean,
    CheckConstraint
)
from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    mapped_column
)


class Base(DeclarativeBase):
    pass


class NewsScore(Base):
    """События"""
    __tablename__ = "news_score"

    pk: Mapped[str] = mapped_column(
        Text,
        primary_key=True,
        nullable=False,
        server_default=func.public.uuid_generate_v4()
    )
    news_id: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="Идентификатор новости"
    )
    score: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        comment="Оценка новости"
    )
    editable: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        comment="Возможность редактирования оценки",
        default=True
    )
    __table_args__ = (
        CheckConstraint(
            (score <= 5) & (score >= 1),
            name="score_value_limit"
        ),
        {
            "schema": "news",
            "comment": "Оценки новостей",
        }
    )
