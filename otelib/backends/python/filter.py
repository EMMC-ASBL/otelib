"""Filter strategy."""

from typing import TYPE_CHECKING

from oteapi.models import FilterConfig

from .base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Filter(BasePythonStrategy):
    """Context class for the filter strategy interfaces for managing i/o
    operations."""

    def __init__(self, url: "Optional[str]" = None, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.strategy_name = "filter"
        self.strategy_config = FilterConfig
