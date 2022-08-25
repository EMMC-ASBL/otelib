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

    import json

    from otelib.backends.python.function import Function

    function = Function('python')

    # We must first create the resource - getting a resource ID
    # NOTE this is failing because I cannot (yet) figure out how 
    # mock the demo function 
    function.create(
        functionType="function/demo",
    )

    content = function.fetch(session_id=None)

    assert json.loads(content) == {}


def test_initialize() -> None:
    """Test `Function.fetch()`."""
    import json

    from otelib.backends.python.function import Function

    #mock_ote_response(
    #    method="post",
    #    endpoint="/function",
    #    return_json={"function_id": ids("function")},
    #)

    #mock_ote_response(
    #    method="post",
    #    endpoint=f"/function/{ids('function')}/initialize",
    #    return_json=testdata("function"),
    #)

    function = Function('python')

    # We must first create the resource - getting a resource ID
    function.create(
        functionType="triples",
    )

    content = function.initialize(session_id=None)

    testdata={}
    assert json.loads(content) == testdata("function")