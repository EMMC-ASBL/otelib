"""Client for python backend."""
from typing import TYPE_CHECKING

from oteapi.plugins import load_strategies

from otelib.backends.client import AbstractBaseClient
from otelib.exceptions import PythonBackendException

if TYPE_CHECKING:  # pragma: no cover
    from typing import Any, Dict, Type

    from otelib.backends.python.base import BasePythonStrategy

CACHE: "Dict[str, Any]" = {}


# pylint: disable=duplicate-code
class OTEPythonClient(AbstractBaseClient):
    """The Python version of the OTEClient object.

    Attributes:
        interpreter (str): Interpreter for the python backend.

    """

    _backend = "python"

    def __init__(self, source: str, **config) -> None:
        """Initiates an OTEAPI Python client."""
        super().__init__(source, **config)

        self._cache = CACHE

        load_strategies()

    @property
    def interpreter(self) -> str:
        """Proxy for the source attribute."""
        return self.source

    def _validate_source(self, source: str) -> None:
        if source != "python":
            raise NotImplementedError(
                f"{source!r} is not a valid Python backend interpreter source. "
                "Only the 'python' interpreter is supported for the Python backend."
            )
        super()._validate_source(source)

    def _create_strategy(  # type: ignore[override]
        self, strategy_cls: "Type[BasePythonStrategy]", **config
    ) -> "BasePythonStrategy":
        strategy = strategy_cls(self.interpreter, self._cache)
        strategy.create(**config)
        return strategy

    def clear_cache(self) -> None:
        """Clear the global CACHE object."""
        global CACHE  # pylint: disable=global-statement
        CACHE = {}
        if self._cache != CACHE and (self._cache or CACHE):
            raise PythonBackendException("Could not clear the global CACHE object.")
