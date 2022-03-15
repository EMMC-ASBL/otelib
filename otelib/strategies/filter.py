"""Filter strategy."""
import requests
from oteapi.models import FilterConfig

from otelib.exceptions import ApiError
from otelib.strategies.abc import AbstractStrategy


class Filter(AbstractStrategy):
    """Context class for the Filter Strategy Interfaces"""

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = FilterConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/filter",
            json=data.dict(),
            params={"session_id": session_id} if session_id else {},
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create filter: {data.filterType!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id = response_json.pop("filter_id")

    def fetch(self, session_id: str) -> bytes:
        response = requests.get(
            f"{self.url}{self.settings.prefix}/filter/{self.id}",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch filter: session_id={session_id!r} "
            f"filter_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        response = requests.post(
            f"{self.url}{self.settings.prefix}/filter/{self.id}/initialize",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize filter: session_id={session_id!r} "
            f"filter_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
