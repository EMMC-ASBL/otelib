"""Pipe object for creating a pipeline."""
# pylint: disable=too-few-public-methods
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict

    from oteapi.interfaces import IStrategy


class Pipe:
    """Pipe object in a pipe-and-filter pattern."""

    def __init__(self, strategy: "IStrategy") -> None:
        self.input = strategy

    def get(self, session: "Dict[str, Any]") -> "Dict[str, Any]":
        """Call the input strategy's `get()` method."""
        return self.input.get(session)
