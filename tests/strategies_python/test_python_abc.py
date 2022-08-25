"""Tests for `otelib.strategies.abc`."""
# pylint: disable=too-many-arguments,too-many-locals,protected-access
from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Union

    from requests_mock import Mocker

    from otelib.backends.services.abc import AbstractStrategy
    from tests.conftest import OTEResponse, ResourceType


@pytest.mark.parametrize(
    "strategy_name,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
def test_get(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    server_url: str,
    strategy_name: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test `AbstractStrategy.get()`."""
    if strategy_name == "function":
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    import requests

    from oteapi.plugins import load_strategies
    load_strategies()
    from otelib.backends import python as strategies



    strategy_name_map = {"dataresource": "DataResource"}

    strategy: "AbstractStrategy" = getattr(
        strategies, strategy_name_map.get(strategy_name, strategy_name.capitalize())
    )(server_url)

    # This is a kind of hacky way to clear the cache and should probably 
    # be done in an automatic fashion
    strategy.cache.clear()

    # We must create the strategy - getting a strategy ID
    strategy.create(**create_kwargs)
    assert strategy.id

    content = strategy.get()
    if strategy_name in ("filter", "mapping"):
        assert json.loads(content) == {}
    else:
        assert json.loads(content) == testdata(strategy_name)

    # The testdata should always be in the full session
    assert (
        strategy._session_id
    ), f"Session ID not found in {strategy_name} ! Is OTEAPI_DEBUG not set?"
    session_ids = [x for x in strategy.cache if 'session' in x]
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
    