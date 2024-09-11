import os
from dotenv import load_dotenv, set_key

DEFAULT_ENV_PATH = '.env.default'
ENV_PATH = '.env'

class DotEnvManager:
    @staticmethod
    def load_env():
        # Check if .env exists; if not, create it from the default
        if not os.path.exists(ENV_PATH):
            DotEnvManager.create_env_from_default()

        # Load the environment variables from .env into the OS environment
        load_dotenv(ENV_PATH)

    @staticmethod
    def create_env_from_default():
        # Check if the default env file exists
        if not os.path.exists(DEFAULT_ENV_PATH):
            raise FileNotFoundError(f"Default environment file {DEFAULT_ENV_PATH} not found.")
        
        # Copy the contents of .env.default to .env
        with open(DEFAULT_ENV_PATH, 'r') as default_file:
            with open(ENV_PATH, 'w') as env_file:
                env_file.write(default_file.read())

        print(f"Created {ENV_PATH} from {DEFAULT_ENV_PATH}.")
