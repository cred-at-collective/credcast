#!/bin/bash

# Make script executable
chmod +x faster-fix.sh

echo "Creating a direct fix for Mermaid diagrams..."

# Create a simple HTML file to test mermaid directly on the server
cat > mermaid-test.html <<'EOL'
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Mermaid Test</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            startOnLoad: true,
            theme: 'dark'
        });
    </script>
</head>
<body style="background-color: #000000; color: #bbbbbb; font-family: 'Anonymous Pro', monospace;">
    <h1>Mermaid Test</h1>
    <div class="mermaid">
        graph LR
        c1[("⚛️")]
        c2[("💫")]
        c3[("🤝")]
        c4[("🦋")]
        c5[("🕊️")]
        w1a["particles"]
        w1b["physics"]
        w2a["manifest"]
        w2b["chaos"]
        w3a["bond"]
        w3b["alliance"]
        w4a["evolve"]
        w4b["metamorphosis"]
        w5a["peace"]
        w5b["release"]
        %% Emoji connections (bold)
        c1 --- c2
        c1 --- c3
        c1 --- c4
        c1 --- c5
        c2 --- c3
        c2 --- c4
        c2 --- c5
        c3 --- c4
        c3 --- c5
        c4 --- c5
        %% Semantic relationships (dotted)
        c1 -.-> w1a
        c1 -.-> w1b
        c2 -.-> w2a
        c2 -.-> w2b
        c3 -.-> w3a
        c3 -.-> w3b
        c4 -.-> w4a
        c4 -.-> w4b
        c5 -.-> w5a
        c5 -.-> w5b
    </div>
    <hr>
    <div class="mermaid">
        graph LR
        p1["particles - ⚛️ - physics - manifest - 💫 - chaos - bond - 🤝 - alliance - evolve - 🦋 - metamorphosis - peace - 🕊️ - release"]
    </div>
</body>
</html>
EOL

# Create a new scripts.js that will properly process mermaid code blocks
cat > scripts.js <<'EOL'
document.addEventListener('DOMContentLoaded', function() {
    // First initialize highlight.js
    hljs.highlightAll();
    
    // Initialize MathJax
    if (typeof MathJax !== 'undefined') {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
    
    // Process existing mermaid diagrams
    console.log("Checking for mermaid diagrams...");
    
    // Find all code blocks with class "language-mermaid" and convert them
    document.querySelectorAll('pre > code.language-mermaid').forEach(function(codeBlock) {
        console.log("Found mermaid code block, converting to diagram");
        
        // Get the content and parent pre element
        var content = codeBlock.textContent;
        var preElement = codeBlock.parentNode;
        
        // Create a new div for mermaid
        var mermaidDiv = document.createElement('div');
        mermaidDiv.className = 'mermaid';
        mermaidDiv.textContent = content;
        
        // Replace the pre element with the mermaid div
        if (preElement.parentNode) {
            preElement.parentNode.replaceChild(mermaidDiv, preElement);
        }
    });
    
    // Re-initialize mermaid to render the newly created diagrams
    if (typeof mermaid !== 'undefined') {
        console.log("Initializing mermaid diagrams");
        try {
            mermaid.initialize({
                theme: 'dark',
                securityLevel: 'loose',
                startOnLoad: true
            });
            
            // Force render all mermaid diagrams
            mermaid.init(undefined, '.mermaid');
            console.log("Mermaid diagrams initialized");
        } catch (err) {
            console.error("Error initializing mermaid:", err);
        }
    } else {
        console.error("Mermaid library not found!");
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

# Prompt for server IP
read -p "Enter your Digital Ocean server IP: " SERVER_IP

# Upload files to server
echo "Uploading fixes to server..."
rsync -avz scripts.js mermaid-test.html root@${SERVER_IP}:/var/www/lux.cred.at/

echo "Fix deployed!"
echo ""
echo "You can verify the fix by going to:"
echo "https://lux.cred.at/mermaid-test.html"
echo ""
echo "If the test page works but your blog still doesn't show diagrams correctly,"
echo "you may need to clear your browser cache or open the site in an incognito window."
