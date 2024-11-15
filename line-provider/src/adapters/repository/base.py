import abc
from typing import Iterable

from src.domain import model
from .schemas import NewsObject


class AbstractRepository(abc.ABC):

    async def add(self, news: model.News) -> NewsObject:
        result = await self._add(news)
        return result

    async def get(self, pk: str) -> model.NewsData:
        news = await self._get(pk)
        return news

    async def get_by_status(self, status: str) -> list[NewsObject]:
        news = await self._get_by_status(status)
        return news

    async def get_not_expired(self) -> list[NewsObject]:
        news = await self._get_not_expired()
        return news

    async def update(self, pk: str, **kwargs) -> model.NewsData:
        news = await self._update(pk=pk, **kwargs)
        return news

    async def delete(self, pk: str):
        await self._delete(pk=pk)

    @abc.abstractmethod
    async def _add(self, news: model.News) -> NewsObject:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get(self, pk: str) -> model.NewsData:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_not_expired(self) -> list[NewsObject]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_by_status(self, status: str) -> list[NewsObject]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update(self, pk: str, **kwargs) -> model.NewsData:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self,
                      limit: int | None = None,
                      offset: int | None = None,
                      **kwargs) -> Iterable[model.NewsData]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete(self, pk: str):
        raise NotImplementedError
