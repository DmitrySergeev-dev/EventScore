from __future__ import annotations
import abc
from src.adapters import repository
from src.core.config import settings
from aioredis import Redis


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


DEFAULT_REDIS_SESSION = Redis.from_url(
    url=str(settings.db.url),
    decode_responses=True
)


class RedisUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session: Redis = DEFAULT_REDIS_SESSION):
        self.session = session

    async def __aenter__(self):
        self.repo = repository.RedisRepository(session=self.session)
        return self

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    def _commit(self):  # будет реализовано через pipeline.multi
        pass

    def rollback(self):  # будет реализовано через pipeline.discard
        pass
