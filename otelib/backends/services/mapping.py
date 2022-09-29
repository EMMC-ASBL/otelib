"""Mapping strategy."""
from typing import TYPE_CHECKING

from oteapi.models import MappingConfig

from .base import AbstractServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Mapping(AbstractServicesStrategy):
    """Context class for the Mapping Strategy Interfaces"""

    strategy_name = "mapping"
    strategy_config = MappingConfig
