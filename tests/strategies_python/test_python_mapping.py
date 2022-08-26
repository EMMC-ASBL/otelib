"""Tests for `otelib.backends.services.mapping`."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_create(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Mapping.create()`."""
    from otelib.backends.python.mapping import Mapping

    mapping = Mapping("python")

    assert mapping.id is None

    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    assert mapping.id


def test_fetch(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Mapping.fetch()`."""
    import json

    from oteapi.plugins import load_strategies

    load_strategies()
    from otelib.backends.python.mapping import Mapping

    mapping = Mapping("python")

    # We must first create the resource - getting a resource ID
    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    content = mapping.fetch(session_id=None)

    assert json.loads(content) == {}


def test_initialize(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Mapping.fetch()`."""
    import json

    from otelib.backends.python.mapping import Mapping

    mapping = Mapping("python")

    # We must first create the resource - getting a resource ID
    mapping.create(
        mappingType="triples",
        **testdata("mapping"),
    )

    content = mapping.initialize(session_id=None)

    assert json.loads(content) == testdata("mapping")
