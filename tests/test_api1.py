import pytest
import requests
import config
from src.schemas.payload import Payload
from src.baseclasses.response import Response
from uuid import uuid4


#@pytest.mark.skip
def test_can_call_endpoint(valuestorage):
    r = requests.get(url=config.ENDPOINT_URL)
    valuestorage.xsrf = {'csrftoken': r.cookies.get('csrftoken')}
    assert r.status_code == 200


def test_xsrf_required(valuestorage):
    r = requests.post(url=config.SERVICE_URL+'create', json=valuestorage.valid_item_object)
    assert r.status_code == 403


@pytest.mark.skip(reason='[ISSUE] double token check doesnt work yet for opendocs compatibility')
def test_valid_xsrf_required(valuestorage):
    r = requests.post(url=config.SERVICE_URL + 'create', headers={'csrftoken': str(uuid4())},
                      json=valuestorage.valid_item_object, cookies={'csrftoken': str(uuid4())})
    Response(r).assert_status_code(403)


@pytest.mark.skip(reason="fetches entire table")
def test_get_all():
    r = requests.get(url=config.SERVICE_URL+'all')
    Response(r).assert_status_code(200).validate(Payload)


#@pytest.mark.skip
def test_create_item(valuestorage):
    r = requests.post(url=config.SERVICE_URL+'create', headers=valuestorage.xsrf,
                      json=valuestorage.valid_item_object, cookies=valuestorage.xsrf)
    valuestorage.valid_item_object['pk'] = r.json()  #tests there depends on each other
    Response(r).assert_status_code(200)


#@pytest.mark.skip
def test_get_item(valuestorage):
    r = requests.get(url=config.SERVICE_URL + 'get?item_id=' + valuestorage.valid_item_object['pk'])
    Response(r).assert_status_code(200).validate(Payload).validate_created_item(valuestorage)


@pytest.mark.parametrize("key", [
    "title",
    "author",
    "description"
])
#@pytest.mark.skip
def test_update_item(valuestorage, key, update_item):
    valuestorage.valid_item_object[key] = update_item
    r = requests.put(url=config.SERVICE_URL+'update', headers=valuestorage.xsrf,
                     json=valuestorage.valid_item_object, cookies=valuestorage.xsrf)
    Response(r).assert_status_code(200)


#@pytest.mark.skip
def test_delete_item(valuestorage):
    r = requests.delete(url=config.SERVICE_URL + 'delete?item_pk=' +
                            valuestorage.valid_item_object['pk'] +
                            '&item_sk=' + valuestorage.valid_item_object['sk'],
                        headers=valuestorage.xsrf, cookies=valuestorage.xsrf)
    Response(r).assert_status_code(200)

