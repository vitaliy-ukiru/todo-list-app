import logging

from didiator import (
    CommandDispatcherImpl,
    EventObserverImpl,
    Mediator,
    MediatorImpl,
    QueryDispatcherImpl
)
from didiator.interface.utils.di_builder import DiBuilder
from didiator.middlewares.di import DiMiddleware, DiScopes
from didiator.middlewares.logging import LoggingMiddleware

from todoapp.application.task.commands import (
    CompleteTask, CompleteTaskHandler,
    CreateTask, CreateTaskHandler,
    UpdateTask, UpdateTaskHandler,
    PutTaskInList, PutTaskInListHandler,
    DeleteTask, DeleteTaskHandler,
)
from todoapp.application.task.queries import (
    FindTasks, FindTasksHandler,
    GetTaskById, GetTaskByIdHandler,
)
from todoapp.application.task_list.commands import (
    MoveTasks, MoveTasksHandler,
    AddTaskInList, AddTaskInListHandler, CreateTaskList, CreateTaskListHandler, DeleteTaskListHandler,
    DeleteTaskList
)
from todoapp.application.task_list.queries import (
    GetListDetailsById,
    GetListDetailsByIdHandler, GetListById, GetListByIdHandler,
)
from todoapp.application.user.commands import (
    CreateUser,
    CreateUserHandler,
)
from todoapp.infrastructure.di import DiScope


def init_mediator(di_builder: DiBuilder) -> Mediator:
    middlewares = (
        LoggingMiddleware("mediator", level=logging.DEBUG),
        DiMiddleware(di_builder, scopes=DiScopes(DiScope.REQUEST)),
    )
    command_dispatcher = CommandDispatcherImpl(middlewares=middlewares)
    query_dispatcher = QueryDispatcherImpl(middlewares=middlewares)
    event_observer = EventObserverImpl(middlewares=middlewares)

    mediator = MediatorImpl(command_dispatcher, query_dispatcher, event_observer)
    return mediator


def setup_mediator(mediator: Mediator) -> None:
    mediator.register_command_handler(CreateUser, CreateUserHandler)

    mediator.register_command_handler(CompleteTask, CompleteTaskHandler)
    mediator.register_command_handler(CreateTask, CreateTaskHandler)
    mediator.register_command_handler(UpdateTask, UpdateTaskHandler)
    mediator.register_command_handler(PutTaskInList, PutTaskInListHandler)
    mediator.register_command_handler(DeleteTask, DeleteTaskHandler)

    mediator.register_query_handler(FindTasks, FindTasksHandler)
    mediator.register_query_handler(GetTaskById, GetTaskByIdHandler)

    mediator.register_command_handler(AddTaskInList, AddTaskInListHandler)
    mediator.register_command_handler(MoveTasks, MoveTasksHandler)
    mediator.register_command_handler(CreateTaskList, CreateTaskListHandler)
    mediator.register_command_handler(DeleteTaskList, DeleteTaskListHandler)

    mediator.register_query_handler(GetListDetailsById, GetListDetailsByIdHandler)
    mediator.register_query_handler(GetListById, GetListByIdHandler)


def get_mediator() -> Mediator:
    raise NotImplemented
