"""Common strategy for Download, Parse and Resource strategies."""

from typing import TYPE_CHECKING

from oteapi.models import ResourceConfig
from otelib.backends.python.base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from oteapi.models import GenericConfig


class DataResource(BasePythonStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "dataresource"
    strategy_config: "type[ResourceConfig]" = ResourceConfig

    def _sanity_checks(self, session_id: str, config: "GenericConfig") -> None:
        """Extend the base sanity checks with some config-specific checks."""
        super()._sanity_checks(session_id, config)

        if (not config.resourceType) or (
            not (
                (config.downloadUrl and config.mediaType)
                or (config.accessUrl and config.accessService)
            )
        ):
            raise ValueError(
                "Missing resourceType or downloadUrl/mediaType or accessUrl/accessService identifier"
            )
