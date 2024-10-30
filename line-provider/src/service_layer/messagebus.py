from __future__ import annotations

import logging
from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING

from src.domain import commands, events

if TYPE_CHECKING:
    from src.adapters.repository import AbstractRepository

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
            self,
            repository: "AbstractRepository",
            event_handlers: Dict[Type[events.Event], List[Callable]],
            command_handlers: Dict[Type[commands.Command], Callable],
    ):
        self.repo = repository
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue = list()

    async def handle(self, message: Message):
        self.queue.append(message)
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                await self.handle_event(message)
            elif isinstance(message, commands.Command):
                await self.handle_command(message)
            else:
                raise Exception(f"{message} was not an Event or Command")

    async def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug("handling event %s with handler %s", event, handler)
                await handler(event)
            except Exception:
                logger.exception("Exception handling event %s", event)
                continue

    async def handle_command(self, command: commands.Command):
        logger.debug("handling command %s", command)
        try:
            handler = self.command_handlers[type(command)]
            await handler(command)
        except Exception:
            logger.exception("Exception handling command %s", command)
            raise
