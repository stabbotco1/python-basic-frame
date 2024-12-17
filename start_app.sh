#!/bin/bash

# Exit script on errors
set -e

# Activate virtual environment if necessary
source scripts/venv_manager.sh

# Set environment variable (optional, if $ENVIRONMENT is not already set)
export ENVIRONMENT=${ENVIRONMENT:-"development"}

# Run the app_base module
python3 -m src.core.app_base $ENVIRONMENT
