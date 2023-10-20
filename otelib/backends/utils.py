"""Utility function and classes for use in the Backends module."""
from platform import python_version

if python_version() >= "3.11":  # pragma: no cover
    from enum import StrEnum  # type: ignore[attr-defined]
else:  # pragma: no cover
    from enum import Enum

    class StrEnum(str, Enum):  # type: ignore[no-redef]
        """Pre-3.11 style string-Enums."""


class Backend(StrEnum):
    """Backend enumeration."""

    PYTHON = "python"
    SERVICES = "services"


class StrategyType(StrEnum):
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
