"""Filter strategy."""

from oteapi.models import FilterConfig

from otelib.backends.python.base import BasePythonStrategy


class Filter(BasePythonStrategy):
    """Context class for the filter strategy interfaces for managing i/o
    operations."""

    strategy_name = "filter"
    strategy_config: "type[FilterConfig]" = FilterConfig
