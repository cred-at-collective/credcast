#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import shutil
import subprocess
import re
import yaml
import markdown
from dateutil import parser as dateutil_parser
from markdown.extensions.codehilite import CodeHiliteExtension
from markdown.extensions.fenced_code import FencedCodeExtension
from datetime import datetime
import argparse

"""
credcast.py - A simple static site generator for cred.at blogs

Usage:
  credcast.py [options] <content_dir>

Options:
  --site-name NAME    Subdomain to use (default: derived from content_dir)
  --output-dir DIR    Local output directory (default: /tmp/credcast-build-{site})
  --deploy            Deploy to server after building
  --server HOST       Server to deploy to (default: root@YOUR_DIGITAL_OCEAN_IP)
  --dry-run           Build locally without deploying

Examples:
  credcast.py ~/repos/lux.cred.at --deploy
  credcast.py content/blog --site-name myname.cred.at --output-dir ./build
"""

# Templates
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | {site_name}</title>
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&display=swap">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            theme: 'dark',
            securityLevel: 'loose',
            startOnLoad: true
        });
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    <script src="/scripts.js"></script>
</head>
<body class="blog-layout">
    <div class="nav-sidebar">
        <div class="nav-header">
            <h2><a href="/">{site_name}</a></h2>
        </div>
        <div class="post-list">
            {post_links}
        </div>
    </div>
    <div class="content-area">
        <article>
            <h1>{title}</h1>
            <time datetime="{date_iso}">{date_display}</time>
            
            <div class="content">
                {content}
            </div>
            
            <div class="tags">
                {tags}
            </div>
        </article>
    </div>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{site_name}</title>
    <link rel="stylesheet" href="/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/styles/atom-one-dark.min.css">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anonymous+Pro:ital,wght@0,400;0,700;1,400;1,700&display=swap">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.7.0/highlight.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <script>
        mermaid.initialize({
            theme: 'dark',
            securityLevel: 'loose',
            startOnLoad: true
        });
    </script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    <script src="/scripts.js"></script>
</head>
<body class="blog-layout">
    <div class="nav-sidebar">
        <div class="nav-header">
            <h2><a href="/">{site_name}</a></h2>
        </div>
        <div class="post-list">
            {post_links}
        </div>
    </div>
    <div class="content-area">
        <!-- Latest post -->
        {latest_post}
    </div>
</body>
</html>
"""

RSS_TEMPLATE = """<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
<channel>
    <title>{site_name}</title>
    <link>https://{site_name}/</link>
    <description>Latest posts from {site_name}</description>
    <language>en-us</language>
    <lastBuildDate>{build_date}</lastBuildDate>
    <atom:link href="https://{site_name}/feed.xml" rel="self" type="application/rss+xml" />
    {items}
</channel>
</rss>
"""

RSS_ITEM_TEMPLATE = """
<item>
    <title>{title}</title>
    <link>https://{site_name}{url}</link>
    <description><![CDATA[{content}]]></description>
    <pubDate>{pub_date}</pubDate>
    <guid>https://{site_name}{url}</guid>
