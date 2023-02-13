from datetime import datetime, timezone
import logging

def log_file_name():
    return datetime.utcnow().isoformat('_', 'seconds').replace(':', '-') + 'Z.log'

logger = logging.getLogger('main')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
logger.addHandler(logging.FileHandler(log_file_name()))
formatter = logging.Formatter('%(asctime)s %(message)s', '%Y-%m-%d %H:%M:%S%z')
for handler in logger.handlers:
    handler.setFormatter(formatter)

logger.info('hello')
