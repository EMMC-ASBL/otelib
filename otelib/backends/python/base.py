"""Base class for strategies in the Python backend."""

import json
import warnings
from typing import TYPE_CHECKING
from uuid import uuid4

from oteapi.models import AttrDict
from oteapi.plugins import create_strategy
from oteapi.utils.config_updater import populate_config_from_session

from otelib.backends.strategies import AbstractBaseStrategy
from otelib.exceptions import ItemNotFoundInCache, PythonBackendException

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Literal, Optional

    from oteapi.models import GenericConfig


class BasePythonStrategy(AbstractBaseStrategy):
    """Base class for strategies for the python backend.

    Parameters:
        source (str): The Python interpreter to use in the local environment.
            Currently only `python` is allowed.

    Attributes:
        interpreter (str): This is always `python` for the Python backend.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    def __init__(self, source: str, cache: "Optional[dict[str, Any]]" = None) -> None:
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

        self.strategy_id = f"{self.strategy_type}-{uuid4()}"
        self.cache[self.strategy_id] = data.model_dump_json(exclude_unset=True)

        if session_id:
            if session_id not in self.cache:
                raise ItemNotFoundInCache(
                    "Session not found in cache, but given to create()", session_id
                )

            # Add strategy ID information to the session object.
            list_key = f"{self.strategy_type}_info"
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

        # Get and update the strategy configuration with the session data
        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))
        session_data = self._fetch_session_data(session_id)
        populate_config_from_session(session_data, config)

        # Perform sanity checks, including session_id and the updated config
        self._sanity_checks(session_id, config)

        # Create strategy and run the method
        strategy = create_strategy(
            self.strategy_type.oteapi_strategy_type,
            config.model_dump(mode="json", exclude_unset=True),
        )

        if not hasattr(strategy, method_name):
            raise PythonBackendException(
                f"{method_name!r} is not a valid method for {strategy}"
            )

        session_update = getattr(strategy, method_name)()

        if isinstance(session_update, dict):
            session_update = AttrDict(**session_update)

        self.cache[session_id].update(
            session_update.model_dump(mode="json", exclude_unset=True)
        )

        return session_update.model_dump_json(exclude_unset=True).encode(
            encoding="utf-8"
        )

    def _sanity_checks(self, session_id: str, config: "GenericConfig") -> None:
        """Perform sanity checks before running a strategy method.

        Parameters:
            session_id: The ID of the session shared by the pipeline.
            config: The strategy configuration object updated with the current session
                data.

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

    def _fetch_session_data(self, session_id: str) -> "dict[str, Any]":
        """Perform sanity checks before running a strategy method.

        Parameters:
            session_id: The ID of the session shared by the pipeline.

        """
        if session_id not in self.cache or not isinstance(
            self.cache.get(session_id, {}), dict
        ):
            raise ItemNotFoundInCache(
                "Did you run this method through get()?", session_id
            )
        return self.cache[session_id]
