"""Common strategy for Download, Prase and Resource strategies."""

import json
from copy import deepcopy

from oteapi.models import ParserConfig
from oteapi.plugins import create_strategy

from otelib.backends.python.base import BasePythonStrategy


class Parser(BasePythonStrategy):
    """Context class for the Parse strategy interfaces for managing i/o
    operations."""

    strategy_name = "parser"
    strategy_config: "type[ParserConfig]" = ParserConfig

    def fetch(self, session_id: str) -> bytes:
        self._sanity_checks(session_id)

        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))
        session_update = create_strategy("parse", config).get(
            session=deepcopy(self.cache[session_id])
        )
        self.cache[session_id].update(session_update)

        return session_update.model_dump_json().encode(encoding="utf-8")

    def initialize(self, session_id: str) -> bytes:
        self._sanity_checks(session_id)

        config = self.strategy_config(**json.loads(self.cache[self.strategy_id]))

        session_update = create_strategy("parse", config).initialize(
            session=deepcopy(self.cache[session_id])
        )
        self.cache[session_id].update(session_update)

        return session_update.model_dump_json().encode(encoding="utf-8")
