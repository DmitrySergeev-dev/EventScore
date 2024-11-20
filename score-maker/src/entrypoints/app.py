import asyncio
import logging
import sys
from pathlib import Path

BASE_PROJECT_DIR = Path(__file__).parent.parent.parent
VENV_PATH = BASE_PROJECT_DIR.joinpath("venv", "lib", "python3.10", "site-packages")
sys.path.append(BASE_PROJECT_DIR.as_posix())
sys.path.insert(0, VENV_PATH.as_posix())

import uvicorn
from fastapi import FastAPI

from src import bootstrap
from src.api import router as api_router
from src.core.logging_config import LOGGING_CONFIG
from src.core.config import settings
from src.entrypoints.redis_eventconsumer import run_event_listener

app = FastAPI(
    title="Score Maker",
    description="Сервис для оценки событий"
)
app.include_router(
    api_router,
    prefix=settings.api.prefix
)

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@app.get('/health')
async def health_check():
    return 1


async def main():
    redis_url = str(settings.redis.url)
    channels = [
        "NewsCreated",
        "NewsDeleted"
    ]
    bus = bootstrap.bootstrap()
    await run_event_listener(url=redis_url, channels_names=channels, msg_bus=bus)


async def start_server():
    config = uvicorn.Config(
        app,
        host=settings.run.host,
        port=settings.run.port
    )
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    logger.info("Starting score-maker service...")
    loop = asyncio.get_event_loop()

    # Запускаем сервер и основную функцию параллельно
    try:
        loop.run_until_complete(asyncio.gather(start_server(), main()))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        loop.close()
