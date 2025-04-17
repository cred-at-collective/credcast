#!/bin/bash

# Make script executable
chmod +x direct-script-deploy.sh

echo "Deploying fixed scripts.js to your server..."

# Prompt for server IP if not provided
read -p "Enter your Digital Ocean server IP: " SERVER_IP

# Copy the fixed script to the server
cp mermaid-fix-script.js scripts.js
rsync -avz --progress scripts.js root@${SERVER_IP}:/var/www/lux.cred.at/

echo "Fixed scripts.js deployed to server!"
echo "Check your website - Mermaid diagrams should now be working."
echo ""
echo "If still having issues, you may need to clear your browser cache or open the site in an incognito window."
