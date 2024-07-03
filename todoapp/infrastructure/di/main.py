__all__ = (
    'init_di_builder',
    'setup_di_builder',
)

from di import Container, bind_by_type
from di.api.providers import DependencyProviderType
from di.api.scopes import Scope
from di.dependent import Dependent
from di.executors import AsyncExecutor
from didiator import CommandMediator, Mediator, QueryMediator
from didiator.interface.utils.di_builder import DiBuilder
from didiator.utils.di_builder import DiBuilderImpl
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from todoapp.application.auth.jwt import JWTAuthenticator
from todoapp.application.common.interfaces.uow import UnitOfWork
from todoapp.application.task.interfaces.repository import TaskRepo
from todoapp.application.task_list.interfaces import TaskListRepo
from todoapp.application.user.interfaces import UserRepo
from todoapp.common.settings import (
    Config,
    DatabaseConfig, AuthConfig
)
from todoapp.domain.user.entities import PasswordHasher
from todoapp.infrastructure.auth.bcrypt import BcryptPasswordHasher
from todoapp.infrastructure.auth.di import get_jwt_authenticator
from todoapp.infrastructure.db.main import (
    build_sa_engine,
    build_sa_session,
    build_sa_session_factory
)
from todoapp.infrastructure.db.repositories import (
    UserRepoImpl, TaskRepoImpl, TaskListRepoImpl, TaskInListFinderImpl
)
from todoapp.infrastructure.db.repositories.task_list import TaskInListFinder
from todoapp.infrastructure.db.uow import SQLAlchemyUoW
from todoapp.infrastructure.mediator import get_mediator
from todoapp.infrastructure.redis.main import build_redis_client
from .constants import DiScope
from ..auth.repository import TokensRepoImpl


def init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = [DiScope.APP, DiScope.REQUEST]
    di_builder = DiBuilderImpl(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def setup_di_builder(di: DiBuilder, config: Config) -> None:
    di.bind(bind_by_type(Dependent(lambda *args: di, scope=DiScope.APP), DiBuilder))
    di.bind(
        bind_by_type(
            Dependent(BcryptPasswordHasher, scope=DiScope.APP),
            PasswordHasher,
            covariant=True,
        )
    )
    di.bind(
        bind_by_type(
            Dependent(get_jwt_authenticator, scope=DiScope.APP),
            JWTAuthenticator,
            covariant=True,
        )
    )

    _setup_mediator_factory(di, get_mediator, DiScope.REQUEST)
    _setup_db_factories(di)
    _setup_repositories(di)
    _setup_di_builder_config(di, config)


def _setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope=DiScope.APP), Config))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=DiScope.APP), DatabaseConfig))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.auth, scope=DiScope.APP), AuthConfig))


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
    di.bind(bind_by_type(Dependent(build_redis_client, scope=DiScope.APP), Redis))


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
            Dependent(TaskInListFinderImpl, scope=DiScope.REQUEST),
            TaskInListFinder,
            covariant=True
        )
    )

    from todoapp.application.auth.interfaces.repository import TokensRepo
    di.bind(
        bind_by_type(
            Dependent(TokensRepoImpl, scope=DiScope.REQUEST),
            TokensRepo,
            covariant=True
        )
    )
