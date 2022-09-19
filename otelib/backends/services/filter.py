"""Filter strategy."""
from typing import TYPE_CHECKING

from oteapi.models import FilterConfig

from .base import AbstractServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Filter(AbstractServicesStrategy):
    """Context class for the Filter Strategy Interfaces"""

    def __init__(self, url: "Optional[str]" = None, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.strategy_name = "filter"
        self.strategy_config = FilterConfig
