# credcast - Simple blogging for cred.at

Credcast is a minimal static site generator designed for the cred.at blogging platform. It takes markdown files with YAML front matter and turns them into beautiful, simple blogs with support for:

- MathJax equations
- Mermaid.js diagrams 
- Syntax highlighting
- RSS feeds
- Mobile-friendly design

## Installation

```bash
# Clone the repository
git clone https://github.com/cred-at-collective/credcast.git
cd credcast

# Run the setup script (creates a virtual environment)
chmod +x setup.sh
./setup.sh
```

## Server Configuration

To configure your server details:

```bash
# Copy the example config and edit it
cp config.example.sh config.sh
nano config.sh  # Edit with your server details
```

This allows you to set your server details once rather than specifying them each time.

## Usage

```bash
./credcast.py [options] <content_dir>
```

### Options

- `--site-name NAME`: Subdomain to use (default: derived from content_dir)
- `--output-dir DIR`: Local output directory (default: /tmp/credcast-build-{site})
- `--deploy`: Deploy to server after building
- `--server HOST`: Server to deploy to (default: gdlx@iad1-shared-b7-24.dreamhost.com)
- `--dry-run`: Build locally without deploying

### Examples

```bash
# Build and deploy your blog
./run.sh ~/repos/lux.cred.at --deploy

# Build locally without deploying
./run.sh content/blog --site-name myname.cred.at --output-dir ./build
```

## Markdown Format

Your markdown files should include YAML front matter at the top:

```markdown
---
title: My Amazing Post
date: 2025-04-17
tags: [example, blog, cred@]
---

# My Amazing Post

This is a sample post with support for **Markdown**, *MathJax* and Mermaid diagrams.

## Mermaid Diagram

```mermaid
graph TD
    A[Start] --> B{Decision}
    B -- Yes --> C[Do Something]
    B -- No --> D[Do Nothing]
    C --> E[End]
    D --> E
```

## Math Equations

When $a \ne 0$, there are two solutions to $ax^2 + bx + c = 0$ and they are:

$$x = {-b \pm \sqrt{b^2-4ac} \over 2a}$$

## Code Example

```python
def hello_world():
    print("Hello from cred.at!")
```
```

## Directory Structure

Organize your content directory however you like. Images should be placed in a folder called `img` within your content directory.

```
my-blog/
├── post1.md
├── post2.md
├── img/
│   ├── image1.jpg
│   └── image2.png
└── drafts/
    └── upcoming-post.md  # Won't be published unless it has front matter
```

## How It Works

1. Parses all markdown files with front matter
2. Converts them to HTML with templates
3. Creates a date-based directory structure
4. Generates an index page showing the latest post
5. Creates an RSS feed
6. (Optional) Deploys to your cred.at subdomain

## License

MIT

## Credits

Created for the cred@ attribution system - https://cred.at
