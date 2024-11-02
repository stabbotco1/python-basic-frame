from src.core.environment_manager.dotenv_manager import DotEnvManager
from src.core.logger import SingletonLogger
import os

def initialize_project(environment='local'):
    """
    Initializes the project based on the given environment.

    :param environment: The environment to initialize (default is 'local').
    """
    
    print("")
    print("Initializing environment")

    if environment == "local":
        print("RUNNING LOCALLY")
        # Load the .env file if it exists, or create it from .env.default
        added_or_changed_vars = DotEnvManager.load_env()

        print("initialize_project:Finished loading vars")
        print(f"added_or_changed_vars: {added_or_changed_vars}")
        print ("")

        # Print the current value of the LOG_LEVEL environment variable
        print(os.getenv("LOG_LEVEL", "Not Set"))
        print("")
        print("initialize_project done")

        logger = SingletonLogger.get_logger()


        # Display added or changed environment variables
        if added_or_changed_vars:
            print("\nAdded or changed environment variables:")
            for key, value in added_or_changed_vars.items():
                print(f"{key} = {value}")
        else:
            print("No environment variables were added or changed.")
                # Initialize the logger
        logger = SingletonLogger.get_logger()

        logger.info(f"INFO:  Project initialized in {environment} environment")
        logger.debug(f"DEBUG: Project initialized in {environment} environment")
        

    else:
        print(f"Running in {environment} environment, assuming variables are already set")
    
