"""Common strategy for Download, Prase and Resource strategies."""

from oteapi.models import ParserConfig

from otelib.backends.services.base import BaseServicesStrategy


class Parser(BaseServicesStrategy):
    """Context class for the Parse strategy interfaces for managing i/o
    operations."""

    strategy_name = "parser"
    strategy_config = ParserConfig
