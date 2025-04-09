"""Transformation strategy."""

from __future__ import annotations

from oteapi.models import TransformationConfig

from otelib.backends.python.base import BasePythonStrategy


class Transformation(BasePythonStrategy):
    """Context class for the mapping strategy interfaces for managing i/o
    operations."""

    strategy_name = "transformation"
    strategy_config: type[TransformationConfig] = TransformationConfig
