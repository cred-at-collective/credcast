#!/bin/bash

# Make this script executable
chmod +x update-3.sh

echo "Updating credcast.py with fixed version using local build directory..."

# Back up the original script if not already backed up
if [ ! -f credcast.py.bak ]; then
    cp credcast.py credcast.py.bak
    echo "Original script backed up to credcast.py.bak"
fi

# Replace with the correctly fixed version
cp credcast-fixed-3.py credcast.py
chmod +x credcast.py
echo "credcast.py updated with fixes"

# Create build directory (will be handled by script)
mkdir -p build
echo "Created local build directory"

echo "Running credcast to rebuild the site..."
./run.sh ~/repos/lux.cred.at --site-name lux.cred.at --deploy

echo "Update complete! The site should now display Mermaid diagrams correctly and not show duplicate titles."
