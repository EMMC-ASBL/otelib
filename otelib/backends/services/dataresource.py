"""Common strategy for Download, Prase and Resource strategies."""
from oteapi.models import ResourceConfig

from otelib.backends.services.base import BaseServicesStrategy


class DataResource(BaseServicesStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""

    strategy_name = "dataresource"
    strategy_config = ResourceConfig
