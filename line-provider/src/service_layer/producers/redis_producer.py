import asyncio
import json

import aioredis

from src.core.config import settings
from src.domain.exceptions import RedisConnectionError


class RedisProducer:
    def __init__(self, url: str):
        self.client = aioredis.from_url(url=url, decode_responses=True)

    async def publish(self, channel: str,
                      message: str | bytes) -> int:
        try:
            subscribers_count = await self.client.publish(
                message=message,
                channel=channel
            )
        except aioredis.ConnectionError:
            raise RedisConnectionError
        return subscribers_count


async def run_test():
    url = str(settings.redis.url)
    producer = RedisProducer(url=url)
    for i in range(20):
        msg = json.dumps(
            dict(data=f'Message №{i}')
        )
        count = await producer.publish(channel="TestChannel", message=msg)
        print(f'Отправка сообщения №{i}. Число подписчиков: {count}')


if __name__ == '__main__':
    asyncio.run(run_test())
