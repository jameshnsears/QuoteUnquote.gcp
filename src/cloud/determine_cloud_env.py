import os


def using_gcp():
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        return True
