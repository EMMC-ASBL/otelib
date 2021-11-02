import requests
import json
from models import *
from apierror import *
from abstractfilter import *

class DataResource(AbstractFilter):
    """ Context class for the datasource Strategy Interfaces for managing i/o operations """
    
    def __init__(self, url):
        self.url = url
        
    def create(self, **kwargs):
        """ Create a data resource """
        data=ResourceConfig(**kwargs)
        response = requests.post(f'{self.url}/datasource/', data=json.dumps(data.dict()))
        if response.status_code !=200:
            raise ApiError(f'Cannot create dataresouce: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('resource_id')
        
    def fetch(self,sessionid):
        """ Fetch a specific data resource with its ID """
        response = requests.get(f'{self.url}/datasource/{self.id}?session_id={sessionid}')
        return response.content

    def initialize(self,sessionid):
        """ Initialize a specific data resource with its ID """
        response = requests.post(f'{self.url}/datasource/{self.id}/initialize?session_id={sessionid}')
        return response.content
    