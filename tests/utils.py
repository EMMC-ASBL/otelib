"""Utility functions for tests."""

import json
from pathlib import Path
from subprocess import run
from typing import TYPE_CHECKING

try:
    # For Python >= 3.11
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        """Pre-3.11 style string-Enums."""


if TYPE_CHECKING:
    from typing import Any, Literal

REPOSITORY_DIR = (Path(__file__).resolve().parent.parent).resolve()
STATIC_DIR = (Path(__file__).resolve().parent / "static").resolve()
HEAD_COMMIT_SHA = (
    run(["git", "rev-parse", "HEAD"], capture_output=True, check=True)
    .stdout.decode()
    .rstrip("\n")
)
path_to_sample_json = STATIC_DIR / "sample.json"
relative_posix_path_to_sample_json = path_to_sample_json.relative_to(
    REPOSITORY_DIR
).as_posix()

TEST_DATA = {
    "dataresource": {
        "downloadUrl": (
            "https://raw.githubusercontent.com/EMMC-ASBL/otelib"
            f"/{HEAD_COMMIT_SHA}/{relative_posix_path_to_sample_json}"
        ),
        "mediaType": "application/json",
    },
    "filter": {"sqlquery": "DROP TABLE myTable;"},
    "function": {},
    "parser": {"content": json.loads((STATIC_DIR / "sample.json").read_text())},
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


class ResourceType(StrEnum):
    """Enumeration of resource types."""

    DATARESOURCE = "dataresource"
    FILTER = "filter"
    PARSER = "parser"
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
                    "get": [
                        self.DATARESOURCE,
                        self.PARSER,
                        self.FUNCTION,
                        self.TRANSFORMATION,
                    ],
                    "initialize": [self.FILTER, self.MAPPING],
                }[method]
            )
        except KeyError as exc:
            raise ValueError(
                "Only 'get' and 'initialize' methods are allowed."
            ) from exc


def strategy_create_kwargs() -> "list[tuple[str, dict[str, Any]]]":
    """List of strategy-to-configuration mapping."""
    return [
        (
            ResourceType.DATARESOURCE.value,
            {
                "downloadUrl": (
                    "https://raw.githubusercontent.com/EMMC-ASBL/otelib"
                    f"/{HEAD_COMMIT_SHA}"
                    f"/{relative_posix_path_to_sample_json}"
                ),
                "mediaType": "application/json",
                "resourceType": "resource/url",
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
            ResourceType.PARSER.value,
            {
                "configuration": {
                    "downloadUrl": (
                        "https://raw.githubusercontent.com/EMMC-ASBL/otelib"
                        f"/{HEAD_COMMIT_SHA}"
                        f"/{relative_posix_path_to_sample_json}"
                    ),
                    "mediaType": "application/json",
                },
                "entity": "http://onto-ns.com/meta/0.4/dummy_entity",
                "parserType": "parser/json",
            },
        ),
        (ResourceType.FUNCTION.value, {"functionType": "function/demo"}),
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
