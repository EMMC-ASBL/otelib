"""Tests for `otelib.backends.services.mapping`."""
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
    """Test `Mapping.create()`."""
    if backend == "services":
        from otelib.backends.services.mapping import Mapping
    elif backend == "python":
        from otelib.backends.python.mapping import Mapping

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/mapping",
        return_json={"mapping_id": ids("mapping")},
        backend=backend,
    )

    mapping = Mapping(server_url)

    assert mapping.id is None

    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    assert mapping.id


def test_create_fails(
    mock_ote_response: "OTEResponse",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Mapping.create()` raises `ApiError` upon request failure."""
    from otelib.backends.services.mapping import Mapping
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/mapping",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    mapping = Mapping(server_url)

    assert mapping.id is None

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        mapping.create(
            mappingType="triples",
            **testdata("mapping"),
            session_id=123,
        )

    assert mapping.id is None


@pytest.mark.parametrize("backend", ["services", "python"])
def test_fetch(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Mapping.fetch()`."""
    import json

    if backend == "services":
        from otelib.backends.services.mapping import Mapping
    elif backend == "python":
        from otelib.backends.python.mapping import Mapping

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/mapping",
        return_json={"mapping_id": ids("mapping")},
        backend=backend,
    )

    mock_ote_response(
        method="get",
        endpoint=f"/mapping/{ids('mapping')}",
        return_json={},
        backend=backend,
    )

    mapping = Mapping(server_url)

    # We must first create the resource - getting a resource ID
    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    content = mapping.fetch(session_id=None)

    assert json.loads(content) == {}


def test_fetch_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Mapping.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.mapping import Mapping
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/mapping",
        return_json={"mapping_id": ids("mapping")},
    )

    mock_ote_response(
        method="get",
        endpoint=f"/mapping/{ids('mapping')}",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    mapping = Mapping(server_url)

    # We must first create the resource - getting a resource ID
    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        mapping.fetch(session_id=123)


@pytest.mark.parametrize("backend", ["services", "python"])
def test_initialize(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Mapping.fetch()`."""
    import json

    if backend == "services":
        from otelib.backends.services.mapping import Mapping
    elif backend == "python":
        from otelib.backends.python.mapping import Mapping

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()
        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests

    mock_ote_response(
        method="post",
        endpoint="/mapping",
        return_json={"mapping_id": ids("mapping")},
        backend=backend,
    )

    mock_ote_response(
        method="post",
        endpoint=f"/mapping/{ids('mapping')}/initialize",
        return_json=testdata("mapping"),
        backend=backend,
    )

    mapping = Mapping(server_url)

    # We must first create the resource - getting a resource ID
    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    content = mapping.initialize(session_id=None)

    assert json.loads(content) == testdata("mapping")


def test_initialize_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Check `Mapping.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.mapping import Mapping
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/mapping",
        return_json={"mapping_id": ids("mapping")},
    )

    mock_ote_response(
        method="post",
        endpoint=f"/mapping/{ids('mapping')}/initialize",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    mapping = Mapping(server_url)

    # We must first create the resource - getting a resource ID
    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        mapping.initialize(session_id=123)
