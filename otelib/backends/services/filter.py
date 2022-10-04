"""Filter strategy."""
from typing import TYPE_CHECKING

from oteapi.models import FilterConfig

from otelib.backends.services.base import BaseServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Filter(BaseServicesStrategy):
    """Context class for the Filter Strategy Interfaces"""

    strategy_name = "filter"
    strategy_config = FilterConfig
