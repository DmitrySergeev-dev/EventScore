from typing import TYPE_CHECKING
from uuid import uuid4

import pytest

from src.adapters.orm import NewsScore
from src.adapters.repository.sqlalchemy_repository import PostgresRepository
from src.core.schemas.news_score import NewsScoreIn

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture
def random_uid():
    return str(uuid4())


@pytest.mark.asyncio
class TestPostgresRepository:

    @pytest.mark.asyncio
    async def test_add(self, async_session, random_uid):
        data = NewsScoreIn(news_id=random_uid).dict()
        async with async_session as session:
            repo = PostgresRepository(session=session)
            created = await repo.add(**data)
        assert created
        assert created.news_id == random_uid
        assert created.score is None
        assert created.editable is True

    @pytest.mark.asyncio
    async def test_get(self, async_session: "AsyncSession"):
        score_news = [NewsScore(news_id=str(uuid4())) for _ in range(1, 5)]
        validated_news_id = score_news[0].news_id

        async with async_session as session:
            session.add_all(score_news)
            await session.commit()
            repo = PostgresRepository(session=session)
            res = await repo.get_by_news_id(news_id=validated_news_id)
        assert res
        assert res.news_id == validated_news_id
        assert res.editable is True
        assert res.score is None

    @pytest.mark.asyncio
    async def test_get_editable(self, async_session):
        editable_news_scores = [NewsScore(news_id=str(uuid4())) for _ in range(5)]
        not_editable_news_scores = [NewsScore(news_id=str(uuid4()), editable=False) for _ in range(5)]
        async with async_session as session:
            repo = PostgresRepository(session=session)
            session.add_all(editable_news_scores)
            session.add_all(not_editable_news_scores)
            await session.commit()
            result = await repo.get_editable()
        assert result
        assert all([el.editable is True for el in result])

    @pytest.mark.asyncio
    async def test_update(self, async_session: "AsyncSession"):
        news_score = NewsScore(news_id=str(uuid4()))
        async with async_session as session:
            session.add(news_score)
            await session.commit()
            await session.refresh(news_score)
            repo = PostgresRepository(session=session)
            await repo.update(news_id=news_score.news_id, score=4, editable=False)
        assert news_score.news_id
        assert news_score.score == 4
        assert news_score.editable is False

    @pytest.mark.asyncio
    async def test_get_all(self, async_session: "AsyncSession"):
        news_score_list = [NewsScore(news_id=str(uuid4())) for _ in range(10)]
        async with async_session as session:
            session.add_all(news_score_list)
            await session.commit()
            repo = PostgresRepository(session=session)
            all_news = await repo.get_all()
            limit = 3
            limited_news = await repo.get_all(limit=limit)
            last_limit_news = await repo.get_all(limit=limit, offset=len(news_score_list) - 3)
        assert len(list(all_news)) >= len(news_score_list)
        assert len(list(limited_news)) == limit
        assert len(list(last_limit_news)) == limit

    @pytest.mark.asyncio
    async def test_delete(self, async_session: "AsyncSession"):
        score_news = NewsScore(news_id=str(uuid4()))
        async with async_session as session:
            session.add(score_news)
            await session.commit()
            await session.refresh(score_news)
            assert score_news.news_id
            repo = PostgresRepository(session=session)
            await repo.delete(news_id=score_news.news_id)
            is_exists = await session.get(NewsScore, score_news.news_id)
        assert not is_exists
