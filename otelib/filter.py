import json
import requests

from oteapi.models import FilterConfig

from otelib.apierror import ApiError
from otelib.abstractfilter import AbstractFilter


class Filter(AbstractFilter):
    """ Context class for the Filter Strategy Interfaces """

    def create(self, **kwargs):
        data = FilterConfig(**kwargs)
        response = requests.post(
            f'{self.url}{self.settings.prefix}/filter',
            data=json.dumps(data.dict())
        )
        if response.status_code != 200:
            raise ApiError(f'Cannot create filter: {response.status_code}')
        self.data = json.loads(response.text)
        self.id = self.data.pop('filter_id')

    def fetch(self, session_id):
        """ Fetch a specific Filter with its ID"""
        response = requests.get(
            f'{self.url}{self.settings.prefix}/filter/{self.id}?'
            f'session_id={session_id}'
        )
        return response.content

    def initialize(self, session_id):
        """ Initialize a specific Filter with its ID"""
        response = requests.post(
            f'{self.url}{self.settings.prefix}/filter/{self.id}/initialize?'
            f'session_id={session_id}'
        )
        return response.content
