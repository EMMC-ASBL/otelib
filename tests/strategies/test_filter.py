"""Tests for `otelib.backends.services.filter`."""
# pylint: disable=redefined-builtin
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
    """Test `Filter.create()`."""
    if backend == "services":
        from otelib.backends.services.filter import Filter
    elif backend == "python":
        from otelib.backends.python.filter import Filter

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/filter",
        return_json={"filter_id": ids("filter")},
    )

    filter = Filter(server_url)

    assert filter.strategy_id is None

    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    assert filter.strategy_id


def test_create_fails(
    mock_ote_response: "OTEResponse",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Filter.create()` raises `ApiError` upon request failure."""
    from otelib.backends.services.filter import Filter
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/filter",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    filter = Filter(server_url)

    assert filter.strategy_id is None

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        filter.create(
            filterType="filter/sql",
            query=testdata("filter")["sqlquery"],
            session_id=123,
        )

    assert filter.strategy_id is None


@pytest.mark.parametrize("backend", ["services", "python"])
def test_fetch(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Filter.fetch()`."""
    import json

    if backend == "services":
        from otelib.backends.services.filter import Filter
    elif backend == "python":
        from otelib.backends.python.filter import Filter

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/filter",
        return_json={"filter_id": ids("filter")},
        backend=backend,
    )

    mock_ote_response(
        method="get",
        endpoint=f"/filter/{ids('filter')}",
        return_json={},
        backend=backend,
    )

    filter = Filter(server_url)

    # We must first create the resource - getting a resource ID
    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    content = filter.fetch(session_id=None)

    assert json.loads(content) == {}


def test_fetch_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Filter.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.filter import Filter
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/filter",
        return_json={"filter_id": ids("filter")},
    )

    mock_ote_response(
        method="get",
        endpoint=f"/filter/{ids('filter')}",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    filter = Filter(server_url)

    # We must first create the resource - getting a resource ID
    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        filter.fetch(session_id=123)


@pytest.mark.parametrize("backend", ["services", "python"])
def test_initialize(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Filter.fetch()`."""
    import json

    if backend == "services":
        from otelib.backends.services.filter import Filter
    elif backend == "python":
        from otelib.backends.python.filter import Filter

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/filter",
        return_json={"filter_id": ids("filter")},
        backend=backend,
    )

    mock_ote_response(
        method="post",
        endpoint=f"/filter/{ids('filter')}/initialize",
        return_json=testdata("filter"),
        backend=backend,
    )

    filter = Filter(server_url)

    # We must first create the resource - getting a resource ID
    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    content = filter.initialize(session_id=None)

    assert json.loads(content) == testdata("filter")


def test_initialize_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Filter.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.filter import Filter
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/filter",
        return_json={"filter_id": ids("filter")},
    )

    mock_ote_response(
        method="post",
        endpoint=f"/filter/{ids('filter')}/initialize",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    filter = Filter(server_url)

    # We must first create the resource - getting a resource ID
    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        filter.initialize(session_id=123)
