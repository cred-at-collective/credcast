#!/usr/bin/env python3
# Simple script to fix the template issues in credcast.py

import re

# Read the existing file
with open('credcast.py', 'r') as f:
    content = f.read()

# Fix: Escape curly braces in the mermaid initialization script
content = content.replace("""    <script>
        mermaid.initialize({
            theme: 'dark',
            securityLevel: 'loose',
            startOnLoad: true
        });
    </script>""", """    <script>
        mermaid.initialize({{
            theme: 'dark',
            securityLevel: 'loose',
            startOnLoad: true
        }});
    </script>""")

# Write the fixed content back
with open('credcast.py', 'w') as f:
    f.write(content)

print("Fixed the template issues in credcast.py. The curly braces in the mermaid initialization are now properly escaped.")
print("Try running your command again:")
print("./run.sh ~/repos/lux.cred.at --site-name lux.cred.at --deploy")
