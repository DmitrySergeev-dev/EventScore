from __future__ import annotations

from typing import List, Dict, Callable, Type, TYPE_CHECKING

from src.domain import events, commands

if TYPE_CHECKING:
    from src.service_layer.unit_of_work import AbstractUnitOfWork


async def create_news_score_row(event: events.NewsCreated,
                                uow: "AbstractUnitOfWork"):
    async with uow:
        await uow.repo.add(news_id=event.pk)
        await uow.commit()


async def delete_news_score_row(event: events.NewsDeleted,
                                uow: "AbstractUnitOfWork"):
    async with uow:
        await uow.repo.delete(news_id=event.pk)
        await uow.commit()


EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.NewsCreated: [create_news_score_row],
    events.NewsDeleted: [delete_news_score_row]
}
COMMAND_HANDLERS: Dict[Type[commands.Command], List[Callable]] = {}
