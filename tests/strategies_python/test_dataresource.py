"""Tests for `otelib.backends.services.dataresource`."""
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from typing import Callable, Union

    from tests.conftest import OTEResponse, ResourceType


def test_create() -> None:
    """Test `DataResource.create()`."""
    from otelib.backends.python.dataresource import DataResource
    data_resource = DataResource('python')

    assert data_resource.id is None

    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    assert data_resource.id


def test_fetch() -> None:
    """Test `DataResource.fetch()`."""
    import json

    from otelib.backends.python.dataresource import DataResource
    from oteapi.plugins import load_strategies
    load_strategies()

    expected_result = {'content': {'firstName': 'Joe',
                       'lastName': 'Jackson',
                       'gender': 'male',
                       'age': 28,
                       'address': 
                       {'streetAddress': '101',
                        'city': 'San Diego', 'state': 'CA'},
                       'phoneNumbers':
                        [{'type': 'home', 'number': '7349282382'}]}}

    data_resource = DataResource('python')
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )
    
    #                            services does not use .json()
    content = data_resource.fetch(session_id=None).json()

    assert json.loads(content) == expected_result 

def test_initialize() -> None:
    """Test `DataResource.fetch()`."""
    import json

    from otelib.backends.python.dataresource import DataResource

    data_resource = DataResource('python')

    # We must first create the resource - getting a resource ID
    data_resource.create(
        downloadUrl="https://filesamples.com/samples/code/json/sample2.json",
        mediaType="application/json",
    )

    # services returns {} not None
    content = data_resource.initialize(session_id=None)

    assert content is None 