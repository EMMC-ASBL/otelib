"""Test OTE Client."""
# pylint: disable=protected-access,invalid-name,too-many-arguments,too-many-locals
from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Union

    from otelib.client import OTEClient
    from otelib.strategies.abc import AbstractStrategy
    from tests.conftest import OTEResponse, ResourceType


@pytest.mark.parametrize("backend", ["services", "python"])
@pytest.mark.parametrize(
    "strategy,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
@pytest.mark.usefixtures("mock_session")
def test_create_strategies(  #
    backend: str,
    client: "OTEClient",
    ids: "Callable[[Union[ResourceType, str]], str]",
    mock_ote_response: "OTEResponse",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    strategy: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test creating any strategy and calling it's `get()` method."""
    if strategy == "function" and "example" not in client.url:
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    import requests

    if backend == "python":
        # This is probably not the most elegant way to
        # switch clients...
        from otelib.client import OTEPythonClient

        client = OTEPythonClient("python")

        from oteapi.plugins import load_strategies

        load_strategies()

        from otelib.backends.python.base import Cache

        Cache().clear()  # Cleanup the cache from other tests
        if strategy == "function":
            pytest.skip("No function strategy exists in oteapi-core yet.")

    # create()
    mock_ote_response(
        method="post",
        endpoint=f"/{strategy}",
        return_json={
            f"{strategy[len('data'):] if strategy.startswith('data') else strategy}"
            "_id": ids(strategy)
        },
        backend=backend,
    )

    # initialize()
    # The filter and mapping returns everything from their `initialize()` method.
    mock_ote_response(
        method="post",
        endpoint=f"/{strategy}/{ids(strategy)}/initialize",
        params={"session_id": ids("session")},
        return_json=(testdata(strategy) if strategy in ("filter", "mapping") else {}),
        backend=backend,
    )

    # fetch()
    # The data resource and transformation returns everything from their `get()`
    # method.
    mock_ote_response(
        method="get",
        endpoint=f"/{strategy}/{ids(strategy)}",
        params={"session_id": ids("session")},
        return_json=(
            testdata(strategy) if strategy in ("dataresource", "transformation") else {}
        ),
        backend=backend,
    )

    # Session content
    mock_ote_response(
        method="get",
        endpoint=f"/session/{ids('session')}",
        return_json=testdata(strategy),
        backend=backend,
    )

    created_strategy: "AbstractStrategy" = getattr(client, f"create_{strategy}")(
        **create_kwargs
    )

    content = created_strategy.get()
    if strategy in ("filter", "mapping"):
        assert json.loads(content) == {}
    else:
        assert json.loads(content) == testdata(strategy)

    # The testdata should always be in the full session
    assert (
        created_strategy._session_id
    ), f"Session ID not found in {created_strategy} ! Is OTEAPI_DEBUG not set?"
    if backend == "services":
        strategy_prefix = created_strategy.settings.prefix
        startegy_sessionid = created_strategy._session_id
        content_session = requests.get(
            f"{created_strategy.url}{strategy_prefix}/session/{startegy_sessionid}"
        )
        session: "Dict[str, Any]" = content_session.json()
    elif backend == "python":
        session_ids = [x for x in created_strategy.cache if "session" in x]
        assert len(session_ids) == 1
        session_id = session_ids[0]
        session = created_strategy.cache[session_id]

    for key, value in testdata(strategy).items():
        if strategy == "mapping" and backend == "python":
            pytest.skip("Issues with tuple/list conversion json for python backend")
        assert key in session
        assert value == session[key]
