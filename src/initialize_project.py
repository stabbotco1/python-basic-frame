import sys
from src.core.environment_manager.dotenv_manager import DotEnvManager
from src.core.logger import SingletonLogger

def initialize_project():
    # Capture the environment value passed from the shell script (default to 'local')
    environment = sys.argv[1] if len(sys.argv) > 1 else "local"
    print ("")
    print (f"initialize_project environment {environment}")
    
    # Handle different environments
    if environment == "local":
        # Load the .env file if it exists, or create it from .env.default
        DotEnvManager.load_env()
        print("Loaded local environment variables")
    else:
        # Assuming that for non-local environments, variables are already injected into the OS
        print(f"Running in {environment} environment, assuming variables are already set")
    
    # Initialize the logger
    logger = SingletonLogger.get_logger()
    logger.info(f"Project initialized in {environment} environment")
    
    # Initialize other modules as necessary (e.g., database)
    # Example: Logger initialization, DB initialization, etc.

if __name__ == "__main__":
    initialize_project()
