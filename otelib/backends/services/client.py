"""Client for services backend."""
from typing import TYPE_CHECKING

from otelib.backends.services import (
    DataResource,
    Filter,
    Function,
    Mapping,
    Transformation,
)

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Optional

# pylint: disable=duplicate-code
class OTEServiceClient:
    """The Service version of the OTEClient object representing a remote OTE REST API.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.

    """

    def __init__(self, url: str, headers: "Optional[Dict[str, Any]]" = None) -> None:
        """Initiates an OTEAPI Service client.

        The `url` is the base URL of the OTEAPI Service.
        """
        self.url: str = url
        self.headers: "Optional[Dict[str, Any]]" = headers

    def create_dataresource(self, **kwargs) -> DataResource:
        """Create a new data resource.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created data resource.

        """
        data_resource = DataResource(self.url, self.headers)
        data_resource.create(**kwargs)
        return data_resource

    def create_transformation(self, **kwargs) -> Transformation:
        """Create a new transformation.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created transformation.

        """
        transformation = Transformation(self.url, self.headers)
        transformation.create(**kwargs)
        return transformation

    def create_filter(self, **kwargs) -> Filter:
        """Create a new filter.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created filter.

        """
        filter_ = Filter(self.url)
        filter_.create(**kwargs)
        return filter_

    def create_mapping(self, **kwargs) -> Mapping:
        """Create a new mapping.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created mapping.

        """
        mapping = Mapping(self.url, self.headers)
        mapping.create(**kwargs)
        return mapping

    def create_function(self, **kwargs) -> Function:
        """Create a new function.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created function.

        """
        function_ = Function(self.url, self.headers)
        function_.create(**kwargs)
        return function_
