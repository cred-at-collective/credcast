#!/bin/bash

# Make this script executable
chmod +x update-local.sh

echo "Updating credcast.py to use local build directory instead of /tmp..."

# Back up the original script if not already backed up
if [ ! -f credcast.py.bak ]; then
    cp credcast.py credcast.py.bak
    echo "Original script backed up to credcast.py.bak"
fi

# Replace with the fixed version that uses local build directory
cp credcast-fixed-3.py credcast.py
chmod +x credcast.py
echo "credcast.py updated with local build directory fix"

# Create .gitignore if it doesn't exist
if [ ! -f .gitignore ]; then
    echo "Creating .gitignore file..."
    echo "# Generated files" > .gitignore
    echo "build/" >> .gitignore
    echo ".venv/" >> .gitignore
    echo "*.bak" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo "__pycache__/" >> .gitignore
else
    # Check if build/ is already in .gitignore
    if ! grep -q "build/" .gitignore; then
        echo "build/" >> .gitignore
        echo "Added build/ to .gitignore"
    fi
fi

echo "Running credcast to rebuild the site..."
./run.sh ~/repos/lux.cred.at --site-name lux.cred.at --deploy

echo "Update complete! Your blog should now use a local build directory instead of /tmp."
echo "The build files are stored in ./build/lux.cred.at/ and ignored by git."
