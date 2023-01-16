"""Mapping strategy."""
from typing import TYPE_CHECKING

from oteapi.models import MappingConfig

from otelib.backends.services.base import BaseServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Mapping(BaseServicesStrategy):
    """Context class for the Mapping Strategy Interfaces"""

    strategy_name = "mapping"
    strategy_config = MappingConfig
