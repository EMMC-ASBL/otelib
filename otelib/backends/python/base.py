"""Abstract Base Class (abc) for strategies."""
import json
import os
from typing import TYPE_CHECKING
from uuid import uuid4

from oteapi.models import AttrDict
from oteapi.models.genericconfig import GenericConfig
from oteapi.plugins import create_strategy

from otelib.backends.strategies import AbstractBaseStrategy
from otelib.settings import Settings

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
    """Abstract class for strategies for the python backend.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.
        settings (otelib.settings.Settings): OTEAPI Service settings.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    strategy_name: str = ""
    strategy_config: GenericConfig = GenericConfig

    cache = Cache()

    # pylint: disable=too-many-instance-attributes
    # pylint: disable=duplicate-code
    def __init__(
        self,
        url: "Optional[str]" = None,
    ) -> None:
        """Initiates a strategy."""
        if not url:
            raise ValueError("Url (python) must be specified.")

        self.url: "Optional[str]" = url
        self.settings: Settings = Settings()
        self.input_pipe: "Optional[Pipe]" = None
        self.id: "Optional[str]" = None  # pylint: disable=invalid-name

        # For debugging/testing
        self.debug: bool = bool(os.getenv("OTELIB_DEBUG", ""))
        self._session_id: "Optional[str]" = None

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = self.strategy_config(**kwargs)

        resource_id = f"{self.strategy_name}-{str(uuid4())}"
        self.id = resource_id
        self.cache[resource_id] = data.json()

        if session_id:
            session = self.cache[session_id]
            list_key = f"{self.strategy_name}_info"
            if list_key in session:
                session[list_key].extend([resource_id])
            else:
                session[list_key] = [resource_id]

    def fetch(self, session_id: str) -> bytes:
        resource_id = self.id

        config = self.strategy_config(**json.loads(self.cache[resource_id]))
        session_data = None if not session_id else self.cache[session_id]
        session_update = create_strategy(self.strategy_name, config)
        session_update = session_update.get(session=session_data)

        if session_update and session_id:
            self.cache[session_id].update(session_update)

        return AttrDict(**session_update).json()

    def initialize(self, session_id: str) -> bytes:
        resource_id = self.id

        config = self.strategy_config(**json.loads(self.cache[resource_id]))
        if session_id:
            session_data = self.cache[session_id]
        else:
            session_data = None

        strategy = create_strategy(self.strategy_name, config)
        session_update = strategy.initialize(session=session_data)
        if session_update and session_id:
            self.cache[session_id].update(session_update)

        return AttrDict(**session_update).json()

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
            session_id = f"session-{str(uuid4())}"
            self.cache[session_id] = {}

        if self.debug:
            self._session_id = session_id

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)
