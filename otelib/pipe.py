"""Pipe object for creating a pipeline."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional

    from otelib.backends.strategies import AbstractBaseStrategy


class Pipe:
    """Pipe object in a pipe-and-filter pattern."""

    def __init__(self, strategy: "AbstractBaseStrategy") -> None:
        self.input: "AbstractBaseStrategy" = strategy

    def get(self, session_id: "Optional[str]" = None) -> bytes:
        """Call the input strategy's `get()` method."""
        return self.input.get(session_id)
