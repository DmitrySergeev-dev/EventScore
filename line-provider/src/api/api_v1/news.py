from typing import Annotated, Any

from fastapi import APIRouter, Query

from src.core.schemas.news import NewsSchema, NewsFilterParams

router = APIRouter(tags=["News"])


@router.get("/")
async def get_news_list(
        params: Annotated[NewsFilterParams, Query()]
):
    return "Got list of news!"


@router.get("/{news_id}")
async def get_news_by_id(news_id: str) -> NewsSchema:
    return f'Got news with id="{news_id}"'


@router.post("/")
async def create_news(data: NewsSchema):
    return dict(action="CREATED", data=data)
