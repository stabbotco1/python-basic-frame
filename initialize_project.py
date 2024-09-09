from src.core.environment_manager.dotenv_manager import DotEnvManager
# Import other module initializations as needed

def initialize_project():
    # Initialize environment variables
    DotEnvManager.load_env()
    
    # Initialize other modules as necessary
    # Example: Logger initialization, DB initialization, etc.

if __name__ == "__main__":
    initialize_project()
    # Start the menu system
    from src.core.menu.main import run_menu
    run_menu()
