import os
import sys
import tty
import termios
import json

from src.core.logger import SingletonLogger
logger = SingletonLogger.get_logger()

# Define the path to the menu JSON file
MENU_JSON_PATH = os.path.join(os.path.dirname(__file__), 'menu.json')

# Simple functions to serve as stubs for now
def load_environment_variables_from_file():
    print("Stub: Loading environment variables from file.")

def show_environment_variables_in_env_file():
    print("Stub: Showing environment variables from .env file.")

def show_loaded_environment_variables():
    print("Stub: Showing currently loaded environment variables.")

def change_logging_directory():
    print("Stub: Changing the logging directory.")

def change_log_level():
    print("Stub: Changing the log level.")

def send_sample_log_message():
    print("Stub: Sending a sample log message.")

def show_venv_state():
    print("Stub: Showing virtual environment state.")

def recreate_venv():
    print("Stub: Recreating virtual environment.")

def activate_venv():
    print("Stub: Activating virtual environment.")

def install_dependencies():
    print("Stub: Installing dependencies.")

# Function to read a single keypress
def read_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())  # Set terminal to raw mode
        ch = sys.stdin.read(1)  # Read one character
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Reset terminal settings
    return ch

# A function to display the main menu
def display_menu(menu):
    print("\nMain Menu (Press 'Esc' to exit):")
    for idx, item in enumerate(menu, 1):
        print(f"{idx}. {item['name']} - {item['description']}")

# A function to display submenu for a category
def display_submenu(commands):
    print("\nSubmenu (Press 'Esc' to go back):")
    for idx, command in enumerate(commands, 1):
        print(f"{idx}. {command['name']} - {command['description']}")

# Function to handle the main menu logic
def main_menu(menu_data):

    logger.info ("INFO --- Starting application ...")
    logger.debug("Debug --- starting")

    while True:
        display_menu(menu_data['menu'])
        key = read_key()

        # Check if escape key is pressed to exit
        if key == '\x1b':
            logger.info("Exiting application")
            break

        # Convert the keypress to a menu selection
        try:
            choice = int(key) - 1
            if 0 <= choice < len(menu_data['menu']):
                selected_category = menu_data['menu'][choice]
                submenu_menu(selected_category['commands'])
            else:
                print("Invalid selection, please try again.")
        except ValueError:
            print("Invalid key press, please use numbers to select an option.")

# Function to handle submenu logic
def submenu_menu(commands):
    while True:
        display_submenu(commands)
        key = read_key()

        # Check if escape key is pressed to go back to the main menu
        if key == '\x1b':
            return  # Return to the previous menu (main menu)

        # Convert the keypress to a submenu selection
        try:
            choice = int(key) - 1
            if 0 <= choice < len(commands):
                selected_command = commands[choice]
                # Execute the stub function based on the user's choice
                script_name = os.path.basename(selected_command['script']).replace('.py', '')
                globals()[script_name]()
            else:
                print("Invalid selection, please try again.")
        except ValueError:
            print("Invalid key press, please use numbers to select an option.")

# Main program execution
def main():
    logger.debug ("... Starting app main function")
    # Load menu from JSON file
    with open(MENU_JSON_PATH, 'r') as file:
        menu_data = json.load(file)

    # Start the main menu loop
    main_menu(menu_data)

if __name__ == "__main__":
    main()
