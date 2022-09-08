"""Base class for strategies."""
import json
import os
from abc import ABC
from typing import TYPE_CHECKING

import requests

from otelib.exceptions import ApiError
from otelib.pipe import Pipe
from otelib.settings import Settings
from otelib.strategies import StrategyType

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Optional, Union


class BaseStrategy(ABC):
    """Base class for Service strategies.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.
        settings (otelib.settings.Settings): OTEAPI Service settings.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    def __init__(self, url: str) -> None:
        """Initiates a strategy."""
        self.url: str = url
        self.settings: Settings = Settings()
        self.input_pipe: "Optional[Pipe]" = None
        self.id: "Optional[str]" = None  # pylint: disable=invalid-name

        # For debugging/testing
        self.debug: bool = bool(os.getenv("OTELIB_DEBUG", ""))
        self._session_id: "Optional[str]" = None

    def create(self, **kwargs) -> None:
        self._create(
            strategy_type=self.__class__.__name__,
            session_id=kwargs.pop("session_id", None),
            **kwargs,
        )

    def _create(
        self,
        strategy_type: "Union[StrategyType, str]",
        session_id: "Optional[str]" = None,
        **kwargs: "Any",
    ) -> None:
        """Create a strategy.

        Actual function to create a strategy.
        This function should be overwritten in the sub-class.
        """
        strategy_type = StrategyType(strategy_type)
        data = strategy_type.config_cls(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/{strategy_type.value}",
            json=data.dict(),
            params={"session_id": session_id},
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create {strategy_type.name}: "
                + " ".join(
                    f"{_}={getattr(data, _)!r}"
                    for _ in strategy_type.relevant_config_fields
                )
                + f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: "dict[str, Any]" = response.json()
        id_name = (
            "resource" if strategy_type.value == "dataresource" else strategy_type.value
        )
        self.id = response_json.pop(f"{id_name}_id")

    def fetch(self, session_id: str) -> bytes:
        return self._fetch(
            strategy_type=self.__class__.__name__,
            session_id=session_id,
        )

    def _fetch(
        self, strategy_type: "Union[StrategyType, str]", session_id: str
    ) -> bytes:
        """Generic method for fetching."""
        strategy_type = StrategyType(strategy_type)
        response = requests.get(
            f"{self.url}{self.settings.prefix}/{strategy_type.value}/{self.id}",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        id_name = (
            "resource" if strategy_type.value == "dataresource" else strategy_type.value
        )
        raise ApiError(
            f"Cannot fetch {strategy_type.name}: session_id={session_id!r} "
            f"{id_name}_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        return self._initialize(
            strategy_type=self.__class__.__name__,
            session_id=session_id,
        )

    def _initialize(
        self, strategy_type: "Union[StrategyType, str]", session_id: str
    ) -> bytes:
        """Generic method for initializing."""
        strategy_type = StrategyType(strategy_type)
        response = requests.post(
            f"{self.url}{self.settings.prefix}/{strategy_type.value}/{self.id}/initialize",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        id_name = (
            "resource" if strategy_type.value == "dataresource" else strategy_type.value
        )
        raise ApiError(
            f"Cannot initialize {strategy_type.name}: session_id={session_id!r} "
            f"{id_name}_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def _set_input(self, input_pipe: Pipe) -> None:
        """Used by `__rshift__` to set the input pipe.

        Parameters:
            input_pipe: A pipe representing the strategy that is "piped" into this
                strategy.

        """
        self.input_pipe = input_pipe

    def __rshift__(self, other: "BaseStrategy") -> "BaseStrategy":
        pipe = Pipe(self)
        other._set_input(pipe)
        return other

    def get(self, session_id: "Optional[str]" = None) -> bytes:
        self.settings = Settings()

        if session_id is None:
            response = requests.post(
                f"{self.url}{self.settings.prefix}/session", json={}
            )
            if not response.ok:
                raise ApiError(
                    f"Cannot create session: {response.status_code}"
                    f"{' content=' + str(response.content) if self.debug else ''}",
                    status=response.status_code,
                )
            session_id = json.loads(response.text)["session_id"]

        if self.debug:
            self._session_id = session_id

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)
