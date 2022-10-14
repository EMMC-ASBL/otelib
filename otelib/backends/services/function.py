"""Function strategy."""
from typing import TYPE_CHECKING

from oteapi.models import FunctionConfig

from otelib.backends.services.base import BaseServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Function(BaseServicesStrategy):
    """Context class for the Function Strategy Interfaces"""

    strategy_name = "function"
    strategy_config = FunctionConfig
