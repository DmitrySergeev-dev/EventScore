from dataclasses import asdict
from typing import Annotated, TYPE_CHECKING

from fastapi.exceptions import HTTPException

from src.domain.exceptions import NewsNotFound
from src.domain.model import News

if TYPE_CHECKING:
    from src.service_layer.unit_of_work import AbstractUnitOfWork

from fastapi import (
    APIRouter, Query,
    Depends, status
)

from src.core.schemas.news import NewsSchema, NewsFilterParams, NewsSchemaOut
from .dependencies import db_uow

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

        Параметры сортировки
        - **order_by**: наименование поля по которому сортируется список
    """

    async with uow:
        news = await uow.repo.get_all(limit=params.limit, offset=params.offset)
    news = [NewsSchemaOut(**asdict(row)) for row in news]
    return news


@router.get("/{news_id}", response_model=NewsSchemaOut)
async def get_news_by_id(
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
    return NewsSchemaOut(pk=news_id, **asdict(news))


@router.post("/", response_model=NewsSchemaOut, status_code=status.HTTP_201_CREATED)
async def create_news(
        data: NewsSchema,
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)]):
    async with uow:
        news = await uow.repo.add(
            news=News(**data.dict())
        )
    return NewsSchemaOut(**asdict(news.data))
