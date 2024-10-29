import abc

from src.domain import model


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen: set[model.News] = set()

    def add(self, news: model.News):
        self._add(news)
        self.seen.add(news)

    def get(self, pk: str) -> model.News:
        news = self._get(pk)
        if news:
            self.seen.add(news)
        return news

    def get_by_status(self, status: model.NewsStatus) -> model.News:
        news = self._get_by_status(status)
        if news:
            self.seen.add(news)
        return news

    @abc.abstractmethod
    def _add(self, news: model.News):
        raise NotImplementedError

    @abc.abstractmethod
    def _get(self, pk: str) -> model.News:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_by_status(self, status: model.NewsStatus) -> model.News:
        raise NotImplementedError


class RedisRepository(AbstractRepository):
    def __init__(self):
        super().__init__()

    def _add(self, news: model.News):
        ...

    def _get(self, pk: str) -> model.News:
        ...

    def _get_by_status(self, status: model.NewsStatus) -> model.News:
        ...
