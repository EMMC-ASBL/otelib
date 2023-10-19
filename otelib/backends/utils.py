"""Utility function and classes for use in the Backends module."""
from enum import Enum


class Backend(str, Enum):
    """Backend enumeration."""

    PYTHON = "python"
    SERVICES = "services"

    def __str__(self) -> str:
        """Return string representation of Backend."""
        return self.value


class StrategyType(str, Enum):
    """Enumeration of strategy types."""

    DATARESOURCE = "dataresource"
    FILTER = "filter"
    FUNCTION = "function"
    MAPPING = "mapping"
    TRANSFORMATION = "transformation"

    @property
    def cls_name(self) -> str:
        """Return Python class name."""
        return {self.DATARESOURCE: "DataResource"}.get(self, self.capitalize())

    def __str__(self) -> str:
        """Return string representation of Backend."""
        return self.value
