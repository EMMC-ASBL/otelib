"""Common strategy for Download, Parse and Resource strategies."""

import json

from oteapi.models import ResourceConfig
from oteapi.utils.config_updater import populate_config_from_session
from oteapi.plugins import create_strategy
from otelib.backends.python.base import BasePythonStrategy


class DataResource(BasePythonStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "dataresource"
    strategy_config: "type[ResourceConfig]" = ResourceConfig

    def fetch(self, session_id: str) -> bytes:
        self._sanity_checks(session_id)
        session_data = self._fetch_session_data(session_id)
        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))
        populate_config_from_session(session_data, config)

        if config.resourceType and (
            (
                (config.downloadUrl and config.mediaType)
                or (config.accessUrl and config.accessService)
            )
        ):
            raise ValueError(
                "Missing resourceType or downloadUrl/mediaType or accessUrl/accessService identifier"
            )
        session_update = create_strategy("resource", config).get()
        self.cache[session_id].update(session_update)

        return session_update.model_dump_json().encode(encoding="utf-8")

    def initialize(self, session_id: str) -> bytes:
        self._sanity_checks(session_id)
        session_data = self._fetch_session_data(session_id)
        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))
        populate_config_from_session(session_data, config)

        if config.resourceType and (
            (
                (config.downloadUrl and config.mediaType)
                or (config.accessUrl and config.accessService)
            )
        ):
            raise ValueError(
                "Missing resourceType or downloadUrl/mediaType or accessUrl/accessService identifier"
            )
        session_update = create_strategy("resource", config).initialize()
        self.cache[session_id].update(session_update)

        return session_update.model_dump_json().encode(encoding="utf-8")
