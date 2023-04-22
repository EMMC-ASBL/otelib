"""Test OTE Client."""
# pylint: disable=protected-access,invalid-name,too-many-arguments,too-many-locals
# pylint: disable=too-many-branches
from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Union

    from otelib.backends.python.base import BasePythonStrategy
    from otelib.backends.services.base import BaseServicesStrategy
    from otelib.client import OTEClient

    from .conftest import OTEResponse, ResourceType

    BaseStrategy = Union[BasePythonStrategy, BaseServicesStrategy]


@pytest.mark.parametrize(
    "strategy,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
@pytest.mark.usefixtures("mock_session")
def test_create_strategies(
    client: "OTEClient",
    ids: "Callable[[Union[ResourceType, str]], str]",
    mock_ote_response: "OTEResponse",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    strategy: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test creating any strategy and calling it's `get()` method."""
    import json

    import requests

    if strategy == "function":
        if client._impl._backend == "services" and "example" in client.url:
            pass
        else:
            pytest.skip("No function strategy exists in oteapi-core yet.")

    backend = client._impl._backend

    if backend == "services":
        # Mock URL responses

        # create()
        mock_ote_response(
            method="post",
            endpoint=f"/{strategy}",
            return_json={
                f"{strategy[len('data'):] if strategy.startswith('data') else strategy}"
                "_id": ids(strategy)
            },
        )

        # initialize()
        # The filter and mapping returns everything from their `initialize()` method.
        mock_ote_response(
            method="post",
            endpoint=f"/{strategy}/{ids(strategy)}/initialize",
            params={"session_id": ids("session")},
            return_json=(
                testdata(strategy) if strategy in ("filter", "mapping") else {}
            ),
        )

        # fetch()
        # The data resource and transformation returns everything from their `get()`
        # method.
        mock_ote_response(
            method="get",
            endpoint=f"/{strategy}/{ids(strategy)}",
            params={"session_id": ids("session")},
            return_json=(
                testdata(strategy)
                if strategy in ("dataresource", "transformation")
                else {}
            ),
        )

        # Session content
        mock_ote_response(
            method="get",
            endpoint=f"/session/{ids('session')}",
            return_json=testdata(strategy),
        )

    created_strategy: "BaseStrategy" = getattr(client, f"create_{strategy}")(
        **create_kwargs
    )

    content = created_strategy.get()
    if strategy in ("filter", "mapping"):
        assert json.loads(content) == {}
    elif (
        strategy in ("transformation",)
        and client._impl._backend == "services"
        and "example" not in client.url
    ):
        # Real backend !
        # Dynamic response content - just check keys are the same and values are
        # non-empty
        _content: "dict[str, Any]" = json.loads(content)
        assert list(_content) == list(testdata(strategy))
        assert all(_content.values())
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
            f"{created_strategy.url}{strategy_prefix}/session/{startegy_sessionid}",
            timeout=30,
        )
        session: "Dict[str, Any]" = content_session.json()

    elif backend == "python":
        session_ids = [
            cache_key for cache_key in created_strategy.cache if "session" in cache_key
        ]
        assert len(session_ids) == 1
        session = created_strategy.cache[session_ids[0]]

    for key, value in testdata(strategy).items():
        assert key in session

        if strategy == "mapping" and key == "triples":
            # The mapping strategy's "triples" key has a Set type value
            session_triples = sorted(list(triple) for triple in session[key])
            assert sorted(value) == session_triples
        elif (
            strategy == "transformation"
            and key == "celery_task_id"
            and "example" not in client.url
        ):
            # The task ID is dynamically generated.
            # Simply check the value is non-empty
            assert key in session and session[key]
        else:
            assert value == session[key]
