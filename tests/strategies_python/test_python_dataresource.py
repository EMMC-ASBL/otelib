"""Tests for `otelib.backends.services.dataresource`."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_python_create() -> None:
    """Test `DataResource.create()`."""
    from otelib.backends.python.dataresource import DataResource

    data_resource = DataResource("python")

    assert data_resource.id is None

    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    assert data_resource.id


# NOTE: this takes too long (6seconds), probably should do some mocking?
def test_python_fetch(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `DataResource.fetch()`."""
    import json

    from oteapi.plugins import load_strategies

    from otelib.backends.python.dataresource import DataResource

    load_strategies()

    data_resource = DataResource("python")
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    content = data_resource.fetch(session_id=None)

    assert json.loads(content) == testdata("dataresource")


def test_python_initialize() -> None:
    """Test `DataResource.fetch()`."""

    import json

    from oteapi.plugins import load_strategies

    from otelib.backends.python.dataresource import DataResource

    load_strategies()

    data_resource = DataResource("python")

    # We must first create the resource - getting a resource ID
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    # services returns {} not None
    content = data_resource.initialize(session_id=None)

    assert json.loads(content) == {}
