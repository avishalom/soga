#!/usr/bin/env python3
"""
Comprehensive analysis of remaining broken image links
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def analyze_all_broken_links():
    """Find all remaining broken image links across the entire site"""
    print("=== COMPREHENSIVE BROKEN LINK ANALYSIS ===\n")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    
    broken_by_section = defaultdict(list)
    total_broken = 0
    total_checked = 0
    
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
        
        # Find all image src attributes
        img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
        matches = re.findall(img_pattern, content, re.IGNORECASE)
        
        html_dir = html_file.parent
        section_name = html_dir.name if html_dir.name != '.' else 'root'
        file_broken = []
        
        for match in matches:
            img_src = match[0]
            total_checked += 1
            
            # Skip external URLs
            if img_src.startswith('http'):
                continue
            
            # Check if file exists locally
            local_img_path = html_dir / img_src
            if not local_img_path.exists():
                file_broken.append(img_src)
                total_broken += 1
        
        if file_broken:
            broken_by_section[section_name].append({
                'file': str(html_file),
                'broken': file_broken[:5]  # First 5 examples
            })
    
    print(f"**SUMMARY**")
    print(f"Total images checked: {total_checked}")
    print(f"Total broken images: {total_broken}")
    print(f"Success rate: {((total_checked - total_broken) / total_checked * 100):.1f}%\n")
    
    # Show broken links by section
    for section, files in sorted(broken_by_section.items()):
        total_files_in_section = len(files)
        total_broken_in_section = sum(len(f['broken']) for f in files)
        
        print(f"📁 **{section.upper()}** ({total_files_in_section} files, ~{total_broken_in_section}+ broken)")
        
        for file_info in files[:3]:  # Show first 3 files per section
            print(f"   📄 {file_info['file']}")
            for broken in file_info['broken']:
                print(f"      ❌ {broken}")
        
        if len(files) > 3:
            print(f"   ... and {len(files) - 3} more files with broken images")
        print()

if __name__ == "__main__":
    analyze_all_broken_links()