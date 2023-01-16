"""Base class for strategies in the service/REST API backend."""
import json
import os
from typing import TYPE_CHECKING

import requests
from oteapi.models.genericconfig import GenericConfig

from otelib.backends.strategies import AbstractBaseStrategy
from otelib.exceptions import ApiError
from otelib.pipe import Pipe
from otelib.settings import Settings

if TYPE_CHECKING:  # pragma: no cover
    from pathlib import Path
    from typing import Optional


class BaseServicesStrategy(AbstractBaseStrategy):
    """Abstract class for strategies.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.
        settings (otelib.settings.Settings): OTEAPI Service settings.
        input_pipe (Optional[Pipe]): An input pipeline.

    """

    strategy_name: str
    strategy_config: GenericConfig

    def __init__(
        self,
        url: "Optional[str]" = None,
    ) -> None:
        """Initiates a strategy."""
        if not url:
            raise ValueError("Url must be specified.")

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

        response = requests.post(
            f"{self.url}{self.settings.prefix}/{self.strategy_name}",
            json=data.dict(),
            params={"session_id": session_id} if session_id else {},
            timeout=self.settings.timeout,
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create {self.strategy_name}: {data!r}"
                f"content={str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id = response_json.pop(f"{self.strategy_name}_id")

    def fetch(self, session_id: str) -> bytes:
        response = requests.get(
            f"{self.url}{self.settings.prefix}/{self.strategy_name}/{self.id}",
            params={"session_id": session_id},
            timeout=self.settings.timeout,
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch {self.strategy_name}: session_id={session_id!r} "
            f"{self.strategy_name}_id={self.id!r}"
            f"content={str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        post_path = (
            f"{self.url}{self.settings.prefix}"
            f"/{self.strategy_name}/{self.id}/initialize"
        )
        response = requests.post(
            post_path,
            params={"session_id": session_id},
            timeout=self.settings.timeout,
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize {self.strategy_name}: session_id={session_id!r} "
            f"{self.strategy_name}_id={self.id!r}"
            f"content={str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

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
            response = requests.post(
                f"{self.url}{self.settings.prefix}/session",
                json={},
                timeout=self.settings.timeout,
            )
            if not response.ok:
                raise ApiError(
                    f"Cannot create session: {response.status_code}"
                    f"content={str(response.content) if self.debug else ''}",
                    status=response.status_code,
                )
            session_id = json.loads(response.text)["session_id"]

        if self.debug:
            self._session_id = session_id

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)
