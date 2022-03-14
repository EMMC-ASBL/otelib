"""Test OTE Client."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Optional, Union

    from otelib.client import OTEClient
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
            ResourceType.FILTER: {"sqlquery": "DROP TABLE myTable;"},
            ResourceType.MAPPING: {},
            ResourceType.TRANSFORMATION: {},
        }[resource_type]

    return _testdata


@pytest.mark.usefixtures("mock_session")
def test_create_dataresource(
    client: "OTEClient",
    ids: "Callable[[Union[ResourceType, str]], str]",
    mock_ote_response: "OTEResponse",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test creating a dataresource."""
    import json

    # DataResource.create()
    mock_ote_response(
        method="post",
        endpoint="/dataresource",
        return_json={"resource_id": ids("dataresource")},
    )

    # DataResource.initialize()
    mock_ote_response(
        method="post",
        endpoint=f"/dataresource/{ids('dataresource')}/initialize",
        params={"session_id": ids("session")},
        return_json={},
    )

    # DataResource.fetch()
    mock_ote_response(
        method="get",
        endpoint=f"/dataresource/{ids('dataresource')}",
        params={"session_id": ids("session")},
        return_json=testdata("dataresource"),
    )

    dataresource = client.create_dataresource(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    # The data resource returns everything from it's `get()` method.
    # However, it should return anything from its `initalize()` method.
    content = dataresource.get()
    assert json.loads(content) == testdata("dataresource")

    content = dataresource.initialize(ids("session"))
    assert json.loads(content) == {}


@pytest.mark.usefixtures("mock_session")
def test_create_filter(
    client: "OTEClient",
    ids: "Callable[[Union[ResourceType, str]], str]",
    mock_ote_response: "OTEResponse",
    testdata: "Callable[[Union[ResourceType, str]], dict]",
) -> None:
    """Test creating a filter."""
    import json

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
        return_json=testdata("filter"),
    )

    # Filter.fetch()
    mock_ote_response(
        method="get",
        endpoint=f"/filter/{ids('filter')}",
        params={"session_id": ids("session")},
        return_json={},
    )

    # pylint: disable=redefined-builtin
    filter = client.create_filter(
        filterType="filter/sql",
        query=testdata("filter")["sqlquery"],
    )

    # The filter does not return anything from it's `get()` method.
    # Rather it returns its filter in the `initalize()` method.
    content = filter.get()
    assert json.loads(content) == {}

    content = filter.initialize(ids("session"))
    assert json.loads(content) == testdata("filter")
