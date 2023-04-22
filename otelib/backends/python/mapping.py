"""Mapping strategy."""
from typing import TYPE_CHECKING

from oteapi.models import MappingConfig

from otelib.backends.python.base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Type


class Mapping(BasePythonStrategy):
    """Context class for the mapping strategy interfaces for managing i/o
    operations."""

    strategy_name = "mapping"
    strategy_config: "Type[MappingConfig]" = MappingConfig
