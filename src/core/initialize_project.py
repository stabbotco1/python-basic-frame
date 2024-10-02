from src.core.environment_manager.dotenv_manager import DotEnvManager
from src.core.logger import SingletonLogger

def initialize_project(environment='local'):
    """
    Initializes the project based on the given environment.

    :param environment: The environment to initialize (default is 'local').
    """
    
    # print(f"\nInitializing project in the '{environment}' environment")

    # Handle different environments
    if environment == "local":
        # Load the .env file if it exists, or create it from .env.default
        DotEnvManager.load_env()
    else:
        # Assuming that for non-local environments, variables are already injected into the OS
        print(f"Running in {environment} environment, assuming variables are already set")
    
    # Initialize the logger
    logger = SingletonLogger.get_logger()
    logger.info(f"Project initialized in {environment} environment")
    logger.debug(f"DEBUG: Project initialized in {environment} environment")
    
    # Initialize other modules as necessary

if __name__ == "__main__":
    # Optional: You could set a default here or handle other logic if it's called directly from the CLI
    pass
