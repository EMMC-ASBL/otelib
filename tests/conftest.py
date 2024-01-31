"""Fixtures and configuration for pytest."""

from typing import TYPE_CHECKING

try:
    # For Python >= 3.11
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        """Pre-3.11 style string-Enums."""


import pytest

if TYPE_CHECKING:
    from typing import Any, Literal, Optional, Protocol, Union

    from requests_mock import Mocker
    from utils import ResourceType

    from otelib.client import OTEClient

    class TestResourceIds(Protocol):
        """Defines a protocol for fetching a test ID based on the provided resource
        type."""

        def __call__(self, resource_type: Union[ResourceType, str]) -> str: ...

    class OTEResponse(Protocol):
        """Defines a protocol for mocking a response from an OTE services server using
        `requests_mock`.

        The implementing callable should ensure that the `endpoint` starts with a
        forward slash (`/`). If it doesn't, one is added. No other manipulation on the
        `endpoint` is done.

        Parameters:
            method: The HTTP method (or its string representation) for the request.
            endpoint: The API endpoint. Should start with a forward slash.
            status_code: The desired HTTP status code for the response. Defaults to 200
                (OK).
            params: Optional request parameters.
            headers: Optional request headers.
            response_content: Optional content to be returned as the response body.
            response_json: Optional JSON data to be returned as the response body.
            response_text: Optional plain text to be returned as the response body.
            ote_client: An optional client instance for making the request.

        """

        def __call__(
            self,
            method: Union["HTTPMethod", str],
            endpoint: str,
            status_code: int = 200,
            params: Optional[Union[dict[str, Any], str]] = None,
            headers: Optional[dict] = None,
            response_content: Optional[bytes] = None,
            response_json: Optional[Union[dict, str]] = None,
            response_text: Optional[str] = None,
            ote_client: Optional[OTEClient] = None,
        ) -> None: ...

    class Testdata(Protocol):
        """Defines a protocol for fetching test data corresponding to a specified
        resource type.

        Test data can be optionally tailored based on a provided method (e.g., "get",
        "initialize"). If no method is specified, the test data is provided in its
        default form.

        Parameters:
            resource_type: The resource type to return test data for.
            method: An optional method specifier which can influence the structure of
                the returned test data.

        """

        def __call__(
            self,
            resource_type: Union[ResourceType, str],
            method: Optional[Literal["get", "initialize"]] = None,
        ) -> dict: ...


class HTTPMethod(StrEnum):
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


def pytest_configure(config) -> None:
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
def resource_type_cls() -> "type[ResourceType]":
    """Return the `ResourceType` Enum."""
    from utils import ResourceType

    return ResourceType


@pytest.fixture
def ids() -> "TestResourceIds":
    """Provide a function to return a test resource id.

    By "resource", any resource is meant, e.g., `sessions`, `filter`, etc.
    """
    from utils import ResourceType

    def _ids(resource_type: "Union[ResourceType, str]") -> str:
        """Return a test id for the given `resource_type`."""
        resource_type = ResourceType(resource_type)
        return f"{resource_type.get_idprefix()}test"

    return _ids


@pytest.fixture(params=["services", "python"])
def backend(request: pytest.FixtureRequest) -> str:
    """Run a test for all backends."""
    if request.param == "python":
        from oteapi.plugins import load_strategies

        load_strategies()

    return request.param


@pytest.fixture
def client(server_url: str, backend: str) -> "OTEClient":
    """Create an `OTEClient` test client."""
    from otelib.client import OTEClient

    if backend == "services":
        return OTEClient(server_url)

    if backend == "python":
        res = OTEClient("python")
        res._impl.clear_cache()
        return res

    raise RuntimeError(f"Unknown backend: {backend!r}")


@pytest.fixture
def mock_session(
    requests_mock: "Mocker",
    client: "OTEClient",
    ids: "TestResourceIds",
    server_url: str,
) -> None:
    """Mock `POST /session`.

    This is called in `AbstractStrategy.get()`.
    """
    from otelib.settings import Settings

    if client._impl._backend == "services" and "example" in server_url:
        requests_mock.post(
            f"{client.url}{Settings().prefix}/session",
            json={"session_id": ids("session")},
        )
    else:
        # Make sure the requests are done for real.
        requests_mock.real_http = True


@pytest.fixture
def mock_ote_response(requests_mock: "Mocker", server_url: str) -> "OTEResponse":
    """Provide a function to mock OTE services responses."""
    from urllib.parse import parse_qs

    from otelib.settings import Settings

    def _mock_response(
        method: "Union[HTTPMethod, str]",
        endpoint: str,
        status_code: int = 200,
        params: "Optional[Union[dict[str, Any], str]]" = None,
        headers: "Optional[dict]" = None,
        response_content: "Optional[bytes]" = None,
        response_json: "Optional[Union[dict, str]]" = None,
        response_text: "Optional[str]" = None,
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
        if response_content is not None:
            mock_kwargs["content"] = response_content
        if response_json is not None:
            mock_kwargs["json"] = response_json
        if response_text is not None:
            mock_kwargs["text"] = response_text
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


@pytest.fixture
def raw_test_data() -> "dict[str, Any]":
    """Return raw test data."""
    from copy import deepcopy

    from utils import TEST_DATA

    return deepcopy(TEST_DATA)


@pytest.fixture
def testdata(raw_test_data: "dict[str, Any]") -> "Testdata":
    """Test data for OTE resource."""
    from utils import ResourceType

    def _testdata(
        resource_type: "Union[ResourceType, str]",
        method: "Optional[Literal['get', 'initialize']]" = None,
    ) -> dict:
        """Return test data for a given resource.

        Parameters:
            resource_type: The resource type to return test data for.
            method: Optionally, provide the method for which to return the test data.
                If not given, the test data will be provided as is.

        """
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.SESSION:
            raise ValueError("No test data available for a session.")

        if method is None:
            return raw_test_data[resource_type.value]

        return (
            raw_test_data[resource_type.value]
            if resource_type.map_method_to_data(method)
            else {}
        )

    return _testdata


@pytest.fixture(autouse=True)
def mock_celery_transformation_strategy(
    monkeypatch: pytest.MonkeyPatch, raw_test_data: "dict[str, Any]"
) -> None:
    """Use celery_worker always for all things.

    Parameters:
        monkeypatch: Monkeypatch fixture for use in pytest.
        raw_test_data: Deep copy of the test data.

    """

    class MockResult:
        """Mock result from 'transformationType=celery/remote'."""

        task_id = raw_test_data["transformation"]["celery_task_id"]

    monkeypatch.setattr(
        "oteapi.strategies.transformation.celery_remote.CELERY_APP.send_task",
        lambda *args, **kwargs: MockResult(),
    )
