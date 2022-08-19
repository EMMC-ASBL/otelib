"""Common strategy for Download, Parse and Resource strategies."""
from .base import BasePythonStrategy 


import json
from oteapi.models import ResourceConfig, AttrDict
from uuid import uuid4

from otelib.exceptions import ApiError
from otelib.strategies.abc import AbstractStrategy

from oteapi.plugins import create_strategy



class DataResource(BasePythonStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = ResourceConfig(**kwargs)

        resource_id = 'dataresource-'+str(uuid4())
        self.id = resource_id
        self.cache[resource_id] = data.json()

        if session_id:
            session = self.cache[session_id]
            list_key = "resource_info"
            if list_key in session:
                session[list_key].extend([resource_id])
            else:
                session[list_key] = [resource_id]

        return 

    def fetch(self, session_id: str) -> bytes:
        resource_id = self.id

        config = ResourceConfig(**json.loads(self.cache[resource_id]))
        session_data = self.cache[session_id]

        if config.downloadUrl and config.mediaType:
            # Download strategy
            session_update = create_strategy("download", config).get(session=session_data)
            if session_update and session_id:
                self.cache[session_id].update(session_update)

            # Parse strategy
            session_update = create_strategy("parse", config).get(session=session_data)
            if session_update and session_id:
                self.cache[session_id].update(session_update)

        elif config.accessUrl and config.accessService:
            # Resource strategy
            session_update = create_strategy("resource", config).get(session=session_data)
            if session_update and session_id:
                self.cache[session_id].update(session_update)
        
        return AttrDict(**session_update)

    def initialize(self, session_id: str) -> bytes:
        resource_id = self.id

        config = ResourceConfig(**json.loads(self.cache[resource_id]))
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
