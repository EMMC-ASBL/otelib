"""Filter strategy."""
from typing import TYPE_CHECKING

from oteapi.models import FilterConfig

from otelib.backends.python.base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Type


class Filter(BasePythonStrategy):
    """Context class for the filter strategy interfaces for managing i/o
    operations."""

    strategy_name = "filter"
    strategy_config: "Type[FilterConfig]" = FilterConfig
