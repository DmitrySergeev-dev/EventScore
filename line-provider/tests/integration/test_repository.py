from datetime import datetime, timedelta

import pytest

from src.domain.model import News, NewsStatus


@pytest.mark.asyncio
class TestRedisRepository:

    async def test_add(self, redis_repo):
        news = News(
            description="Новость дня",
            deadline=datetime.now() + timedelta(days=1)
        )
        res = await redis_repo.add(news=news)
        assert res
        assert res.data.description == news.description
        assert res.data.status == news.status
        assert res.data.deadline == news.deadline_as_str

    async def test_get_by_status(self, redis_repo):
        deadline = datetime.now() + timedelta(days=1)
        news = News(description=f'Новость', deadline=deadline)
        await redis_repo.add(news=news)
        pkeys = await redis_repo.get_pkeys()
        await redis_repo.update(pk=pkeys[0], status=NewsStatus.SCORED_GOOD)
        filtered_news = await redis_repo.get_by_status(status=NewsStatus.SCORED_GOOD)
        assert all([news.data.status == NewsStatus.SCORED_GOOD for news in filtered_news])

    async def test_get_not_expired(self, redis_repo):
        deadline = datetime.now() + timedelta(days=1)
        news = News(description=f'Новость старая', deadline=deadline)
        await redis_repo.add(news=news)
        filtered_news = await redis_repo.get_not_expired()
        assert all(
            [datetime.strptime(news.data.deadline, News.DATETIME_PATTERN) > datetime.now()
             for news in filtered_news]
        )
