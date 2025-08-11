#!/bin/bash

# Install system dependencies
apt-get update
apt-get install -y python3-dev build-essential

# Install Python dependencies
pip install -r requirements.txt

# Make the script executable
chmod +x setup.sh
