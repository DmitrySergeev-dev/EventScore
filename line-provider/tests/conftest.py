import asyncio
from typing import TYPE_CHECKING

import pytest
import pytest_asyncio
from aioredis import Redis
from redis import Redis as SyncRedis
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from tenacity import retry, stop_after_delay

from src.adapters.orm import Base
from src.adapters.repository import RedisRepository
from src.service_layer.unit_of_work import RedisUnitOfWork

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
    from typing import AsyncGenerator


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def redis_url():
    return "redis://0.0.0.0:6380/1"


@pytest.fixture(scope="session")
def redis_session(redis_url):
    return Redis.from_url(url=redis_url, decode_responses=True)


@pytest.fixture(scope="session")
def redis_repo(redis_session):
    return RedisRepository(session=redis_session)


@pytest.fixture(scope="session")
def redis_uow(redis_session):
    return RedisUnitOfWork(session=redis_session)


@pytest.fixture(scope='function', autouse=True)
def flush_redis(redis_url):
    redis = SyncRedis.from_url(url=redis_url)
    redis.flushdb()
    yield
    redis.flushdb()


@pytest.fixture(scope="session")
def db_url():
    return "postgresql+asyncpg://user:password@localhost:5434/test_line_provider"


@retry(stop=stop_after_delay(3))
async def wait_for_postgres_to_come_up(engine):
    async with engine.connect() as conn:
        return conn


@pytest_asyncio.fixture(scope="session")
async def db_engine(db_url) -> "AsyncGenerator[AsyncEngine]":
    engine = create_async_engine(db_url, echo=True)
    await wait_for_postgres_to_come_up(engine=engine)
    async with engine.connect() as conn:  # чтоб вручную управлять транзакциями
        await conn.execute(
            text(
                """
                CREATE OR REPLACE FUNCTION public.uuid_generate_v4()
                RETURNS uuid
                LANGUAGE 'c'
                    COST 1
                    VOLATILE STRICT PARALLEL SAFE
                    AS '$libdir/uuid-ossp', 'uuid_generate_v4'
                ;
                """
            )
        )
        await conn.execute(text("CREATE SCHEMA IF NOT EXISTS news;"))
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
        engine.sync_engine.dispose()
        yield engine
        await conn.run_sync(Base.metadata.drop_all)
        await conn.commit()
        await engine.dispose()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def async_session(db_engine) -> "AsyncGenerator[AsyncSession]":
    session_maker = async_sessionmaker(
        bind=db_engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )
    async with session_maker() as session:
        yield session
