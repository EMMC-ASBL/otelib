"""Filter strategy."""
from typing import TYPE_CHECKING

from oteapi.models import TransformationConfig

from .base import AbstractServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Transformation(AbstractServicesStrategy):
    """Context class for the Transformation Strategy Interfaces"""

    strategy_name = "transformation"
    strategy_config = TransformationConfig
