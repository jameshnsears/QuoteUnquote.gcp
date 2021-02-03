from flask import jsonify

from storage import storage_adapter
from validation import request_validation


def test_http_get_not_supported(client):
    assert client.get("/receive").status_code == 405


def test_invalid_request(client):
    response = client.post('/receive', json={'code': ''})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_LENGTH_CODE
    assert response.status_code == 400


def test_valid_request_but_unknown_code(client):
    response = client.post('/receive', json={'code': '1234567825'})
    assert response.json['error'] == request_validation.ERROR_JSON_NOT_VALID
    assert response.json['reason'] == request_validation.REASON_NO_DIGESTS_FOR_CODE
    assert response.status_code == 400


def test_valid_request(client):
    # NOTE: it takes n seconds for Firestore database to be viewable
    response = client.post('/receive', json={'code': storage_adapter.DEFAULT_CODE})
    assert response.is_json
    assert response.data == jsonify(storage_adapter.DEFAULT_DIGESTS).data
    assert response.status_code == 200
