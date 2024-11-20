from __future__ import annotations

import abc
from typing import TYPE_CHECKING

from aioredis import Redis
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

from src.adapters import repository
from src.core.config import settings

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import (
        AsyncSession,
        AsyncEngine
    )


class AbstractUnitOfWork(abc.ABC):
    repo: repository.AbstractRepository

    async def __aenter__(self) -> AbstractUnitOfWork:
        return self

    async def __aexit__(self, *args):
        await self.rollback()

    async def commit(self):
        await self._commit()

    @abc.abstractmethod
    async def _commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError


DEFAULT_REDIS_SESSION = Redis.from_url(
    url=str(settings.redis.url),
    decode_responses=True
)


class PostgresUnitOfWork(AbstractUnitOfWork):
    def __init__(self,
                 url: str = settings.db.url,
                 echo: bool = False,
                 echo_pool: bool = False,
                 pool_size: int = 5,
                 max_overflow: int = 10):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
        )
        self.session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    async def __aenter__(self):
        self.session = await self.session_maker().__aenter__()
        self.repo = repository.PostgresRepository(session=self.session)
        return self

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.__aexit__(*args)
        await self.session.close()

    async def _commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
