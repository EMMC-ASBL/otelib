"""Function strategy."""
from typing import TYPE_CHECKING

from oteapi.models import FunctionConfig

from .base import AbstractServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Function(AbstractServicesStrategy):
    """Context class for the Function Strategy Interfaces"""

    def __init__(self, url: "Optional[str]" = None, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.strategy_name = "function"
        self.strategy_config = FunctionConfig
