#!/usr/bin/env python3
"""
Final verification script to count remaining broken image links
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def analyze_broken_links():
    """Analyze broken image links in all HTML files"""
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    broken_links = []
    working_links = []
    total_files = 0
    
    # Find all HTML files
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    
    for html_file in html_files:
        total_files += 1
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {html_file}: {e}")
            continue
        
        # Find all image src attributes
        img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
        matches = re.findall(img_pattern, content, re.IGNORECASE)
        
        for match in matches:
            img_src = match[0]
            
            # Skip external URLs
            if img_src.startswith('http'):
                continue
            
            # Check if file exists
            html_dir = html_file.parent
            img_path = html_dir / img_src
            
            if img_path.exists():
                working_links.append((html_file, img_src))
            else:
                broken_links.append((html_file, img_src))
    
    # Summary statistics
    total_links = len(working_links) + len(broken_links)
    success_rate = (len(working_links) / total_links * 100) if total_links > 0 else 0
    
    print("=== FINAL IMAGE LINK STATUS ===")
    print(f"Total HTML files processed: {total_files}")
    print(f"Total image references: {total_links}")
    print(f"Working links: {len(working_links)} ({success_rate:.1f}%)")
    print(f"Broken links: {len(broken_links)} ({100-success_rate:.1f}%)")
    
    # Categorize remaining broken links
    if broken_links:
        print(f"\n=== REMAINING BROKEN LINKS ANALYSIS ===")
        
        # Group by type
        external = []
        same_dir = []
        complex_path = []
        url_encoded = []
        
        for html_file, img_src in broken_links[:50]:  # Show first 50 for analysis
            if img_src.startswith('http'):
                external.append((html_file, img_src))
            elif '/' not in img_src:
                same_dir.append((html_file, img_src))
            elif '%' in img_src:
                url_encoded.append((html_file, img_src))
            else:
                complex_path.append((html_file, img_src))
        
        print(f"External URLs: {len(external)}")
        print(f"Same directory: {len(same_dir)}")
        print(f"URL encoded: {len(url_encoded)}")  
        print(f"Complex paths: {len(complex_path)}")
        
        # Show some examples
        if same_dir:
            print(f"\nSample same-directory broken links:")
            for i, (html_file, img_src) in enumerate(same_dir[:5]):
                print(f"  {html_file}: {img_src}")
        
        if complex_path:
            print(f"\nSample complex path broken links:")
            for i, (html_file, img_src) in enumerate(complex_path[:5]):
                print(f"  {html_file}: {img_src}")

    return len(working_links), len(broken_links)

if __name__ == "__main__":
    working, broken = analyze_broken_links()