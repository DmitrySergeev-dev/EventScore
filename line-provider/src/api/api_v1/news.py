import json
from dataclasses import asdict
from typing import Annotated, TYPE_CHECKING

from fastapi.exceptions import HTTPException

from src.domain.exceptions import NewsNotFound
from src.domain.model import News
from ...domain.commands import NotifyAboutCreatedNews

if TYPE_CHECKING:
    from src.service_layer.unit_of_work import AbstractUnitOfWork
    from src.service_layer.producers import RedisProducer

from fastapi import (
    APIRouter, Query,
    Depends, status
)

from src.core.schemas.news import NewsSchema, NewsFilterParams, NewsSchemaOut
from .dependencies import db_uow, redis_broker

router = APIRouter(
    tags=["News"],
    dependencies=[
        Depends(db_uow),
    ]
)


@router.get("/", response_model=list[NewsSchemaOut], status_code=status.HTTP_200_OK)
async def get_news_list(
        params: Annotated[NewsFilterParams, Query()],
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)]
):
    """
        Возвращает список событий:

        Параметры пагинации
        - **limit**: количество объектов
        - **offset**: количесвто пропускаемых объектов
    """

    async with uow:
        news = await uow.repo.get_all(limit=params.limit, offset=params.offset)
    news = [NewsSchemaOut(**asdict(row)) for row in news]
    return news


@router.get("/{news_id}", response_model=NewsSchemaOut)
async def get_news(
        news_id: str,
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)]
):
    async with uow:
        try:
            news = await uow.repo.get(pk=news_id)
        except NewsNotFound:
            raise HTTPException(
                status_code=404,
                detail="Событие с таким pk не найдено в базе"
            )
    return NewsSchemaOut(**asdict(news))


@router.post("/", response_model=NewsSchemaOut, status_code=status.HTTP_201_CREATED)
async def create_news(
        data: NewsSchema,
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)],
        broker: Annotated["RedisProducer", Depends(redis_broker)]):
    async with uow:
        news = await uow.repo.add(
            news=News(**data.dict())
        )
    command = NotifyAboutCreatedNews(
        pk=news.pk,
        deadline=str(news.data.deadline),
        description=news.data.description,
        status=news.data.status
    )
    msg = json.dumps(asdict(command))
    await broker.publish(channel="score_maker.news_created", message=msg)
    return NewsSchemaOut(**asdict(news.data))


@router.delete("/{news_id}", status_code=status.HTTP_200_OK)
async def delete_news(
        news_id: str,
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)]
):
    async with uow:
        await uow.repo.delete(pk=news_id)
        await uow.commit()
    return "Ok"


@router.patch("/{news_id}", response_model=NewsSchemaOut, status_code=status.HTTP_200_OK)
async def patch_news(
        news_id: str,
        data: NewsSchema,
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)]
):
    async with uow:
        edited_news = await uow.repo.update(pk=news_id, **data.dict())
        await uow.commit()
    return NewsSchemaOut(**asdict(edited_news))
