import os
import logging
import json
import threading
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
from src.core.core_utilities import CoreUtilities


class JSONFormatter(logging.Formatter):
    def format(self, record):
        """Format log messages as a structured JSON log."""
        utc_time = datetime.utcnow().isoformat(timespec='microseconds') + 'Z'
        
        log_message = {
            'time': utc_time,
            'level': record.levelname,
            'message': record.getMessage(),
            'logger': record.name,
            'file': record.pathname,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # If an exception is logged, include the stack trace
        if record.exc_info:
            log_message['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_message)


def get_env_bool(key: str, default: bool = False) -> bool:
    """Convert an environment variable to a boolean value."""
    return os.getenv(key, str(default)).strip().lower() in ('true', '1', 't', 'yes', 'y')


class SingletonLogger:
    _logger = None
    _lock = threading.Lock()

    @staticmethod
    def get_logger():
        """Returns a singleton logger instance."""
        if SingletonLogger._logger is None:
            with SingletonLogger._lock:
                if SingletonLogger._logger is None:  # Double-checked locking
                    SingletonLogger._logger = SingletonLogger._create_logger()
        return SingletonLogger._logger

    @staticmethod
    def _create_logger():
        """Creates and configures the logger."""
        default_log_level = "INFO"
        default_send_logs_to_console = False

        # Create logger instance
        logger = logging.getLogger('app_logger')
        log_level = os.getenv('LOG_LEVEL', default_log_level).upper()

        # Set log level with validation
        if log_level not in logging._nameToLevel:
            logger.warning(f"Invalid log level '{log_level}' provided, falling back to DEBUG.")
            log_level = 'DEBUG'

        logger.setLevel(logging._nameToLevel[log_level])

        # Set up log directory
        project_root = CoreUtilities.get_root_directory()
        log_dir = os.path.join(project_root, 'logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f'app_{datetime.utcnow().strftime("%Y_%m_%d")}.log')

        # Clear logs on startup if the environment variable is set
        clear_logs_on_startup = get_env_bool('CLEAR_LOGS_ON_STARTUP', True)
        if clear_logs_on_startup and os.path.exists(log_file):
            os.remove(log_file)  # Removes the existing log file instead of truncating

        # Use a TimedRotatingFileHandler to rotate logs daily and keep 7 days of history
        file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

        # Determine if logs should be sent to console
        send_logs_to_console = get_env_bool('SEND_LOGS_TO_CONSOLE', default_send_logs_to_console)
        if send_logs_to_console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(JSONFormatter())
            logger.addHandler(stream_handler)

        return logger
