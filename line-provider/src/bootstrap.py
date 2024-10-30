import inspect
from typing import Callable, Any
from typing import TYPE_CHECKING

from src.adapters.repository import RedisRepository
from src.service_layer import handlers, messagebus

if TYPE_CHECKING:
    from src.adapters.repository import AbstractRepository


def bootstrap(repository: "AbstractRepository" = RedisRepository) -> messagebus.MessageBus:
    dependencies = {"repository": repository}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        repository=repository,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler: Callable, dependencies: dict[str: Any]):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
