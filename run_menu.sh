#!/bin/bash

# Activate virtual environment if necessary
source scripts/venv_manager.sh

# Define environment (use 'local' by default if none provided)
ENVIRONMENT=${1:-local}

# Run the initialization and menu system as a module within src
python3 -m src.initialize_project $ENVIRONMENT
python3 -m src.core.menu.main