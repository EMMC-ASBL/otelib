"""Base API for backend strategies."""
import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from otelib.backends.utils import StrategyType
from otelib.pipe import Pipe

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional, Type, Union

    from oteapi.models.genericconfig import GenericConfig


class AbstractBaseStrategy(ABC):
    """The abstract base class defining the API for strategies."""

    strategy_name: "Union[StrategyType, str]"
    strategy_config: "Type[GenericConfig]"

    def __init__(self, source: str) -> None:
        """Initiates a strategy."""
        if not source:
            raise ValueError("source must be provided.")

        self.input_pipe: "Optional[Pipe]" = None
        self.strategy_id: str = ""
        self.strategy_name = StrategyType(self.strategy_name)

        # For debugging/testing
        self.debug = bool(os.getenv("OTELIB_DEBUG", ""))
        self._session_id: "Optional[str]" = None

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
            The result of calling the `get()` method on the current strategy

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
        if session_id is None:
            session_id = self._create_session()

        if self.debug:
            self._session_id = session_id

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)

    @abstractmethod
    def _create_session(self) -> str:
        """Create a new session.

        This method should not be run by a user, hence it is "private".
        The method is used within the `get()` method and allows a backend to customize
        its session creation method.

        Returns:
            The newly created session's ID.

        """

    def _set_input(self, input_pipe: Pipe) -> None:
        """Used by `__rshift__` to set the input pipe.

        Parameters:
            input_pipe: A pipe representing the strategy that is "piped" into this
                strategy.

        """
        self.input_pipe = input_pipe

    def __rshift__(self, other: "AbstractBaseStrategy") -> "AbstractBaseStrategy":
        """Implements strategy concatenation using the `>>` symbol.

        Parameters:
            other: The next strategy this one is "piping" into.

        Returns:
            The next strategy this one is "piped" into.

        """
        pipe = Pipe(self)
        other._set_input(pipe)
        return other
