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