"""Mapping strategy."""
from typing import TYPE_CHECKING

from oteapi.models import MappingConfig

from .base import AbstractServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Mapping(AbstractServicesStrategy):
    """Context class for the Mapping Strategy Interfaces"""

    def __init__(self, url: "Optional[str]" = None, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.strategy_name = "mapping"
        self.strategy_config = MappingConfig
