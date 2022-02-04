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
        if response.status_code != 200:
            raise ApiError(
                f"Cannot create dataresouce: downloadUrl={data.downloadUrl} "
                f"accessService={data.accessService} mediaType={data.mediaType} "
                f"({response.status_code})"
            )

        response_json: dict = response.json()
        self.id_ = response_json.pop("resource_id")

    def fetch(self, session_id):
        """Fetch a specific data resource with its ID"""
        response = requests.get(
            f"{self.url}{self.settings.prefix}/dataresource/{self.id_}"
            f"?session_id={session_id}"
        )
        return response.content

    def initialize(self, session_id):
        """Initialize a specific data resource with its ID"""
        response = requests.post(
            f"{self.url}{self.settings.prefix}/dataresource/{self.id_}/"
            f"initialize?session_id={session_id}"
        )
        return response.content
