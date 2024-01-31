"""Function strategy."""

from oteapi.models import FunctionConfig

from otelib.backends.python.base import BasePythonStrategy


class Function(BasePythonStrategy):
    """Context class for the function resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "function"
    strategy_config: "type[FunctionConfig]" = FunctionConfig
