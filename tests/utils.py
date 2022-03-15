"""Utility functions for tests."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Dict, List, Tuple


def strategy_create_kwargs() -> "List[Tuple[str, Dict[str, Any]]]":
    """Strategy to creation key-word-arguments."""
    from conftest import TEST_DATA, ResourceType

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
