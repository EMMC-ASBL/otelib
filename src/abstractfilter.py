from abc import ABC, abstractmethod
import requests
import json
from models import *
from pipe import *
from apierror import *

class AbstractFilter(ABC):
    """AbstractFilter class for (Filters, Dataresource, mappers, transformations)"""

    @abstractmethod
    def __init__(self, url):
        pass
    
    @abstractmethod
    def create(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def fetch(self,resource_id):
        pass
    
    @abstractmethod
    def initialize(self,resource_id):
        pass
    

    def _set_input(self, input_pipe):
        self.input_pipe=input_pipe
    

    def __rshift__(self, other):
        p = Pipe(self)
        other._set_input(p)
        return other
       

    def get(self, sessionid=None): 
        if sessionid==None:
            response = requests.post(f'{self.url}/session/', data='{}')
            if response.status_code !=200:
                raise ApiError(f'Cannot create session: {response.status_code}')
            sessionid = json.loads(response.text)['session_id']
            print(sessionid)
        if hasattr(self, 'input_pipe'):
            self.initialize(sessionid)  
            self.input_pipe.get(sessionid)  
            return self.fetch(sessionid)
        else:
            self.initialize(sessionid) 
            return self.fetch(sessionid)