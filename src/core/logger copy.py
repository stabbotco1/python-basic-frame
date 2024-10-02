import os
import logging
import json
from datetime import datetime
from src.core.core_utilities import CoreUtilities

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

            default_log_level = "INFO" 
            logger = logging.getLogger('app_logger')
            level = os.getenv('LOG_LEVEL', default_log_level).upper()

            try:
                # Try to set the log level
                logger.setLevel(level)
            except ValueError:
                # If invalid level, fall back to DEBUG
                logger.setLevel(logging.DEBUG)
                logger.debug(f"Invalid log level '{level}' provided, falling back to DEBUG.")

            log_directory = os.path.join(CoreUtilities.get_root_directory(), 'logs')
            os.makedirs(log_directory, exist_ok=True)

            project_root = CoreUtilities.get_root_directory()
            log_dir = os.path.join(project_root, 'logs')

            if not os.path.exists(log_dir):
                os.makedirs(log_dir)

            log_file = os.path.join(log_dir, f'app_{datetime.utcnow().strftime("%Y_%m_%d")}.log')

            # Fetching clear_logs_on_startup from environment, defaulting to True
            clear_logs_on_startup = os.getenv('CLEAR_LOGS_ON_STARTUP', 'true').lower() in ('true', '1', 't', 'yes', 'y')

            # Improved test for truthy/falsy values
            if clear_logs_on_startup:
                with open(log_file, 'w'):
                    pass  # This will truncate the file

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(JSONFormatter())

            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(JSONFormatter())

            logger.addHandler(file_handler)
            logger.addHandler(stream_handler)

            file_handler.flush = lambda: None
            stream_handler.flush = lambda: None

            file_handler.flush()

            SingletonLogger._logger = logger

        return SingletonLogger._logger
