#!/bin/bash

# Script to build and deploy the site using the fixed mermaid renderer

# Set executable permissions
chmod +x credcast-fixed-mermaid.py

# Run the fixed version of the script with the provided arguments
./credcast-fixed-mermaid.py $@

echo "Site built with fixed Mermaid rendering!"
