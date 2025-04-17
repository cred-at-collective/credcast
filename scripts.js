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
