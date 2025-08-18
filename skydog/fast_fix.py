#!/usr/bin/env python3
"""
Fast targeted image link fixing script for remaining issues
"""

import os
import re
import shutil
import urllib.parse
from pathlib import Path
from collections import defaultdict

def decode_url_path(path):
    """Decode URL encoded paths like 'BGP-Sloped%20copy.gif'"""
    return urllib.parse.unquote(path)

def find_all_images():
    """Build comprehensive map of all image files"""
    image_map = {}
    
    print("Building image database...")
    
    # Find all image files with common extensions
    for ext in ['*.jpg', '*.jpeg', '*.png', '*.gif', '*.bmp']:
        for img_file in Path('.').rglob(ext):
            filename = img_file.name.lower()  # Use lowercase for matching
            if filename not in image_map:
                image_map[filename] = []
            image_map[filename].append(img_file)
    
    print(f"Found {sum(len(v) for v in image_map.values())} total image files")
    print(f"Found {len(image_map)} unique filenames")
    return image_map

def fix_html_file_fast(html_file_path, image_map, dry_run=True):
    """Fast fix for common broken image link patterns"""
    
    with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    fixes_made = 0
    
    # Find all image src attributes
    img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
    
    def replace_src(match):
        nonlocal fixes_made
        full_src = match.group(1)
        
        # Skip external URLs
        if full_src.startswith('http'):
            return match.group(0)
        
        # Check if the current path exists
        html_dir = Path(html_file_path).parent
        current_path = html_dir / full_src
        
        if current_path.exists():
            return match.group(0)  # No change needed
        
        # URL decode the path
        decoded_src = decode_url_path(full_src)
        decoded_filename = Path(decoded_src).name.lower()
        
        # Try to find the image in our database
        if decoded_filename in image_map:
            # Find the closest match
            possible_files = image_map[decoded_filename]
            best_match = None
            shortest_path = float('inf')
            
            for img_path in possible_files:
                try:
                    rel_path = os.path.relpath(img_path, html_dir)
                    if len(rel_path) < shortest_path:
                        shortest_path = len(rel_path)
                        best_match = rel_path
                except ValueError:
                    continue
            
            if best_match and best_match != full_src:
                fixes_made += 1
                return f'src="{best_match}"'
        
        # Try original filename if URL decode didn't help
        original_filename = Path(full_src).name.lower()
        if original_filename != decoded_filename and original_filename in image_map:
            possible_files = image_map[original_filename]
            best_match = None
            shortest_path = float('inf')
            
            for img_path in possible_files:
                try:
                    rel_path = os.path.relpath(img_path, html_dir)
                    if len(rel_path) < shortest_path:
                        shortest_path = len(rel_path)
                        best_match = rel_path
                except ValueError:
                    continue
            
            if best_match and best_match != full_src:
                fixes_made += 1
                return f'src="{best_match}"'
        
        return match.group(0)  # No replacement found
    
    new_content = re.sub(img_pattern, replace_src, content, flags=re.IGNORECASE)
    
    if not dry_run and new_content != original_content:
        # Create backup if it doesn't exist
        backup_path = str(html_file_path) + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(html_file_path, backup_path)
        
        # Write fixed content
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return fixes_made

def main():
    print("=== FAST IMAGE LINK FIXER ===")
    print("Targeting URL encoding and case sensitivity issues")
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Build image database
    image_map = find_all_images()
    
    # Find all HTML files
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    print(f"Found {len(html_files)} HTML files to process")
    
    # First, do a dry run
    print("\n=== DRY RUN ===")
    total_fixes = 0
    files_with_fixes = 0
    
    for html_file in html_files:
        fixes = fix_html_file_fast(html_file, image_map, dry_run=True)
        if fixes > 0:
            print(f"{html_file}: {fixes} fixes possible")
            total_fixes += fixes
            files_with_fixes += 1
    
    print(f"\nSummary: {total_fixes} fixes possible across {files_with_fixes} files")
    
    # Apply fixes
    if total_fixes > 0:
        print("\n=== APPLYING FIXES ===")
        actual_fixes = 0
        for html_file in html_files:
            fixes = fix_html_file_fast(html_file, image_map, dry_run=False)
            actual_fixes += fixes
            if fixes > 0:
                print(f"Fixed {html_file}: {fixes} links")
        
        print(f"\nCompleted! Fixed {actual_fixes} image links")
    else:
        print("No fixes needed")

if __name__ == "__main__":
    main()