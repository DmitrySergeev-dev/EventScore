from datetime import datetime
from typing import TYPE_CHECKING, Iterable

import aioredis

from src.core.config import settings
from src.core.utils import gen_timestamp_hash
from src.domain import model
from src.domain.exceptions import NewsNotFound
from .base import AbstractRepository
from .schemas import NewsObject

if TYPE_CHECKING:
    from aioredis import Redis


class RedisRepository(AbstractRepository):
    HASH_PREFIX = "News_"

    def __init__(self, session: "Redis"):
        self.session = session
        super().__init__()

    async def _add(self, news: model.News) -> NewsObject:
        pk = f"{self.HASH_PREFIX}{gen_timestamp_hash()}"
        await self.session.hset(name=pk, mapping=news.to_dict())
        result = await self._get(pk=pk)
        return NewsObject(pk=pk, data=result)

    async def _get(self, pk: str) -> model.NewsData:
        result = await self.session.hgetall(name=pk)
        if not result:
            raise NewsNotFound
        return model.NewsData(pk=pk, **result)

    async def _get_by_status(self, status: str) -> list[NewsObject]:
        pkeys = await self.get_pkeys()
        news = list()
        for pk in pkeys:
            data = await self._get(pk=pk)
            if data.status != status:
                continue
            news.append(
                NewsObject(pk=pk, data=data)
            )
        return news

    async def _get_not_expired(self) -> list[NewsObject]:
        pkeys = await self.get_pkeys()
        current_datetime = datetime.now()
        news = list()
        for pk in pkeys:
            data = await self._get(pk=pk)
            if datetime.strptime(data.deadline,
                                 model.News.DATETIME_PATTERN) >= current_datetime:
                continue
            news.append(
                NewsObject(pk=pk, data=data)
            )
        return news

    async def _update(self, pk: str, **kwargs) -> model.NewsData:
        await self.session.hset(pk, mapping=kwargs)
        result = await self._get(pk=pk)
        return result

    async def get_pkeys(self) -> list[str]:
        pkeys = await self.session.keys(f'{self.HASH_PREFIX}*')
        return pkeys

    async def flush(self):
        await self.session.flushdb(asynchronous=True)

    async def get_all(self,
                      limit: int | None = None,
                      offset: int | None = None,
                      **kwargs) -> Iterable[model.NewsData]:
        pkeys = await self.get_pkeys()
        news_list = [await self._get(pk=pk) for pk in pkeys]
        if not all([limit, offset]):
            return news_list
        return news_list[offset:offset + limit]


def get_redis_repository() -> RedisRepository:
    redis_instance = aioredis.from_url(str(settings.db.url), decode_responses=True)
    return RedisRepository(session=redis_instance)
