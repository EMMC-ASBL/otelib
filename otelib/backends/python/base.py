"""Abstract Base Class (abc) for strategies."""
import json
import os
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import uuid4

from otelib.exceptions import ApiError
from otelib.pipe import Pipe
from otelib.settings import Settings

if TYPE_CHECKING:  # pragma: no cover
    from pathlib import Path
    from typing import Optional


class Singleton(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


# Note this is a buggy way of having the Cache in memory
# most notably, it is hard to 'clear' the contents
class Cache(Singleton, dict):
    pass


class BasePythonStrategy(ABC):
    """Abstract class for strategies for the python backend.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.
        settings (otelib.settings.Settings): OTEAPI Service settings.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    def __init__(
        self,
        url: "Optional[str]" = None,
        py_exec: "Optional[Path]" = None,
        clear_cache=True,
    ) -> None:
        """Initiates a strategy."""
        if not url and not py_exec or all((url, py_exec)):
            raise ValueError("Either url or py_exec must be specified, not both.")

        self.url: "Optional[str]" = url
        self.settings: Settings = Settings()
        self.input_pipe: "Optional[Pipe]" = None
        self.id: "Optional[str]" = None  # pylint: disable=invalid-name

        # Maybe there is a smarter way to have a persistant cache...
        self.cache = Cache()
        # if clear_cache:
        #    self.cache.clear()

        # For debugging/testing
        self.debug: bool = bool(os.getenv("OTELIB_DEBUG", ""))
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

    def _set_input(self, input_pipe: Pipe) -> None:
        """Used by `__rshift__` to set the input pipe.

        Parameters:
            input_pipe: A pipe representing the strategy that is "piped" into this
                strategy.

        """
        self.input_pipe = input_pipe

    def __rshift__(self, other: "BasePythonStrategy") -> "BasePythonStrategy":
        """Implements strategy concatenation using the `>>` symbol.

        Parameters:
            other: The next strategy this one is "piping" into.

        Returns:
            The next strategy this one is "piped" into.

        """
        pipe = Pipe(self)
        other._set_input(pipe)
        return other

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
        self.settings = Settings()

        if session_id is None:
            session_id = "session-" + str(uuid4())
            self.cache[session_id] = {}

        if self.debug:
            self._session_id = session_id

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)
