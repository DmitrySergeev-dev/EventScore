import asyncio
from datetime import datetime, timedelta

import pytest

from src.adapters.repository import RedisRepository
from src.domain.model import News, NewsStatus
from .redis_client import r


@pytest.fixture(autouse=True, scope="session")  # fixme не запускается почему то
async def setup_and_teardown():
    await r.flushdb(asynchronous=True)
    yield
    await r.flushdb(asynchronous=True)
    await r.close()


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
        await self.repo.flush()
        news = News(
            description="Новость дня",
            deadline=datetime.now() + timedelta(days=1)
        )
        res = await self.repo.add(news=news)
        assert res
        assert res.description == news.description
        assert res.status == news.status
        assert res.deadline == news.deadline_as_str
        await self.repo.flush()  # todo автоматизировать

    async def test_get_by_status(self):
        deadline = datetime.now() + timedelta(days=1)
        news = News(description=f'Новость', deadline=deadline)
        await self.repo.add(news=news)
        pkeys = await self.repo.get_pkeys()
        await self.repo.update(pk=pkeys[0], status=NewsStatus.SCORED_GOOD)
        filtered_news = await self.repo.get_by_status(status=NewsStatus.SCORED_GOOD)
        for news in filtered_news:
            assert news.status == NewsStatus.SCORED_GOOD

        await self.repo.flush()  # todo автоматизировать

    async def test_get_not_expired(self):
        await self.repo.flush()
        deadline = datetime.now() + timedelta(days=1)
        news = News(description=f'Новость старая', deadline=deadline)
        await self.repo.add(news=news)
        filtered_news = await self.repo.get_not_expired()
        for news in filtered_news:
            news_deadline = datetime.strptime(news.deadline, News.DATETIME_PATTERN)
            assert news_deadline > datetime.now()

        await self.repo.flush()  # todo автоматизировать
