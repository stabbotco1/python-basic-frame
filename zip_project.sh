#!/bin/bash

# Name of the zip file
ZIP_FILE="project.zip"

# Create a zip file excluding specific directories and files
zip -r $ZIP_FILE . -x \
    ".git/*" \
    "venv/*" \
    "**/__pycache__/*" \
    "logs/*" \
    "*.log" \
    "*.DS_Store"

# Print success message
echo "Project zipped successfully into $ZIP_FILE, with exclusions: .git, venv, __pycache__, logs, *.log, *.DS_Store"
