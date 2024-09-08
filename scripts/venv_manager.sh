#!/bin/bash

# --------------------------------------------------------------------
# Script: manage_venv.sh
#
# Description:
# This script automates the management of a Python virtual environment.
# It performs the following actions:
# 1. Checks if a virtual environment (venv) exists. If not, it creates one.
# 2. Activates the virtual environment.
# 3. Compares installed packages with the ones listed in requirements.txt.
# 4. Installs any missing dependencies listed in requirements.txt.
# 5. If requirements.txt is missing, it generates one from the current environment.
# 6. Optionally, can update requirements.txt to reflect current installed packages
#    (useful after installing or uninstalling packages).
#
# Usage:
# Run this script any time you want to set up or sync your virtual environment:
#   ./scripts/manage_venv.sh
#
# --------------------------------------------------------------------

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "No virtual environment found. Creating one..."
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Check if requirements.txt exists
if [ -f "requirements.txt" ]; then
    echo "Checking installed packages against requirements.txt..."

    # Create a temp file to store missing dependencies
    missing_deps=$(mktemp)

    # Compare installed packages with requirements.txt
    pip freeze > installed_packages.txt
    comm -23 <(sort requirements.txt) <(sort installed_packages.txt) > "$missing_deps"

    if [ -s "$missing_deps" ]; then
        echo "Missing packages found. Installing missing packages..."
        pip install -r "$missing_deps"
    else
        echo "All required packages are installed."
    fi

    # Clean up
    rm "$missing_deps" installed_packages.txt

else
    echo "No requirements.txt found. Creating one from the current environment..."
    pip freeze > requirements.txt
fi

echo "Updating requirements.txt with current environment packages..."
pip freeze > requirements.txt

echo "Virtual environment setup and package synchronization complete."
