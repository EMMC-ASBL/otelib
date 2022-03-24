"""Function strategy."""
import requests
from oteapi.models import FunctionConfig

from otelib.exceptions import ApiError
from otelib.strategies.abc import AbstractStrategy


class Function(AbstractStrategy):
    """Context class for the Function Strategy Interface."""

    def create(self, **kwargs) -> None:
        session_id = kwargs.pop("session_id", None)
        data = FunctionConfig(**kwargs)

        response = requests.post(
            f"{self.url}{self.settings.prefix}/function",
            json=data.dict(),
            params={"session_id": session_id},
        )
        if not response.ok:
            raise ApiError(
                f"Cannot create function: {data.functionType!r}"
                f"{' content=' + str(response.content) if self.debug else ''}",
                status=response.status_code,
            )

        response_json: dict = response.json()
        self.id = response_json.pop("function_id")

    def fetch(self, session_id: str) -> bytes:
        response = requests.get(
            f"{self.url}{self.settings.prefix}/function/{self.id}",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot fetch function: session_id={session_id!r} "
            f"function_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )

    def initialize(self, session_id: str) -> bytes:
        response = requests.post(
            f"{self.url}{self.settings.prefix}/function/{self.id}/initialize",
            params={"session_id": session_id},
        )
        if response.ok:
            return response.content
        raise ApiError(
            f"Cannot initialize function: session_id={session_id!r} "
            f"function_id={self.id!r}"
            f"{' content=' + str(response.content) if self.debug else ''}",
            status=response.status_code,
        )
