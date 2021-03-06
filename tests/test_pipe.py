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
@pytest.mark.usefixtures("mock_session")
def test_pipe(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    server_url: str,
    strategy_name: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test creating a `Pipe` and run the `get()` method."""
    if strategy_name == "function" and "example" not in server_url:
        pytest.skip("No function strategy exists in oteapi-core yet.")

    import json

    import requests

    from otelib import strategies
    from otelib.pipe import Pipe

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
    content_session = requests.get(
        f"{strategy.url}{strategy.settings.prefix}" f"/session/{strategy._session_id}"
    )
    session: "Dict[str, Any]" = content_session.json()
    for key, value in testdata(strategy_name).items():
        assert key in session
        assert value == session[key]


@pytest.mark.usefixtures("mock_session")
def test_pipeing_strategies(
    mock_ote_response: "OTEResponse",
    ids: "Callable[[Union[ResourceType, str]], str]",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    server_url: str,
) -> None:
    """A simple pipeline will be tested."""
    import json

    import requests

    from otelib.strategies import DataResource, Filter

    # create()
    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        return_json={"resource_id": ids("dataresource")},
    )
    mock_ote_response(
        method="post",
        endpoint="/filter",
        return_json={"filter_id": ids("filter")},
    )

    # initialize()
    mock_ote_response(
        method="post",
        endpoint=f"/dataresource/{ids('dataresource')}/initialize",
        params={"session_id": ids("session")},
        return_json={},
    )
    mock_ote_response(
        method="post",
        endpoint=f"/filter/{ids('filter')}/initialize",
        params={"session_id": ids("session")},
        return_json=testdata("filter"),
    )

    # fetch()
    mock_ote_response(
        method="get",
        endpoint=f"/dataresource/{ids('dataresource')}",
        params={"session_id": ids("session")},
        return_json=testdata("dataresource"),
    )
    mock_ote_response(
        method="get",
        endpoint=f"/filter/{ids('filter')}",
        params={"session_id": ids("session")},
        return_json={},
    )

    # Session content
    session_test_content = testdata("filter")
    session_test_content.update(testdata("dataresource"))
    mock_ote_response(
        method="get",
        endpoint=f"/session/{ids('session')}",
        return_json=session_test_content,
    )

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

    # All the test data should however be present in the session
    assert (
        pipeline._session_id
    ), f"Session ID not found in {pipeline} ! Is OTEAPI_DEBUG not set?"
    content_session = requests.get(
        f"{pipeline.url}{pipeline.settings.prefix}/session/{pipeline._session_id}"
    )
    session: "Dict[str, Any]" = content_session.json()
    for key, value in session_test_content.items():
        assert key in session
        assert value == session[key]

    ##
    # Reverse the pipeline and try again
    ##

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

    # Since the "last" strategy now returns something from its `get()` method,
    # this can be tested.
    assert json.loads(content) == testdata("dataresource")

    # All the test data should however be present in the session
    assert (
        pipeline._session_id
    ), f"Session ID not found in {pipeline} ! Is OTEAPI_DEBUG not set?"
    content_session = requests.get(
        f"{pipeline.url}{pipeline.settings.prefix}" f"/session/{pipeline._session_id}"
    )
    session: "Dict[str, Any]" = content_session.json()
    for key, value in session_test_content.items():
        assert key in session
        assert value == session[key]
