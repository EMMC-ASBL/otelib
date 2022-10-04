"""Filter strategy."""
from typing import TYPE_CHECKING

from oteapi.models import TransformationConfig

from otelib.backends.services.base import BaseServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Transformation(BaseServicesStrategy):
    """Context class for the Transformation Strategy Interfaces"""

    strategy_name = "transformation"
    strategy_config = TransformationConfig
