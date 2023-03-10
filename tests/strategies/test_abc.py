"""Tests for `otelib.strategies.abc`."""
# pylint: disable=too-many-arguments,too-many-locals,protected-access
from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Union

    from requests_mock import Mocker

    from otelib.backends.python.base import BasePythonStrategy
    from otelib.backends.services.base import BaseServicesStrategy

    from ..conftest import OTEResponse, ResourceType

    BaseStrategy = Union[BasePythonStrategy, BaseServicesStrategy]


@pytest.mark.parametrize(
    "strategy_name,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
@pytest.mark.usefixtures("mock_session")
def test_get(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    server_url: str,
    strategy_name: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test `AbstractStrategy.get()`."""
    if strategy_name == "function":
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import importlib
    import json

    import requests

    strategies = importlib.import_module(f"otelib.backends.{backend}")
    server_url = server_url if backend != "python" else backend

    if backend == "services":
        # Mock URL responses

        ## create()
        mock_ote_response(
            method="post",
            endpoint=f"/{strategy_name}",
            return_json={
                f"{strategy_name[len('data'):] if strategy_name.startswith('data') else strategy_name}"  # pylint: disable=line-too-long
                "_id": ids(strategy_name)
            },
        )

        # initialize()
        # The filter and mapping returns everything from their `initialize()` method.
        mock_ote_response(
            method="post",
            endpoint=f"/{strategy_name}/{ids(strategy_name)}/initialize",
            params={"session_id": ids("session")},
            return_json=(
                testdata(strategy_name)
                if strategy_name in ("filter", "mapping")
                else {}
            ),
        )

        # fetch()
        # The data resource and transformation returns everything from their `get()`
        # method.
        mock_ote_response(
            method="get",
            endpoint=f"/{strategy_name}/{ids(strategy_name)}",
            params={"session_id": ids("session")},
            return_json=(
                testdata(strategy_name)
                if strategy_name in ("dataresource", "transformation")
                else {}
            ),
        )

        # Session content
        mock_ote_response(
            method="get",
            endpoint=f"/session/{ids('session')}",
            return_json=testdata(strategy_name),
        )

    strategy_name_map = {"dataresource": "DataResource"}

    strategy: "BaseStrategy" = getattr(
        strategies, strategy_name_map.get(strategy_name, strategy_name.capitalize())
    )(server_url)

    # We must create the strategy - getting a strategy ID
    strategy.create(**create_kwargs)
    assert strategy.strategy_id

    # There must be a strategy name associated with the strategy
    assert strategy.strategy_name == strategy_name

    content = strategy.get()
    assert isinstance(content, bytes)
    if strategy_name in ("filter", "mapping"):
        assert json.loads(content) == {}
    elif (
        strategy_name in ("transformation",)
        and backend == "services"
        and "example" not in server_url
    ):
        # Real backend !
        # Dynamic response content - just check keys are the same and values are
        # non-empty
        _content: "dict[str, Any]" = json.loads(content)
        assert list(_content) == list(testdata(strategy_name))
        assert all(_content.values())
    else:
        assert json.loads(content) == testdata(strategy_name)

    ## The testdata should always be in the full session
    assert (
        strategy._session_id
    ), f"Session ID not found in {strategy_name} ! Is OTEAPI_DEBUG not set?"

    if backend == "services":
        content_session = requests.get(
            f"{strategy.url}{strategy.settings.prefix}/session/{strategy._session_id}",
            timeout=30,
        )
        session: "Dict[str, Any]" = content_session.json()
    elif backend == "python":
        session_ids = [x for x in strategy.cache if "session" in x]
        assert len(session_ids) == 1
        session_id = session_ids[0]
        session = strategy.cache[session_id]

    for key, value in testdata(strategy_name).items():
        assert key in session

        if strategy_name == "mapping" and key == "triples":
            # The mapping strategy's "triples" key has a Set type value
            session_triples = sorted(list(triple) for triple in session[key])
            assert sorted(value) == session_triples
        elif (
            strategy_name == "transformation"
            and key == "celery_task_id"
            and "example" not in server_url
        ):
            # The task ID is dynamically generated.
            # Simply check the value is non-empty
            assert key in session and session[key]
        else:
            assert value == session[key]


@pytest.mark.parametrize(
    "strategy_name,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
def test_services_get_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    strategy_name: str,
    create_kwargs: "Dict[str, Any]",
    requests_mock: "Mocker",
) -> None:
    """Check `AbstractStrategy.get()` raises `ApiError` upon request failure."""
    from otelib.backends import services as strategies
    from otelib.exceptions import ApiError
    from otelib.settings import Settings

    wrong_url = "https://non.existing.url.org"

    # create()
    mock_ote_response(
        method="post",
        endpoint=f"/{strategy_name}",
        return_json={
            f"{strategy_name[len('data'):] if strategy_name.startswith('data') else strategy_name}"  # pylint: disable=line-too-long
            "_id": ids(strategy_name)
        },
    )

    # Creating a session
    requests_mock.post(
        f"{wrong_url}{Settings().prefix}/session",
        status_code=500,
        content=b"Internal Server Error",
    )

    strategy_name_map = {"dataresource": "DataResource"}

    strategy: "BaseStrategy" = getattr(
        strategies, strategy_name_map.get(strategy_name, strategy_name.capitalize())
    )(server_url)

    # We must create the strategy - getting a strategy ID
    strategy.create(**create_kwargs)
    assert strategy.strategy_id

    with pytest.raises(ApiError, match=f"^{ApiError.__name__}.*"):
        # Change `url` attribute to hit a wrong URL and raise
        strategy.url = wrong_url
        strategy.get()
