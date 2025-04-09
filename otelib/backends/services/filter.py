"""Filter strategy."""

from __future__ import annotations

from oteapi.models import FilterConfig

from otelib.backends.services.base import BaseServicesStrategy


class Filter(BaseServicesStrategy):
    """Context class for the Filter Strategy Interfaces"""

    strategy_name = "filter"
    strategy_config = FilterConfig
