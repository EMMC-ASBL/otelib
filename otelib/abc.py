"""Abstract Base Class (abc) for strategies."""
import json
import os
from abc import ABC, abstractmethod

import requests

from otelib.exceptions import ApiError
from otelib.pipe import Pipe
from otelib.settings import Settings


class AbstractStrategy(ABC):
    """Abstract class for strategies."""

    def __init__(self, url):
        """Initiates a strategy.
        The `url` is the base URL of the OTEAPI Services.
        """
        self.url = url
        self.settings = Settings()
        self.input_pipe = None
        self.id_: str = ""

        # For debugging/testing
        self.debug = bool(os.getenv("OTELIB_DEBUG", ""))

    @abstractmethod
    def create(self, **kwargs):
        """Create a strategy.

        It should post the configuration for the created strategy.
        """

    @abstractmethod
    def fetch(self, session_id):
        """Returns the result of the current strategy.

        This method is called by get() while propagating up the pipeline.

        The `session_id` is id of the session shared by the pipeline.
        """

    @abstractmethod
    def initialize(self, session_id):
        """Initialise the current strategy.

        This method is called by get() when propagating down the pipeline.

        The `session_id` is id of the session shared by the pipeline.
        """

    def _set_input(self, input_pipe):
        self.input_pipe = input_pipe

    def __rshift__(self, other):
        """Implements strategy concatenation using the `>>` symbol."""
        pipe = Pipe(self)
        other._set_input(pipe)
        return other

    def get(self, session_id=None):
        """Executes a pipeline.

        The `session_id` is id of the session shared by the pipeline.

        This will call initialize() and then the get() method on the
        input pipe, which in turn will call the get() method on the
        strategy connected to its input and so forth until the beginning
        of the pipeline.

        Finally fetch() is called and its output is returned.
        """
        self.settings = Settings()

        if session_id is None:
            response = requests.post(
                f"{self.url}{self.settings.prefix}/session/", data="{}"
            )
            if not response.ok:
                raise ApiError(
                    f"Cannot create session: {response.status_code}"
                    f"{' content=' + str(response.content) if self.debug else ''}",
                    status=response.status_code,
                )
            session_id = json.loads(response.text)["session_id"]

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)
