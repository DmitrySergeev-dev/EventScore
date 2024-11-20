from fastapi import APIRouter
from src.core.config import settings
from .news_scores import router as news_router


router = APIRouter(
    prefix=settings.api.v1.prefix,
)
router.include_router(
    news_router,
    prefix=settings.api.v1.scores,
)

