from abc import ABC, abstractmethod
import json
import requests

from otelib.apierror import ApiError
from otelib.pipe import Pipe
from otelib.settings import Settings


class AbstractFilter(ABC):
    """Abstract class for filters."""

    def __init__(self, url):
        """Initiates a filter.
        The `url` is the base URL of the OTEAPI Services.
        """
        self.url = url
        self.settings = Settings()
        self.input_pipe = None

    @abstractmethod
    def create(self, **kwargs):
        """Create a filter.

        It should post the configuration for the created filter.
        """

    @abstractmethod
    def fetch(self, session_id):
        """Returns the result of the current filter.

        This method is called by get() while propagating up the pipeline.

        The `session_id` is id of the session shared by the pipeline.
        """

    @abstractmethod
    def initialize(self, session_id):
        """Initialise the current filter.

        This method is called by get() when propagating down the pipeline.

        The `session_id` is id of the session shared by the pipeline.
        """

    def _set_input(self, input_pipe):
        self.input_pipe = input_pipe

    def __rshift__(self, other):
        """Implements filter concatenation using the `>>` symbol."""
        p = Pipe(self)
        other._set_input(p)
        return other

    def get(self, session_id=None):
        """Executes a pipeline.

        The `session_id` is id of the session shared by the pipeline.

        This will call initialize() and then the get() method on the
        input pipe, which in turn will call the get() method on the
        filter connected to its input and so forth until the beginning
        of the pipeline.

        Finally fetch() is called and its output is returned.
        """
        self.settings = Settings()

        if session_id is None:
            response = requests.post(
                f'{self.url}{self.settings.prefix}/session/', data='{}'
            )
            if response.status_code != 200:
                raise ApiError(
                    f'Cannot create session: {response.status_code}'
                )
            session_id = json.loads(response.text)['session_id']

        self.initialize(session_id)
        if self.input_pipe:
            self.input_pipe.get(session_id)
        return self.fetch(session_id)
