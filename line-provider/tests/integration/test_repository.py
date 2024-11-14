from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING

import pytest
from sqlalchemy import update, select

from src.adapters.orm import News as db_news_model
from src.adapters.repository.sqlalchemy_repository import PostgresRepository
from src.domain.model import News, NewsStatus

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


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
        news = News(description=f'Новость актуальная', deadline=deadline)
        await redis_repo.add(news=news)
        filtered_news = await redis_repo.get_not_expired()
        assert all(
            [datetime.strptime(news.data.deadline, News.DATETIME_PATTERN) > datetime.now()
             for news in filtered_news]
        )


@pytest.mark.asyncio
class TestPostgresRepository:

    @pytest.mark.asyncio
    async def test_add(self, async_session):
        news = News(
            description="Новость дня",
            deadline=datetime.now(tz=timezone.utc) + timedelta(days=1)
        )
        async with async_session as session:
            repo = PostgresRepository(session=session)
            res = await repo.add(news=news)
        assert res
        assert res.pk
        assert res.data.description == news.description
        assert res.data.status == news.status
        assert res.data.deadline == news.deadline

    @pytest.mark.asyncio
    async def test_get(self, async_session: "AsyncSession"):
        news_list = [db_news_model(description=f'Новость_{i}',
                                   deadline=datetime.now() + timedelta(days=1))
                     for i in range(5)
                     ]
        news_example = news_list[0]
        query = select(db_news_model.pk).where(
            db_news_model.description == news_example.description
        )
        async with async_session as session:
            for news in news_list:
                session.add(news)
                await session.commit()
            session.add(news)
            await session.commit()
            pkeys = await session.scalars(statement=query)
            pk = pkeys.first()
            repo = PostgresRepository(session=session)
            res = await repo.get(pk=pk)
        assert res
        assert res.pk == news_example.pk
        assert res.description == news_example.description
        assert res.status == news_example.status
        assert res.deadline == news_example.deadline

    @pytest.mark.asyncio
    async def test_get_by_status(self, async_session):
        news_list = [db_news_model(description=f'Новость_{i}',
                                   deadline=datetime.now() + timedelta(days=1))
                     for i in range(5)
                     ]
        async with async_session as session:
            repo = PostgresRepository(session=session)
            for news in news_list:
                session.add(news)
                await session.commit()
            query = update(db_news_model).where(
                db_news_model.description == news.description  # только последнюю новость
            ).values(status=NewsStatus.SCORED_GOOD)
            await session.execute(query)
            await session.commit()
            result = await repo.get_by_status(status=NewsStatus.SCORED_GOOD)
        assert result
        assert all([el.data.status == NewsStatus.SCORED_GOOD for el in result])

    @pytest.mark.asyncio
    async def test_get_not_expired(self, async_session: "AsyncSession"):
        news_list = [db_news_model(description=f'Новость_{i}',
                                   deadline=datetime.now(tz=timezone.utc) + timedelta(days=1))
                     for i in range(5)]

        async with async_session as session:
            for news in news_list:
                session.add(news)
            await session.commit()
            query = update(db_news_model).where(
                db_news_model.description == news.description  # только последнюю новость
            ).values(deadline=datetime.now() - timedelta(days=1))
            await session.execute(query)
            await session.commit()
            repo = PostgresRepository(session=session)
            actual_news = await repo.get_not_expired()
        assert all(
            [news.data.deadline > datetime.now(tz=timezone.utc)
             for news in actual_news]
        )

    @pytest.mark.asyncio
    async def test_update(self, async_session: "AsyncSession"):
        news = db_news_model(
            description='Новость',
            deadline=datetime.now() + timedelta(days=1)
        )
        async with async_session as session:
            session.add(news)
            await session.commit()
            await session.refresh(news)
            repo = PostgresRepository(session=session)
            new_description = "Новость ред."
            new_status = NewsStatus.SCORED_BAD
            await repo.update(pk=news.pk, description=new_description, status=new_status)
        assert news.pk
        assert news.description == new_description
        assert news.status == new_status

    @pytest.mark.asyncio
    async def test_get_all(self, async_session: "AsyncSession"):
        news_list = [db_news_model(description=f'Новость_{i}',
                                   deadline=datetime.now() + timedelta(days=1))
                     for i in range(20)]
        async with async_session as session:
            for news in news_list:
                session.add(news)
            await session.commit()
            repo = PostgresRepository(session=session)
            all_news = await repo.get_all()
            limit = 3
            limited_news = await repo.get_all(limit=limit)
            last_limit_news = await repo.get_all(limit=limit, offset=len(news_list) - 3)
        assert len(list(all_news)) >= len(news_list)
        assert len(list(limited_news)) == limit
        assert len(list(last_limit_news)) == limit
