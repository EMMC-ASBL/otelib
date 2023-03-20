"""Pytest for testing kwargs in clients"""

import warnings

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
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=DeprecationWarning)
            warnings.filterwarnings(
                "ignore", message=".*No global cache used for Python backend strategy.*"
            )
            OTEClient(backend, **config)
    assert len(record) == 1

    assert str(record[0].message) == message
