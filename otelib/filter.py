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
            f"{self.url}{self.settings.prefix}/filter", json=data.dict()
        )
        if response.status_code != 200:
            raise ApiError(
                f"Cannot create filter: {data.filterType!r} ({response.status_code})"
            )

        response_json: dict = response.json()
        self.id_ = response_json.pop("filter_id")

    def fetch(self, session_id):
        """Fetch a specific Filter with its ID"""
        response = requests.get(
            f"{self.url}{self.settings.prefix}/filter/{self.id_}?"
            f"session_id={session_id}"
        )
        return response.content

    def initialize(self, session_id):
        """Initialize a specific Filter with its ID"""
        response = requests.post(
            f"{self.url}{self.settings.prefix}/filter/{self.id_}/initialize?"
            f"session_id={session_id}"
        )
        return response.content
