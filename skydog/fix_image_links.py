#!/usr/bin/env python3
"""
Script to fix broken image links in the Skydog Sports website
"""

import os
import re
import shutil
from pathlib import Path
from collections import defaultdict

def find_all_images():
    """Find all image files and their actual locations"""
    image_map = {}
    
    print("Mapping all image files...")
    for img_file in Path('.').rglob('*.jpg'):
        filename = img_file.name
        if filename not in image_map:
            image_map[filename] = []
        image_map[filename].append(str(img_file))
    
    for img_file in Path('.').rglob('*.gif'):
        filename = img_file.name
        if filename not in image_map:
            image_map[filename] = []
        image_map[filename].append(str(img_file))
    
    for img_file in Path('.').rglob('*.png'):
        filename = img_file.name
        if filename not in image_map:
            image_map[filename] = []
        image_map[filename].append(str(img_file))
        
    for img_file in Path('.').rglob('*.bmp'):
        filename = img_file.name
        if filename not in image_map:
            image_map[filename] = []
        image_map[filename].append(str(img_file))

    print(f"Found {len(image_map)} unique image filenames")
    return image_map

def find_best_match(html_file_path, broken_src, image_map):
    """Find the best matching image file for a broken src"""
    filename = Path(broken_src).name
    
    if filename not in image_map:
        return None
    
    possible_files = image_map[filename]
    html_dir = Path(html_file_path).parent
    
    # Try to find the closest match by directory structure
    best_match = None
    shortest_path = float('inf')
    
    for img_path in possible_files:
        try:
            # Calculate relative path from HTML file to image
            rel_path = os.path.relpath(img_path, html_dir)
            if len(rel_path) < shortest_path:
                shortest_path = len(rel_path)
                best_match = rel_path
        except ValueError:
            continue
    
    return best_match

def fix_html_file(html_file_path, image_map, dry_run=True):
    """Fix broken image links in a single HTML file"""
    with open(html_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original_content = content
    fixes_made = 0
    
    # Find all image src attributes
    img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
    
    def replace_src(match):
        nonlocal fixes_made
        full_src = match.group(1)
        
        # Check if the current path exists
        html_dir = Path(html_file_path).parent
        current_path = html_dir / full_src
        
        if current_path.exists():
            return match.group(0)  # No change needed
        
        # Find replacement
        replacement = find_best_match(html_file_path, full_src, image_map)
        if replacement:
            fixes_made += 1
            return f'src="{replacement}"'
        else:
            return match.group(0)  # No replacement found
    
    new_content = re.sub(img_pattern, replace_src, content, flags=re.IGNORECASE)
    
    if not dry_run and new_content != original_content:
        # Create backup
        backup_path = str(html_file_path) + '.backup'
        if not os.path.exists(backup_path):
            shutil.copy2(html_file_path, backup_path)
        
        # Write fixed content
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return fixes_made

def main():
    print("=== Skydog Image Link Fixer ===")
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Build image map
    image_map = find_all_images()
    
    # Find all HTML files
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    print(f"Found {len(html_files)} HTML files to process")
    
    # First, do a dry run to see what would be fixed
    print("\n=== DRY RUN ===")
    total_fixes = 0
    files_with_fixes = 0
    
    for html_file in html_files:
        fixes = fix_html_file(html_file, image_map, dry_run=True)
        if fixes > 0:
            print(f"{html_file}: {fixes} fixes possible")
            total_fixes += fixes
            files_with_fixes += 1
    
    print(f"\nSummary: {total_fixes} total fixes possible across {files_with_fixes} files")
    
    # Ask for confirmation before actual fixes
    if total_fixes > 0:
        print("\nProceeding with fixes automatically...")
        if True:  # Auto-proceed
            print("\n=== APPLYING FIXES ===")
            actual_fixes = 0
            for html_file in html_files:
                fixes = fix_html_file(html_file, image_map, dry_run=False)
                actual_fixes += fixes
                if fixes > 0:
                    print(f"Fixed {html_file}: {fixes} links")
            
            print(f"\nCompleted! Fixed {actual_fixes} image links total")
            print("Backup files created with .backup extension")
        else:
            print("Operation cancelled")

if __name__ == "__main__":
    main()