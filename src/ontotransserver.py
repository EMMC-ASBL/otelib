from abc import ABC, abstractmethod
import requests
import json
from dataclasses import dataclass
from pydantic import BaseModel
from typing import Optional


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
    def readurl(self): # returns the fetch url!
        pass
    
    @abstractmethod
    def create(self, *args, **kwargs):
        pass
    
    @abstractmethod
    def fetch(self,resource_id):
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
            self.sessionid = json.loads(response.text)['session_id']
        else:
            self.sessionid = sessionid
            
        if self.data:
            response = requests.put(f'{self.url}/session/{self.sessionid}',data=json.dumps(self.data))
            if response.status_code !=200:
                raise ApiError(f'Cannot update session: {response.status_code}')  
                
        if hasattr(self, 'input_pipe'):
            return self.input_pipe.get(sessionid)
        else:
            return 'Data' # return the readurl or whatever fetches the required data!!        
        
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
        
    def create(self,uri, mediatype):
        """ Create a data resource """
        data = json.dumps({"downloadUrl":uri, "mediaType":mediatype,  "accessUrl":uri,  "license": "string",  "accessRights": "string",  "description": "string", "published":"string",  "configuration": {}})
        response = requests.post(f'{self.url}/datasource/',data = data)
        if response.status_code !=200:
            raise ApiError(f'Cannot create dataresouce: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('resource_id')
        
    def fetch(self,resource_id):
        """ Fetch a specific data resource with its ID """
        self.id=resource_id
    
    def read(self):
        """ Read the data in a specific data resource """
        response = requests.get(f'{self.url}/datasource/{self.id}/read')
        if response.status_code !=200:
            raise ApiError(f'Cannot read data from  datasource {self.id}: {response.status_code}')
        return response.text
    
    def info(self):
        """ Get the schema for a datasource """
        response = requests.get(f'{self.url}/datasource/{self.id}/info')
        if response.status_code !=200:
            raise ApiError(f'Cannot read schema from dataresouce {self.id}: {response.status_code}')
        return response.text
    
    def readurl(self):
        source_url = self.url+'/datasource/'+ self.id +'/read'
        return source_url
    
    
 
class Transformation(AbstractFilter):
    """ Context class for the Transformation Strategy Interfaces """
    
    def __init__(self, url):
        self.url = url
    
    def create(self, transformation_type, name, description, due, priority, secret, configuration):
        """ Create a Transformation """
        data = json.dumps({  "transformation_type":transformation_type,  "name":name,  "description":description,  "due": "2021-10-12T10:52:33.349Z",  "priority":priority,  "secret":secret,  "configuration":configuration})
        response = requests.post(f'{self.url}/transformation', data=data)
        if response.status_code !=200:
            raise ApiError(f'Cannot create transformation: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('transformation_id')
        
        
    def fetch(self,resource_id):
        """ Fetch a specific Transformation with its ID"""
        self.id=resource_id        

    def execute(self):
        response = requests.post(f'{self.url}/transformation/{self.id}/run')
        if response.status_code !=200:
            raise ApiError(f'Cannot run transformation: {response.status_code}')
        return response.text
    
    def readurl(self):
        transformation_url = f'{self.url}/transformation/{self.id}'
        return transformation_url
    
class Filter(AbstractFilter):
    """ Context class for the Filter Strategy Interfaces """
    
    def __init__(self, url):
        self.url = url
    
    def create(self, filterType, query, condition, limit, configuration):
        """ Create a Filter """
        data = json.dumps({"filterType":filterType,  "query":query,  "condition":condition,  "limit":limit,  "configuration":configuration})
        response = requests.post(f'{self.url}/filter', data=data)
        if response.status_code !=200:
            raise ApiError(f'Cannot create filter: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('filter_id')
        
    def fetch(self,filter_id):
        """ Fetch a specific Filter with its ID"""
        self.id=filter_id        

    def readurl(self):
        filter_url = f'{self.url}/filter/{self.id}'
        return filter_url

class Mapping(AbstractFilter):
    """ Context class for the Mapping Strategy Interfaces """
    
    def __init__(self, url):
        self.url = url
    
    def create(self,  mappingType, prefixes, triples, configuration):
        """ Create a Mapping """
        data = json.dumps({"mappingType":mappingType,  "prefixes":prefixes,  "triples":triples,"configuration":configuration})
        response = requests.post(f'{self.url}/mapping', data=data)
        if response.status_code !=200:
            raise ApiError(f'Cannot create filter: {response.status_code}')
        self.data=json.loads(response.text)
        self.id = self.data.pop('mapping_id')
        
    def fetch(self,mapping_id):
        """ Fetch a specific Mapping with its ID"""
        self.id=mapping_id        

    def readurl(self):
        mapping_url = f'{self.url}/mapping/{self.id}'
        return mapping_url
    
class OntoTransServer(object):
    """ The OntoTransServer object represent a remote OntoTrans REST API on the network. """
    
    def __init__(self, url):
        self.url = url
        
    def say_hello(self):
        """ Say hello """
        return "hello !!!"
    
    def create_dataresource(self, uri, mediatype):
        """ Create a new datasource """
        dr = DataResource(self.url)
        dr.create(uri, mediatype)
        return dr
        pass    
    
    def create_transformation(self, transformation_type, name, description, due, priority, secret, configuration):
        """ create new tranformation """
        tr = Transformation(self.url)
        tr.create(transformation_type, name, description, due, priority, secret, configuration)
        return tr

    def create_filter(self, filterType, query, condition, limit, configuration):
        """ create new filter """
        ft= Filter(self.url)
        ft.create(filterType, query, condition, limit, configuration)
        return ft
    
    def create_mapping(self, mappingType, prefixes, triples, configuration):
        """ create new mapping """
        mp= Mapping(self.url)
        mp.create(mappingType, prefixes, triples, configuration)
        return mp
 