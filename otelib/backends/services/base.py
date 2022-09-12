"""Abstract Base Class (abc) for strategies."""
import json
import os
from abc import abstractmethod
from typing import TYPE_CHECKING

import requests

from otelib.backends.strategies import AbstractBaseStrategy
from otelib.exceptions import ApiError
from otelib.pipe import Pipe
from otelib.settings import Settings

if TYPE_CHECKING:  # pragma: no cover
    from pathlib import Path
    from typing import Optional


class AbstractServicesStrategy(AbstractBaseStrategy):
    """Abstract class for strategies.

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
