"""OTE Client."""
from importlib import import_module
from typing import TYPE_CHECKING

from otelib.exceptions import AuthorizationError
from otelib.settings import Settings
from otelib.strategies import DataResource, Filter, Function, Mapping, Transformation

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Callable, Dict, Optional, Union

settings = Settings()


class OTEClient:
    """The OTEClient object representing a remote OTE REST API.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.

    """

    def __init__(
        self, url: str = None, auth_function=None, headers: dict = None
    ) -> None:
        """Initiates an OTEAPI Service client.

        The `url` is the base URL of the OTEAPI Service.
        """

        self.url: str = url or settings.default_host
        self.headers: "Optional[Dict[Any, Any]]" = headers
        self._auth = auth_function

    def _auth_func_from_settings(self) -> "Union[Callable, None]":
        if settings.auth_function:
            module, _, funcname = settings.auth_function.replace(" ", str()).rpartition(
                "."
            )
            try:
                func = getattr(import_module(module), funcname)
            except Exception as error:
                raise error
        else:
            func = None
        return func

    def login(self, *args, **kwargs):
        """call the function for fetching an access token
        and add it to the header of each http-request for the
        client."""
        func = self._auth_func_from_settings() or self._auth
        if not func:
            raise AuthorizationError("function for authorization not defined")
        self.headers = func(*args, **kwargs)

    def create_dataresource(self, **kwargs) -> DataResource:
        """Create a new data resource.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created data resource.

        """
        data_resource = DataResource(self.url, headers=self.headers)
        data_resource.create(**kwargs)
        return data_resource

    def create_transformation(self, **kwargs) -> Transformation:
        """Create a new transformation.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created transformation.

        """
        transformation = Transformation(self.url, headers=self.headers)
        transformation.create(**kwargs)
        return transformation

    def create_filter(self, **kwargs) -> Filter:
        """Create a new filter.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created filter.

        """
        filter_ = Filter(self.url, headers=self.headers)
        filter_.create(**kwargs)
        return filter_

    def create_mapping(self, **kwargs) -> Mapping:
        """Create a new mapping.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created mapping.

        """
        mapping = Mapping(self.url, headers=self.headers)
        mapping.create(**kwargs)
        return mapping

    def create_function(self, **kwargs) -> Function:
        """Create a new function.

        Any given keyword arguments are passed on to the `create()` method.

        Returns:
            The newly created function.

        """
        function_ = Function(self.url, headers=self.headers)
        function_.create(**kwargs)
        return function_