</item>
"""

SCRIPTS_JS = """document.addEventListener('DOMContentLoaded', function() {
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
"""

STYLE_CSS = """:root {
    --bg-color: #000000;
    --text-color: #bbbbbb;
    --nav-bg: #000000;
    --border-color: #333;
    --link-color: #00b7ff;
    --code-bg: #1e1e1e;
}

/* Base styles */
html,
body {
    margin: 0;
    padding: 0;
    height: 100%;
    background: var(--bg-color);
    color: var(--text-color);
    font-family: "Anonymous Pro", monospace;
    font-size: 20px;
    line-height: 1.3;
}

/* Blog layout specific */
.blog-layout {
    display: flex;
    min-height: 100vh;
    background: var(--bg-color);
    margin: 0;
    padding: 0;
}

/* Navigation sidebar */
.nav-sidebar {
    width: 220px;
    background: var(--nav-bg);
    padding: 20px;
    border-right: 1px solid var(--border-color);
    height: 100vh;
    overflow-y: auto;
    position: fixed;
    top: 0;
    left: 0;
    box-sizing: border-box;
}

/* Content area */
.content-area {
    margin-left: 260px; /* nav width + padding */
    padding: 20px;
    max-width: 800px;
    min-height: 100vh;
    overflow-y: auto;
    box-sizing: border-box;
    flex-grow: 1;
}

/* For non-blog-layout pages */
.post-content {
    margin-left: 260px;
    padding: 20px;
    max-width: 800px;
    box-sizing: border-box;
}

/* Navigation styling */
.nav-header {
    margin-bottom: 30px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border-color);
}

.nav-header h2 {
    margin: 0;
}

.nav-header a {
    text-decoration: none;
    color: var(--text-color);
}

.post-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.post-link a {
    text-decoration: none;
    color: #999;
    display: block;
    padding: 5px 0;
}

.post-link .date {
    display: block;
    color: var(--link-color);
    font-size: 0.9em;
}

.post-link .title {
    display: block;
    padding-left: 1em;
    word-wrap: break-word;
}

/* Links */
a {
    color: var(--link-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

/* Headers */

h1,
h2,
h3 {
    color: #0090cc;
    border-bottom: 1px solid rgba(0, 183, 255, 0.2);
    padding-bottom: 0.3em;
}

h4,
h5,
h6 {
    color: var(--text-color);
}

em {
    color: #888888;
    font-style: italic;
}

/* Make sure images don't overflow */
img {
    max-width: 100%;
    height: auto;
}

/* Base code block styling */
pre {
    background: #1e1e1e;
    padding: 1em;
    margin: 1em 0;
    border-radius: 4px;
    border: 1px solid var(--border-color);
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
    overflow-x: auto;
}

pre code {
    background: none;
    padding: 0;
    color: #ffffff;
    white-space: pre-wrap;
    word-wrap: break-word;
    overflow-wrap: break-word;
}

/* Inline code */
code {
    background: #1e1e1e;
    padding: 0.2em 0.4em;
    border-radius: 3px;
    font-size: 0.9em;
}

/* Disable highlight.js for cred blocks */
pre code.language-cred {
    color: #ffffff !important;
}

/* Special styling for Mermaid diagrams */
.mermaid {
    background: transparent;
    margin: 1.5em 0;
}

/* Make MathJax formulas stand out */
.MathJax {
    color: #cccccc !important;
}

/* Custom cred@ highlighting */
pre code.language-cred {
    position: relative;
}

/* Use JavaScript to add this class to the cred@ text */
.cred-highlight {
    color: #00b7ff !important;
}

/* phone layout */
@media screen and (max-width: 768px) {
    html,
    body {
        font-size: 22px;
    }

    /* Fix mobile layout */
    .blog-layout {
        flex-direction: column;
    }

    .nav-sidebar {
        width: 100%;
        height: auto;
        position: static;
        border-right: none;
        border-bottom: 1px solid var(--border-color);
    }

    .content-area,
    .post-content {
        margin-left: 0;
        width: 100%;
        padding: 15px;
        box-sizing: border-box;
    }

    /* Make code blocks more readable on mobile */
    pre {
        padding: 10px;
        font-size: 0.8em;
    }

    /* Adjust heading sizes for mobile */
    h1 {
        font-size: 1.8em;
    }
    h2 {
        font-size: 1.5em;
    }
    h3 {
        font-size: 1.2em;
    }
}

.graphviz-diagram {
    background: transparent !important;
    display: block !important;
    margin: 2em auto !important;
    max-width: 100% !important;
}

.graphviz-diagram path {
    stroke: #00b7ff !important;
    stroke-width: 1.5 !important;
}

.graphviz-diagram text {
    fill: #bbbbbb !important;
}

.graphviz-diagram polygon {
    fill: transparent !important;
    stroke: #00b7ff !important;
}

.graphviz-diagram ellipse {
    fill: transparent !important;
    stroke: #00b7ff !important;
}

/* Style dotted lines */
.graphviz-diagram path[style*="dotted"] {
    stroke-dasharray: 2, 2 !important;
    stroke-width: 1 !important;
}
"""

def parse_frontmatter(content):
    """Extract YAML front matter from markdown content"""
    if content.startswith('---'):
        end_idx = content.find('---', 3)
        if end_idx != -1:
            front_matter = yaml.safe_load(content[3:end_idx])
            content = content[end_idx+3:].strip()
            return front_matter, content
    return {}, content

def format_date(date_value):
    """Format date for display"""
    if isinstance(date_value, str):
        try:
            date_obj = dateutil_parser.parse(date_value)
            return date_obj.strftime('%B %d, %Y')
        except ValueError:
            return date_value
    elif hasattr(date_value, 'strftime'):
        # It's a datetime object
        return date_value.strftime('%B %d, %Y')
    else:
        return str(date_value)

def format_rfc822_date(date_value):
    """Format date in RFC 822 format for RSS"""
    if isinstance(date_value, str):
        try:
            date_obj = dateutil_parser.parse(date_value)
            return date_obj.strftime('%a, %d %b %Y %H:%M:%S +0000')
        except ValueError:
            return datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
    elif hasattr(date_value, 'strftime'):
        # It's a datetime object
        return date_value.strftime('%a, %d %b %Y %H:%M:%S +0000')
    else:
        return datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')

def parse_markdown_file(file_path):
    """Parse a markdown file and extract metadata and content"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse front matter
    front_matter, markdown_content = parse_frontmatter(content)
    
    # Extract metadata with defaults
    title = front_matter.get('title', os.path.splitext(os.path.basename(file_path))[0])
    
    # Handle date - try to parse it if string, use as is if datetime
    date_value = front_matter.get('date')
    if date_value is None:
        date_value = datetime.now()
    elif isinstance(date_value, str):
        try:
            date_value = dateutil_parser.parse(date_value)
        except ValueError:
            print(f"Warning: Could not parse date '{date_value}' in {file_path}. Using current date.")
            date_value = datetime.now()
    
    tags = front_matter.get('tags', [])
    
    # Remove title manually from markdown content
    # This handles different ways the title might appear
    lines = markdown_content.strip().split('\n')
    sanitized_lines = []
    title_found = False
    
    for i, line in enumerate(lines):
        # Check for various formats of title
        if i == 0 and (line.startswith('# ') and line[2:].strip() == title or line.strip() == title):
            title_found = True
            continue
        # Also skip empty line after title
        if title_found and i == 1 and not line.strip():
            continue
        sanitized_lines.append(line)
    
    # Use the sanitized content
    markdown_content = '\n'.join(sanitized_lines)
    
    # Convert to HTML
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
    
    # Format date strings
    date_display = format_date(date_value)
    date_iso = date_value.strftime('%Y-%m-%d')
    
    return {
        'title': title,
        'date': date_value,
        'date_display': date_display,
        'date_iso': date_iso,
        'tags': tags,
        'content': html_content,
        'source_path': file_path
    }

def process_markdown_files(content_dir):
    """Process all markdown files in a directory and its subdirectories"""
    posts = []
    
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                post = parse_markdown_file(file_path)
                posts.append(post)
    
    # Sort posts by date (newest first)
    posts.sort(key=lambda x: x['date'], reverse=True)
    return posts

def generate_post_links(posts, current_post=None):
    """Generate HTML for the post links sidebar"""
    links = []
    for post in posts:
        # Handle date that might be a string or datetime object
        date_value = post['date']
        if isinstance(date_value, str):
            try:
                date_obj = dateutil_parser.parse(date_value)
            except ValueError:
                date_obj = datetime.now()
        else:
            # Already a datetime or date object
            date_obj = date_value
        
        url = f"/{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}/"
        
        # Highlight current post
        current_class = ' current' if current_post and current_post['title'] == post['title'] else ''
        
        # Format date display
        date_display = format_date(date_value)
        
        link_html = f"""<div class="post-link{current_class}">
            <a href="{url}">
                <span class="date">{date_display}</span>
                <span class="title">{post['title']}</span>
            </a>
        </div>"""
        links.append(link_html)
    
    return '\n'.join(links)

def generate_tags_html(tags):
    """Generate HTML for post tags"""
    if not tags:
        return ''
    
    tags_html = []
    for tag in tags:
        tags_html.append(f'<span class="tag">#{tag}</span>')
    
    return ' '.join(tags_html)

def generate_post_html(post, posts, site_name):
    """Generate HTML for a single post"""
    post_links = generate_post_links(posts, post)
    tags_html = generate_tags_html(post['tags'])
    
    return HTML_TEMPLATE.format(
        title=post['title'],
        site_name=site_name,
        date_iso=post['date_iso'],
        date_display=post['date_display'],
        content=post['content'],
        tags=tags_html,
        post_links=post_links
    )

def generate_index_html(posts, site_name):
    """Generate HTML for the index page"""
    if not posts:
        return f"<h1>Welcome to {site_name}</h1><p>No posts yet!</p>"
    
    latest_post = posts[0]
    post_links = generate_post_links(posts, latest_post)
    tags_html = generate_tags_html(latest_post['tags'])
    
    latest_post_html = f"""<article>
        <h1>{latest_post['title']}</h1>
        <time datetime="{latest_post['date_iso']}">{latest_post['date_display']}</time>
        
        <div class="content">
            {latest_post['content']}
        </div>
        
        <div class="tags">
            {tags_html}
        </div>
    </article>"""
    
    return INDEX_TEMPLATE.format(
        site_name=site_name,
        post_links=post_links,
        latest_post=latest_post_html
    )

def generate_rss_feed(posts, site_name):
    """Generate RSS feed XML"""
    items = []
    for post in posts:
        # Handle date that might be a string or datetime object
        date_value = post['date']
        if isinstance(date_value, str):
            try:
                date_obj = dateutil_parser.parse(date_value)
            except ValueError:
                date_obj = datetime.now()
        else:
            # Already a datetime or date object
            date_obj = date_value
            
        url = f"/{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}/"
        
        item = RSS_ITEM_TEMPLATE.format(
            title=post['title'],
            site_name=site_name,
            url=url,
            content=post['content'],
            pub_date=format_rfc822_date(date_value)
        )
        items.append(item)
    
    rss = RSS_TEMPLATE.format(
        site_name=site_name,
        build_date=format_rfc822_date(datetime.now()),
        items='\n'.join(items)
    )
    
    return rss

def create_output_directories(output_dir, posts):
    """Create output directories for posts"""
    for post in posts:
        # Handle date that might be a string or datetime object
        date_value = post['date']
        if isinstance(date_value, str):
            try:
                date_obj = dateutil_parser.parse(date_value)
            except ValueError:
                # If we can't parse the date format, use today's date
                print(f"Warning: Could not parse date '{date_value}' for post '{post['title']}'. Using today's date.")
                date_obj = datetime.now()
        else:
            # Already a datetime object
            date_obj = date_value
        
        post_dir = os.path.join(
            output_dir,
            str(date_obj.year),
            f"{date_obj.month:02d}",
            f"{date_obj.day:02d}"
        )
        os.makedirs(post_dir, exist_ok=True)

def copy_image_files(content_dir, output_dir):
    """Copy image files from content directory to output directory"""
    img_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.svg']
    img_dir = os.path.join(output_dir, 'img')
    os.makedirs(img_dir, exist_ok=True)
    
    for root, _, files in os.walk(content_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in img_extensions):
                src_path = os.path.join(root, file)
                dest_path = os.path.join(img_dir, file)
                shutil.copy2(src_path, dest_path)
                print(f"Copied image: {file}")

def write_output_files(output_dir, posts, site_name):
    """Write all output files"""
    # Create output directories
    create_output_directories(output_dir, posts)
    
    # Write post files
    for post in posts:
        # Handle date that might be a string or datetime object
        date_value = post['date']
        if isinstance(date_value, str):
            try:
                date_obj = dateutil_parser.parse(date_value)
            except ValueError:
                print(f"Warning: Could not parse date '{date_value}' for post '{post['title']}'. Using today's date.")
                date_obj = datetime.now()
        else:
            # Already a datetime object
            date_obj = date_value
            
        post_path = os.path.join(
            output_dir,
            str(date_obj.year),
            f"{date_obj.month:02d}",
            f"{date_obj.day:02d}",
            'index.html'
        )
        
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(generate_post_html(post, posts, site_name))
        
        print(f"Generated: {post_path}")
    
    # Write index file
    index_path = os.path.join(output_dir, 'index.html')
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(generate_index_html(posts, site_name))
    
    print(f"Generated: {index_path}")
    
    # Write RSS feed
    rss_path = os.path.join(output_dir, 'feed.xml')
    with open(rss_path, 'w', encoding='utf-8') as f:
        f.write(generate_rss_feed(posts, site_name))
    
    print(f"Generated: {rss_path}")
    
    # Write style.css
    css_path = os.path.join(output_dir, 'style.css')
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(STYLE_CSS)
    
    print(f"Generated: {css_path}")
    
    # Write scripts.js
    js_path = os.path.join(output_dir, 'scripts.js')
    with open(js_path, 'w', encoding='utf-8') as f:
        f.write(SCRIPTS_JS)
    
    print(f"Generated: {js_path}")

def deploy_to_server(output_dir, site_name, server="root@YOUR_DIGITAL_OCEAN_IP", remote_path=None):
    """Deploy the site to the server using rsync"""
    if remote_path is None:
        remote_path = f"/var/www/{site_name}"
    
    cmd = [
        "rsync", "-avz", "--delete", "--progress",
        f"{output_dir}/",
        f"{server}:{remote_path}/"
    ]
    
    print(f"Deploying to {server}:{remote_path}...")
    subprocess.run(cmd)
    print(f"Deployment complete! Site is live at https://{site_name}/")

def main():
    parser = argparse.ArgumentParser(description="credcast - Simple static site generator for cred.at blogs")
    parser.add_argument("content_dir", help="Directory containing markdown files")
    parser.add_argument("--site-name", help="Subdomain name (default: derived from content_dir)")
    parser.add_argument("--output-dir", help="Local output directory")
    parser.add_argument("--deploy", action="store_true", help="Deploy to server after building")
    parser.add_argument("--server", default="root@YOUR_DIGITAL_OCEAN_IP", 
                        help="Server to deploy to")
    parser.add_argument("--remote-path", default="/var/www/{site_name}",
                        help="Remote path template (use {site_name} as placeholder)")
    parser.add_argument("--dry-run", action="store_true", help="Build locally without deploying")
    
    args = parser.parse_args()
    
    # Normalize paths
    content_dir = os.path.abspath(args.content_dir)
    
    # Determine site name from directory if not specified
    site_name = args.site_name if args.site_name else os.path.basename(content_dir)
    
    # Determine output directory
    if args.output_dir:
        output_dir = os.path.abspath(args.output_dir)
    else:
        output_dir = f"/tmp/credcast-build-{site_name}"
    
    print(f"Building site: {site_name}")
    print(f"Content directory: {content_dir}")
    print(f"Output directory: {output_dir}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Process markdown files
    posts = process_markdown_files(content_dir)
    print(f"Found {len(posts)} posts")
    
    # Copy images
    copy_image_files(content_dir, output_dir)
    
    # Write output files
    write_output_files(output_dir, posts, site_name)
    
    # Deploy if requested
    if args.deploy and not args.dry_run:
        # Format remote path with site_name
        remote_path = args.remote_path.format(site_name=site_name)
        deploy_to_server(output_dir, site_name, args.server, remote_path)
    elif args.dry_run:
        print(f"Dry run complete. Site built at {output_dir}")
    else:
        print(f"Build complete. To deploy, run with --deploy option")

if __name__ == "__main__":
    main()
