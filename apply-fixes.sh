#!/bin/bash

# Make script executable
chmod +x apply-fixes.sh

# Update scripts.js with fixes
echo "Updating scripts.js with mermaid rendering fix..."
cp scripts-fix.js .venv/lib/python3.11/site-packages/scripts.js

# Update the parse_markdown_file function to fix duplicate titles
echo "Applying markdown parser fix for duplicate titles..."
echo "Copy the contents of markdown-fix.py and replace the parse_markdown_file function in credcast.py"
echo "Then run ./run.sh again to rebuild your blog with these fixes"

echo "Fix files have been created. Please manually integrate them into credcast.py."