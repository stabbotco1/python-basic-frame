# Title

.
├── .gitignore
├── .vscode/
│   └── settings.json
├── logs/
│   └── app_2024_09_07.log
├── run_menu.sh
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── core_utilities.py  # New: Manages global references (e.g., ROOT_DIRECTORY)
│   ├── environment_manager/
│   │   ├── __init__.py
│   │   └── environment_utilities.py
│   ├── logger.py  # Updated: Integrates core_utilities for ROOT_DIRECTORY
│   ├── menu/
│   │   ├── __init__.py
│   │   ├── commands/
│   │   │   ├── environment_variables/
│   │   │   │   ├── load_environment_variables_from_file.py
│   │   │   │   ├── show_environment_variables_in_env_file.py
│   │   │   │   └── show_loaded_environment_variables.py
│   │   │   ├── logging_setup/
│   │   │   │   ├── change_log_level.py
│   │   │   │   ├── change_logging_directory.py
│   │   │   │   └── send_sample_log_message.py
│   │   └── main.py
│   │   └── menu.json
│   ├── utilities/
│   │   ├── __init__.py
│   │   └── file_system_utilities.py
└── tests/
    └── test_core_utilities.py  # Optional: For future testing
