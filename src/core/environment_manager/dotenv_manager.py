import os
from dotenv import load_dotenv, set_key

DEFAULT_ENV_PATH = '.env.default'
ENV_PATH = '.env'

class DotEnvManager:
    @staticmethod
    def load_env():
        # Check if .env exists
        if not os.path.exists(ENV_PATH):
            print(f"{ENV_PATH} not found. Creating from {DEFAULT_ENV_PATH}.")
            DotEnvManager.create_env_from_default()
        
        # Load the environment variables
        load_dotenv(ENV_PATH)
        print(f"Loaded environment variables from {ENV_PATH}.")

    @staticmethod
    def create_env_from_default():
        # Check if default env file exists
        if not os.path.exists(DEFAULT_ENV_PATH):
            raise FileNotFoundError(f"Default environment file {DEFAULT_ENV_PATH} not found.")
        
        # Copy default file to .env
        with open(DEFAULT_ENV_PATH) as default_env_file, open(ENV_PATH, 'w') as env_file:
            env_file.write(default_env_file.read())
        print(f"Created {ENV_PATH} from {DEFAULT_ENV_PATH}.")

    @staticmethod
    def set_env_variable(key, value):
        set_key(ENV_PATH, key, value)
        print(f"Set {key} in {ENV_PATH} to {value}.")

