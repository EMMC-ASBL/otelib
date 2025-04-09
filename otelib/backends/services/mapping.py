"""Mapping strategy."""

from __future__ import annotations

from oteapi.models import MappingConfig

from otelib.backends.services.base import BaseServicesStrategy


class Mapping(BaseServicesStrategy):
    """Context class for the Mapping Strategy Interfaces"""

    strategy_name = "mapping"
    strategy_config = MappingConfig
