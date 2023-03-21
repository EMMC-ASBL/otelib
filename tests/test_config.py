"""Pytest for testing kwargs in clients"""
import pytest


def test_warning(backend: str, server_url: str) -> None:
    """Pytest for unloaded kwargs warning."""
    import warnings

    from otelib import OTEClient
    from otelib.warnings import IgnoringConfigOptions

    valid_config = {"headers": {"foo": "bar"}}
    invalid_config = valid_config["headers"]
    source = backend if backend == "python" else server_url

    if backend == "services":
        # no warning should be emitted
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            OTEClient(source, **valid_config)
    elif backend == "python":
        # headers are not supported for the Python backend
        with pytest.warns(IgnoringConfigOptions, match=r"^The given configuration.*"):
            OTEClient(source, **valid_config)
    else:
        pytest.fail(f"Unknown backend: {backend}")

    # invalid configuration
    with pytest.warns(IgnoringConfigOptions, match=r"^The given configuration.*"):
        OTEClient(source, **invalid_config)
