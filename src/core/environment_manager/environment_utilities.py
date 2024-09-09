# src/core/environment_manager/environment_utilities.py
import os
from shutil import copyfile

try:
    from dotenv import load_dotenv, set_key, find_dotenv
    DOTENV_AVAILABLE = True
except ModuleNotFoundError:
    DOTENV_AVAILABLE = False

def load_env():
    """Load environment variables from .env or default_settings.env if dotenv is available."""
    if not DOTENV_AVAILABLE:
        # If dotenv is not available, set a flag indicating it's not loaded
        os.environ['DOTENV_LOADED'] = 'False'
        return False

    if not os.path.exists('.env'):
        copyfile('default_settings.env', '.env')

    dotenv_loaded = load_dotenv()
    if dotenv_loaded:
        set_env_var('DOTENV_LOADED', 'True')
        return True
    else:
        set_env_var('DOTENV_LOADED', 'False')
        return False

def get_env_var(key, default=None):
    """Get environment variable."""
    return os.getenv(key, default)

def set_env_var(key, value):
    """Set environment variable in .env file."""
    if DOTENV_AVAILABLE:
        dotenv_path = find_dotenv()
        if dotenv_path:
            set_key(dotenv_path, key, value)
        else:
            os.environ[key] = value
    else:
        os.environ[key] = value
