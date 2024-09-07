import os
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'time': self.formatTime(record, self.datefmt),
            'level': record.levelname,
            'message': record.getMessage(),
        }
        return json.dumps(log_record)

def setup_logger(name='app'):
    log_directory = os.path.join(os.path.dirname(__file__), '../logs')
    os.makedirs(log_directory, exist_ok=True)
    log_file = os.path.join(log_directory, f'{name}.log')

    handler = logging.FileHandler(log_file)
    handler.setFormatter(JSONFormatter())

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

    return logger
