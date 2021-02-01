from unittest.mock import Mock

from storage import storage_facade
from validation import request_validation
from storage.unable_to_save_exception import UnableToSaveException


def test_http_get_not_supported(client):
    assert client.get("/save").status_code == 405


def test_json_not_sent(client):
    response = client.post('/save')
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_NO_JSON
    assert response.status_code == 400


def test_empty_json(client):
    response = client.post('/save', json={})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_EMPTY_JSON
    assert response.status_code == 400


def test_no_code(client):
    response = client.post('/save', json={'': ''})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_NO_CODE
    assert response.status_code == 400


def test_code_length(client):
    response = client.post('/save', json={'code': ''})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_LENGTH_CODE
    assert response.status_code == 400


def test_invalid_code(client):
    response = client.post('/save', json={'code': '0123456789'})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_CRC_FAIL
    assert response.status_code == 400


def test_valid_code_but_missing_digests(client):
    response = client.post('/save', json={'code': storage_facade.DEFAULT_CODE})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_NO_DIGESTS
    assert response.status_code == 400


def test_valid_code_but_digests_length(client):
    response = client.post('/save', json={'code': storage_facade.DEFAULT_CODE, 'digests': []})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_LENGTH_DIGESTS
    assert response.status_code == 400


def test_valid_request(client):
    response = client.post('/save',
                           json={'code': storage_facade.DEFAULT_CODE, 'digests': storage_facade.DEFAULT_DIGESTS})
    assert not response.is_json
    assert response.status_code == 200


def test_unable_to_save(client):
    storage_facade.save = Mock(side_effect=UnableToSaveException())
    response = client.post('/save',
                           json={'code': storage_facade.DEFAULT_CODE, 'digests': storage_facade.DEFAULT_DIGESTS})
    assert response.json['error'] == request_validation.ERROR_UNABLE_TO_SAVE
    assert response.status_code == 400
