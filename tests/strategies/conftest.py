"""Pytest fixtures for everything in tests/strategies."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Literal, Tuple, Type, Union

    from otelib.backends import python as python_backend
    from otelib.backends import services as services_backend

    from ..conftest import ResourceType

    StrategyCls = Union[
        python_backend.DataResource,
        python_backend.Filter,
        python_backend.Function,
        python_backend.Mapping,
        python_backend.Transformation,
        services_backend.DataResource,
        services_backend.Filter,
        services_backend.Function,
        services_backend.Mapping,
        services_backend.Transformation,
    ]


@pytest.fixture(
    params=["dataresource", "filter", "function", "mapping", "transformation"]
)
def strategy_implementation(
    request: pytest.FixtureRequest,
    backend: str,
    resource_type_cls: "Type[ResourceType]",
) -> "Tuple[Type[StrategyCls], ResourceType, Literal['python', 'services']]":
    """Return a given strategy class implementation as well as the current backend.

    Returns:
        Tuple of the backend-specific strategy class, the `ResourceType` Enum
        representation of the strategy, and the given backend.

    """
    import importlib

    strategy = resource_type_cls(request.param)

    module = importlib.import_module(f"otelib.backends.{backend}.{strategy.value}")
    return getattr(module, strategy.get_class_name()), strategy, backend
