import hashlib

from flask import jsonify

ERROR_JSON_NOT_VALID = 'JSON not valid'
ERROR_UNABLE_TO_SAVE = 'unable to save'

REASON_CRC_FAIL = 'crc fail'
REASON_EMPTY_JSON = 'empty json'
REASON_LENGTH_CODE = 'code length'
REASON_LENGTH_DIGESTS = 'digests length'
REASON_NO_CODE = 'no code'
REASON_NO_DIGESTS_FOR_CODE = 'no digests for code'
REASON_NO_DIGESTS = 'no digests'
REASON_NO_JSON = 'no json'


def check_save(request):
    invalid_code_response = _check_code(request)
    if invalid_code_response is not None:
        return invalid_code_response

    if request.json.get('digests', None) is None:
        return error_with_request(REASON_NO_DIGESTS)

    if len(request.json.get('digests')) == 0:
        return error_with_request(REASON_LENGTH_DIGESTS)

    return None


def check_receive(request):
    return _check_code(request)


def _check_code(request):
    if not request.is_json:
        return error_with_request(REASON_NO_JSON)

    if request.json == {}:
        return error_with_request(REASON_EMPTY_JSON)

    if request.json.get('code', None) is None:
        return error_with_request(REASON_NO_CODE)

    if len(request.json.get('code')) != 10:
        return error_with_request(REASON_LENGTH_CODE)

    if not _crc_check(request.json.get('code')):
        return error_with_request(REASON_CRC_FAIL)

    return None


def error_with_request(reason):
    return jsonify({'error': ERROR_JSON_NOT_VALID, 'reason': reason}), 400


def error_in_saving():
    return jsonify({'error': ERROR_UNABLE_TO_SAVE}), 400


def _crc_check(code):
    if code[8:] != hashlib.md5(code[:8].encode('utf-8')).hexdigest()[:2]:
        return False
    return True
