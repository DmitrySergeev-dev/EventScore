import asyncio
import json
import logging
from typing import TYPE_CHECKING, Iterable

import aioredis

from src.domain.exceptions import WrongMessage

if TYPE_CHECKING:
    from pydantic import RedisDsn

from src.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_event_listener(url: "RedisDsn", channels_names: Iterable[str]):
    redis = aioredis.from_url(url, decode_responses=True)
    psub = redis.pubsub(ignore_subscribe_messages=True)
    async with psub as p:
        await p.subscribe(*channels_names)
        async for message in p.listen():
            data = message["data"]
            try:
                data_json = json.loads(data)
            except json.JSONDecodeError:
                raise WrongMessage("Не корректная структура сообщения об оценке события!")
            logger.info("Got message: %r", data_json)


if __name__ == "__main__":
    redis_url = str(settings.db.url)
    channels = ["news_scored"]
    asyncio.run(
        run_event_listener(url=redis_url, channels_names=channels)
    )
