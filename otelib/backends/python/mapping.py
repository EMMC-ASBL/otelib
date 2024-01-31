"""Mapping strategy."""

from oteapi.models import MappingConfig

from otelib.backends.python.base import BasePythonStrategy


class Mapping(BasePythonStrategy):
    """Context class for the mapping strategy interfaces for managing i/o
    operations."""

    strategy_name = "mapping"
    strategy_config: "type[MappingConfig]" = MappingConfig
