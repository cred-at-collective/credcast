document.addEventListener('DOMContentLoaded', function() {
    // Initialize highlight.js
    hljs.highlightAll();
    
    // Initialize MathJax
    if (typeof MathJax !== 'undefined') {
        MathJax.Hub.Queue(["Typeset", MathJax.Hub]);
    }
    
    // Extra Mermaid initialization
    if (typeof mermaid !== 'undefined') {
        // Force re-render mermaid diagrams
        document.querySelectorAll('.mermaid').forEach(function(el) {
            const content = el.textContent;
            el.innerHTML = ''; // Clear the element
            el.textContent = content; // Restore the content
        });
        
        // Give it some time before reinitializing
        setTimeout(function() {
            mermaid.init(undefined, '.mermaid:not(.mermaid-processed)');
            document.querySelectorAll('.mermaid').forEach(function(el) {
                el.classList.add('mermaid-processed');
            });
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