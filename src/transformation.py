import requests
import json
from models import *
from abstractfilter import *


class Transformation(AbstractFilter):
    """ Context class for the Transformation Strategy Interfaces """
    
    def __init__(self, url):
        self.url = url

    def create(self, **kwargs):
        """ Create a Transformation """
        data=TransformationConfig( **kwargs)
        response = requests.post(f'{self.url}/transformation', data=json.dumps(data.dict()))
        if response.status_code !=200:
            raise ApiError(f'Cannot create transformation: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('transformation_id')        
        
    def fetch(self,sessionid):
        """ Fetch a specific Transformation with its ID"""        
        response = requests.get(f'{self.url}/transformation/{self.id}?session_id={sessionid}')
        return response.content      
    
    def initialize(self,sessionid):
        """ Initialize a specific Transformation with its ID"""        
        response = requests.post(f'{self.url}/transformation/{self.id}/initialize?session_id={sessionid}')
        return response.content     