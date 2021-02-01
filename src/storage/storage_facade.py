from cloud.determine_cloud_env import using_gcp
from cloud.gcp import gcp_firestore

DEFAULT_CODE = 'qski!$£90d'
DEFAULT_DIGESTS = ["d1", "d2"]


def save(request):
    if using_gcp():
        return gcp_firestore.save(request.json.get('code'), request.json.get('digests'))


def retrieve(request):
    if using_gcp():
        return gcp_firestore.retrieve(request.json.get('code'))
