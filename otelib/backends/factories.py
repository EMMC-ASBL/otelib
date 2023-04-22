"""Backend factory functions."""
import importlib
from typing import TYPE_CHECKING

from otelib.backends.utils import Backend, StrategyType
from otelib.exceptions import InvalidBackend, InvalidStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Type, Union

    from otelib.backends.client import AbstractBaseClient
    from otelib.backends.strategies import AbstractBaseStrategy


def client_factory(backend: "Union[str, Backend]") -> "Type[AbstractBaseClient]":
    """Return a backend client class."""
    try:
        backend = Backend(backend)
    except ValueError as exc:
        raise InvalidBackend(f"{str(backend)!r} is not a valid backend.") from exc

    client_module = importlib.import_module(f"otelib.backends.{backend}.client")

    if backend == backend.PYTHON:
        return getattr(client_module, "OTEPythonClient")

    if backend == backend.SERVICES:
        return getattr(client_module, "OTEServiceClient")

    raise InvalidBackend(f"{str(backend)!r} is not a valid backend.")


def strategy_factory(
    backend: "Union[str, Backend]", strategy_type: "Union[str, StrategyType]"
) -> "Type[AbstractBaseStrategy]":
    """Return a backend-specific strategy class."""
    try:
        backend = Backend(backend)
    except ValueError as exc:
        raise InvalidBackend(f"{str(backend)!r} is not a valid backend.") from exc

    try:
        strategy_type = StrategyType(strategy_type)
    except ValueError as exc:
        raise InvalidStrategy(
            f"{str(strategy_type)!r} is not a valid strategy."
        ) from exc

    strategy_module = importlib.import_module(
        f"otelib.backends.{backend}.{strategy_type}"
    )
    try:
        return getattr(strategy_module, strategy_type.cls_name)
    except AttributeError as exc:
        raise NotImplementedError(
            f"The {str(strategy_type)!r} is (currently) not supported by the "
            f"{str(backend)!r} backend."
        ) from exc
