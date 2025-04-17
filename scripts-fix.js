document.addEventListener('DOMContentLoaded', function() {
    // Initialize highlight.js
    hljs.highlightAll();
    
    // Initialize MathJax
    if (typeof MathJax !== 'undefined') {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
    
    // Initialize Mermaid
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            theme: 'dark',
            securityLevel: 'loose',
            startOnLoad: true
        });
        // Manually call mermaid render for any diagrams that might not be caught automatically
        setTimeout(function() {
            mermaid.init(undefined, '.mermaid');
        }, 500);
    }
    
    // Highlight cred@ syntax in code blocks
    document.querySelectorAll('code.language-cred').forEach(function(block) {
        let html = block.innerHTML;
        // Match cred@ patterns
        html = html.replace(/(@cred@[a-zA-Z0-9:._-]+)/g, '<span class="cred-highlight">$1</span>');
        block.innerHTML = html;
    });
});