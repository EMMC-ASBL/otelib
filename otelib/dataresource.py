import json
import requests

from oteapi.models import ResourceConfig

from otelib.abstractfilter import AbstractFilter
from otelib.apierror import ApiError


class DataResource(AbstractFilter):
    """Context class for the datasource strategy interfaces for managing i/o operations."""

    def create(self, **kwargs):
        """ Create a data resource """
        data = ResourceConfig(**kwargs)
        response = requests.post(
            f'{self.url}{self.settings.prefix}/dataresource/',
            data=json.dumps(data.dict())
        )
        if response.status_code != 200:
            raise ApiError(
                f'Cannot create dataresouce: {response.status_code}'
            )
        self.data = json.loads(response.text)
        self.id = self.data.pop('resource_id')

    def fetch(self, session_id):
        """ Fetch a specific data resource with its ID """
        response = requests.get(
            f'{self.url}{self.settings.prefix}/dataresource/{self.id}'
            f'?session_id={session_id}'
        )
        return response.content

    def initialize(self, session_id):
        """ Initialize a specific data resource with its ID """
        response = requests.post(
            f'{self.url}{self.settings.prefix}/dataresource/{self.id}/'
            f'initialize?session_id={session_id}'
        )
        return response.content
