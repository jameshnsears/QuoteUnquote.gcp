from google.cloud import logging

logging_client = logging.Client()
logger = logging_client.logger("QuoteUnquote.cloudLib.functions")
