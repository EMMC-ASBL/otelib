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
        if not response.ok:
            raise ApiError(
                f"Cannot create transformation: {data.transformationType!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id_ = response_json.pop("transformation_id")

    def fetch(self, session_id):
        """Fetch a specific Transformation with its ID."""
        response = requests.get(
            f"{self.url}{self.settings.prefix}/transformation/{self.id_}?"
            f"session_id={session_id}"
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch transformation: session_id={session_id!r} "
            f"transformation_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id):
        """Initialize a specific Transformation with its ID."""
        response = requests.post(
            f"{self.url}{self.settings.prefix}/transformation/{self.id_}/"
            f"initialize?session_id={session_id}"
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize transformation: session_id={session_id!r} "
            f"transformation_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
