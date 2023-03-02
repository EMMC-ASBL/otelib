"""Base class for strategies in the Python backend."""
import json
import warnings
from copy import deepcopy
from typing import TYPE_CHECKING
from uuid import uuid4

from oteapi.plugins import create_strategy

from otelib.backends.strategies import AbstractBaseStrategy
from otelib.exceptions import ItemNotFoundInCache, PythonBackendException

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Literal, Optional

    from oteapi.models import SessionUpdate


class BasePythonStrategy(AbstractBaseStrategy):
    """Base class for strategies for the python backend.

    Parameters:
        source (str): The Python interpreter to use in the local environment.
            Currently only `python` is allowed.

    Attributes:
        interpreter (str): This is always `python` for the Python backend.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    def __init__(self, source: str, cache: "Optional[Dict[str, Any]]" = None) -> None:
        super().__init__(source)

        self.interpreter: "Optional[str]" = source
        if cache is None:
            warnings.warn(f"No global cache used for Python backend strategy {self}")
        self.cache = cache if cache is not None else {}

        if self.interpreter != "python":
            raise ValueError(
                "Only the 'python' interpreter source is currently supported."
            )

    def create(self, **config) -> None:
        session_id = config.pop("session_id", None)
        data = self.strategy_config(**config)

        self.strategy_id = f"{self.strategy_name}-{uuid4()}"
        self.cache[self.strategy_id] = data.json()

        if session_id:
            if session_id not in self.cache:
                raise ItemNotFoundInCache(
                    "Session not found in cache, but given to create()", session_id
                )

            # Add strategy ID information to the session object.
            list_key = f"{self.strategy_name}_info"
            if list_key in self.cache[session_id]:
                if not isinstance(self.cache[session_id][list_key], list):
                    raise TypeError(
                        f"Expected type for {list_key!r} field in session to be a "
                        f"list, found {type(self.cache[session_id][list_key])!r}."
                    )
                self.cache[session_id][list_key].append(self.strategy_id)
            else:
                self.cache[session_id][list_key] = [self.strategy_id]

    def fetch(self, session_id: str) -> bytes:
        return self._run_strategy_method("get", session_id)

    def initialize(self, session_id: str) -> bytes:
        return self._run_strategy_method("initialize", session_id)

    def _create_session(self) -> str:
        session_id = f"session-{uuid4()}"
        self.cache[session_id] = {}
        return session_id

    def _run_strategy_method(
        self, method_name: "Literal['get', 'initialize']", session_id: str
    ) -> bytes:
        """Generic implementation of the `fetch()` and `initialize()` methods.

        This will run the `method_name` method on the strategy and return the
        serialized session update object.

        Parameters:
            method_name: The name of the strategy's method to execute.
            session_id: The ID of the session shared by the pipeline.

        Returns:
            The bytes-serialized output from the given strategy method.

        """
        if method_name not in ["get", "initialize"]:
            raise PythonBackendException(
                "method_name should be either 'get' or 'initialize'."
            )

        self._sanity_checks(session_id)

        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))
        strategy = create_strategy(self.strategy_name, config)

        if not hasattr(strategy, method_name):
            raise PythonBackendException(
                f"{method_name!r} is not a valid method for {strategy}"
            )

        session_update: "SessionUpdate" = getattr(strategy, method_name)(
            session=deepcopy(self.cache[session_id])
        )

        self.cache[session_id].update(session_update)

        return session_update.json().encode(encoding="utf-8")

    def _sanity_checks(self, session_id: str) -> None:
        """Perform sanity checks before running a strategy method.

        Parameters:
            session_id: The ID of the session shared by the pipeline.

        """
        if not self.strategy_id or self.strategy_id not in self.cache:
            raise ItemNotFoundInCache(
                "Run create() prior to initialize()", self.strategy_id
            )

        if session_id not in self.cache or not isinstance(
            self.cache.get(session_id, {}), dict
        ):
            raise ItemNotFoundInCache(
                "Did you run this method through get()?", session_id
            )
