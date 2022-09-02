"""Fixtures and configuration for pytest."""
# pylint: disable=too-many-arguments
from enum import Enum
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Optional, Union

    from requests_mock import Mocker

    from otelib.client import OTEClient

    OTEResponse = Callable[
        [
            Union["HTTPMethod", str],
            str,
            int,
            Optional[Union[Dict[str, Any], str]],
            Optional[dict],
            Optional[bytes],
            Optional[Union[dict, str]],
            Optional[str],
            Optional[OTEClient],
        ],
        None,
    ]


class ResourceType(str, Enum):
    """Enumeration of resource types."""

    DATARESOURCE = "dataresource"
    FILTER = "filter"
    FUNCTION = "function"
    MAPPING = "mapping"
    SESSION = "session"
    TRANSFORMATION = "transformation"

    def get_idprefix(self) -> str:
        """Get the `IDPREFIX` used in oteapi-services."""
        return {
            "dataresource": "dataresource-",
            "filter": "filter-",
            "function": "function-",
            "mapping": "mapping-",
            "session": "session-",
            "transformation": "transformation-",
        }[self.value]


class HTTPMethod(str, Enum):
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


def pytest_configure(config) -> None:  # pylint: disable=unused-argument
    """Method that runs before pytest collects tests, so no modules are imported."""
    import os

    os.environ["OTELIB_DEBUG"] = "True"


@pytest.fixture
def server_url() -> str:
    """Return a possibly set real server URL.

    The server URL must be set through the environment variable
    `OTELIB_TEST_OTE_SERVER_URL`.
    """
    import os

    return os.getenv("OTELIB_TEST_OTE_SERVER_URL", "https://example.org")


@pytest.fixture
def resource_type_cls() -> ResourceType:
    """Return the `ResourceType` Enum."""
    return ResourceType


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
def client(server_url: str) -> "OTEClient":
    """Create an `OTEClient` test client."""
    from otelib.client import OTEClient

    return OTEClient(server_url)


@pytest.fixture
def mock_session(
    backend: str,
    requests_mock: "Mocker",
    client: "OTEClient",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Mock `POST /session`.

    This is called in `AbstractStrategy.get()`.
    """
    from otelib.settings import Settings

    # For now I need python backend to run test for real
    if "example" in server_url and backend != "python":
        requests_mock.post(
            f"{client.url}{Settings().prefix}/session",
            json={"session_id": ids("session")},
        )
    else:
        # Make sure the requests are done for real.
        requests_mock.real_http = True


@pytest.fixture
def mock_ote_response(
    requests_mock: "Mocker", server_url: str
) -> "Callable[[Union[HTTPMethod, str], str, int, Optional[Union[Dict[str, Any], str]], Optional[dict], Optional[bytes], Optional[Union[dict, str]], Optional[str], Optional[OTEClient]], None]":  # pylint: disable=line-too-long
    """Provide a function to mock OTE services responses."""
    from urllib.parse import parse_qs

    from otelib.settings import Settings

    def _mock_response(
        method: "Union[HTTPMethod, str]",
        endpoint: str,
        status_code: int = 200,
        params: "Optional[Union[Dict[str, Any], str]]" = None,
        headers: "Optional[dict]" = None,
        return_content: "Optional[bytes]" = None,
        return_json: "Optional[Union[dict, str]]" = None,
        return_text: "Optional[str]" = None,
        ote_client: "Optional[OTEClient]" = None,
    ) -> None:
        """Use `requests_mock` to mock a response from an OTE services server.

        It will only be ensured that the `endpoint` starts with a forward slash.
        If it does not, one will be added. Otherwise, `endpoint` is not manipulated.
        """
        if "example" not in server_url:
            # Make sure the requests are done for real.
            requests_mock.real_http = True
            return

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

        mock_kwargs = {}
        if return_content is not None:
            mock_kwargs["content"] = return_content
        if return_json is not None:
            mock_kwargs["json"] = return_json
        if return_text is not None:
            mock_kwargs["text"] = return_text
        if headers is not None:
            mock_kwargs["headers"] = headers

        print(
            f"Mocking request: {method} "
            f"{ote_client.url if ote_client else server_url}{Settings().prefix}"
            f"{endpoint}{params} "
            f"status_code={status_code} "
            + " ".join(f"{key}={value}" for key, value in mock_kwargs.items())
        )

        requests_mock.request(
            method=method,
            url=(
                f"{ote_client.url if ote_client else server_url}{Settings().prefix}"
                f"{endpoint}{params}"
            ),
            status_code=status_code,
            **mock_kwargs,
        )

    return _mock_response


TEST_DATA = {
    "dataresource": {
        "content": {
            "firstName": "Joe",
            "lastName": "Jackson",
            "gender": "male",
            "age": 28,
            "address": {
                "streetAddress": "101",
                "city": "San Diego",
                "state": "CA",
            },
            "phoneNumbers": [{"type": "home", "number": "7349282382"}],
        }
    },
    "filter": {"sqlquery": "DROP TABLE myTable;"},
    "function": {},
    "mapping": {
        "prefixes": {
            "map": "http://example.org/0.0.1/mapping_ontology#",
            "onto": "http://example.org/0.2.1/ontology#",
        },
        "triples": [
            ["http://onto-ns.com/meta/1.0/Foo#a", "map:mapsTo", "onto:A"],
            ["http://onto-ns.com/meta/1.0/Foo#b", "map:mapsTo", "onto:B"],
            ["http://onto-ns.com/meta/1.0/Bar#a", "map:mapsTo", "onto:C"],
        ],
    },
    "transformation": {"data": {}},
}


@pytest.fixture
def raw_test_data() -> "Dict[str, Any]":
    """Return raw test data."""
    from copy import deepcopy

    return deepcopy(TEST_DATA)


@pytest.fixture
def testdata(
    raw_test_data: "Dict[str, Any]",
) -> "Callable[[Union[ResourceType, str]], dict]":
    """Test data for OTE resource."""

    def _testdata(resource_type: "Union[ResourceType, str]") -> dict:
        """Return test data for a given resource."""
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.SESSION:
            raise ValueError("No test data available for a session.")

        return raw_test_data[resource_type.value]

    return _testdata
