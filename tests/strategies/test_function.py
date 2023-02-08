"""Tests for `otelib.backends.services.function`."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from ..conftest import OTEResponse, ResourceType


@pytest.mark.parametrize("backend", ["services", "python"])
def test_create(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Function.create()`."""
    if backend == "services":
        from otelib.backends.services.function import Function
    elif backend == "python":
        from otelib.backends.python.function import Function

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
        backend=backend,
    )

    function = Function(server_url)

    assert function.strategy_id is None

    function.create(
        functionType="triples",
        **testdata("function"),
    )

    assert function.strategy_id


def test_create_fails(
    mock_ote_response: "OTEResponse",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Function.create()` raises `ApiError` upon request failure."""
    from otelib.backends.services.function import Function
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/function",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    function = Function(server_url)

    assert function.strategy_id is None

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        function.create(
            functionType="triples",
            **testdata("function"),
            session_id=123,
        )

    assert function.strategy_id is None


@pytest.mark.parametrize("backend", ["services", "python"])
def test_fetch(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Function.fetch()`."""
    if "example" not in server_url:
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    if backend == "services":
        from otelib.backends.services.function import Function
    elif backend == "python":
        pytest.skip("No function strategy exists in oteapi-core yet.")
        # the following code will be needed once we can run this
        from otelib.backends.python.function import Function

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
        backend=backend,
    )

    mock_ote_response(
        method="get",
        endpoint=f"/function/{ids('function')}",
        return_json={},
        backend=backend,
    )

    function = Function(server_url)

    # We must first create the resource - getting a resource ID
    function.create(
        functionType="function/demo",
        **testdata("function"),
    )

    content = function.fetch(session_id=None)

    assert json.loads(content) == {}


def test_fetch_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Function.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.function import Function
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
    )

    mock_ote_response(
        method="get",
        endpoint=f"/function/{ids('function')}",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    function = Function(server_url)

    # We must first create the resource - getting a resource ID
    function.create(
        functionType="function/demo",
        **testdata("function"),
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        function.fetch(session_id=123)


@pytest.mark.parametrize("backend", ["services", "python"])
def test_initialize(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Function.fetch()`."""
    if "example" not in server_url:
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    if backend == "services":
        from otelib.backends.services.function import Function
    elif backend == "python":
        pytest.skip("No function strategy exists in oteapi-core yet.")
        from otelib.backends.python.function import Function

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
        backend=backend,
    )

    mock_ote_response(
        method="post",
        endpoint=f"/function/{ids('function')}/initialize",
        return_json=testdata("function"),
        backend=backend,
    )

    function = Function(server_url)

    # We must first create the resource - getting a resource ID
    function.create(
        functionType="triples",
        **testdata("function"),
    )

    content = function.initialize(session_id=None)

    assert json.loads(content) == testdata("function")


def test_initialize_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Function.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.function import Function
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
    )

    mock_ote_response(
        method="post",
        endpoint=f"/function/{ids('function')}/initialize",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    function = Function(server_url)

    # We must first create the resource - getting a resource ID
    function.create(
        functionType="triples",
        **testdata("function"),
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        function.initialize(session_id=123)
