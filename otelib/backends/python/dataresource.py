"""Common strategy for Download, Parse and Resource strategies."""
import json
from copy import deepcopy

from oteapi.models import ResourceConfig
from oteapi.plugins import create_strategy

from otelib.backends.python.base import BasePythonStrategy


class DataResource(BasePythonStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "dataresource"
    strategy_config: "type[ResourceConfig]" = ResourceConfig

    def fetch(self, session_id: str) -> bytes:
        self._sanity_checks(session_id)

        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))

        if config.downloadUrl and config.mediaType:
            # Download strategy
            session_update = create_strategy("download", config).get(
                session=deepcopy(self.cache[session_id])
            )
            self.cache[session_id].update(session_update)

            # Parse strategy
            session_update = create_strategy("parse", config).get(
                session=deepcopy(self.cache[session_id])
            )
            self.cache[session_id].update(session_update)

        elif config.accessUrl and config.accessService:
            # Resource strategy
            session_update = create_strategy("resource", config).get(
                session=deepcopy(self.cache[session_id])
            )
            self.cache[session_id].update(session_update)

        return session_update.model_dump_json().encode(encoding="utf-8")

    def initialize(self, session_id: str) -> bytes:
        self._sanity_checks(session_id)

        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))

        if config.downloadUrl and config.mediaType:
            # Download strategy
            session_update = create_strategy("download", config).initialize(
                session=deepcopy(self.cache[session_id])
            )
            self.cache[session_id].update(session_update)

            # Parse strategy
            session_update = create_strategy("parse", config).initialize(
                session=deepcopy(self.cache[session_id])
            )
            self.cache[session_id].update(session_update)

        elif config.accessUrl and config.accessService:
            # Resource strategy
            session_update = create_strategy("resource", config).initialize(
                session=deepcopy(self.cache[session_id])
            )
            self.cache[session_id].update(session_update)

        return session_update.model_dump_json().encode(encoding="utf-8")
