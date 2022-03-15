"""Tests for `otelib.strategies.transformation`."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_create(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Test `Transformation.create()`."""
    from otelib.strategies.transformation import Transformation

    mock_ote_response(
        method="post",
        endpoint="/transformation",
        return_json={"transformation_id": ids("transformation")},
    )

    transformation = Transformation(server_url)

    assert transformation.id is None

    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    assert transformation.id


def test_create_fails(
    mock_ote_response: "OTEResponse",
    server_url: str,
) -> None:
    """Check `Transformation.create()` raises `ApiError` upon request failure."""
    from otelib.exceptions import ApiError
    from otelib.strategies.transformation import Transformation

    mock_ote_response(
        method="post",
        endpoint="/transformation",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    transformation = Transformation(server_url)

    assert transformation.id is None

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        transformation.create(
            transformationType="celery/remote",
            configuration={"task_name": "test-task", "args": []},
            session_id=123,
        )

    assert transformation.id is None


def test_fetch(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Transformation.fetch()`."""
    import json

    from otelib.strategies.transformation import Transformation

    mock_ote_response(
        method="post",
        endpoint="/transformation",
        return_json={"transformation_id": ids("transformation")},
    )

    mock_ote_response(
        method="get",
        endpoint=f"/transformation/{ids('transformation')}",
        return_json=testdata("transformation"),
    )

    transformation = Transformation(server_url)

    # We must first create the resource - getting a resource ID
    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    content = transformation.fetch(session_id=None)

    assert json.loads(content) == testdata("transformation")


def test_fetch_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Check `Transformation.fetch()` raises `ApiError` upon request failure."""
    from otelib.exceptions import ApiError
    from otelib.strategies.transformation import Transformation

    mock_ote_response(
        method="post",
        endpoint="/transformation",
        return_json={"transformation_id": ids("transformation")},
    )

    mock_ote_response(
        method="get",
        endpoint=f"/transformation/{ids('transformation')}",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    transformation = Transformation(server_url)

    # We must first create the resource - getting a resource ID
    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        transformation.fetch(session_id=123)


def test_initialize(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Test `Transformation.fetch()`."""
    import json

    from otelib.strategies.transformation import Transformation

    mock_ote_response(
        method="post",
        endpoint="/transformation",
        return_json={"transformation_id": ids("transformation")},
    )

    mock_ote_response(
        method="post",
        endpoint=f"/transformation/{ids('transformation')}/initialize",
        return_json={},
    )

    transformation = Transformation(server_url)

    # We must first create the resource - getting a resource ID
    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    content = transformation.initialize(session_id=None)

    assert json.loads(content) == {}


def test_initialize_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
) -> None:
    """Check `Transformation.fetch()` raises `ApiError` upon request failure."""
    from otelib.exceptions import ApiError
    from otelib.strategies.transformation import Transformation

    mock_ote_response(
        method="post",
        endpoint="/transformation",
        return_json={"transformation_id": ids("transformation")},
    )

    mock_ote_response(
        method="post",
        endpoint=f"/transformation/{ids('transformation')}/initialize",
        status_code=500,
        return_content=b"Internal Server Error",
    )

    transformation = Transformation(server_url)

    # We must first create the resource - getting a resource ID
    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    with pytest.raises(ApiError, match="APIError"):
        # `session_id` has a wrong type, the request should fail.
        transformation.initialize(session_id=123)
