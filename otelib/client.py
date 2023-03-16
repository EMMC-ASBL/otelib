"""OTE Client."""
from typing import TYPE_CHECKING

from pydantic import AnyHttpUrl, ValidationError, parse_obj_as

from otelib.backends.factories import client_factory
from otelib.backends.utils import Backend, StrategyType

if TYPE_CHECKING:  # pragma: no cover
    from otelib.backends.strategies import AbstractBaseStrategy


class OTEClient:
    """The OTEClient object representing a remote OTE REST API.

    Parameters:
        url (str): The base URL of the OTEAPI Service.

    Attributes:
        url (str): The base URL of the OTEAPI Service.

    """

    def __init__(self, url: str, **config) -> None:
        """Initialize an OTE Client.

        Parameters:
            url: The base URL of the OTE Service (or Python interpreter for local
                OTEAPI Core usage).
            config: Custom client configuration properties.

        """
        try:
            parse_obj_as(AnyHttpUrl, url)
        except ValidationError:
            backend = Backend.PYTHON
        else:
            backend = Backend.SERVICES

        self._impl = client_factory(backend)(url, **config)

    @property
    def url(self) -> str:
        """The base URL of the OTE Service.

        This may also be the Python interpreter for local OTEAPI Core usage.
        """
        return self._impl.source

    def create_dataresource(self, **config) -> "AbstractBaseStrategy":
        """Create a new data resource.

        Any given keyword arguments are passed on to the `create_strategy()` method.

        Returns:
            The newly created data resource.

        """
        return self._impl.create_strategy(StrategyType.DATARESOURCE, **config)

    def create_filter(self, **config) -> "AbstractBaseStrategy":
        """Create a new filter.

        Any given keyword arguments are passed on to the `create_strategy()` method.

        Returns:
            The newly created filter.

        """
        return self._impl.create_strategy(StrategyType.FILTER, **config)

    def create_function(self, **config) -> "AbstractBaseStrategy":
        """Create a new function.

        Any given keyword arguments are passed on to the `create_strategy()` method.

        Returns:
            The newly created function.

        """
        return self._impl.create_strategy(StrategyType.FUNCTION, **config)

    def create_mapping(self, **config) -> "AbstractBaseStrategy":
        """Create a new mapping.

        Any given keyword arguments are passed on to the `create_strategy()` method.

        Returns:
            The newly created mapping.

        """
        return self._impl.create_strategy(StrategyType.MAPPING, **config)

    def create_transformation(self, **config) -> "AbstractBaseStrategy":
        """Create a new transformation.

        Any given keyword arguments are passed on to the `create_strategy()` method.

        Returns:
            The newly created transformation.

        """
        return self._impl.create_strategy(StrategyType.TRANSFORMATION, **config)
