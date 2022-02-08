"""Test parse strategies."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from requests_mock import Mocker


def test_dataresource(requests_mock: "Mocker") -> None:
    """Test dataresource parse strategy."""
    import json

    from otelib.ontotransserver import OntoTransServer
    from otelib.settings import Settings

    data = {
        "firstName": "Joe",
        "lastName": "Jackson",
        "gender": "male",
        "age": 28,
        "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
        "phoneNumbers": [{"type": "home", "number": "7349282382"}],
    }
    resource_id = {"resource_id": "dataresource-test"}
    session_id = {"session_id": "sessions-test"}
    url_prefix = Settings().prefix

    server = OntoTransServer("http://example.org")

    # DataResource.create()
    requests_mock.post(
        f"{server.url}{url_prefix}/dataresource/",
        text=json.dumps(resource_id),
    )

    # AbstractStrategy.get() (DataResource.get())
    requests_mock.post(
        f"{server.url}{url_prefix}/session/",
        text=json.dumps(session_id),
    )

    # DataResource.initialize()
    requests_mock.post(
        f"{server.url}{url_prefix}/dataresource/{resource_id['resource_id']}/"
        f"initialize?session_id={session_id['session_id']}",
        text="{}",
    )

    # DataResource.fetch()
    requests_mock.get(
        f"{server.url}{url_prefix}/dataresource/{resource_id['resource_id']}"
        f"?session_id={session_id['session_id']}",
        text=json.dumps(data),
    )

    dataresource = server.create_dataresource(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="text/json",
    )
    content = json.loads(dataresource.get())
    assert content == data
