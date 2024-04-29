import pytest

from src.generators.api_object import ApiObjectBuilder


@pytest.fixture()
def update_item(key):
    return ApiObjectBuilder().update_key(key)


@pytest.fixture(scope='session')
def valuestorage():
    yield __ValueStorage


class __ValueStorage:
    xsrf = {}
    created_item_id = None
    valid_item_object = ApiObjectBuilder.build()
