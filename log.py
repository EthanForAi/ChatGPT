import logging
from datetime import datetime

log = logging.getLogger()
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
log.setLevel(logging.INFO)
log.addHandler(stream_handler)

def info(operation_id, text):
    log.info("{} [INFO] [operationID:{}] [{}]".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operation_id, text))

def warn(operation_id, text):
    log.warn("{} [INFO] [operationID:{}] [{}]".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operation_id, text))

def debug(operation_id, text):
    log.debug("{} [INFO] [operationID:{}] [{}]".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operation_id, text))

def error(operation_id, text):
    log.error("{} [INFO] [operationID:{}] [{}]".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), operation_id, text))
