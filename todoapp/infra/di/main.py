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
from todoapp.application.user.interfaces.repo import UserRepo
from todoapp.common.settings import Config, DatabaseConfig
from todoapp.domain.user.entities import PasswordHasher
from todoapp.infra.db.main import build_sa_engine, build_sa_session, build_sa_session_factory
from todoapp.infra.db.repo.user import UserRepoImpl
from todoapp.infra.db.uow import SQLAlchemyUoW
from todoapp.infra.di import DiScope
from todoapp.infra.mediator import get_mediator
from todoapp.infra.passhash.bcrypt import BcryptPasswordHasher


def init_di_builder() -> DiBuilder:
    di_container = Container()
    di_executor = AsyncExecutor()
    di_scopes = [DiScope.APP, DiScope.REQUEST]
    di_builder = DiBuilderImpl(di_container, di_executor, di_scopes=di_scopes)
    return di_builder


def setup_di_builder(di_builder: DiBuilder) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: di_builder, scope=DiScope.APP), DiBuilder))
    di_builder.bind(bind_by_type(Dependent(SQLAlchemyUoW, scope=DiScope.REQUEST), UnitOfWork))
    di_builder.bind(
        bind_by_type(Dependent(BcryptPasswordHasher, scope=DiScope.APP), PasswordHasher, covariant=True))
    setup_mediator_factory(di_builder, get_mediator, DiScope.REQUEST)
    setup_db_factories(di_builder)


def setup_mediator_factory(
    di_builder: DiBuilder,
    mediator_factory: DependencyProviderType,
    scope: Scope,
) -> None:
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), Mediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), QueryMediator))
    di_builder.bind(bind_by_type(Dependent(mediator_factory, scope=scope), CommandMediator))


def setup_db_factories(di_builder: DiBuilder) -> None:
    di_builder.bind(bind_by_type(Dependent(build_sa_engine, scope=DiScope.APP), AsyncEngine))
    di_builder.bind(
        bind_by_type(
            Dependent(build_sa_session_factory, scope=DiScope.APP),
            async_sessionmaker[AsyncSession],
        ),
    )
    di_builder.bind(bind_by_type(Dependent(build_sa_session, scope=DiScope.REQUEST), AsyncSession))
    di_builder.bind(
        bind_by_type(Dependent(UserRepoImpl, scope=DiScope.REQUEST), UserRepo, covariant=True)
    )

def setup_di_builder_config(di_builder: DiBuilder, config: Config) -> None:
    di_builder.bind(bind_by_type(Dependent(lambda *args: config, scope=DiScope.APP), Config))
    di_builder.bind(bind_by_type(Dependent(lambda *args: config.db, scope=DiScope.APP), DatabaseConfig))