"""Common strategy for Download, Prase and Resource strategies."""
from typing import TYPE_CHECKING

import requests
from oteapi.models import ResourceConfig

from otelib.backends.services.base import BaseServicesStrategy
from otelib.exceptions import ApiError

if TYPE_CHECKING:  # pragma: no cover
    from typing import Optional


class DataResource(BaseServicesStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "dataresource"
    strategy_config = ResourceConfig

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = ResourceConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/dataresource",
            json=data.dict(),
            params={"session_id": session_id},
            timeout=self.settings.timeout,
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
            timeout=self.settings.timeout,
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
            timeout=self.settings.timeout,
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize data resource: session_id={session_id!r} "
            f"resource_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
