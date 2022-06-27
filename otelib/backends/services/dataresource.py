"""Common strategy for Download, Parse and Resource strategies."""
from otelib.backends.services.base import BaseStrategy


class DataResource(BaseStrategy):
    """Context class for the data resource strategy interfaces for managing i/o
    operations."""
