"""Test the `otelib.pipe` module."""

from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Union

    from requests_mock import Mocker

    from otelib.backends import python as python_backend
    from otelib.backends import services as services_backend
    from otelib.backends.python.base import BasePythonStrategy
    from otelib.backends.services.base import BaseServicesStrategy

    from .conftest import OTEResponse, Testdata, TestResourceIds

    BaseStrategy = Union[BasePythonStrategy, BaseServicesStrategy]

    DataResource = Union[python_backend.DataResource, services_backend.DataResource]
    Parser = Union[python_backend.Parser, services_backend.DataResource]
    Filter = Union[python_backend.Filter, services_backend.Filter]


@pytest.mark.parametrize(
    "strategy_name,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
@pytest.mark.usefixtures("mock_session")
def test_pipe(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "TestResourceIds",
    testdata: "Testdata",
    server_url: str,
    strategy_name: str,
    create_kwargs: "dict[str, Any]",
    requests_mock: "Mocker",
) -> None:
    """Test creating a `Pipe` and run the `get()` method."""
    if strategy_name == "function":
        if backend == "services" and "example" in server_url:
            pass
        else:
            pytest.skip("No function strategy exists in oteapi-core yet.")

    import importlib
    import json

    import requests

    from otelib.pipe import Pipe

    strategies = importlib.import_module(f"otelib.backends.{backend}")
    server_url = server_url if backend != "python" else backend

    if backend == "services":
        # Mock URL responses

        # create()
        mock_ote_response(
            method="post",
            endpoint=f"/{strategy_name}",
            response_json={
                f"{strategy_name[len('data'):] if strategy_name.startswith('data') else strategy_name}"  # noqa: E501
                "_id": ids(strategy_name)
            },
        )

        # initialize()
        # The filter and mapping returns everything from their `initialize()` method.
        mock_ote_response(
            method="post",
            endpoint=f"/{strategy_name}/{ids(strategy_name)}/initialize",
            params={"session_id": ids("session")},
            response_json=(
                testdata(strategy_name)
                if strategy_name in ("filter", "mapping")
                else {}
            ),
        )

        # fetch()
        # The data resource, parser and transformation returns everything from their `get()`
        # method.
        mock_ote_response(
            method="get",
            endpoint=f"/{strategy_name}/{ids(strategy_name)}",
            params={"session_id": ids("session")},
            response_json=(
                testdata(strategy_name)
                if strategy_name in ("dataresource", "transformation", "parser")
                else {}
            ),
        )

        # Session content
        mock_ote_response(
            method="get",
            endpoint=f"/session/{ids('session')}",
            response_json=testdata(strategy_name),
        )

    if backend == "python" and strategy_name == "parser":
        # Mock URL responses to ensure we don't hit the real (external) URL
        requests_mock.request(
            method="get",
            url=create_kwargs["configuration"]["downloadUrl"],
            status_code=200,
            json=testdata(strategy_name, "get")["content"],
        )

    strategy_name_map = {"dataresource": "DataResource", "parser": "Parser"}

    strategy: "BaseStrategy" = getattr(
        strategies, strategy_name_map.get(strategy_name, strategy_name.capitalize())
    )(server_url)

    # We must create the strategy - getting a strategy ID
    strategy.create(**create_kwargs)
    assert strategy.strategy_id

    pipe = Pipe(strategy)

    content = pipe.get()
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

    # The testdata should always be in the full session
    if backend == "services":
        content_session = requests.get(
            f"{strategy.url}{strategy.settings.prefix}/session/{strategy._session_id}",
            timeout=30,
        )
        session: "dict[str, Any]" = content_session.json()
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


@pytest.mark.usefixtures("mock_session")
def test_pipeing_strategies(
    backend: str,
    mock_ote_response: "OTEResponse",
    ids: "TestResourceIds",
    testdata: "Testdata",
    server_url: str,
    requests_mock: "Mocker",
) -> None:
    """A simple pipeline will be tested."""
    import importlib
    import json

    import requests

    strategies = importlib.import_module(f"otelib.backends.{backend}")
    server_url = server_url if backend != "python" else backend

    session_test_content = testdata("filter")
    session_test_content.update(testdata("dataresource"))

    if backend == "services":
        # Mock URL responses

        # create()
        mock_ote_response(
            method="post",
            endpoint="/dataresource",
            response_json={"resource_id": ids("dataresource")},
        )
        mock_ote_response(
            method="post",
            endpoint="/parser",
            response_json={"parser_id": ids("parser")},
        )
        mock_ote_response(
            method="post",
            endpoint="/filter",
            response_json={"filter_id": ids("filter")},
        )

        # initialize()
        mock_ote_response(
            method="post",
            endpoint=f"/dataresource/{ids('dataresource')}/initialize",
            params={"session_id": ids("session")},
            response_json={},
        )
        mock_ote_response(
            method="post",
            endpoint=f"/parser/{ids('parser')}/initialize",
            params={"session_id": ids("session")},
            response_json={},
        )
        mock_ote_response(
            method="post",
            endpoint=f"/filter/{ids('filter')}/initialize",
            params={"session_id": ids("session")},
            response_json=testdata("filter"),
        )

        # fetch()
        mock_ote_response(
            method="get",
            endpoint=f"/dataresource/{ids('dataresource')}",
            params={"session_id": ids("session")},
            response_json=testdata("dataresource"),
        )
        mock_ote_response(
            method="get",
            endpoint=f"/parser/{ids('parser')}",
            params={"session_id": ids("session")},
            response_json=testdata("parser"),
        )
        mock_ote_response(
            method="get",
            endpoint=f"/filter/{ids('filter')}",
            params={"session_id": ids("session")},
            response_json={},
        )

        # Session content
        mock_ote_response(
            method="get",
            endpoint=f"/session/{ids('session')}",
            response_json=session_test_content,
        )

    if backend == "python":
        # Mock URL responses to ensure we don't hit the real (external) URL
        requests_mock.request(
            method="get",
            url=dict(strategy_create_kwargs())["parser"]["configuration"][
                "downloadUrl"
            ],
            status_code=200,
            json=testdata("parser", "get")["content"],
        )

    strategy_kwargs = {}
    if backend == "python":
        # Setup custom cache
        cache = {}
        strategy_kwargs["cache"] = cache

    data_resource: "DataResource" = strategies.DataResource(
        server_url, **strategy_kwargs
    )
    parser: "Parser" = strategies.Parser(server_url, **strategy_kwargs)
    filter: "Filter" = strategies.Filter(server_url, **strategy_kwargs)

    # We must create the data resource and filter - getting IDs
    create_kwargs = dict(strategy_create_kwargs())
    data_resource.create(**create_kwargs["dataresource"])
    assert data_resource.strategy_id
    parser.create(**create_kwargs["parser"])
    assert parser.strategy_id
    filter.create(**create_kwargs["filter"])
    assert filter.strategy_id

    pipeline = data_resource >> parser >> filter

    content = pipeline.get()

    # Since the "last" strategy does not return anything from its `get()` method,
    # this should return an empty dictionary.
    assert json.loads(content) == {}

    # All the test data should however be present in the session
    assert (
        pipeline._session_id
    ), f"Session ID not found in {pipeline} ! Is OTEAPI_DEBUG not set?"

    if backend == "services":
        content_session = requests.get(
            f"{pipeline.url}{pipeline.settings.prefix}/session/{pipeline._session_id}",
            timeout=30,
        )
        session: "dict[str, Any]" = content_session.json()
    elif backend == "python":
        session_ids = [x for x in pipeline.cache if "session" in x]
        assert len(session_ids) == 1
        session_id = session_ids[0]
        session = pipeline.cache[session_id]
    for key, value in session_test_content.items():
        assert key in session
        assert value == session[key]

    ##
    # Reverse the pipeline and try again
    ##
    strategy_kwargs = {}
    if backend == "python":
        # Setup custom cache
        cache = {}
        strategy_kwargs["cache"] = cache

    data_resource: "DataResource" = strategies.DataResource(
        server_url, **strategy_kwargs
    )
    filter: "Filter" = strategies.Filter(server_url, **strategy_kwargs)

    # We must create the data resource and filter - getting IDs
    create_kwargs = dict(strategy_create_kwargs())
    data_resource.create(**create_kwargs["dataresource"])
    assert data_resource.strategy_id
    filter.create(**create_kwargs["filter"])
    assert filter.strategy_id

    pipeline = filter >> data_resource

    content = pipeline.get()

    # Since the "last" strategy now returns something from its `get()` method,
    # this can be tested.
    assert json.loads(content) == testdata("dataresource")

    # All the test data should however be present in the session
    assert (
        pipeline._session_id
    ), f"Session ID not found in {pipeline} ! Is OTEAPI_DEBUG not set?"

    if backend == "services":
        content_session = requests.get(
            f"{pipeline.url}{pipeline.settings.prefix}/session/{pipeline._session_id}",
            timeout=30,
        )
        session: "dict[str, Any]" = content_session.json()
    elif backend == "python":
        session_ids = [x for x in pipeline.cache if "session" in x]
        assert len(session_ids) == 1
        session_id = session_ids[0]
        session = pipeline.cache[session_id]
    for key, value in session_test_content.items():
        assert key in session
        assert value == session[key]


def test_pipeing_concatenate(
    backend: str,
    server_url: str,
) -> None:
    """Tests for the correct chaining of resources and filters in a pipeline.
    This function tests for issue 110: https://github.com/EMMC-ASBL/otelib/issues/110
    """

    import importlib

    strategies = importlib.import_module(f"otelib.backends.{backend}")
    server_url = server_url if backend != "python" else backend

    strategy_kwargs = {}
    if backend == "python":
        # Setup custom cache
        cache = {}
        strategy_kwargs["cache"] = cache

    data_resource1: "DataResource" = strategies.DataResource(
        server_url, **strategy_kwargs
    )
    dataid1 = data_resource1.strategy_id
    parser1: "Parser" = strategies.Parser(server_url, **strategy_kwargs)
    parserid1 = parser1.strategy_id
    filter1: "Filter" = strategies.Filter(server_url, **strategy_kwargs)
    filterid1 = filter1.strategy_id
    pipeline1 = data_resource1 >> parser1 >> filter1

    data_resource2: "DataResource" = strategies.DataResource(
        server_url, **strategy_kwargs
    )
    dataid2 = data_resource2.strategy_id
    parser2: "Parser" = strategies.Parser(server_url, **strategy_kwargs)
    parserid2 = parser2.strategy_id
    filter2: "Filter" = strategies.Filter(server_url, **strategy_kwargs)
    filterid2 = filter2.strategy_id
    pipeline2 = data_resource2 >> filter2

    pipeline_combined = pipeline1 >> parser2 >> pipeline2

    # confirm that we can retrieve the strategy ids
    pipeline_tail = pipeline_combined  # or should it be pipeline head?
    assert pipeline_tail.strategy_id == dataid1
    pipeline_tail = pipeline_tail.input_pipe.input
    assert pipeline_tail.strategy_id == parserid1
    pipeline_tail = pipeline_tail.input_pipe.input
    assert pipeline_tail.strategy_id == filterid1
    pipeline_tail = pipeline_tail.input_pipe.input
    assert pipeline_tail.strategy_id == dataid2
    pipeline_tail = pipeline_tail.input_pipe.input
    assert pipeline_tail.strategy_id == parserid2
    pipeline_tail = pipeline_tail.input_pipe.input
    assert pipeline_tail.strategy_id == filterid2
