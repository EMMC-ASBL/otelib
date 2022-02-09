"""OTE Client."""
from otelib.dataresource import DataResource
from otelib.filter import Filter
from otelib.mapping import Mapping
from otelib.transformation import Transformation


class OTEClient:
    """The OTEClient object representing a remote OTE REST API."""

    def __init__(self, url):
        self.url = url

    def create_dataresource(self, **kwargs):
        """Create a new datasource."""
        data_resource = DataResource(self.url)
        data_resource.create(**kwargs)
        return data_resource

    def create_transformation(self, **kwargs):
        """Create new tranformation."""
        transformation = Transformation(self.url)
        transformation.create(**kwargs)
        return transformation

    def create_filter(self, **kwargs):
        """Create new filter."""
        # pylint: disable=redefined-builtin
        filter = Filter(self.url)
        filter.create(**kwargs)
        return filter

    def create_mapping(self, **kwargs):
        """Create new mapping."""
        mapping = Mapping(self.url)
        mapping.create(**kwargs)
        return mapping
