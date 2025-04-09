"""OTElib warnings."""

from __future__ import annotations


class BaseOtelibWarning(Warning):
    """A base OTElib warning."""


class IgnoringConfigOptions(BaseOtelibWarning):
    """Some given configuration option(s) for the client is/are ignored."""
