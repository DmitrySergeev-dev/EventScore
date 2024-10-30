import uvicorn
from fastapi import FastAPI

from src.api import router as api_router
from src.core.config import settings

app = FastAPI()
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
