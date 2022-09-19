"""Mapping strategy."""
from typing import TYPE_CHECKING

from oteapi.models import MappingConfig

from .base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Mapping(BasePythonStrategy):
    """Context class for the mapping strategy interfaces for managing i/o
    operations."""

    def __init__(self, url: "Optional[str]" = None, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.strategy_name = "mapping"
        self.strategy_config = MappingConfig
