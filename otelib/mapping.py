import json
import requests

from oteapi.models import MappingConfig

from otelib.apierror import ApiError
from otelib.abstractfilter import AbstractFilter


class Mapping(AbstractFilter):
    """Context class for the Mapping Strategy Interfaces"""

    def create(self, **kwargs):
        """Create a Mapping."""
        data = MappingConfig(**kwargs)
        response = requests.post(
            f'{self.url}{self.settings.prefix}/mapping',
            data=json.dumps(data.dict())
        )
        if response.status_code != 200:
            raise ApiError(f'Cannot create filter: {response.status_code}')
        self.data = json.loads(response.text)
        self.id = self.data.pop('mapping_id')

    def fetch(self, session_id):
        """Fetch a specific Mapping with its ID."""
        response = requests.get(
            f'{self.url}{self.settings.prefix}/mapping/{self.id}?'
            f'session_id={session_id}'
        )
        return response.content

    def initialize(self, session_id):
        """Initialize a specific Mapping with its ID."""
        response = requests.post(
            f'{self.url}{self.settings.prefix}/mapping/{self.id}/initialize?'
            f'session_id={session_id}'
        )
        return response.content
