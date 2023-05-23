"""Base API for backend client."""
import warnings
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from otelib.backends.factories import strategy_factory
from otelib.backends.utils import Backend, StrategyType
from otelib.warnings import IgnoringConfigOptions

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Type, Union

    from otelib.backends.strategies import AbstractBaseStrategy


class AbstractBaseClient(ABC):
    """The abstract base class defining the API for a backend client."""

    _backend: "Union[Backend, str]"

    def __init__(self, source: str, **config) -> None:
        """Initiates a client."""
        if not source:
            raise ValueError("source must be provided.")

        self._source = ""
        self._backend = Backend(self._backend)

        self._validate_source(source)
        self._set_config(config)

    @property
    def source(self) -> str:
        """The backend/source the client is using.

        This may be an OTE Services base URL or a Python interpreter.
        """
        return self._source

    def _validate_source(self, source: str) -> None:
        """Validate the `source` initialization variable.

        This method should be overridden in the given implementation, and finally,
        _this_ parent method must be called to set the `source` attribute.
        """
        if self.source:
            raise RuntimeError(
                "'source' should not be set prior to calling '_validate_source()'."
            )
        self._source = source

    def _set_config(self, config: "Dict[str, Any]") -> None:
        """Set the custom client configuration options."""
        if config:
            warnings.warn(
                f"The given configuration option(s) for {tuple(config)} is/are "
                "ignored.",
                IgnoringConfigOptions,
            )

    @abstractmethod
    def _create_strategy(
        self, strategy_cls: "Type[AbstractBaseStrategy]", **config
    ) -> "AbstractBaseStrategy":
        """Create a strategy.

        This method should not be run by a user, hence it is "private".
        The method is used with the `create_strategy()` method and allows a backend to
        customize its strategy creation method.

        Returns:
            The newly created strategy.

        """

    def create_strategy(
        self, strategy_type: "Union[str, StrategyType]", **config
    ) -> "AbstractBaseStrategy":
        """Create a strategy."""
        strategy_cls = strategy_factory(self._backend, strategy_type)
        return self._create_strategy(strategy_cls, **config)
