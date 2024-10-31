import sys
from pathlib import Path

BASE_PROJECT_DIR = Path(__file__).parent.parent.parent
VENV_PATH = BASE_PROJECT_DIR.joinpath("venv", "lib", "python3.10", "site-packages")
sys.path.append(BASE_PROJECT_DIR.as_posix())
sys.path.insert(0, VENV_PATH.as_posix())

import uvicorn
from fastapi import FastAPI

from src.api import router as api_router
from src.core.config import settings

app = FastAPI(
    title="Line Provider",
    description="Сервис для публикации событий"
)
app.include_router(
    api_router,
    prefix=settings.api.prefix
)

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True
    )
