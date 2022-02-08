"""Fixtures and configuration for pytest."""
from enum import Enum
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Optional, Union

    from requests_mock import Mocker

    from otelib.ontotransserver import OntoTransServer


class ResourceType(Enum):
    """Enumeration of resource types."""

    DATARESOURCE = "dataresource"
    FILTER = "filter"
    MAPPING = "mapping"
    RESOURCE = "resource"
    SESSION = "session"
    TRANSFORMATION = "transformation"

    def get_idprefix(self) -> str:
        """Get the `IDPREFIX` used in oteapi-services."""
        return {
            "dataresource": "dataresource-",
            "filter": "filter-",
            "mapping": "mapping-",
            "resource": "dataresource-",
            "session": "session-",
            "transformation": "transformation-",
        }[self.value]


class HTTPMethod(Enum):
    """Allowed HTTP methods.

    See `requests_mock.mocker` for the reference list.
    """

    DELETE = "delete"
    GET = "get"
    HEAD = "head"
    OPTIONS = "options"
    PATCH = "patch"
    POST = "post"
    PUT = "put"


@pytest.fixture
def dataresource_data() -> "Dict[str, Any]":
    """Test data for a DataResource"""
    return {
        "firstName": "Joe",
        "lastName": "Jackson",
        "gender": "male",
        "age": 28,
        "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
        "phoneNumbers": [{"type": "home", "number": "7349282382"}],
    }


@pytest.fixture
def ids() -> "Callable[[Union[ResourceType, str]], str]":
    """Provide a function to return a test resource id.

    By "resource", any resource is meant, e.g., `sessions`, `filter`, etc.
    """

    def _ids(resource_type: "Union[ResourceType, str]") -> str:
        """Return a test id for the given `resource_type`."""
        resource_type = ResourceType(resource_type)
        return f"{resource_type.get_idprefix()}test"

    return _ids


@pytest.fixture
def server() -> "OntoTransServer":
    """Create an `OntoTransServer` test server."""
    from otelib.ontotransserver import OntoTransServer

    return OntoTransServer("https://example.org")


@pytest.fixture
def mock_session(
    requests_mock: "Mocker",
    server: "OntoTransServer",
    ids: "Callable[[Union[ResourceType, str]], str]",
) -> None:
    """Mock `POST /session/`.

    This is called in `AbstractStrategy.get()`.
    """
    from otelib.settings import Settings

    requests_mock.post(
        f"{server.url}{Settings().prefix}/session/",
        json={"session_id": ids("session")},
    )


@pytest.fixture
def mock_ote_response(
    requests_mock: "Mocker", server: "OntoTransServer"
) -> "Callable[[Union[HTTPMethod, str], str, Optional[Union[Dict[str, Any], str]], Optional[Union[dict, str]]], None]":  # pylint: disable=line-too-long
    """Provide a function to mock OTE services responses."""
    from urllib.parse import parse_qs

    from otelib.settings import Settings

    def _mock_response(
        method: "Union[HTTPMethod, str]",
        endpoint: str,
        params: "Optional[Union[Dict[str, Any], str]]" = None,
        data: "Optional[Union[dict, str]]" = None,
        ote_server: "Optional[OntoTransServer]" = None,
    ) -> None:
        """Use `requests_mock` to mock a response from an OTE services server.

        It will only be ensured that the `endpoint` starts with a forward slash.
        If it does not, one will be added. Otherwise, `endpoint` is not manipulated.

        The `data` is expected to be a dictionary passed through with the `json`
        parameter.
        """
        method: str = (
            HTTPMethod(method.lower())
            if isinstance(method, str)
            else HTTPMethod(method)
        ).value.upper()
        if not endpoint.startswith("/"):
            endpoint = f"/{endpoint}"
        if params:
            if isinstance(params, str):
                params = parse_qs(params)
            _params = "?"

            key = sorted(params)[0]
            values = (
                [params.pop(key)]
                if isinstance(params[key], (str, int, float))
                else params.pop(key)
            )
            _params += "&".join(f"{key}={value}" for value in sorted(values))
            while params:
                key = sorted(params)[0]
                values = (
                    [params.pop(key)]
                    if isinstance(params[key], (str, int, float))
                    else params.pop(key)
                )
                _params += "&" + "&".join(f"{key}={value}" for value in sorted(values))

            params = _params
        else:
            params = ""

        requests_mock.request(
            method=method,
            url=(
                f"{ote_server.url if ote_server else server.url}{Settings().prefix}"
                f"{endpoint}{params}"
            ),
            json=data or {},
        )

    return _mock_response
