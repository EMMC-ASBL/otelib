"""Client for services backend."""
from typing import TYPE_CHECKING

from otelib.backends.client import AbstractBaseClient

if TYPE_CHECKING:  # pragma: no cover
    from typing import Type

    from otelib.backends.services.base import BaseServicesStrategy


# pylint: disable=duplicate-code
class OTEServiceClient(AbstractBaseClient):
    """The Service version of the OTEClient object representing a remote OTE REST API.

    Attributes:
        url (str): The base URL of the OTEAPI Service.

    """

    _backend = "services"

    @property
    def url(self) -> str:
        """Proxy for the source attribute."""
        return self.source

    def _create_strategy(  # type: ignore[override]
        self, strategy_cls: "Type[BaseServicesStrategy]", **config
    ) -> "BaseServicesStrategy":
        strategy = strategy_cls(self.url)
        strategy.create(**config)
        return strategy
