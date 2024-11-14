from __future__ import annotations

from typing import List, Dict, Callable, Type, TYPE_CHECKING

from src.domain import events, commands

if TYPE_CHECKING:
    from src.service_layer.unit_of_work import AbstractUnitOfWork
from src.domain.model import News


async def update_news_status(event: events.NewsScored,
                             uow: "AbstractUnitOfWork"):
    status = News.define_status_by_score(score_value=event.score_value)
    async with uow:
        await uow.repo.update(pk=event.news_hash, status=status)


EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.NewsScored: [update_news_status],
}
COMMAND_HANDLERS: Dict[Type[commands.Command], List[Callable]] = {}
