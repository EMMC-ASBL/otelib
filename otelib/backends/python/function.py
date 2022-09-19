"""Function strategy."""
from typing import TYPE_CHECKING

from oteapi.models import FunctionConfig

from .base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Function(BasePythonStrategy):
    """Context class for the function resource strategy interfaces for managing i/o
    operations."""

    def __init__(self, url: "Optional[str]" = None, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.strategy_name = "function"
        self.strategy_config = FunctionConfig
