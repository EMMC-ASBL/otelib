"""Base API for backend strategies."""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class AbstractBaseStrategy(ABC):
    """The abstract base class defining the API for strategies."""

    @abstractmethod
    def create(self, **kwargs) -> None:
        """Create a strategy.

        It should post the configuration for the created strategy.
        """

    @abstractmethod
    def fetch(self, session_id: str) -> bytes:
        """Returns the result of the current strategy.

        This method is called by `get()` while propagating up the pipeline.

        Parameters:
            session_id: The ID of the session shared by the pipeline.

        Returns:
            The response from the OTEAPI Service.

        """

    @abstractmethod
    def initialize(self, session_id: str) -> bytes:
        """Initialise the current strategy.

        This method is called by `get()` when propagating down the pipeline.

        Parameters:
            session_id: The ID of the session shared by the pipeline.

        Returns:
            The response from the OTEAPI Service.

        """

    @abstractmethod
    def get(self, session_id: "Optional[str]" = None) -> bytes:
        """Executes a pipeline.

        This will call `initialize()` and then the `get()` method on the
        input pipe, which in turn will call the `get()` method on the
        strategy connected to its input and so forth until the beginning
        of the pipeline.

        Finally, `fetch()` is called and its output is returned.

        Parameters:
            session_id: The ID of the session shared by the pipeline.

        Returns:
            The output from `fetch()`.

        """

    @abstractmethod
    def __rshift__(self, other: "AbstractBaseStrategy") -> "AbstractBaseStrategy":
        """Implements strategy concatenation using the `>>` symbol.

        Parameters:
            other: The next strategy this one is "piping" into.

        Returns:
            The next strategy this one is "piped" into.

        """
