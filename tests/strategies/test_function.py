"""Tests for `otelib.strategies.function`."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_create(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Function.create()`."""
    from otelib.strategies.function import Function

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
    )

    function = Function(server_url)

    assert function.id is None

    function.create(
        functionType="triples",
        **testdata("function"),
    )

    assert function.id


def test_create_fails(
    mock_ote_response: "OTEResponse",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Function.create()` raises `ApiError` upon request failure."""
    from otelib.exceptions import ApiError
    from otelib.strategies.function import Function

    mock_ote_response(
        method="post",
        endpoint="/function",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    function = Function(server_url)

    assert function.id is None

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        function.create(
            functionType="triples",
            **testdata("function"),
            session_id=123,
        )

    assert function.id is None


def test_fetch(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Function.fetch()`."""
    if "example" not in server_url:
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    from otelib.strategies.function import Function

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
    )

    mock_ote_response(
        method="get",
        endpoint=f"/function/{ids('function')}",
        return_json={},
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
    from otelib.exceptions import ApiError
    from otelib.strategies.function import Function

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


def test_initialize(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Function.fetch()`."""
    if "example" not in server_url:
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    from otelib.strategies.function import Function

    mock_ote_response(
        method="post",
        endpoint="/function",
        return_json={"function_id": ids("function")},
    )

    mock_ote_response(
        method="post",
        endpoint=f"/function/{ids('function')}/initialize",
        return_json=testdata("function"),
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
    from otelib.exceptions import ApiError
    from otelib.strategies.function import Function

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
