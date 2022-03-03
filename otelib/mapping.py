"""Mapping strategy."""
import requests
from oteapi.models import MappingConfig

from otelib.abc import AbstractStrategy
from otelib.exceptions import ApiError


class Mapping(AbstractStrategy):
    """Context class for the Mapping Strategy Interfaces"""

    def create(self, **kwargs):
        """Create a Mapping."""
        data = MappingConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/mapping", json=data.dict()
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create filter: {data.mappingType!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id_ = response_json.pop("mapping_id")

    def fetch(self, session_id):
        """Fetch a specific Mapping with its ID."""
        response = requests.get(
            f"{self.url}{self.settings.prefix}/mapping/{self.id_}?"
            f"session_id={session_id}"
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch mapping: session_id={session_id!r} "
            f"mapping_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id):
        """Initialize a specific Mapping with its ID."""
        response = requests.post(
            f"{self.url}{self.settings.prefix}/mapping/{self.id_}/initialize?"
            f"session_id={session_id}"
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize mapping: session_id={session_id!r} "
            f"mapping_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
