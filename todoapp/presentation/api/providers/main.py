from di import ScopeState
from didiator import CommandMediator, EventMediator, Mediator, QueryMediator
from didiator.interface.utils.di_builder import DiBuilder
from fastapi import FastAPI

from .di import StateProvider, get_di_builder, get_di_state
from .mediator import MediatorProvider
from .stub import Stub


# noinspection PyUnresolvedReferences
def setup_providers(
    app: FastAPI,
    mediator: Mediator,
    di_builder: DiBuilder,
    di_state: ScopeState | None = None,
) -> None:
    mediator_provider = MediatorProvider(mediator)

    app.dependency_overrides[Stub(Mediator)] = mediator_provider
    app.dependency_overrides[Stub(CommandMediator)] = mediator_provider
    app.dependency_overrides[Stub(QueryMediator)] = mediator_provider
    app.dependency_overrides[Stub(EventMediator)] = mediator_provider

    state_provider = StateProvider(di_state)

    app.dependency_overrides[get_di_builder] = lambda: di_builder
    app.dependency_overrides[get_di_state] = state_provider
