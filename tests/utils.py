"""Utility functions for tests."""
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Literal, Tuple


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
    "function": {},
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
    "transformation": {"celery_task_id": "some_task_id"},
}


class ResourceType(str, Enum):
    """Enumeration of resource types."""

    DATARESOURCE = "dataresource"
    FILTER = "filter"
    FUNCTION = "function"
    MAPPING = "mapping"
    SESSION = "session"
    TRANSFORMATION = "transformation"

    def get_idprefix(self) -> str:
        """Get the `IDPREFIX` used in oteapi-services."""
        return f"{self.value}-"

    def get_class_name(self) -> str:
        """Get the internal Python class name for the resource type."""
        if self == self.SESSION:
            raise ValueError("SESSION does not have a class name.")
        return {"dataresource": "DataResource"}.get(
            self.value, str(self.value).capitalize()
        )

    def get_return_id_key(self) -> str:
        """Return the expected key used to store in OTE Services session cache."""
        if self == self.DATARESOURCE:
            return "resource_id"
        return f"{self.value}_id"

    def map_method_to_data(self, method: "Literal['get', 'initialize']") -> bool:
        """Return whether a given method should return non-empty (test) data."""
        try:
            return (
                self
                in {
                    "get": [self.DATARESOURCE, self.FUNCTION, self.TRANSFORMATION],
                    "initialize": [self.FILTER, self.MAPPING],
                }[method]
            )
        except KeyError as exc:
            raise ValueError(
                "Only 'get' and 'initialize' methods are allowed."
            ) from exc


def strategy_create_kwargs() -> "List[Tuple[str, Dict[str, Any]]]":
    """Strategy to creation key-word-arguments."""
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
            ResourceType.FUNCTION.value,
            {
                "functionType": "function/demo",
                **TEST_DATA[ResourceType.FUNCTION.value],
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
