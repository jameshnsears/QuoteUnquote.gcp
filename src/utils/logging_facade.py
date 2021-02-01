from cloud.determine_cloud_env import using_gcp

from cloud.gcp import gcp_logging


def info(message):
    if using_gcp():
        gcp_logging.logger.log_text(message)
