import os
import logging
import json
from datetime import datetime
from src.core.core_utilities import CoreUtilities

clear_logs_on_startup = False

class JSONFormatter(logging.Formatter):
    def format(self, record):
        # Format the time in ISO 8601 with 6 decimal places (microseconds)
        utc_time = datetime.utcnow().isoformat(timespec='microseconds') + 'Z'
        
        log_message = {
            'time': utc_time,
            'level': record.levelname,
            'message': record.getMessage()
        }
        return json.dumps(log_message)

class SingletonLogger:
    _logger = None

    @staticmethod
    def get_logger():

        if SingletonLogger._logger is None:

            default_log_level = "debug"
            logger = logging.getLogger('app_logger')
            level = os.getenv('LOG_LEVEL', default_log_level).upper()
            logger.setLevel(level)

            log_directory = os.path.join(CoreUtilities.get_root_directory(), 'logs')
            os.makedirs(log_directory, exist_ok=True)

            project_root = CoreUtilities.get_root_directory()
            log_dir = os.path.join(project_root, 'logs')

            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            # File handler with the log path at project root
            log_file = os.path.join(log_dir, f'app_{datetime.utcnow().strftime("%Y_%m_%d")}.log')

            # Check if logs should be cleared on startup
            if clear_logs_on_startup == True:
                with open(log_file, 'w'):
                    pass  # This will truncate the file

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(JSONFormatter())

            # Create a StreamHandler to force real-time log flushing
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(JSONFormatter())

            # Add the file handler and stream handler to the logger
            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

            # Ensure the logger flushes immediately
            file_handler.flush = lambda: None
            stream_handler.flush = lambda: None

            # Force file handler to flush after every log entry
            file_handler.flush()

            SingletonLogger._logger = logger

        return SingletonLogger._logger
