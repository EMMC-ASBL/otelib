"""Tests for `otelib.backends.services.dataresource`."""
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
) -> None:
    """Test `DataResource.create()`."""

    if backend == "services":
        from otelib.backends.services.dataresource import DataResource
    elif backend == "python":
        from otelib.backends.python.dataresource import DataResource

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()

    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        return_json={"resource_id": ids("dataresource")},
    )

    data_resource = DataResource(server_url)

    assert data_resource.strategy_id is None

    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    assert data_resource.strategy_id


def test_create_fails(
    mock_ote_response: "OTEResponse",
    server_url: str,
) -> None:
    """Check `DataResource.create()` raises `ApiError` upon request failure."""
    from otelib.backends.services.dataresource import DataResource
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    data_resource = DataResource(server_url)

    assert data_resource.strategy_id is None

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        data_resource.create(
            downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
            mediaType="application/json",
            session_id=123,
        )

    assert data_resource.strategy_id is None


@pytest.mark.parametrize("backend", ["services", "python"])
def test_fetch(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `DataResource.fetch()`."""
    import json

    if backend == "services":
        from otelib.backends.services.dataresource import DataResource
    elif backend == "python":
        from otelib.backends.python.dataresource import DataResource

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()

    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        return_json={"resource_id": ids("dataresource")},
        backend=backend,
    )

    mock_ote_response(
        method="get",
        endpoint=f"/dataresource/{ids('dataresource')}",
        return_json=testdata("dataresource"),
        backend=backend,
    )

    data_resource = DataResource(server_url)

    # We must first create the resource - getting a resource ID
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    content = data_resource.fetch(session_id=None)

    assert json.loads(content) == testdata("dataresource")


def test_fetch_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Check `DataResource.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.dataresource import DataResource
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        return_json={"resource_id": ids("dataresource")},
    )

    mock_ote_response(
        method="get",
        endpoint=f"/dataresource/{ids('dataresource')}",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    data_resource = DataResource(server_url)

    # We must first create the resource - getting a resource ID
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        data_resource.fetch(session_id=123)


@pytest.mark.parametrize("backend", ["services", "python"])
def test_initialize(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Test `DataResource.fetch()`."""
    import json

    if backend == "services":
        from otelib.backends.services.dataresource import DataResource
    elif backend == "python":
        from otelib.backends.python.dataresource import DataResource

        server_url = "python"
        from oteapi.plugins import load_strategies

        load_strategies()

    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        return_json={"resource_id": ids("dataresource")},
        backend=backend,
    )

    mock_ote_response(
        method="post",
        endpoint=f"/dataresource/{ids('dataresource')}/initialize",
        return_json={},
        backend=backend,
    )

    data_resource = DataResource(server_url)

    # We must first create the resource - getting a resource ID
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    content = data_resource.initialize(session_id=None)

    assert json.loads(content) == {}


def test_initialize_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Check `DataResource.fetch()` raises `ApiError` upon request failure."""
    from otelib.backends.services.dataresource import DataResource
    from otelib.exceptions import ApiError

    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        return_json={"resource_id": ids("dataresource")},
    )

    mock_ote_response(
        method="post",
        endpoint=f"/dataresource/{ids('dataresource')}/initialize",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    data_resource = DataResource(server_url)

    # We must first create the resource - getting a resource ID
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        data_resource.initialize(session_id=123)
