from datetime import datetime
from typing import TYPE_CHECKING, Iterable

from sqlalchemy import select

from src.domain import model
from .base import AbstractRepository
from .schemas import NewsObject
from ..orm import News
from ...domain.exceptions import NewsNotFound

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class PostgresRepository(AbstractRepository):
    def __init__(self, session: "AsyncSession"):
        super().__init__()
        self.session = session

    async def _add(self, news: model.News) -> NewsObject:
        db_news = News(**news.to_dict())
        self.session.add(db_news)
        await self.session.commit()
        await self.session.refresh(db_news)

        return NewsObject(pk=db_news.pk,
                          data=model.NewsData(
                              pk=db_news.pk,
                              description=db_news.description,
                              deadline=db_news.deadline,
                              status=db_news.status
                          ))

    async def _get(self, pk: str) -> model.NewsData:
        result = await self.session.get(News, ident=pk)
        if not result:
            raise NewsNotFound
        return model.NewsData(pk=pk,
                              description=result.description,
                              deadline=result.deadline,
                              status=result.status)

    async def _get_by_status(self, status: str) -> list[NewsObject]:
        query = select(News).where(News.status == status)
        news = await self.session.scalars(query)
        news = news.all()
        result = [
            NewsObject(
                pk=el.pk,
                data=model.NewsData(pk=el.pk,
                                    description=el.description,
                                    deadline=el.deadline,
                                    status=el.status)
            ) for el in news
        ]
        return result

    async def _get_not_expired(self) -> list[NewsObject]:
        current_datetime = datetime.now()
        query = select(News).where(News.deadline >= current_datetime)
        news = await self.session.scalars(query)
        news = news.all()
        result = [
            NewsObject(
                pk=el.pk,
                data=model.NewsData(pk=el.pk,
                                    description=el.description,
                                    deadline=el.deadline,
                                    status=el.status)
            ) for el in news
        ]
        return result

    async def _update(self, pk: str, **kwargs) -> model.NewsData:
        news = await self.session.get(News, ident=pk)
        for attr, value in kwargs.items():
            setattr(news, attr, value)
        await self.session.commit()
        return model.NewsData(pk=pk,
                              description=news.description,
                              deadline=news.deadline,
                              status=news.status)

    async def get_all(self,
                      limit: int | None = None,
                      offset: int | None = None,
                      **kwargs) -> Iterable[model.NewsData]:
        query = select(News).limit(limit=limit).offset(offset=offset)
        news_list = await self.session.scalars(statement=query)
        news_list = news_list.all()
        news_list = [
            model.NewsData(pk=news.pk,
                           description=news.description,
                           deadline=news.deadline,
                           status=news.status)
            for news in news_list
        ]
        return news_list
