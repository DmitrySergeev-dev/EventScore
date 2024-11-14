from __future__ import annotations

import logging
from typing import Callable, Dict, List, Union, Type, TYPE_CHECKING

from src.domain import commands, events

if TYPE_CHECKING:
    from src.service_layer import unit_of_work

logger = logging.getLogger(__name__)

Message = Union[commands.Command, events.Event]


class MessageBus:
    def __init__(
            self,
            uow: unit_of_work.AbstractUnitOfWork,
            event_handlers: Dict[Type[events.Event], List[Callable]],
            command_handlers: Dict[Type[commands.Command], List[Callable]]
    ):
        self.uow = uow
        self.event_handlers = event_handlers
        self.command_handlers = command_handlers
        self.queue: list[Message] = list()

    async def handle(self, message: Message):
        self.queue.append(message)
        while self.queue:
            message = self.queue.pop(0)
            if isinstance(message, events.Event):
                await self.handle_event(message)
            elif isinstance(message, commands.Command):
                await self.handle_command(message)
            else:
                raise Exception(f'"{message}" не является ни событием, ни командой!')

    async def handle_event(self, event: events.Event):
        for handler in self.event_handlers[type(event)]:
            try:
                logger.debug('Обработка события: %s обработчиком: %s', event, handler)
                await handler(event)
            except Exception as e:
                logger.exception('Ошибка при обработке события %s: %r', event, e)
                continue

    async def handle_command(self, command: commands.Command):
        logger.debug("Обработка команды: %s", command)
        for handler in self.command_handlers[type(command)]:
            try:
                logger.debug('Обработка команды: %s обработчиком: %s', command, handler)
                await handler(command)
            except Exception:
                logger.exception('Ошибка при обработке команды: %s', command)
                raise
