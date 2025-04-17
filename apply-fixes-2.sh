#!/bin/bash

# Make this script executable
chmod +x apply-fixes-2.sh

echo "Applying fixes to credcast..."

# Back up the original credcast.py
cp credcast.py credcast.py.bak
echo "Created backup: credcast.py.bak"

# 1. Copy the improved scripts.js to the output directory
echo "Updating scripts.js..."
cp mermaid-fix.js /tmp/credcast-build-lux.cred.at/scripts.js 

# 2. Copy scripts.js for next run
mkdir -p .venv/fix-files
cp mermaid-fix.js .venv/fix-files/scripts.js

# 3. Instructions for manual edits
echo "Fix files have been created. You will need to manually:"
echo ""
echo "1. Update the HTML_TEMPLATE variable in credcast.py with the contents of html-template-fix.html"
echo "2. Replace the parse_markdown_file function with the contents of title-fix.py"
echo "3. Replace the SCRIPTS_JS variable with the contents of mermaid-fix.js"
echo ""
echo "After making these changes, run:"
echo "./run.sh ~/repos/lux.cred.at --site-name lux.cred.at --deploy"
echo ""
echo "The fixes have also been applied to the current build in /tmp/credcast-build-lux.cred.at/"
echo "You can deploy just that build folder with:"
echo "rsync -avz --delete --progress /tmp/credcast-build-lux.cred.at/ root@YOUR_DIGITAL_OCEAN_IP:/var/www/lux.cred.at/"
