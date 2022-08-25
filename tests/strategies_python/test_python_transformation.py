"""Tests for `otelib.backends.services.transformation`."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_create() -> None:
    """Test `Transformation.create()`."""
    from otelib.backends.python.transformation import Transformation

    transformation = Transformation('python')

    assert transformation.id is None

    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    assert transformation.id


def test_fetch(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Transformation.fetch()`."""
    import json

    from otelib.backends.python.transformation import Transformation
    from oteapi.plugins import load_strategies
    load_strategies()

    transformation = Transformation('python')

    # We must first create the resource - getting a resource ID
    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    content = transformation.fetch(session_id=None)

    assert json.loads(content) == testdata("transformation")


def test_initialize() -> None:
    """Test `Transformation.fetch()`."""
    import json

    from otelib.backends.python.transformation import Transformation

    transformation = Transformation('python')

    # We must first create the resource - getting a resource ID
    transformation.create(
        transformationType="celery/remote",
        configuration={"task_name": "test-task", "args": []},
    )

    content = transformation.initialize(session_id=None)

    assert json.loads(content) == {}