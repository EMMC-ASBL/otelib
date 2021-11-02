import requests
import json
from models import *
from apierror import *
from abstractfilter import *


class Filter(AbstractFilter):
    """ Context class for the Filter Strategy Interfaces """
    
    def __init__(self, url):
        self.url = url
    
    def create(self,**kwargs):
        data= FilterConfig(**kwargs)
        response = requests.post(f'{self.url}/filter', data=json.dumps(data.dict()))
        if response.status_code !=200:
            raise ApiError(f'Cannot create filter: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('filter_id')
        
    def fetch(self,sessionid):
        """ Fetch a specific Filter with its ID"""
        response = requests.get(f'{self.url}/filter/{self.id}?session_id={sessionid}')
        return response.content       
    
    def initialize(self,sessionid):
        """ Initialize a specific Filter with its ID"""
        response = requests.post(f'{self.url}/filter/{self.id}/initialize?session_id={sessionid}')
        return response.content
