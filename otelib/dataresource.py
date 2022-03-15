"""Common strategy for Download, Prase and Resource strategies."""
import requests
from oteapi.models import ResourceConfig

from otelib.abc import AbstractStrategy
from otelib.exceptions import ApiError


class DataResource(AbstractStrategy):
    """Context class for the datasource strategy interfaces for managing i/o
    operations."""

    def create(self, **kwargs):
        """Create a data resource"""
        data = ResourceConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/dataresource/",
            json=data.dict(),
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create dataresouce: downloadUrl={data.downloadUrl} "
                f"accessService={data.accessService} mediaType={data.mediaType}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id_ = response_json.pop("resource_id")

    def fetch(self, session_id):
        """Fetch a specific data resource with its ID"""
        response = requests.get(
            f"{self.url}{self.settings.prefix}/dataresource/{self.id_}"
            f"?session_id={session_id}"
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch dataresource: session_id={session_id!r} "
            f"resource_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id):
        """Initialize a specific data resource with its ID"""
        response = requests.post(
            f"{self.url}{self.settings.prefix}/dataresource/{self.id_}/"
            f"initialize?session_id={session_id}"
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize dataresource: session_id={session_id!r} "
            f"resource_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
