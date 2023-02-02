"""Transformation strategy."""
from typing import TYPE_CHECKING

from oteapi.models import TransformationConfig

from otelib.backends.python.base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Type


class Transformation(BasePythonStrategy):
    """Context class for the mapping strategy interfaces for managing i/o
    operations."""

    strategy_name = "transformation"
    strategy_config: "Type[TransformationConfig]" = TransformationConfig
