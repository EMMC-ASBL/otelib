"""Tests for `otelib.backends.services.function`."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_create() -> None:
    """Test `Function.create()`."""
    from otelib.backends.python.function import Function


    function = Function('python')

    assert function.id is None

    function.create(
        functionType="triples",
    )

    assert function.id


def test_fetch() -> None:
    """Test `Function.fetch()`."""

    pytest.skip("No function strategy exists in oteapi-core yet.")
    import json

    from otelib.backends.python.function import Function

    function = Function('python')

    # We must first create the resource - getting a resource ID
    function.create(
        functionType="function/demo",
    )

    content = function.fetch(session_id=None)

    assert json.loads(content) == {}


def test_initialize() -> None:
    """Test `Function.fetch()`."""

    pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    from otelib.backends.python.function import Function


    function = Function('python')

    # We must first create the resource - getting a resource ID
    function.create(
        functionType="triples",
    )

    content = function.initialize(session_id=None)

    testdata={}
    assert json.loads(content) == testdata("function")