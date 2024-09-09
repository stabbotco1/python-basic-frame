#!/bin/bash

# Activate virtual environment if necessary
source scripts/venv_manager.sh

# Run the main menu system as a module
python3 -m src.core.menu.main
