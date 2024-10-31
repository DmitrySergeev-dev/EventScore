import asyncio
import json
from datetime import datetime, timedelta
from typing import TYPE_CHECKING

import pytest

from src.bootstrap import bootstrap
from src.domain.events import NewsScored
from src.domain.model import News, NewsStatus
from src.entrypoints.redis_eventconsumer import run_event_listener

if TYPE_CHECKING:
    from src.service_layer.messagebus import MessageBus
from aioredis import Redis
from dataclasses import asdict


@pytest.fixture
def messagebus(redis_uow) -> "MessageBus":
    return bootstrap(uow=redis_uow)


async def publish_message(channel_name: str, message: dict, redis_url: str):
    publisher = Redis.from_url(url=redis_url, decode_responses=True)
    await publisher.publish(channel=channel_name, message=json.dumps(message))


@pytest.mark.asyncio
async def test_handle_news_scored(redis_repo, redis_url, messagebus):
    redis_repo.flush()  # todo автоматизировать
    news = News(
        description="Test News",
        deadline=datetime.now() + timedelta(days=2)
    )
    news_redis = await redis_repo.add(news=news)
    assert news_redis.data.status == NewsStatus.NOT_SCORED
    event = NewsScored(news_hash=news_redis.pk, score_value=5)

    channel_names = ["NewsScored"]

    consumer_task = asyncio.create_task(
        run_event_listener(url=redis_url,
                           channels_names=channel_names,
                           msg_bus=messagebus)
    )
    await asyncio.sleep(1)
    producer_task = asyncio.create_task(
        publish_message(
            redis_url=redis_url,
            channel_name="NewsScored",
            message=asdict(event)
        )
    )

    # Даем время для обработки сообщения
    await asyncio.sleep(1)

    try:
        await asyncio.wait_for(asyncio.gather(consumer_task, producer_task), timeout=5.0)
    except asyncio.TimeoutError:
        print("Таймаут: задачи не завершились в установленное время.")

    updated_news = await redis_repo.get(pk=news_redis.pk)

    assert updated_news.status == NewsStatus.SCORED_GOOD

    redis_repo.flush()  # todo автоматизировать
