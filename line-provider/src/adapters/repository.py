import abc
from typing import TYPE_CHECKING

from src.core.utils import gen_timestamp_hash
from src.domain import model

if TYPE_CHECKING:
    from aioredis import Redis


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set[model.News] = set()

    async def add(self, news: model.News):
        result = await self._add(news)
        self.seen.add(news)
        return result

    async def get(self, pk: str) -> model.News:
        news = await self._get(pk)
        if news:
            self.seen.add(news)
        return news

    async def get_by_status(self, status: model.NewsStatus) -> model.News:
        news = await self._get_by_status(status)
        if news:
            self.seen.add(news)
        return news

    @abc.abstractmethod
    async def _add(self, news: model.News):
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, pk: str) -> model.News:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_by_status(self, status: model.NewsStatus) -> model.News:
        raise NotImplementedError


class RedisRepository(AbstractRepository):
    def __init__(self, redis: "Redis"):
        self._redis = redis
        super().__init__()

    async def _add(self, news: model.News):
        hash_key = f"News_{gen_timestamp_hash()}"
        await self._redis.hset(name=hash_key, mapping=news.to_dict())
        result = await self._redis.hgetall(name=hash_key)
        return result

    async def _get(self, pk: str) -> model.News:
        ...

    async def _get_by_status(self, status: model.NewsStatus) -> model.News:
        ...
