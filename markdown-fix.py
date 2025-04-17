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
    
    # Check if the first line of markdown is an H1 with the same title
    # If so, strip it out to avoid duplication
    lines = markdown_content.strip().split('\n')
    if lines and lines[0].startswith('# ') and lines[0][2:].strip() == title:
        # Remove the first line (H1 title)
        markdown_content = '\n'.join(lines[1:]).strip()
    
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