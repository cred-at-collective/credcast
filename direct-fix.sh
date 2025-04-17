#!/bin/bash

# Make this script executable
chmod +x direct-fix.sh

echo "Deploying fixed scripts.js directly to server..."

# Make sure we have the server IP
read -p "Enter your server IP or hostname (e.g., 123.456.789.10): " SERVER_IP

# Create the scripts.js file with fixes
cat > scripts.js <<'EOL'
document.addEventListener('DOMContentLoaded', function() {
    // Initialize highlight.js
    hljs.highlightAll();
    
    // Initialize MathJax
    if (typeof MathJax !== 'undefined') {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
    
    // Extra Mermaid initialization for diagrams
    if (typeof mermaid !== 'undefined') {
        // Give mermaid time to process the page
        setTimeout(function() {
            // Force re-render any unprocessed diagrams
            try {
                mermaid.init(undefined, '.mermaid:not(.mermaid-processed)');
                
                // Mark all diagrams as processed
                document.querySelectorAll('.mermaid').forEach(function(el) {
                    el.classList.add('mermaid-processed');
                });
                
                console.log('Mermaid diagrams initialized');
            } catch (e) {
                console.error('Error initializing mermaid:', e);
            }
        }, 1000);
    }
    
    // Highlight cred@ syntax in code blocks
    document.querySelectorAll('code.language-cred').forEach(function(block) {
        let html = block.innerHTML;
        // Match cred@ patterns
        html = html.replace(/(@cred@[a-zA-Z0-9:._-]+)/g, '<span class="cred-highlight">$1</span>');
        block.innerHTML = html;
    });
});
EOL

# Deploy the scripts.js file directly
rsync -avz --progress scripts.js root@${SERVER_IP}:/var/www/lux.cred.at/

echo "Fixed scripts.js deployed to server!"
echo ""
echo "For the duplicate title issue: when creating markdown files,"
echo "if you include the title in front matter, don't repeat it as an H1 heading"
echo "in the markdown body."
