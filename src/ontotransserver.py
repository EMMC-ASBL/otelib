import requests

class ApiError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return f"APIError: status={self.status}"

    
class DataResource(object):
    """ Context class for the DataResource Strategy Interfaces for managing i/o operations """
    
    def __init__(self, url, dataresource_id):
        self.url = url
        self.dataresource_id = dataresource_id
        
    def read(self):
        print ("reading data")
        pass
        
    def write(self, blob):
        print ("writing data")
        pass
    
    def schema(self):
        pass
    
    def remove_data(self):
        pass
    
    
class Transformation(object):
    """ Context class for the Transformation Strategy Interfaces """
    def __init__(self, url, transformation_id):
        self.url = url
        self.transformation_id = transformation_id
    
    
class Mapping(object):
    """ Context class for the Mapping Strategy Interfaces """
    def __init__(self, url, mapping_id):
        self.url = url
        self.mapping_id = mapping_id


class Pipe(object):
    """ Pipe object in a pipe-and-filter pattern """
    def __init__(self, i):
        self.input = i
        
    def get(self):
        return self.input.get()
        

class Filter(object):
    """ Filter operation to be executed in a pipeline """
    def __init__(self, msg):
        self.input_pipe = []
        self.msg = msg
    
    def _set_input(self, input_pipe : Pipe):
        self.input_pipe.append(input_pipe)
    
    def __add__(self, other):        
        self.input_pipe.append(other)
        return other
    
    def __rshift__(self, other):
        p = Pipe(self)
        other._set_input(p)
        return other
        
    def get(self):        
        for i in self.input_pipe:
            i.get()
        print ("operation", self.msg, self.input_pipe)
        
            
class OntoTransServer(object):
    """ The OntoTransServer object represent a remote OntoTrans REST API on the network. """
    
    def __init__(self, url):
        self.url = url
        
    def say_hello(self):
        """ Say hello """
        response = requests.get(f'{self.url}/hello')
        if response.status_code != 200:
            raise ApiError(f'Cannot say hello: {response.status_code}')
        return response.text
        
    def list_dataresources(self):
        """ List existing dataresources """
        response = requests.get(f'{self.url}/dataresource')
        if response.status_code != 200:
            raise ApiError(f'Cannot list dataresources: {response.status_code}')
        return response.text
    
        pass
    
    def get_dataresource(self, resource_id):
        """ Fetch a specific dataresource """
        dr = DataResource(self.url, resource_id)
        return dr
    
    def add_dataresource(self, resource):
        """ Create a new dataresource """
        pass
    
        
    def list_transformations(self):
        """ display tranformations """
        pass    
    
    def add_transformation(self, t):
        """ create new tranformation """
        pass
    
    def get_transformation(self, transformation_id):
        """ Fetch a specific transformation """
        t = Transformation(self.url, transformation_id)
        return t
    
    def describe_transformation(self, transformation_id):
        """ describe transformation """
        pass
    
    def list_mappings(self):
        pass
    
    def add_mapping(self, m):
        pass
    
    def get_mapping(self, mapping_id):
        """ Returns a specific mapping """
        m = Mapping(self.url, mapping_id)
        return m
    
    def describe_mapping(self, mapping_id):
        pass
    
    def remove_mapping(self, mapping_id):
        pass
    
    
