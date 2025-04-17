#!/bin/bash

# Load configuration if available
if [ -f "config.sh" ]; then
    source config.sh
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Virtual environment not found. Running setup first..."
    ./setup.sh
fi

# Activate virtual environment
source .venv/bin/activate

# Add server and remote path from config if available
ARGS=("$@")
if [ -n "$CREDCAST_SERVER" ]; then
    ARGS+=("--server" "$CREDCAST_SERVER")
fi

if [ -n "$CREDCAST_REMOTE_PATH" ]; then
    ARGS+=("--remote-path" "$CREDCAST_REMOTE_PATH")
fi

# Run credcast with all arguments
python credcast.py "${ARGS[@]}"
