document.addEventListener('DOMContentLoaded', function() {
    // Initialize highlight.js
    if (typeof hljs !== 'undefined') {
        hljs.highlightAll();
    }
    
    // Initialize MathJax
    if (typeof MathJax !== 'undefined') {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
    
    console.log("DOM loaded, checking for mermaid diagrams...");
    
    // Check for mermaid code blocks and convert them to mermaid div elements
    document.querySelectorAll('pre code.language-mermaid').forEach(function(el) {
        console.log("Found mermaid code block, converting to mermaid diagram");
        const content = el.textContent;
        const pre = el.parentNode;
        const div = document.createElement('div');
        div.className = 'mermaid';
        div.textContent = content;
        pre.parentNode.replaceChild(div, pre);
    });
    
    // Better Mermaid initialization with multiple attempts
    if (typeof mermaid !== 'undefined') {
        console.log("Mermaid library found, initializing...");
        
        // Configure mermaid
        mermaid.initialize({
            theme: 'dark',
            securityLevel: 'loose',
            startOnLoad: true,
            flowchart: { 
                useMaxWidth: false,
                htmlLabels: true
            }
        });
        
        // First attempt immediately
        try {
            mermaid.init(undefined, '.mermaid');
            console.log("Initial mermaid initialization complete");
        } catch (e) {
            console.error("Error in initial mermaid initialization:", e);
        }
        
        // Second attempt after a delay
        setTimeout(function() {
            try {
                console.log("Running delayed mermaid initialization");
                mermaid.init(undefined, '.mermaid:not(.mermaid-processed)');
                document.querySelectorAll('.mermaid').forEach(function(el) {
                    el.classList.add('mermaid-processed');
                });
                console.log("Delayed mermaid initialization complete");
            } catch (e) {
                console.error("Error in delayed mermaid initialization:", e);
            }
        }, 1000);
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
