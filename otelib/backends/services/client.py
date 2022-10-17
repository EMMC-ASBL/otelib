"""Client for services backend."""
from typing import TYPE_CHECKING

from requests.auth import HTTPBasicAuth

from otelib.backends.services import (
    DataResource,
    Filter,
    Function,
    Mapping,
    Transformation,
)

if TYPE_CHECKING:
    from typing import Optional, Tuple, Union


# pylint: disable=duplicate-code
class OTEServiceClient:
    """The Service version of the OTEClient object representing a remote OTE REST API.

    Parameters:
        url (str): The base URL of the OTEAPI Service.
        auth (Optional[Union[str, Tuple[str, str]]]): A

    Attributes:
        url (str): The base URL of the OTEAPI Service.

    """

    def __init__(
        self, url: str, auth: "Optional[Union[str, Tuple[str, str]]]" = None
    ) -> None:
        """Initiates an OTEAPI Service client.

        The `url` is the base URL of the OTEAPI Service.
        """
        self.url: str = url
        self.auth: "Optional[HTTPBasicAuth]" = self._set_auth(auth) if auth else None

    def _set_auth(self, auth: "Union[str, Tuple[str, str]]") -> HTTPBasicAuth:
        """Set authentication settings.

        If only a string is supplied for `auth`, it is expected that a token is
        supplied.

        Parameters:
            auth: User-supplied authentication information.

        Returns:
            Basic HTTP authentication settings.

        Raises:
            TypeError: If auth is neither a string or tuple of length 2.

        """
        if isinstance(auth, str):
            return HTTPBasicAuth(username="__token__", password=auth)
        if isinstance(auth, tuple) and len(auth) == 2:
            return HTTPBasicAuth(*auth)
        raise TypeError("auth must be either a string or a tuple of length 2.")

    def create_dataresource(self, **kwargs) -> DataResource:
        """Create a new data resource.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created data resource.

        """
        data_resource = DataResource(self.url, self.auth)
        data_resource.create(**kwargs)
        return data_resource

    def create_transformation(self, **kwargs) -> Transformation:
        """Create a new transformation.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created transformation.

        """
        transformation = Transformation(self.url, self.auth)
        transformation.create(**kwargs)
        return transformation

    def create_filter(self, **kwargs) -> Filter:
        """Create a new filter.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created filter.

        """
        filter_ = Filter(self.url, self.auth)
        filter_.create(**kwargs)
        return filter_

    def create_mapping(self, **kwargs) -> Mapping:
        """Create a new mapping.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created mapping.

        """
        mapping = Mapping(self.url, self.auth)
        mapping.create(**kwargs)
        return mapping

    def create_function(self, **kwargs) -> Function:
        """Create a new function.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created function.

        """
        function_ = Function(self.url, self.auth)
        function_.create(**kwargs)
        return function_
