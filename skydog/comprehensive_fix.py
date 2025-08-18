#!/usr/bin/env python3
"""
Comprehensive image link fixing script for Skydog Sports website
Handles URL encoding, fuzzy matching, and advanced path resolution
"""

import os
import re
import shutil
import urllib.parse
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher

def decode_url_path(path):
    """Decode URL encoded paths like 'BGP-Sloped%20copy.gif'"""
    return urllib.parse.unquote(path)

def fuzzy_match_filename(target_filename, available_files, threshold=0.8):
    """Find the best fuzzy match for a filename"""
    best_match = None
    best_ratio = 0
    
    target_lower = target_filename.lower()
    target_base = Path(target_filename).stem.lower()
    
    for available_file in available_files:
        available_lower = available_file.name.lower()
        available_base = available_file.stem.lower()
        
        # Direct filename match
        ratio = SequenceMatcher(None, target_lower, available_lower).ratio()
        if ratio > best_ratio and ratio >= threshold:
            best_ratio = ratio
            best_match = available_file
            
        # Base filename match (without extension)  
        base_ratio = SequenceMatcher(None, target_base, available_base).ratio()
        if base_ratio > best_ratio and base_ratio >= threshold:
            best_ratio = base_ratio
            best_match = available_file
    
    return best_match if best_ratio >= threshold else None

def find_all_images():
    """Build comprehensive map of all image files"""
    image_map = {}
    all_images = []
    
    print("Building comprehensive image database...")
    
    # Find all image files
    for img_file in Path('.').rglob('*.jpg'):
        filename = img_file.name
        if filename not in image_map:
            image_map[filename] = []
        image_map[filename].append(img_file)
        all_images.append(img_file)
    
    for ext in ['*.gif', '*.png', '*.bmp', '*.jpeg']:
        for img_file in Path('.').rglob(ext):
            filename = img_file.name
            if filename not in image_map:
                image_map[filename] = []
            image_map[filename].append(img_file)
            all_images.append(img_file)
    
    print(f"Found {len(all_images)} total image files")
    print(f"Found {len(image_map)} unique filenames")
    return image_map, all_images

def find_advanced_match(html_file_path, broken_src, image_map, all_images):
    """Advanced matching with URL decoding, fuzzy matching, and path resolution"""
    
    # Step 1: Try URL decoding
    decoded_src = decode_url_path(broken_src)
    if decoded_src != broken_src:
        decoded_filename = Path(decoded_src).name
        if decoded_filename in image_map:
            # Find the closest match
            html_dir = Path(html_file_path).parent
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
            
            if best_match:
                return best_match
    
    # Step 2: Direct filename match
    filename = Path(broken_src).name
    if filename in image_map:
        html_dir = Path(html_file_path).parent
        possible_files = image_map[filename]
        
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
        
        if best_match:
            return best_match
    
    # Step 3: Fuzzy matching
    fuzzy_match = fuzzy_match_filename(filename, all_images, threshold=0.85)
    if fuzzy_match:
        html_dir = Path(html_file_path).parent
        try:
            return os.path.relpath(fuzzy_match, html_dir)
        except ValueError:
            pass
    
    # Step 4: Look in expected directories based on filename patterns
    html_dir = Path(html_file_path).parent
    html_section = html_dir.name if html_dir.name != '.' else 'root'
    
    # Check common patterns
    search_patterns = [
        html_dir / filename,  # Same directory
        html_dir / 'images' / filename,  # images subdirectory
        Path('.') / 'images' / filename,  # root images
    ]
    
    # Add year-based patterns for specific sections
    if 'Windsurfing' in str(html_file_path):
        for year in ['2009', '2010', '2013', '2014', '2015', '2017', '2018']:
            search_patterns.append(html_dir / year / filename)
    
    for pattern in search_patterns:
        if pattern.exists():
            try:
                return os.path.relpath(pattern, html_dir)
            except ValueError:
                continue
    
    return None

def fix_html_file_comprehensive(html_file_path, image_map, all_images, dry_run=True):
    """Comprehensive fix for all types of broken image links"""
    
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
        
        # Find replacement using advanced matching
        replacement = find_advanced_match(html_file_path, full_src, image_map, all_images)
        if replacement and replacement != full_src:
            fixes_made += 1
            return f'src="{replacement}"'
        else:
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
    print("=== COMPREHENSIVE IMAGE LINK FIXER ===")
    print("Handles URL encoding, fuzzy matching, and advanced path resolution")
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Build comprehensive image database
    image_map, all_images = find_all_images()
    
    # Find all HTML files
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    print(f"Found {len(html_files)} HTML files to process")
    
    # First, do a dry run to see what would be fixed
    print("\n=== DRY RUN - COMPREHENSIVE ANALYSIS ===")
    total_fixes = 0
    files_with_fixes = 0
    
    for html_file in html_files:
        fixes = fix_html_file_comprehensive(html_file, image_map, all_images, dry_run=True)
        if fixes > 0:
            print(f"{html_file}: {fixes} additional fixes possible")
            total_fixes += fixes
            files_with_fixes += 1
    
    print(f"\nSummary: {total_fixes} additional fixes possible across {files_with_fixes} files")
    
    # Apply fixes automatically
    if total_fixes > 0:
        print("\n=== APPLYING COMPREHENSIVE FIXES ===")
        actual_fixes = 0
        for html_file in html_files:
            fixes = fix_html_file_comprehensive(html_file, image_map, all_images, dry_run=False)
            actual_fixes += fixes
            if fixes > 0:
                print(f"Fixed {html_file}: {fixes} additional links")
        
        print(f"\nCompleted! Fixed {actual_fixes} additional image links")
        print("All fixes applied with backups preserved")
    else:
        print("No additional fixes needed - all fixable links already resolved")

if __name__ == "__main__":
    main()