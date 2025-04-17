#!/usr/bin/env python3
import os
import yaml
import sys

def main():
    """Debug the date in Markdown front matter"""
    if len(sys.argv) < 2:
        print("Usage: debug.py <content_dir>")
        sys.exit(1)
    
    content_dir = sys.argv[1]
    
    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"\nExamining file: {file_path}")
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse front matter
                if content.startswith('---'):
                    end_idx = content.find('---', 3)
                    if end_idx != -1:
                        try:
                            front_matter = yaml.safe_load(content[3:end_idx])
                            date = front_matter.get('date')
                            print(f"  Date: {date}")
                            print(f"  Type: {type(date)}")
                            
                            # If it's a date object, show its components
                            if hasattr(date, 'year'):
                                print(f"  Year: {date.year}")
                                print(f"  Month: {date.month}")
                                print(f"  Day: {date.day}")
                            
                        except Exception as e:
                            print(f"  Error parsing front matter: {e}")

if __name__ == "__main__":
    main()
