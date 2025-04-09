"""Utility function and classes for use in the Backends module."""

from __future__ import annotations

import sys

if sys.version_info >= (3, 11):
    from enum import StrEnum
else:
    from enum import Enum

    class StrEnum(str, Enum):
        """Pre-3.11 style string-Enums."""


class Backend(StrEnum):
    """Backend enumeration."""

    PYTHON = "python"
    SERVICES = "services"


class StrategyType(StrEnum):
    """Enumeration of strategy types."""

    DATARESOURCE = "dataresource"
    PARSER = "parser"
    FILTER = "filter"
    FUNCTION = "function"
    MAPPING = "mapping"
    TRANSFORMATION = "transformation"

    @property
    def cls_name(self) -> str:
        """Return Python class name."""
        return {self.DATARESOURCE: "DataResource"}.get(self, self.capitalize())

    @property
    def oteapi_strategy_type(self) -> str:
        """Return the OTEAPI strategy type."""
        return {self.DATARESOURCE: "resource", self.PARSER: "parse"}.get(
            self, self.lower()
        )
