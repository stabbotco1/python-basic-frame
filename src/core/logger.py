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

        print("getting logger")
        
        if SingletonLogger._logger is None:
            print ("Initializing logger")
            default_log_level = "INFO"
            default_send_logs_to_console = False

            logger = logging.getLogger('app_logger')
            level = os.getenv('LOG_LEVEL', default_log_level).upper()
            print(f"---- level {level}")

            try:
                print(f"SingletonLogger: trying to set log level {level}")
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

            if clear_logs_on_startup:
                with open(log_file, 'w'):
                    pass  # This will truncate the file

            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(JSONFormatter())

            logger.addHandler(file_handler)

            # Get the value from the environment or use the default
            send_logs_to_console = os.getenv('SEND_LOGS_TO_CONSOLE', None)
            if send_logs_to_console is None:
                send_logs_to_console = default_send_logs_to_console
            else:
                send_logs_to_console = send_logs_to_console.lower() in ('true', '1', 't', 'yes', 'y')

            if send_logs_to_console:
                stream_handler = logging.StreamHandler()
                stream_handler.setFormatter(JSONFormatter())
                logger.addHandler(stream_handler)

            file_handler.flush = lambda: None
            file_handler.flush()

            SingletonLogger._logger = logger
            message = (f"Logger initialized with log level: {level}")
            print(message)
            logger.info(message)
            logger.debug(message)
        return SingletonLogger._logger
