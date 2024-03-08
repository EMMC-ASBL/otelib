"""Common strategy for Download, Parse and Resource strategies."""

from oteapi.models import ParserConfig
from otelib.backends.python.base import BasePythonStrategy


class Parser(BasePythonStrategy):
    """Context class for the Parse strategy interfaces for managing i/o
    operations."""

    strategy_name = "parser"
    strategy_config: "type[ParserConfig]" = ParserConfig
