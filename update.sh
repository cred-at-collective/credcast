#!/bin/bash

# Make this script executable
chmod +x update.sh

echo "Updating credcast.py with fixes for Mermaid and duplicate titles..."

# Back up the original script
cp credcast.py credcast.py.bak
echo "Original script backed up to credcast.py.bak"

# Replace with the fixed version
cp credcast-fixed.py credcast.py
chmod +x credcast.py
echo "credcast.py updated with fixes"

echo "Running credcast to rebuild the site..."
./run.sh ~/repos/lux.cred.at --site-name lux.cred.at --deploy

echo "Update complete! The site should now display Mermaid diagrams correctly and not show duplicate titles."
