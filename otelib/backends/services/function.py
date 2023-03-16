"""Function strategy."""
from oteapi.models import FunctionConfig

from otelib.backends.services.base import BaseServicesStrategy


class Function(BaseServicesStrategy):
    """Context class for the Function Strategy Interfaces"""

    strategy_name = "function"
    strategy_config = FunctionConfig
