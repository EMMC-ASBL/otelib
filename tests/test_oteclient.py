"""Test OTE Client."""
# pylint: disable=protected-access,invalid-name,too-many-arguments
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, List, Optional, Tuple, Union

    from otelib.client import OTEClient
    from otelib.strategies.abc import AbstractStrategy
    from tests.conftest import HTTPMethod, ResourceType

    OTEResponse = Callable[
        [
            Union[HTTPMethod, str],
            str,
            Optional[Union[Dict[str, Any], str]],
            Optional[Union[dict, str]],
            Optional[OTEClient],
        ],
        None,
    ]


TEST_DATA = {
    "dataresource": {
        "content": {
            "firstName": "Joe",
            "lastName": "Jackson",
            "gender": "male",
            "age": 28,
            "address": {
                "streetAddress": "101",
                "city": "San Diego",
                "state": "CA",
            },
            "phoneNumbers": [{"type": "home", "number": "7349282382"}],
        }
    },
    "filter": {"sqlquery": "DROP TABLE myTable;"},
    "mapping": {
        "prefixes": {
            "map": "http://example.org/0.0.1/mapping_ontology#",
            "onto": "http://example.org/0.2.1/ontology#",
        },
        "triples": [
            ["http://onto-ns.com/meta/1.0/Foo#a", "map:mapsTo", "onto:A"],
            ["http://onto-ns.com/meta/1.0/Foo#b", "map:mapsTo", "onto:B"],
            ["http://onto-ns.com/meta/1.0/Bar#a", "map:mapsTo", "onto:C"],
        ],
    },
    "transformation": {"data": {}},
}


@pytest.fixture
def testdata(
    resource_type_cls: "ResourceType",
) -> "Callable[[Union[ResourceType, str]], dict]":
    """Test data for OTE resource."""
    ResourceType = resource_type_cls

    def _testdata(resource_type: "Union[ResourceType, str]") -> dict:
        """Return test data for a given resource."""
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.SESSION:
            raise ValueError("No test data available for a session.")

        return TEST_DATA[resource_type.value]

    return _testdata


def strategy_create_kwargs() -> "List[Tuple[str, Dict[str, Any]]]":
    """Strategy to creation key-word-arguments."""
    from tests.conftest import ResourceType

    return [
        (
            ResourceType.DATARESOURCE.value,
            {
                "downloadUrl": "https://filesamples.com/samples/code/json/sample2.json",
                "mediaType": "application/json",
            },
        ),
        (
            ResourceType.FILTER.value,
            {
                "filterType": "filter/sql",
                "query": TEST_DATA[ResourceType.FILTER.value]["sqlquery"],
            },
        ),
        (
            ResourceType.MAPPING.value,
            {
                "mappingType": "triples",
                **TEST_DATA[ResourceType.MAPPING.value],
            },
        ),
        (
            ResourceType.TRANSFORMATION.value,
            {
                "transformationType": "celery/remote",
                "configuration": {
                    "task_name": "test-task",
                    "args": [],
                },
            },
        ),
    ]


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
    """Test creating any strategy."""
    import json

    import requests

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
        return_json=(testdata(strategy) if strategy in ("filter", "mapping") else {}),
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
    )

    # Session content
    mock_ote_response(
        method="get",
        endpoint=f"/session/{ids('session')}",
        return_json=testdata(strategy),
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
    ), f"Session ID not found in {strategy} ! Is OTEAPI_DEBUG not set?"
    content_session = requests.get(
        f"{created_strategy.url}{created_strategy.settings.prefix}"
        f"/session/{created_strategy._session_id}"
    )
    session: "Dict[str, Any]" = content_session.json()
    for key, value in testdata(strategy).items():
        assert key in session
        assert value == session[key]
