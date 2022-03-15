"""Tests for `otelib.strategies.abc`."""
# pylint: disable=too-many-arguments,too-many-locals,protected-access
from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Union

    from requests_mock import Mocker

    from otelib.strategies.abc import AbstractStrategy
    from tests.conftest import OTEResponse, ResourceType


@pytest.mark.parametrize(
    "strategy_name,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
@pytest.mark.usefixtures("mock_session")
def test_get(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    server_url: str,
    strategy_name: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test `AbstractStrategy.get()`."""
    import json

    import requests

    from otelib import strategies

    # create()
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
            testdata(strategy_name) if strategy_name in ("filter", "mapping") else {}
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

    strategy_name_map = {
        "dataresource": "DataResource",
        "filter": "Filter",
        "mapping": "Mapping",
        "transformation": "Transformation",
    }

    strategy: "AbstractStrategy" = getattr(
        strategies, strategy_name_map[strategy_name]
    )(server_url)

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
    content_session = requests.get(
        f"{strategy.url}{strategy.settings.prefix}/session/{strategy._session_id}"
    )
    session: "Dict[str, Any]" = content_session.json()
    for key, value in testdata(strategy_name).items():
        assert key in session
        assert value == session[key]


@pytest.mark.parametrize(
    "strategy_name,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
def test_get_fails(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    server_url: str,
    strategy_name: str,
    create_kwargs: "Dict[str, Any]",
    requests_mock: "Mocker",
) -> None:
    """Check `AbstractStrategy.get()` raises `ApiError` upon request failure."""
    from otelib import strategies
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

    strategy_name_map = {
        "dataresource": "DataResource",
        "filter": "Filter",
        "mapping": "Mapping",
        "transformation": "Transformation",
    }

    strategy: "AbstractStrategy" = getattr(
        strategies, strategy_name_map[strategy_name]
    )(server_url)

    # We must create the strategy - getting a strategy ID
    strategy.create(**create_kwargs)
    assert strategy.id

    with pytest.raises(ApiError, match="APIError"):
        # Change `url` attribute to hit a wrong URL and raise
        strategy.url = wrong_url
        strategy.get()
