#!/usr/bin/env python3
"""
Systematically map ALL broken image links across the entire site
Create a comprehensive broken.temp.txt file for systematic recovery
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def map_all_broken_links():
    """Map every broken image link with its source page and expected location"""
    print("=== MAPPING ALL BROKEN LINKS SYSTEMATICALLY ===\n")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    broken_links = []
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    
    total_checked = 0
    total_broken = 0
    
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
        
        for match in matches:
            img_src = match[0]
            total_checked += 1
            
            # Skip external URLs
            if img_src.startswith('http'):
                continue
            
            # Skip malformed filenames with brackets or other issues
            if '[' in img_src or ']' in img_src:
                continue
            
            # Check if file exists locally
            local_img_path = html_dir / img_src
            if not local_img_path.exists():
                total_broken += 1
                
                # Determine the base URL for this section
                if section_name == 'root':
                    base_url = "http://skydogsports.com"
                else:
                    base_url = f"http://skydogsports.com/{section_name}"
                
                broken_entry = {
                    'html_file': str(html_file),
                    'img_src': img_src,
                    'local_path': str(local_img_path),
                    'source_url': f"{base_url}/{img_src}",
                    'section': section_name
                }
                
                broken_links.append(broken_entry)
    
    print(f"ANALYSIS COMPLETE:")
    print(f"Total images checked: {total_checked}")
    print(f"Total broken images found: {total_broken}")
    print(f"Success rate: {((total_checked - total_broken) / total_checked * 100):.1f}%")
    
    return broken_links

def write_broken_links_file(broken_links):
    """Write systematic broken links file for recovery"""
    
    # Group by section for better organization
    by_section = defaultdict(list)
    for link in broken_links:
        by_section[link['section']].append(link)
    
    with open('broken.temp.txt', 'w') as f:
        f.write("# SYSTEMATIC BROKEN LINKS MAPPING\n")
        f.write("# Format: HTML_FILE|IMG_SRC|LOCAL_PATH|SOURCE_URL|SECTION\n")
        f.write(f"# Total broken links: {len(broken_links)}\n\n")
        
        # Write by section for systematic recovery
        for section in sorted(by_section.keys()):
            links = by_section[section]
            f.write(f"## SECTION: {section} ({len(links)} broken images)\n")
            
            # Group by HTML file within section
            by_file = defaultdict(list)
            for link in links:
                by_file[link['html_file']].append(link)
            
            for html_file in sorted(by_file.keys()):
                file_links = by_file[html_file]
                f.write(f"### FILE: {html_file} ({len(file_links)} broken images)\n")
                
                for link in file_links:
                    f.write(f"{link['html_file']}|{link['img_src']}|{link['local_path']}|{link['source_url']}|{link['section']}\n")
                
                f.write("\n")
            f.write("\n")
    
    print(f"Written broken links mapping to: broken.temp.txt")
    
    # Summary by section
    print(f"\nBROKEN LINKS BY SECTION:")
    for section in sorted(by_section.keys()):
        print(f"  {section}: {len(by_section[section])} broken images")

def main():
    """Create comprehensive mapping of all broken links"""
    broken_links = map_all_broken_links()
    write_broken_links_file(broken_links)
    
    print(f"\n=== MAPPING COMPLETE ===")
    print(f"Next step: Use broken.temp.txt for systematic recovery")

if __name__ == "__main__":
    main()