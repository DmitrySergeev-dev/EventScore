from src.adapters.repository import RedisRepository
from .redis_client import r
from src.domain.model import News, NewsStatus
from datetime import datetime, timedelta
import pytest


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
