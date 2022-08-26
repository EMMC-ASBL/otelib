"""Tests for `otelib.backends.services.filter`."""
# pylint: disable=redefined-builtin
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_create(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Filter.create()`."""
    from otelib.backends.python.filter import Filter

    filter = Filter("python")

    assert filter.id is None

    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    assert filter.id


def test_fetch(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Filter.fetch()`."""
    import json

    from oteapi.plugins import load_strategies

    load_strategies()

    from otelib.backends.python.filter import Filter

    filter = Filter("python")

    # We must first create the resource - getting a resource ID
    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    content = filter.fetch(session_id=None)

    assert json.loads(content) == {}


def test_initialize(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test `Filter.fetch()`."""
    import json

    from otelib.backends.python.filter import Filter

    filter = Filter("python")

    # We must first create the resource - getting a resource ID
    filter.create(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    content = filter.initialize(session_id=None)

    assert json.loads(content) == testdata("filter")
