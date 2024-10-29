from src.core.environment_manager.dotenv_manager import DotEnvManager
from src.core.logger import SingletonLogger

def initialize_project(environment='local'):
    """
    Initializes the project based on the given environment.

    :param environment: The environment to initialize (default is 'local').
    """
    
    if environment == "local":
        # Load the .env file if it exists, or create it from .env.default
        added_or_changed_vars = DotEnvManager.load_env()

        # Display added or changed environment variables
        if added_or_changed_vars:
            print("\nAdded or changed environment variables:")
            for key, value in added_or_changed_vars.items():
                print(f"{key} = {value}")
        else:
            print("No environment variables were added or changed.")
    else:
        print(f"Running in {environment} environment, assuming variables are already set")
    
    # Initialize the logger
    logger = SingletonLogger.get_logger()
    logger.info(f"Project initialized in {environment} environment")
    logger.debug(f"DEBUG: Project initialized in {environment} environment")
    
    # Initialize other modules as necessary

if __name__ == "__main__":
    initialize_project()
