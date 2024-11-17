from src.core.environment_manager.dotenv_manager import DotEnvManager
from src.core.logger import SingletonLogger
import os

def initialize_project(environment='local'):
    """
    Initializes the project based on the given environment.

    :param environment: The environment to initialize (default is 'local').
    """
    
    if environment == "local":
        DotEnvManager.load_env()
        logger = SingletonLogger.get_logger()
        logger.debug("src/core/initialize_project.py: Initialized project")
        log_level = os.getenv("LOG_LEVEL")
        logger.info(f"INFO:  Project initialized in {environment} environment. log_level: {log_level}")
    else:
        print(f"Running in {environment} environment, assuming variables are already set")
    
