"""Client for services backend."""
from typing import TYPE_CHECKING

from otelib.backends.client import AbstractBaseClient

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any

    from otelib.backends.services.base import BaseServicesStrategy


class OTEServiceClient(AbstractBaseClient):
    """The Service version of the OTEClient object representing a remote OTE REST API.

    Attributes:
        url (str): The base URL of the OTEAPI Service.

    """

    _backend = "services"

    # config
    _headers: "dict[str, Any]" = {}

    @property
    def url(self) -> str:
        """Proxy for the source attribute."""
        return self.source

    def _create_strategy(  # type: ignore[override]
        self, strategy_cls: "type[BaseServicesStrategy]", **config
    ) -> "BaseServicesStrategy":
        strategy = strategy_cls(self.url)
        strategy.headers = self.headers
        strategy.create(**config)
        return strategy

    @property
    def headers(self) -> "dict[str, Any]":
        """URL headers to use for all requests to the OTEAPI Service."""
        value = self._headers
        if "Content-Type" not in value:
            value["Content-Type"] = "application/json"
        return value

    @headers.setter
    def headers(self, value: "dict[str, Any]") -> None:
        """Set the URL headers to use for all requests to the OTEAPI Service."""
        if not isinstance(value, dict):
            raise TypeError("headers must be a dictionary")
        self._headers = value

    def _set_config(self, config: "dict[str, Any]") -> None:
        self.headers = config.pop("headers", {})
        return super()._set_config(config)
