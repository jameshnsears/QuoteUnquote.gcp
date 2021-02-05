from flask import Response

from storage import storage_adapter
from storage.unable_to_save_exception import UnableToSaveException
from validation import request_validation


def save(request):
    invalid_request_response = request_validation.check_save(request)
    if invalid_request_response is not None:
        return invalid_request_response

    try:
        storage_adapter.save(request)
        return Response(status=200)
    except UnableToSaveException:
        return request_validation.error_in_saving()


def receive(request):
    invalid_request_response = request_validation.check_receive(request)
    if invalid_request_response is not None:
        return invalid_request_response

    retrieved_digests = storage_adapter.retrieve(request)
    if retrieved_digests is not None:
        return retrieved_digests, 200
    else:
        return request_validation.error_with_request(request_validation.REASON_NO_DIGESTS_FOR_CODE)
