"""Filter strategy."""
from oteapi.models import TransformationConfig

from otelib.backends.services.base import BaseServicesStrategy


class Transformation(BaseServicesStrategy):
    """Context class for the Transformation Strategy Interfaces"""

    strategy_name = "transformation"
    strategy_config = TransformationConfig
