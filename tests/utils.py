"""Utility functions for tests."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Tuple


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
