from otelib.dataresource import DataResource
from otelib.transformation import Transformation
from otelib.filter import Filter
from otelib.mapping import Mapping


class OntoTransServer:
    """The OntoTransServer object represent a remote OntoTrans REST API on the network."""

    def __init__(self, url):
        self.url = url

    def create_dataresource(self, **kwargs):
        """Create a new datasource."""
        dr = DataResource(self.url)
        dr.create(**kwargs)
        return dr

    def create_transformation(self, **kwargs):
        """Create new tranformation."""
        tr = Transformation(self.url)
        tr.create(**kwargs)
        return tr

    def create_filter(self, **kwargs):
        """Create new filter."""
        ft = Filter(self.url)
        ft.create(**kwargs)
        return ft

    def create_mapping(self, **kwargs):
        """Create new mapping."""
        mp = Mapping(self.url)
        mp.create(**kwargs)
        return mp
