from abc import ABC, abstractmethod
import requests
import json
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional
from models import *


class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return f"APIError: status={self.status}"
    

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
        
class Pipe(object):
    """ Pipe object in a pipe-and-filter pattern """
    def __init__(self, i):
        self.input = i
        
    def get(self, sessionid):        
        return self.input.get(sessionid)
              
            
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
    
class OntoTransServer(object):
    """ The OntoTransServer object represent a remote OntoTrans REST API on the network. """
    
    def __init__(self, url):
        self.url = url
    
    def create_dataresource(self, **kwargs):
        """ Create a new datasource """
        dr = DataResource(self.url)
        dr.create(**kwargs)
        return dr
        pass    
    
    def create_transformation(self, **kwargs):
        """ create new tranformation """
        tr = Transformation(self.url)
        tr.create(**kwargs)
        return tr

    def create_filter(self, **kwargs):
        """ create new filter """
        ft= Filter(self.url)
        ft.create(**kwargs)
        return ft
    
    def create_mapping(self, **kwargs):
        """ create new mapping """
        mp= Mapping(self.url)
        mp.create(**kwargs)
        return mp
 