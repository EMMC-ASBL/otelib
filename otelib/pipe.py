"""Pipe object for creating a pipeline."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover

    from otelib.backends.strategies import AbstractBaseStrategy


class Pipe:
    """Pipe object in a pipe-and-filter pattern."""

    def __init__(self, strategy: AbstractBaseStrategy) -> None:
        self.input: AbstractBaseStrategy = strategy

    def get(self, session_id: str | None = None) -> bytes:
        """Call the input strategy's `get()` method."""
        return self.input.get(session_id)
