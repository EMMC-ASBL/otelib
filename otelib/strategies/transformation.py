"""Transformation strategy."""
import requests
from oteapi.models import TransformationConfig

from otelib.exceptions import ApiError
from otelib.strategies.abc import AbstractStrategy


class Transformation(AbstractStrategy):
    """Context class for the Transformation Strategy Interfaces."""

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = TransformationConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/transformation",
            json=data.dict(),
            params={"session_id": session_id},
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create transformation: {data.transformationType!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id = response_json.pop("transformation_id")

    def fetch(self, session_id: str) -> bytes:
        response = requests.get(
            f"{self.url}{self.settings.prefix}/transformation/{self.id}",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch transformation: session_id={session_id!r} "
            f"transformation_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        response = requests.post(
            f"{self.url}{self.settings.prefix}/transformation/{self.id}/initialize",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize transformation: session_id={session_id!r} "
            f"transformation_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
