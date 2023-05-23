"""Base class for strategies in the service/REST API backend."""
import json
from typing import TYPE_CHECKING

import requests

from otelib.backends.strategies import AbstractBaseStrategy
from otelib.exceptions import ApiError
from otelib.settings import Settings

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional


class BaseServicesStrategy(AbstractBaseStrategy):
    """Abstract class for strategies.

    Parameters:
        source (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.
        settings (otelib.settings.Settings): OTEAPI Service settings.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    def __init__(self, source: str) -> None:
        super().__init__(source)

        self.url: "Optional[str]" = source
        self._headers: "Optional[Dict[str, Any]]" = None
        self.settings = Settings()

    @property
    def headers(self) -> "Dict[str, Any]":
        """URL headers to use for all requests to the OTEAPI Service."""
        value = self._headers or {}
        if "Content-Type" not in value:
            value["Content-Type"] = "application/json"
        return value

    @headers.setter
    def headers(self, value: "Dict[str, Any]") -> None:
        """Set the URL headers to use for all requests to the OTEAPI Service."""
        if not isinstance(value, dict):
            raise TypeError("headers must be a dictionary")
        self._headers = value

    def create(self, **config) -> None:
        session_id = config.pop("session_id", None)
        data = self.strategy_config(**config)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/{self.strategy_name}",
            data=data.json(),
            params={"session_id": session_id} if session_id else {},
            timeout=self.settings.timeout,
            headers=self.headers,
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create {self.strategy_name}: {data!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.strategy_id = (
            response_json.pop(f"{self.strategy_name}_id")
            if f"{self.strategy_name}_id" in response_json
            else response_json.pop(f"{self.strategy_name[len('data'):]}_id")
        )

    def fetch(self, session_id: str) -> bytes:
        response = requests.get(
            f"{self.url}{self.settings.prefix}/{self.strategy_name}/{self.strategy_id}",
            params={"session_id": session_id},
            timeout=self.settings.timeout,
            headers=self.headers,
        )
        if response.ok:
            return response.content
        strategy_name = (
            self.strategy_name[len("data") :]
            if self.strategy_name.startswith("data")
            else self.strategy_name
        )
        raise ApiError(
            f"Cannot fetch {self.strategy_name}: session_id={session_id!r} "
            f"{strategy_name}_id={self.strategy_id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        post_path = (
            f"{self.url}{self.settings.prefix}"
            f"/{self.strategy_name}/{self.strategy_id}/initialize"
        )
        response = requests.post(
            post_path,
            params={"session_id": session_id},
            timeout=self.settings.timeout,
            headers=self.headers,
        )
        if response.ok:
            return response.content
        strategy_name = (
            self.strategy_name[len("data") :]
            if self.strategy_name.startswith("data")
            else self.strategy_name
        )
        raise ApiError(
            f"Cannot initialize {self.strategy_name}: session_id={session_id!r} "
            f"{strategy_name}_id={self.strategy_id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def _create_session(self) -> str:
        response = requests.post(
            f"{self.url}{self.settings.prefix}/session",
            json={},
            headers=self.headers,
            timeout=self.settings.timeout,
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create session: {response.status_code} "
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )
        return json.loads(response.text)["session_id"]
