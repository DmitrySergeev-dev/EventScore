import asyncio
from datetime import datetime, timedelta

import pytest

from src.adapters.repository import RedisRepository
from src.domain.model import News, NewsStatus
from .redis_client import r


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
class TestRedisRepository:
    repo = RedisRepository(redis=r)

    async def test_add(self):
        news = News(
            description="Новость дня",
            deadline=datetime.now() + timedelta(days=1)
        )
        res = await self.repo.add(news=news)
        assert res
        assert res.description == news.description
        assert res.status == news.status
        assert res.deadline == news.deadline_as_str

    async def test_get_by_status(self):
        deadline = datetime.now() + timedelta(days=1)
        news = News(description=f'Новость', deadline=deadline)
        await self.repo.add(news=news)
        pkeys = await self.repo.get_pkeys()
        await self.repo.update(pk=pkeys[0], status=NewsStatus.SCORED_GOOD)
        filtered_news = await self.repo.get_by_status(status=NewsStatus.SCORED_GOOD)
        for news in filtered_news:
            assert news.status == NewsStatus.SCORED_GOOD
