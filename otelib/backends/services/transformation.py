"""Filter strategy."""
from typing import TYPE_CHECKING

from oteapi.models import TransformationConfig

from .base import AbstractServicesStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class Transformation(AbstractServicesStrategy):
    """Context class for the Transformation Strategy Interfaces"""

    def __init__(self, url: "Optional[str]" = None, **kwargs) -> None:
        super().__init__(url, **kwargs)
        self.strategy_name = "transformation"
        self.strategy_config = TransformationConfig
