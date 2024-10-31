import pytest
from aioredis import Redis

from src.adapters.repository import RedisRepository
from src.service_layer.unit_of_work import RedisUnitOfWork


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
