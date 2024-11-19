import abc
from typing import Iterable

from ..orm import NewsScore


class AbstractRepository(abc.ABC):

    async def add(self, **kwargs) -> NewsScore:
        result = await self._add(**kwargs)
        return result

    async def get_by_news_id(self, news_id: str) -> NewsScore:
        score = await self._get_by_news_id(news_id)
        return score

    async def get_editable(self, *args, **kwargs) -> list[NewsScore]:
        news = await self._get_editable(*args, **kwargs)
        return news

    async def update(self, news_id: str, **kwargs) -> NewsScore:
        score = await self._update(news_id=news_id, **kwargs)
        return score

    async def delete(self, news_id: str):
        await self._delete(news_id=news_id)

    @abc.abstractmethod
    async def _add(self, **kwargs) -> NewsScore:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_by_news_id(self, news_id: str) -> NewsScore:
        raise NotImplementedError

    @abc.abstractmethod
    async def _get_editable(self, *args, **kwargs) -> list[NewsScore]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _update(self, news_id: str, **kwargs) -> NewsScore:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_all(self,
                      limit: int | None = None,
                      offset: int | None = None,
                      **kwargs) -> Iterable[NewsScore]:
        raise NotImplementedError

    @abc.abstractmethod
    async def _delete(self, news_id: str):
        raise NotImplementedError
