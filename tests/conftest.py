"""Fixtures and configuration for pytest."""
# pylint: disable=too-many-arguments,protected-access
from enum import Enum
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Literal, Optional, Type, Union

    from requests_mock import Mocker
    from utils import ResourceType

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
def resource_type_cls() -> "Type[ResourceType]":
    """Return the `ResourceType` Enum."""
    from utils import ResourceType

    return ResourceType


@pytest.fixture
def ids() -> "Callable[[Union[ResourceType, str]], str]":
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
        res._impl.clear_cache()  # pylint: disable=no-member
        return res

    raise RuntimeError(f"Unknown backend: {backend!r}")


@pytest.fixture
def mock_session(
    requests_mock: "Mocker",
    client: "OTEClient",
    ids: "Callable[[Union[ResourceType, str]], str]",
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


@pytest.fixture
def raw_test_data() -> "Dict[str, Any]":
    """Return raw test data."""
    from copy import deepcopy

    from utils import TEST_DATA

    return deepcopy(TEST_DATA)


@pytest.fixture
def testdata(
    raw_test_data: "Dict[str, Any]",
) -> "Callable[[Union[ResourceType, str]], dict]":
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
    monkeypatch: pytest.MonkeyPatch, raw_test_data: "Dict[str, Any]"
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
