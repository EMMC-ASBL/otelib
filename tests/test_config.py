"""Pytest for testing kwargs in clients"""

import pytest
from otelib import OTEClient


@pytest.mark.parametrize(
    "backend,config",
    [
        ("python", {"headers": {"foo": "bar"}}),
        ("http://localhost:8080", {"foo": "bar"}),
    ],
)
def test_warning(backend, config):
    """Pytest for unloaded kwargs warning."""
    message = f"The given configuration option(s) for {tuple(config)} is/are ignored."
    with pytest.warns(UserWarning) as record:
        OTEClient(backend, **config)
    assert len(record) == 1
    record[0].message == message
