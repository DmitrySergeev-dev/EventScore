import inspect
from typing import Callable, Any

from src.service_layer import handlers, messagebus, unit_of_work


def bootstrap(
        uow: unit_of_work.AbstractUnitOfWork = unit_of_work.PostgresUnitOfWork()
) -> messagebus.MessageBus:
    dependencies = {"uow": uow}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies)
            for handler in event_handlers
        ]
        for event_type, event_handlers in handlers.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: [
            inject_dependencies(handler, dependencies)
            for handler in command_handlers
        ]
        for command_type, command_handlers in handlers.COMMAND_HANDLERS.items()
    }

    return messagebus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers
    )


def inject_dependencies(handler: Callable, dependencies: dict[str, Any]) -> Callable:
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency
        for name, dependency in dependencies.items()
        if name in params
    }
    return lambda message: handler(message, **deps)
