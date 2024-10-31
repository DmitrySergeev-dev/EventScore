import abc
from datetime import datetime
from typing import TYPE_CHECKING

import aioredis

from src.core.config import settings
from src.core.utils import gen_timestamp_hash
from src.domain import model

if TYPE_CHECKING:
    from aioredis import Redis


class AbstractRepository(abc.ABC):

    async def add(self, news: model.News) -> model.NewsData:
        result = await self._add(news)
        return result

    async def get(self, pk: str) -> model.NewsData:
        news = await self._get(pk)
        return news

    async def get_by_status(self, status: str) -> [model.NewsData]:
        news = await self._get_by_status(status)
        return news

    async def get_not_expired(self) -> [model.NewsData]:
        news = await self._get_not_expired()
        return news

    async def update(self, pk: str, **kwargs) -> model.NewsData:
        news = await self._update(pk=pk, **kwargs)
        return news

    @abc.abstractmethod
    async def _add(self, news: model.News) -> model.NewsData:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, pk: str) -> model.NewsData:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_not_expired(self) -> [model.NewsData]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_by_status(self, status: str) -> [model.NewsData]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update(self, pk: str, **kwargs) -> [model.NewsData]:
        raise NotImplementedError


class RedisRepository(AbstractRepository):
    HASH_PREFIX = "News_"

    def __init__(self, session: "Redis"):
        self.session = session
        super().__init__()

    async def _add(self, news: model.News) -> model.NewsData:
        pk = f"{self.HASH_PREFIX}{gen_timestamp_hash()}"
        await self.session.hset(name=pk, mapping=news.to_dict())
        result = await self._get(pk=pk)
        return result

    async def _get(self, pk: str) -> model.NewsData:
        result = await self.session.hgetall(name=pk)
        return model.NewsData(**result)

    async def _get_by_status(self, status: str) -> [model.NewsData]:
        pkeys = await self.get_pkeys()
        news = [await self._get(pk=pk) for pk in pkeys]
        news = list(filter(lambda data: data.status == status, news))
        return news

    async def _get_not_expired(self) -> [model.NewsData]:
        pkeys = await self.get_pkeys()
        news = [await self._get(pk=pk) for pk in pkeys]
        current_datetime = datetime.now()
        news = list(
            filter(
                lambda data: datetime.strptime(
                    data.deadline,
                    model.News.DATETIME_PATTERN
                ) < current_datetime,
                news
            )
        )
        return news

    async def _update(self, pk: str, **kwargs) -> model.NewsData:
        await self.session.hset(pk, mapping=kwargs)
        result = await self._get(pk=pk)
        return result

    async def get_pkeys(self) -> [str]:
        pkeys = await self.session.keys(f'{self.HASH_PREFIX}*')
        return pkeys

    async def flush(self):
        await self.session.flushdb(asynchronous=True)


def get_redis_repository() -> RedisRepository:
    redis_instance = aioredis.from_url(str(settings.db.url), decode_responses=True)
    return RedisRepository(session=redis_instance)
