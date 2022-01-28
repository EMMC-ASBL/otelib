import json
import requests

from oteapi.models import TransformationConfig

from otelib.apierror import ApiError
from otelib.abstractfilter import AbstractFilter


class Transformation(AbstractFilter):
    """Context class for the Transformation Strategy Interfaces."""

    def create(self, **kwargs):
        """Create a Transformation."""
        data = TransformationConfig(**kwargs)
        response = requests.post(
            f'{self.url}{self.settings.prefix}/transformation',
            data=json.dumps(data.dict())
        )
        if response.status_code != 200:
            raise ApiError(
                f'Cannot create transformation: {response.status_code}'
            )
        self.data = json.loads(response.text)
        self.id = self.data.pop('transformation_id')

    def fetch(self, session_id):
        """Fetch a specific Transformation with its ID."""
        response = requests.get(
            f'{self.url}{self.settings.prefix}/transformation/{self.id}?'
            f'session_id={session_id}'
        )
        return response.content

    def initialize(self, session_id):
        """Initialize a specific Transformation with its ID."""
        response = requests.post(
            f'{self.url}{self.settings.prefix}/transformation/{self.id}/'
            f'initialize?session_id={session_id}'
        )
        return response.content
