"""Transformation strategy."""
import requests
from oteapi.models import TransformationConfig

from otelib.abc import AbstractStrategy
from otelib.exceptions import ApiError


class Transformation(AbstractStrategy):
    """Context class for the Transformation Strategy Interfaces."""

    def create(self, **kwargs):
        """Create a Transformation."""
        data = TransformationConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/transformation",
            json=data.dict(),
        )
        if response.status_code != 200:
            raise ApiError(
                f"Cannot create transformation: {data.transformationType!r} "
                f"({response.status_code})"
            )

        response_json: dict = response.json()
        self.id_ = response_json.pop("transformation_id")

    def fetch(self, session_id):
        """Fetch a specific Transformation with its ID."""
        response = requests.get(
            f"{self.url}{self.settings.prefix}/transformation/{self.id_}?"
            f"session_id={session_id}"
        )
        return response.content

    def initialize(self, session_id):
        """Initialize a specific Transformation with its ID."""
        response = requests.post(
            f"{self.url}{self.settings.prefix}/transformation/{self.id_}/"
            f"initialize?session_id={session_id}"
        )
        return response.content
