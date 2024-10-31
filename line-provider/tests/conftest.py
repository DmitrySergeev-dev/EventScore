import asyncio

import pytest
from aioredis import Redis
from redis import Redis as SyncRedis

from src.adapters.repository import RedisRepository
from src.service_layer.unit_of_work import RedisUnitOfWork


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
