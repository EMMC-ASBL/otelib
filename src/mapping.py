import requests
import json
from models import *
from apierror import *
from abstractfilter import *

class Mapping(AbstractFilter):
    """ Context class for the Mapping Strategy Interfaces """
    
    def __init__(self, url):
        self.url = url
    
    def create(self, **kwargs):
        """ Create a Mapping """
        data=MappingConfig(**kwargs)
        response = requests.post(f'{self.url}/mapping',data=json.dumps(data.dict()))
        if response.status_code !=200:
            raise ApiError(f'Cannot create filter: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('mapping_id')
        
    def fetch(self,sessionid):
        """ Fetch a specific Mapping with its ID"""
        response = requests.get(f'{self.url}/mapping/{self.id}?session_id={sessionid}')
        return response.content

    def initialize(self,sessionid):
        """ Initialize a specific Mapping with its ID"""
        response = requests.post(f'{self.url}/mapping/{self.id}/initialize?session_id={sessionid}')
        return response.content