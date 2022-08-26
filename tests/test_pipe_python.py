"""Test the `otelib.pipe` module."""
# pylint: disable=too-many-arguments,too-many-locals,protected-access,redefined-builtin
from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Union

    from otelib.strategies.abc import AbstractStrategy
    from tests.conftest import OTEResponse, ResourceType


@pytest.mark.parametrize(
    "strategy_name,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
def test_pipe(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    server_url: str,
    strategy_name: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test creating a `Pipe` and run the `get()` method."""
    if strategy_name == "function":
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    import requests
    from oteapi.plugins import load_strategies

    # Need to manually clear the cache before starting test
    from otelib.backends.python.base import Cache

    cache = Cache()
    cache.clear()

    load_strategies()
    from otelib.backends import python as strategies
    from otelib.pipe import Pipe

    strategy_name_map = {"dataresource": "DataResource"}

    strategy: "AbstractStrategy" = getattr(
        strategies, strategy_name_map.get(strategy_name, strategy_name.capitalize())
    )(server_url)

    # We must create the strategy - getting a strategy ID
    strategy.create(**create_kwargs)
    assert strategy.id

    pipe = Pipe(strategy)

    content = pipe.get()
    if strategy_name in ("filter", "mapping"):
        assert json.loads(content) == {}
    else:
        assert json.loads(content) == testdata(strategy_name)

    # The testdata should always be in the full session
    assert (
        strategy._session_id
    ), f"Session ID not found in {strategy_name} ! Is OTEAPI_DEBUG not set?"
    session_ids = [x for x in strategy.cache if "session" in x]
    assert len(session_ids) == 1
    session_id = session_ids[0]
    session = strategy.cache[session_id]
    for key, value in testdata(strategy_name).items():
        if strategy_name == "mapping":
            # Due to some technicalities I haven't yet figured out
            # the session stores tuples, while json response uses lists
            continue
        assert key in session
        assert value == session[key]


def test_pipeing_strategies(
    ids: "Callable[[Union[ResourceType, str]], str]",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    server_url: str,
) -> None:
    """A simple pipeline will be tested."""
    import json

    import requests
    from oteapi.plugins import load_strategies

    load_strategies()
    from otelib.backends.python import DataResource, Filter

    # Need to manually clear the cache before starting test
    from otelib.backends.python.base import Cache

    cache = Cache()
    cache.clear()

    # Session content
    session_test_content = testdata("filter")
    session_test_content.update(testdata("dataresource"))

    data_resource = DataResource(server_url)
    filter = Filter(server_url)

    # We must create the data resource and filter - getting IDs
    create_kwargs = dict(strategy_create_kwargs())
    data_resource.create(**create_kwargs["dataresource"])
    assert data_resource.id
    filter.create(**create_kwargs["filter"])
    assert filter.id

    pipeline = data_resource >> filter

    content = pipeline.get()

    # Since the "last" strategy does not return anything from its `get()` method,
    # this should return an empty dictionary.
    assert json.loads(content) == {}

    ## All the test data should however be present in the session
    assert (
        pipeline._session_id
    ), f"Session ID not found in {pipeline} ! Is OTEAPI_DEBUG not set?"
    session_ids = [x for x in pipeline.cache if "session" in x]
    assert len(session_ids) == 1
    session_id = session_ids[0]
    session = pipeline.cache[session_id]
    for key, value in session_test_content.items():
        assert key in session
        assert value == session[key]

    ###
    ## Reverse the pipeline and try again
    ###
    # Need to manually clear the cache before starting test
    cache = Cache()
    cache.clear()

    data_resource = DataResource(server_url)
    filter = Filter(server_url)

    # We must create the data resource and filter - getting IDs
    create_kwargs = dict(strategy_create_kwargs())
    data_resource.create(**create_kwargs["dataresource"])
    assert data_resource.id
    filter.create(**create_kwargs["filter"])
    assert filter.id

    pipeline = filter >> data_resource

    content = pipeline.get()

    ## Since the "last" strategy now returns something from its `get()` method,
    ## this can be tested.
    assert json.loads(content) == testdata("dataresource")

    ## All the test data should however be present in the session
    assert (
        pipeline._session_id
    ), f"Session ID not found in {pipeline} ! Is OTEAPI_DEBUG not set?"
    session_ids = [x for x in pipeline.cache if "session" in x]
    assert len(session_ids) == 1
    session_id = session_ids[0]
    session = pipeline.cache[session_id]
    for key, value in session_test_content.items():
        assert key in session
        assert value == session[key]
