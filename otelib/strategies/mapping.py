"""Mapping strategy."""
import requests
from oteapi.models import MappingConfig

from otelib.exceptions import ApiError
from otelib.strategies.abc import AbstractStrategy


class Mapping(AbstractStrategy):
    """Context class for the Mapping Strategy Interfaces"""

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = MappingConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/mapping",
            json=data.dict(),
            params={"session_id": session_id},
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create mapping: {data.mappingType!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id = response_json.pop("mapping_id")

    def fetch(self, session_id: str) -> bytes:
        response = requests.get(
            f"{self.url}{self.settings.prefix}/mapping/{self.id}",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch mapping: session_id={session_id!r} "
            f"mapping_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        response = requests.post(
            f"{self.url}{self.settings.prefix}/mapping/{self.id}/initialize",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize mapping: session_id={session_id!r} "
            f"mapping_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
