import pytest
import requests
import config
from allure import severity,severity_level
from src.schemas.payload import Payload
from src.baseclasses.response import Response
from uuid import uuid4

@severity(severity_level.BLOCKER)
@pytest.mark.smoke
def test_can_call_endpoint(valuestorage):
    """
    Basic smoke test to make sure the endpoint is responding
    """
    r = requests.get(url=config.ENDPOINT_URL)
    valuestorage.xsrf = {'csrftoken': r.cookies.get('csrftoken')}
    assert r.status_code == 200


@severity(severity_level.NORMAL)
def test_xsrf_required(valuestorage):
    """
    Tests if server returns non 2** for payload missing csrf token
    """
    r = requests.post(url=config.SERVICE_URL+'create', json=valuestorage.valid_item_object)
    assert r.status_code == 403


@severity(severity_level.NORMAL)
@pytest.mark.skip(reason='[ISSUE] double token check doesnt work yet for opendocs compatibility')
def test_valid_xsrf_required(valuestorage):
    """
    Tests if server returns non 2** for payload with incorrect csrf token
    """
    r = requests.post(url=config.SERVICE_URL + 'create', headers={'csrftoken': str(uuid4())},
                      json=valuestorage.valid_item_object, cookies={'csrftoken': str(uuid4())})
    Response(r).assert_status_code(403)

@severity(severity_level.CRITICAL)
@pytest.mark.skip(reason="fetches entire table")
def test_get_all():
    """
    Fetches entire existing table
    """
    r = requests.get(url=config.SERVICE_URL+'all')
    Response(r).assert_status_code(200).validate(Payload)

@severity(severity_level.CRITICAL)
def test_create_item(valuestorage):
    """
    Creates specific valid item on server and tests if server returns 200.\n
    Then saves the created item id from the response.
    """
    r = requests.post(url=config.SERVICE_URL+'create', headers=valuestorage.xsrf,
                      json=valuestorage.valid_item_object, cookies=valuestorage.xsrf)
    valuestorage.valid_item_object['pk'] = r.json()  #tests there depends on each other
    Response(r).assert_status_code(200)

@severity(severity_level.CRITICAL)
def test_get_item(valuestorage):
    """
    Tests if created item id actually exists.Asserts that the item is of valid schema,\n
    has every required field, and server returns 200.
    """
    r = requests.get(url=config.SERVICE_URL + 'get?item_id=' + valuestorage.valid_item_object['pk'])
    Response(r).assert_status_code(200).validate(Payload).validate_created_item(valuestorage)

@severity(severity_level.CRITICAL)
@pytest.mark.parametrize("key", [
    "title",
    "author",
    "description",
    "params"
])
def test_update_item(valuestorage, key, update_item):
    """
    Changes one specific field of created item to a new random value. Checks if server returns 200
    """
    valuestorage.valid_item_object[key] = update_item
    r = requests.put(url=config.SERVICE_URL+'update', headers=valuestorage.xsrf,
                     json=valuestorage.valid_item_object, cookies=valuestorage.xsrf)
    Response(r).assert_status_code(200)

@severity(severity_level.CRITICAL)
def test_delete_item(valuestorage):
    """
    Deletes the item created in "create item" test. Checks if server returns 200
    """
    r = requests.delete(url=config.SERVICE_URL + 'delete?item_pk=' +
                            valuestorage.valid_item_object['pk'] +
                            '&item_sk=' + valuestorage.valid_item_object['sk'],
                        headers=valuestorage.xsrf, cookies=valuestorage.xsrf)
    Response(r).assert_status_code(200)
