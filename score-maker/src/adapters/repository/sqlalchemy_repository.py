from typing import TYPE_CHECKING, Iterable

from sqlalchemy import select, delete

from .base import AbstractRepository
from ..orm import NewsScore

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.exceptions import NewsScoreNotFound


class PostgresRepository(AbstractRepository):
    def __init__(self, session: "AsyncSession"):
        super().__init__()
        self.session = session

    async def _add(self, **kwargs) -> NewsScore:
        db_news_score = NewsScore(**kwargs)
        self.session.add(db_news_score)
        await self.session.commit()
        await self.session.refresh(db_news_score)
        return NewsScore

    async def _get_by_news_id(self, news_id: str) -> NewsScore:
        db_news_score = await self.session.get(NewsScore, ident=news_id)
        if not db_news_score:
            raise NewsScoreNotFound
        return db_news_score

    async def _get_editable(self,
                            limit: int | None = None,
                            offset: int | None = None, ) -> list[NewsScore]:
        query = select(NewsScore).where(
            NewsScore.editable is True
        ).limit(limit).offset(offset)
        db_news_scores = await self.session.scalars(query)
        db_news_scores = db_news_scores.all()
        result = list(db_news_scores)
        return result

    async def _update(self, news_id: str, **kwargs) -> NewsScore:
        db_score_news = await self.session.get(NewsScore, ident=news_id)
        if not db_score_news:
            raise NewsScoreNotFound
        for attr, value in kwargs.items():
            setattr(db_score_news, attr, value)
        await self.session.commit()
        return db_score_news

    async def get_all(self,
                      limit: int | None = None,
                      offset: int | None = None,
                      **kwargs) -> Iterable[NewsScore]:
        query = select(NewsScore).limit(limit=limit).offset(offset=offset)
        score_news_list = await self.session.scalars(statement=query)
        score_news_list = score_news_list.all()
        score_news_list = list(score_news_list)
        return score_news_list

    async def _delete(self, news_id: str):
        stmt = delete(NewsScore).where(NewsScore.news_id == news_id)
        await self.session.execute(statement=stmt)
