from src.adapters.repository import RedisRepository
from .redis_client import r
from src.domain.model import News
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
        assert res["description"] == news.description
        assert res["status"] == news.status
        assert res["deadline"] == news.deadline_as_str


