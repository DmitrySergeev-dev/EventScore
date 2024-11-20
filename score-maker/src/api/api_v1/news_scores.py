import json
from dataclasses import asdict
from typing import Annotated, TYPE_CHECKING

from fastapi.exceptions import HTTPException

from src.domain.exceptions import NewsScoreNotFound
from ...domain import commands

if TYPE_CHECKING:
    from src.service_layer.unit_of_work import AbstractUnitOfWork
    from src.service_layer.producers import RedisProducer

from fastapi import (
    APIRouter, Query,
    Depends, status
)

from src.core.schemas.news_score import (
    NewsScoreIn, NewsScoreOut,
    ScoresFilterParams, NewsScorePatch
)
from .dependencies import db_uow, redis_broker

router = APIRouter(
    tags=["Scores"],
    dependencies=[
        Depends(db_uow),
    ]
)


@router.get("/", response_model=list[NewsScoreOut], status_code=status.HTTP_200_OK)
async def get_scores_list(
        params: Annotated[ScoresFilterParams, Query()],
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)]
):
    """
        Возвращает список оценок:

        Параметры пагинации
        - **limit**: количество объектов
        - **offset**: количесвто пропускаемых объектов
    """

    async with uow:
        db_scores = await uow.repo.get_editable(limit=params.limit, offset=params.offset)
        await uow.commit()
    return db_scores


@router.get("/{news_id}", response_model=NewsScoreOut, status_code=status.HTTP_200_OK)
async def get_news(
        news_id: str,
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)]
):
    async with uow:
        try:
            db_score = await uow.repo.get_by_news_id(news_id=news_id)
            await uow.commit()
        except NewsScoreNotFound:
            raise HTTPException(
                status_code=404,
                detail="Оценка события с таким pk не найдена в базе"
            )
    return db_score


@router.patch("/{news_id}", response_model=NewsScoreOut, status_code=status.HTTP_200_OK)
async def patch_score(
        news_id: str,
        data: NewsScorePatch,
        uow: Annotated["AbstractUnitOfWork", Depends(db_uow)],
        broker: Annotated["RedisProducer", Depends(redis_broker)]
):
    async with uow:
        score = await uow.repo.update(news_id=news_id, **data.dict())
        await uow.commit()
    command = commands.NotifyAboutScoredNews(pk=score.news_id, score_value=score.score)
    msg = json.dumps(asdict(command))
    await broker.publish(channel="NewsScored", message=msg)
    return score
