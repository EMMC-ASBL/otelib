"""Test OTE Client."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Optional, Union

    from otelib.ontotransserver import OntoTransServer
    from tests.conftest import HTTPMethod, ResourceType

    OTEResponse = Callable[
        [
            Union[HTTPMethod, str],
            str,
            Optional[Union[Dict[str, Any], str]],
            Optional[Union[dict, str]],
            Optional[OntoTransServer],
        ],
        None,
    ]


@pytest.fixture
def testdata() -> "Callable[[Union[ResourceType, str]], dict]":
    """Test data for OTE resource."""
    from tests.conftest import ResourceType

    def _testdata(resource_type: "Union[ResourceType, str]") -> dict:
        """Return test data for a given resource."""
        resource_type = ResourceType(resource_type)
        if resource_type == ResourceType.RESOURCE:
            resource_type = ResourceType.DATARESOURCE
        if resource_type == ResourceType.SESSION:
            raise ValueError("No test data available for a session.")

        return {
            ResourceType.DATARESOURCE: {
                "firstName": "Joe",
                "lastName": "Jackson",
                "gender": "male",
                "age": 28,
                "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
                "phoneNumbers": [{"type": "home", "number": "7349282382"}],
            },
            ResourceType.FILTER: {},
            ResourceType.MAPPING: {},
            ResourceType.TRANSFORMATION: {},
        }[resource_type]

    return _testdata


@pytest.mark.usefixtures("mock_session")
def test_create_dataresource(
    server: "OntoTransServer",
    ids: "Callable[[Union[ResourceType, str]], str]",
    mock_ote_response: "OTEResponse",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test creating a dataresource."""
    import json

    # DataResource.create()
    mock_ote_response(
        method="post",
        endpoint="/dataresource/",
        return_json={"resource_id": ids("dataresource")},
    )

    # DataResource.initialize()
    mock_ote_response(
        method="post",
        endpoint=f"/dataresource/{ids('dataresource')}/initialize",
        params={"session_id": ids("session")},
    )

    # DataResource.fetch()
    mock_ote_response(
        method="get",
        endpoint=f"/dataresource/{ids('dataresource')}",
        params={"session_id": ids("session")},
        return_json=testdata("dataresource"),
    )

    dataresource = server.create_dataresource(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="text/json",
    )
    content = json.loads(dataresource.get())
    assert content == testdata("dataresource")


@pytest.mark.usefixtures("mock_session")
def test_create_filter(
    server: "OntoTransServer",
    ids: "Callable[[Union[ResourceType, str]], str]",
    mock_ote_response: "OTEResponse",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test creating a filter."""
    import json

    sql_query = "DROP TABLE myTable;"

    # Filter.create()
    mock_ote_response(
        method="post",
        endpoint="/filter",
        return_json={"filter_id": ids("filter")},
    )

    # Filter.initialize()
    mock_ote_response(
        method="post",
        endpoint=f"/filter/{ids('filter')}/initialize",
        params={"session_id": ids("session")},
        return_json={"sqlquery": sql_query},
    )

    # Filter.fetch()
    mock_ote_response(
        method="get",
        endpoint=f"/filter/{ids('filter')}",
        params={"session_id": ids("session")},
    )

    # pylint: disable=redefined-builtin
    filter = server.create_filter(
        filterType="filter/sql",
        query=sql_query,
    )
    content = json.loads(filter.get())
    assert content == testdata("filter")