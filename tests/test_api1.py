import pytest
import requests
import config
from src.schemas.payload import Payload
from src.baseclasses.response import Response
from uuid import uuid4


#@pytest.mark.skip
def test_can_call_endpoint(ValueStorage):
    r = requests.get(url=config.ENDPOINT_URL)
    ValueStorage.xsrf = {'csrftoken' : r.cookies.get('csrftoken')}
    assert r.status_code == 200

def test_xsrf_required(ValueStorage):
    r=requests.post(url=config.SERVICE_URL+'create',json = ValueStorage.valid_item_object)
    assert r.status_code == 403

@pytest.mark.skip(reason='[ISSUE] double token check doesnt work yet for opendocs compatibility')
def test_valid_xsrf_required(ValueStorage):
    r = requests.post(url=config.SERVICE_URL + 'create', headers={'csrftoken':str(uuid4())}, json=ValueStorage.valid_item_object, cookies={'csrftoken':str(uuid4())})
    assert r.status_code == 403

@pytest.mark.skip(reason="fetches entire table")
def test_get_all():
    r = requests.get(url=config.SERVICE_URL+'all')
    response = Response(r)
    response.assert_status_code(200).validate(Payload)

#@pytest.mark.skip
def test_create_item(ValueStorage):
    r=requests.post(url=config.SERVICE_URL+'create',headers=ValueStorage.xsrf,json=ValueStorage.valid_item_object,cookies=ValueStorage.xsrf)
    ValueStorage.valid_item_object['pk'] = r.json()
    Response(r).assert_status_code(200)

#@pytest.mark.skip
def test_get_item(ValueStorage):
    r = requests.get(url=config.SERVICE_URL+'get?item_id='+ValueStorage.valid_item_object['pk'])
    Response(r).assert_status_code(200).validate(Payload).validate_created_item(ValueStorage)


@pytest.mark.parametrize("key", [
    "title",
    "author",
    "description"
])

#@pytest.mark.skip
def test_update_item(ValueStorage, key, update_item):
    ValueStorage.valid_item_object[key] = update_item
    r = requests.put(url=config.SERVICE_URL+'update', headers=ValueStorage.xsrf, json=ValueStorage.valid_item_object,cookies=ValueStorage.xsrf)
    Response(r).assert_status_code(200)

#@pytest.mark.skip
def test_delete_item(ValueStorage):
    r = requests.delete(url=config.SERVICE_URL+'delete?item_pk=' +
                            ValueStorage.valid_item_object['pk'] +'&item_sk='+
                            ValueStorage.valid_item_object['sk'], headers=ValueStorage.xsrf,cookies=ValueStorage.xsrf)
    Response(r).assert_status_code(200)





