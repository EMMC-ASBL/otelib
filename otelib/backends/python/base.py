"""Base class for strategies in the Python backend."""
import json
import os
from typing import TYPE_CHECKING
from uuid import uuid4

from oteapi.models import AttrDict
from oteapi.models.genericconfig import GenericConfig
from oteapi.plugins import create_strategy

from otelib.backends.strategies import AbstractBaseStrategy

if TYPE_CHECKING:  # pragma: no cover
    from pathlib import Path
    from typing import Optional

    from otelib.pipe import Pipe


class Singleton:
    """
    Initializes a singleton object
    """

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(Singleton, cls).__new__(cls)
        return cls.instance


class Cache(Singleton, dict):
    """
    Singleton dictionary class. Can be cleared with the .clear() method
    """


class BasePythonStrategy(AbstractBaseStrategy):
    """Base class for strategies for the python backend.

    Parameters:
        interpreter (str): Must be set to `"python"` or a `ValueError` is raised.

    Attributes:
        interpreter (str): This is always `"python"` for the Python backend.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    strategy_name: str
    strategy_config: GenericConfig

    cache = Cache()

    def __init__(
        self,
        interpreter: "Optional[str]" = None,
    ) -> None:
        """Initiates a strategy."""
        if not interpreter:
            raise ValueError("Interpreter (python) must be specified.")

        self.interpreter: "Optional[str]" = interpreter

        if interpreter != "python":
            raise NotImplementedError(
                "Only python interpreter supported for python backend"
            )

        self.input_pipe: "Optional[Pipe]" = None
        self.id: "Optional[str]" = None  # pylint: disable=invalid-name

        # For debugging/testing
        self.debug: bool = bool(os.getenv("OTELIB_DEBUG", ""))
        self._session_id: "Optional[str]" = None

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = self.strategy_config(**kwargs)

        self.id = f"{self.strategy_name}-{str(uuid4())}"
        self.id = self.id
        self.cache[self.id] = data.json()

        if session_id:
            session = self.cache[session_id]
            list_key = f"{self.strategy_name}_info"
            if list_key in session:
                session[list_key].extend([self.id])
            else:
                session[list_key] = [self.id]

    def fetch(self, session_id: str) -> bytes:
        config = self.strategy_config(**json.loads(self.cache[self.id]))
        session_data = None if not session_id else self.cache[session_id]
        session_update = create_strategy(self.strategy_name, config)
        session_update = session_update.get(session=session_data)

        if session_update and session_id:
            self.cache[session_id].update(session_update)

        return bytes(AttrDict(**session_update).json(), encoding="utf-8")

    def initialize(self, session_id: str) -> bytes:
        config = self.strategy_config(**json.loads(self.cache[self.id]))
        if session_id:
            session_data = self.cache[session_id]
        else:
            session_data = None

        strategy = create_strategy(self.strategy_name, config)
        session_update = strategy.initialize(session=session_data)
        if session_update and session_id:
            self.cache[session_id].update(session_update)

        return bytes(AttrDict(**session_update).json(), encoding="utf-8")

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
            session_id = f"session-{str(uuid4())}"
            self.cache[session_id] = {}

        if self.debug:
            self._session_id = session_id

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)
