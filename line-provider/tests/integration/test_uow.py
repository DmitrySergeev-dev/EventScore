from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import pytest
from sqlalchemy import select

from src.adapters.orm import News as db_news_model
from src.domain.model import News
from src.service_layer.unit_of_work import PostgresUnitOfWork

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
class TestPostgresUnitOfWork:
    @pytest.mark.asyncio
    async def test_add_news(self, db_url: str, async_session: "AsyncSession"):
        news = News(
            description="Новость дня",
            deadline=datetime.now() + timedelta(days=1)
        )
        uow = PostgresUnitOfWork(url=db_url, echo=True)
        async with uow:
            await uow.repo.add(news=news)
            await uow.commit()

        async with async_session as session:
            news_list = await session.scalars(select(db_news_model))
            news_list = news_list.all()
        assert news_list
