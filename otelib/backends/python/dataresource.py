"""Common strategy for Download, Parse and Resource strategies."""
import json
from typing import TYPE_CHECKING

from oteapi.models import AttrDict, ResourceConfig
from oteapi.plugins import create_strategy

from otelib.backends.python.base import BasePythonStrategy

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class DataResource(BasePythonStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "dataresource"
    strategy_config = ResourceConfig

    def fetch(self, session_id: str) -> bytes:
        resource_id = self.id

        config = self.strategy_config(**json.loads(self.cache[resource_id]))
        session_data = None if not session_id else self.cache[session_id]

        if config.downloadUrl and config.mediaType:
            # Download strategy
            session_update = create_strategy("download", config).get(
                session=session_data
            )
            if session_update and session_id:
                self.cache[session_id].update(session_update)

            # Parse strategy
            session_update = create_strategy("parse", config).get(session=session_data)
            if session_update and session_id:
                self.cache[session_id].update(session_update)

        elif config.accessUrl and config.accessService:
            # Resource strategy
            session_update = create_strategy("resource", config).get(
                session=session_data
            )
            if session_update and session_id:
                self.cache[session_id].update(session_update)

        return bytes(AttrDict(**session_update).json(), encoding="utf-8")

    def initialize(self, session_id: str) -> bytes:
        resource_id = self.id

        config = self.strategy_config(**json.loads(self.cache[resource_id]))
        if session_id:
            session_data = self.cache[session_id]
        else:
            session_data = None

        if config.downloadUrl and config.mediaType:
            # Download strategy
            session_update = create_strategy("download", config).initialize(
                session=session_data
            )
            if session_update and session_id:
                self.cache[session_id].update(session_update)

            # Parse strategy
            session_update = create_strategy("parse", config).initialize(
                session=session_data
            )
            if session_update and session_id:
                self.cache[session_id].update(session_update)

        elif config.accessUrl and config.accessService:
            # Resource strategy
            session_update = create_strategy("resource", config).initialize(
                session=session_data
            )
            if session_update and session_id:
                self.cache[session_id].update(session_update)

        return bytes(AttrDict(**session_update).json(), encoding="utf-8")
