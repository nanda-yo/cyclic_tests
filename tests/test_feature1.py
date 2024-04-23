import pytest
import requests
import config
from src.schemas.payload import Payload
from src.baseclasses.response import Response
from conftest import ValueStorage
from uuid import uuid4

#@pytest.mark.skip
def test_can_call_endpoint():
    r = requests.get(url=config.ENDPOINT_URL)
    ValueStorage.xsrf = {'csrftoken' : r.cookies.get('csrftoken')}
    assert r.status_code == 200

def test_xsrf_required():
    r=requests.post(url=config.SERVICE_URL+'create',json =ValueStorage.valid_item_object)
    assert r.status_code == 403

@pytest.mark.skip(reason="for the sake of making swagger doc page working, currently there is no such thing as header xsrf token check, it just accepts one from cookies, as long as it exists")
def test_valid_xsrf_required():
    r = requests.post(url=config.SERVICE_URL + 'create', headers={'csrftoken':str(uuid4())}, json=ValueStorage.valid_item_object, cookies={'csrftoken':str(uuid4())})
    assert r.status_code == 403

@pytest.mark.skip(reason="this fetches entire table")
def test_get_all():
    r = requests.get(url=config.SERVICE_URL+'all')
    response = Response(r)
    response.assert_status_code(200).validate(Payload)

#@pytest.mark.skip
def test_create_item():
    r=requests.post(url=config.SERVICE_URL+'create',headers=ValueStorage.xsrf,json =ValueStorage.valid_item_object,cookies=ValueStorage.xsrf)
    ValueStorage.created_item_id = r.json()
    Response(r).assert_status_code(200)

#@pytest.mark.skip
def test_get_item():
    r = requests.get(url=config.SERVICE_URL+'get?item_id='+ValueStorage.created_item_id)
    Response(r).assert_status_code(200).validate(Payload).validate_created_item(ValueStorage)
#@pytest.mark.skip
def test_update_item():
    ValueStorage.valid_item_object['sk'] = 'Testing sk updated'
    r = requests.put(url=config.SERVICE_URL+'update', headers=ValueStorage.xsrf, json=ValueStorage.valid_item_object,cookies=ValueStorage.xsrf)
    Response(r).assert_status_code(200)

#@pytest.mark.skip
def test_delete_item():
    r = requests.delete(url=config.SERVICE_URL+'delete?item_id='+ValueStorage.created_item_id, headers=ValueStorage.xsrf, json=ValueStorage.valid_item_object,cookies=ValueStorage.xsrf)
    Response(r).assert_status_code(200)





