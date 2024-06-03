__all__ = (
    'build_di_builder',
)

from di import Container, bind_by_type
from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import CommandMediator, Mediator, QueryMediator
from didiator.interface.utils.di_builder import DiBuilder
from didiator.utils.di_builder import DiBuilderImpl
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.application.user.interfaces import UserRepo
from todoapp.common.settings import (
    Config,
    DatabaseConfig
)
from todoapp.domain.user.entities import PasswordHasher
from todoapp.infrastructure.db.main import (
    build_sa_engine,
    build_sa_session,
    build_sa_session_factory
)
from todoapp.infrastructure.db.repositories import (
    UserRepoImpl, TaskRepoImpl, TaskListRepoImpl, TaskMoverImpl
)
from todoapp.infrastructure.db.uow import SQLAlchemyUoW
from todoapp.infrastructure.mediator import get_mediator
from todoapp.infrastructure.passhash.bcrypt import BcryptPasswordHasher
from .constants import DiScope
from ...application.task_list.interfaces.task_mover import TaskMover


def build_di_builder(config: Config) -> DiBuilder:
    di = _init_di_builder()
    _setup_di_builder(di)
    setup_di_builder_config(di, config)
    return di


def _init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = [DiScope.APP, DiScope.REQUEST]
    di_builder = DiBuilderImpl(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def _setup_di_builder(di: DiBuilder) -> None:
    di.bind(bind_by_type(Dependent(lambda *args: di, scope=DiScope.APP), DiBuilder))
    di.bind(
        bind_by_type(
            Dependent(BcryptPasswordHasher, scope=DiScope.APP),
            PasswordHasher,
            covariant=True,
        )
    )

    _setup_mediator_factory(di, get_mediator, DiScope.REQUEST)
    _setup_db_factories(di)
    _setup_repositories(di)


def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope=DiScope.APP), Config))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=DiScope.APP), DatabaseConfig))


def _setup_mediator_factory(
    di: DiBuilder,
    mediator_factory: DependencyProviderType,
    scope: Scope,
) -> None:
    di.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di.bind(bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator))
    di.bind(bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator))


def _setup_db_factories(di: DiBuilder) -> None:
    di.bind(bind_by_type(Dependent(build_sa_engine, scope=DiScope.APP), AsyncEngine))
    di.bind(
        bind_by_type(
            Dependent(build_sa_session_factory, scope=DiScope.APP),
            async_sessionmaker[AsyncSession],
        ),
    )
    di.bind(bind_by_type(Dependent(build_sa_session, scope=DiScope.REQUEST), AsyncSession))
    di.bind(bind_by_type(Dependent(SQLAlchemyUoW, scope=DiScope.REQUEST), UnitOfWork))


def _setup_repositories(di: DiBuilder):
    di.bind(
        bind_by_type(
            Dependent(UserRepoImpl, scope=DiScope.REQUEST),
            UserRepo,
            covariant=True,
        )
    )

    di.bind(
        bind_by_type(
            Dependent(TaskRepoImpl, scope=DiScope.REQUEST),
            TaskRepo,
            covariant=True,
        )
    )

    di.bind(
        bind_by_type(
            Dependent(TaskListRepoImpl, scope=DiScope.REQUEST),
            TaskListRepo,
            covariant=True,
        )
    )

    di.bind(
        bind_by_type(
            Dependent(TaskMoverImpl, scope=DiScope.REQUEST),
            TaskMover,
            covariant=True
        )
    )
