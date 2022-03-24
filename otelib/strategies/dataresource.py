"""Common strategy for Download, Prase and Resource strategies."""
import requests
from oteapi.models import ResourceConfig

from otelib.exceptions import ApiError
from otelib.strategies.abc import AbstractStrategy


class DataResource(AbstractStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = ResourceConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/dataresource",
            json=data.dict(),
            params={"session_id": session_id},
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create data resouce: downloadUrl={data.downloadUrl} "
                f"accessService={data.accessService} mediaType={data.mediaType}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id = response_json.pop("resource_id")

    def fetch(self, session_id: str) -> bytes:
        response = requests.get(
            f"{self.url}{self.settings.prefix}/dataresource/{self.id}",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch data resource: session_id={session_id!r} "
            f"resource_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        response = requests.post(
            f"{self.url}{self.settings.prefix}/dataresource/{self.id}/initialize",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize data resource: session_id={session_id!r} "
            f"resource_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
