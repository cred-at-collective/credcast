#!/bin/bash

# Make all scripts executable
chmod +x credcast.py
chmod +x run.sh

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Credcast setup complete!"
echo "To use credcast, always run: source .venv/bin/activate first"
echo "Then you can run: ./credcast.py --help"
