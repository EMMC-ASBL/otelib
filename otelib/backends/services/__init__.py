"""The strategies to be created by the client."""
from enum import Enum
from typing import TYPE_CHECKING

from oteapi.models import (
    FilterConfig,
    FunctionConfig,
    MappingConfig,
    ResourceConfig,
    TransformationConfig,
)

from .dataresource import DataResource
from .filter import Filter
from .function import Function
from .mapping import Mapping
from .transformation import Transformation

if TYPE_CHECKING:  # pragma: no cover
    from typing import Type, Union

    from oteapi.models import StrategyConfig


__all__ = (
    "DataResource",
    "Filter",
    "Function",
    "Mapping",
    "StrategyType",
    "Transformation",
)


class StrategyType(str, Enum):
    """An OTELib strategy type enumeration."""

    def __new__(
        cls,
        value: str,
        strategy_cls: "Type[Union[DataResource, Filter, Function, Mapping, Transformation]]",
        required_attrs: tuple[str, ...],
        config_cls: "Type[StrategyConfig]",
    ) -> "StrategyType":
        obj = str.__new__(cls, value)
        obj._value_ = value
        obj.strategy_cls = strategy_cls
        obj.relevant_config_fields = required_attrs
        obj.config_cls = config_cls
        return obj

    DataResource = (
        "dataresource",
        DataResource,
        ("downloadUrl", "mediaType", "accessService"),
        ResourceConfig,
    )
    Filter = ("filter", Filter, ("filterType",), FilterConfig)
    Function = ("function", Function, ("functionType",), FunctionConfig)
    Mapping = ("mapping", Mapping, ("mappingType",), MappingConfig)
    Transformation = (
        "transformation",
        Transformation,
        ("transformationType,"),
        TransformationConfig,
    )

    @classmethod
    def _missing_(cls, value: "Union[StrategyType, str]") -> "StrategyType":
        if isinstance(value, str):
            value = value.lower()
            if value in (_.value for _ in cls.__members__.values()):
                return cls(value)
        return None
