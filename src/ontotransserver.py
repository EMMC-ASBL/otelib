from models import *
from dataresource import *
from transformation import *
from filter import *
from mapping import *
   
    
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
 