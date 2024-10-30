from __future__ import annotations

from typing import List, Dict, Callable, Type, TYPE_CHECKING

from src.domain import events

if TYPE_CHECKING:
    from src.adapters.repository import AbstractRepository
from src.domain.model import News


async def update_news_status(event: events.NewsScored,
                             repository: "AbstractRepository"):
    status = News.define_status_by_score(score_value=event.score_value)
    await repository.update(pk=event.news_hash, status=status)


EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {
    events.NewsScored: [update_news_status],
}
COMMAND_HANDLERS: Dict[Type[events.Event], List[Callable]] = {}
