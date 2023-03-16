"""The strategies to be created by the client."""
from .dataresource import DataResource
from .filter import Filter
from .function import Function
from .mapping import Mapping
from .transformation import Transformation

# pylint: disable=duplicate-code
__all__ = (
    "DataResource",
    "Filter",
    "Function",
    "Mapping",
    "Transformation",
)
