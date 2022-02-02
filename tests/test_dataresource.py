"""Test parse strategies."""


def test_dataresource():
    """Test dataresource parse strategy."""
    import json
    from otelib import Server

    data = {
        "firstName": "Joe",
        "lastName": "Jackson",
        "gender": "male",
        "age": 28,
        "address": {"streetAddress": "101", "city": "San Diego", "state": "CA"},
        "phoneNumbers": [{"type": "home", "number": "7349282382"}],
    }
    OTEServer = Server('http://localhost:80')
    dataresource = OTEServer.create_dataresource(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="text/json",
    )
    content = json.loads(dataresource.get())
    assert content == data
