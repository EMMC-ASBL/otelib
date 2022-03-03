"""Filter strategy."""
import requests
from oteapi.models import FilterConfig

from otelib.abc import AbstractStrategy
from otelib.exceptions import ApiError


class Filter(AbstractStrategy):
    """Context class for the Filter Strategy Interfaces"""

    def create(self, **kwargs):
        data = FilterConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/filter",
            json=data.dict(),
            params={"session_id": kwargs.pop("session_id", None)},
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create filter: {data.filterType!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id_ = response_json.pop("filter_id")

    def fetch(self, session_id):
        """Fetch a specific Filter with its ID"""
        response = requests.get(
            f"{self.url}{self.settings.prefix}/filter/{self.id_}",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch filter: session_id={session_id!r} "
            f"filter_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id):
        """Initialize a specific Filter with its ID"""
        response = requests.post(
            f"{self.url}{self.settings.prefix}/filter/{self.id_}/initialize",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize filter: session_id={session_id!r} "
            f"filter_id={self.id_!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
