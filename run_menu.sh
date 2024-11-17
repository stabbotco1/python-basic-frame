#!/bin/bash

# Activate virtual environment if necessary
source scripts/venv_manager.sh

# Set the environment variable
ENVIRONMENT=${1:-local}

# invoke the menu main function
python3 -m src.core.menu.main $ENVIRONMENT