#!/bin/bash

# Exit immediately if any command fails
set -e

# Print each command before executing it (optional, for debugging)
set -x

# Define project directory and zip file name
PROJECT_DIR="$HOME/projects/python-basic-frame"
ZIP_FILE="$HOME/projects/python-basic-frame.zip"

# Navigate to the parent directory of the project
cd "$HOME/projects"

# Check if the zip file already exists and delete it if it does
if [ -f "$ZIP_FILE" ]; then
  echo "Deleting existing zip file: $ZIP_FILE"
  rm "$ZIP_FILE"
fi

# Create the zip file, excluding common Python-ignored files
zip -r "$ZIP_FILE" "python-basic-frame" \
  -x "python-basic-frame/venv/*" \
  -x "python-basic-frame/__pycache__/*" \
  -x "python-basic-frame/**/*.pyc" \
  -x "python-basic-frame/**/*.pyo" \
  -x "python-basic-frame/**/*.egg-info/*" \
  -x "python-basic-frame/.pytest_cache/*" \
  -x "python-basic-frame/.mypy_cache/*" \
  -x "python-basic-frame/.tox/*" \
  -x "python-basic-frame/.idea/*" \
  -x "python-basic-frame/.vscode/*" \
  -x "python-basic-frame/.DS_Store" \
  -x "python-basic-frame/.coverage" \
  -x "python-basic-frame/.env" \
  -x "python-basic-frame/.git/*" \
  -x "python-basic-frame/.gitignore" \
  -x "python-basic-frame/node_modules/*"

echo "Zip file created at: $ZIP_FILE"
