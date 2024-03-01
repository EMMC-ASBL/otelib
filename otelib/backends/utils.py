"""Utility function and classes for use in the Backends module."""

try:  # pragma: no cover
    # Don't cover this block in codecoverage because we're only uploading coverage
    # reports for Python 3.9 runs. We are testing this code on Python 3.9-3.11, so the
    # block _will_ be tested.

    # For Python >= 3.11
    from enum import StrEnum  # type: ignore[attr-defined]
except ImportError:
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
