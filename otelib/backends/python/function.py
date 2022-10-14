"""Function strategy."""
from typing import TYPE_CHECKING

from oteapi.models import FunctionConfig

from otelib.backends.python.base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Function(BasePythonStrategy):
    """Context class for the function resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "function"
    strategy_config = FunctionConfig
