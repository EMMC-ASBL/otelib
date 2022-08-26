"""Test OTE Client."""
# pylint: disable=protected-access,invalid-name,too-many-arguments
from typing import TYPE_CHECKING

import pytest
from utils import strategy_create_kwargs

if TYPE_CHECKING:
    from typing import Any, Callable, Dict, Union

    from otelib.client import OTEClient
    from otelib.strategies.abc import AbstractStrategy
    from tests.conftest import OTEResponse, ResourceType


@pytest.mark.parametrize(
    "strategy,create_kwargs",
    strategy_create_kwargs(),
    ids=[_[0] for _ in strategy_create_kwargs()],
)
def test_create_strategies(
    testdata: "Callable[[Union[ResourceType, str]], dict]",
    strategy: str,
    create_kwargs: "Dict[str, Any]",
) -> None:
    """Test creating any strategy and calling it's `get()` method."""

    from oteapi.plugins import load_strategies

    load_strategies()
    import json

    from otelib.client import OTEPythonClient

    client = OTEPythonClient("python")
    if strategy == "function":
        pytest.skip("No function strategy exists in oteapi-core yet.")

    created_strategy: "AbstractStrategy" = getattr(client, f"create_{strategy}")(
        **create_kwargs
    )

    content = created_strategy.get()
    if strategy in ("filter", "mapping"):
        assert json.loads(content) == {}
    else:
        assert json.loads(content) == testdata(strategy)

    ## The testdata should always be in the full session
    # assert (
    #    created_strategy._session_id
    # ), f"Session ID not found in {strategy} ! Is OTEAPI_DEBUG not set?"
    # content_session = requests.get(
    #    f"{created_strategy.url}{created_strategy.settings.prefix}"
    #    f"/session/{created_strategy._session_id}"
    # )
    # session: "Dict[str, Any]" = content_session.json()
    # for key, value in testdata(strategy).items():
    #    assert key in session
    #    assert value == session[key]
