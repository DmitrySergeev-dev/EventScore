import pytest
from aioredis import Redis
from src.adapters.repository import RedisRepository


@pytest.fixture(scope="session")
def redis_session():
    connection_params = dict(
        host="0.0.0.0",
        port=6380,
        db=1,
        decode_responses=True
    )
    return Redis(**connection_params)


@pytest.fixture(scope="session")
def redis_repo(redis_session):
    return RedisRepository(session=redis_session)
