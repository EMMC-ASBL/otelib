"""Pipe object for creating a pipeline."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from otelib.strategies.abc import AbstractStrategy


class Pipe:
    """Pipe object in a pipe-and-filter pattern."""

    def __init__(self, strategy: "AbstractStrategy") -> None:
        self.input: "AbstractStrategy" = strategy

    def get(self, session: str) -> bytes:
        """Call the input strategy's `get()` method."""
        return self.input.get(session)
