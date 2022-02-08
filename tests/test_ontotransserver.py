"""Test OTE Client."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Optional, Union

    from otelib.ontotransserver import OntoTransServer

    from .conftest import HTTPMethod, ResourceType

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


@pytest.mark.usefixtures("mock_session")
def test_create_dataresource(
    dataresource_data: "Dict[str, Any]",
    server: "OntoTransServer",
    ids: "Callable[[Union[ResourceType, str]], str]",
    mock_ote_response: "OTEResponse",
) -> None:
    """Test dataresource parse strategy."""
    import json

    # DataResource.create()
    mock_ote_response(
        method="post",
        endpoint="/dataresource/",
        data={"resource_id": ids("dataresource")},
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
        data=dataresource_data,
    )

    dataresource = server.create_dataresource(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )
    content = json.loads(dataresource.get())
    assert content == dataresource_data
