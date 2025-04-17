#!/usr/bin/env python3
import sys
import re
import os

def fix_mermaid_rendering(file_path):
    """
    Fix the mermaid rendering issue by modifying the credcast.py file.
    The issue is that mermaid code blocks are being converted to divs, but then
    those divs are being processed by the syntax highlighter.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # The issue is in the parse_markdown_file function
    # We need to modify the markdown conversion process
    
    # Find the section where mermaid blocks are processed
    mermaid_regex_pattern = r'# Special handling for mermaid code blocks\s+markdown_content = re\.sub\(\s+r\'```mermaid\s*\([\s\S]*?\)```\',\s+r\'<div class="mermaid">\\\1</div>\',\s+markdown_content\s+\)'
    
    # Modified approach:
    # 1. Process markdown first without modifying mermaid blocks
    # 2. After HTML conversion, find and replace code blocks with mermaid language class to proper mermaid divs
    replacement = """# Convert to HTML using the standard process
    html_content = markdown.markdown(
        markdown_content,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.smarty',
            'markdown.extensions.toc',
            CodeHiliteExtension(css_class='highlight'),
            FencedCodeExtension()
        ]
    )
    
    # After HTML conversion, replace any code blocks with language-mermaid class
    # with proper mermaid divs
    html_content = re.sub(
        r'<pre><code class="language-mermaid">([\s\S]*?)</code></pre>',
        r'<div class="mermaid">\\1</div>',
        html_content
    )"""
    
    # Remove the original mermaid preprocessing and conversion to HTML
    content = re.sub(
        r'# Special handling for mermaid code blocks.*?# Convert to HTML.*?html_content = markdown\.markdown\(.*?\s+\)',
        replacement,
        content,
        flags=re.DOTALL
    )
    
    # Write the modified content back to the file
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Fixed mermaid rendering in {file_path}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python fix-mermaid-rendering.py <path_to_credcast.py>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} does not exist")
        sys.exit(1)
    
    fix_mermaid_rendering(file_path)

if __name__ == "__main__":
    main()
