import inspect
from adapters.orm import start_mappers
from services import message_bus, unit_of_work


def bootstrap(
    start_orm: bool = True,
    uow: unit_of_work.AbstractUnitOfWork = unit_of_work.SqlAlchemyUnitOfWork(),
    # notifications: AbstractNotifications = None,
    # publish: Callable = redis_eventpublisher.publish,
) -> message_bus:

    # if notifications is None:
    #     notifications = EmailNotifications()

    if start_orm:
        start_mappers()

    # dependencies = {"uow": uow, "notifications": notifications, "publish": publish}
    dependencies = {"uow": uow}
    injected_event_handlers = {
        event_type: [
            inject_dependencies(handler, dependencies) for handler in event_handlers
        ]
        for event_type, event_handlers in message_bus.EVENT_HANDLERS.items()
    }
    injected_command_handlers = {
        command_type: inject_dependencies(handler, dependencies)
        for command_type, handler in message_bus.COMMAND_HANDLERS.items()
    }

    return message_bus.MessageBus(
        uow=uow,
        event_handlers=injected_event_handlers,
        command_handlers=injected_command_handlers,
    )


def inject_dependencies(handler, dependencies):
    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)