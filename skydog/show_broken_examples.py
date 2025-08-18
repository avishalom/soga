#!/usr/bin/env python3
"""
Show examples of image links that are still broken
"""

import os
import re
from pathlib import Path

def find_broken_examples():
    """Find examples of remaining broken image links"""
    print("=== EXAMPLES OF REMAINING BROKEN IMAGE LINKS ===\n")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    examples_found = 0
    
    for html_file in html_files[:20]:  # Check first 20 files
        if examples_found >= 10:  # Limit to 10 examples
            break
            
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            continue
        
        # Find all image src attributes
        img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
        matches = re.findall(img_pattern, content, re.IGNORECASE)
        
        html_dir = html_file.parent
        file_examples = []
        
        for match in matches:
            img_src = match[0]
            
            # Skip external URLs
            if img_src.startswith('http'):
                continue
            
            # Check if file exists locally
            local_img_path = html_dir / img_src
            if not local_img_path.exists():
                file_examples.append(img_src)
                if len(file_examples) >= 3:  # Max 3 per file
                    break
        
        if file_examples:
            print(f"📄 **File**: {html_file}")
            for img_src in file_examples:
                print(f"   ❌ Missing: {img_src}")
                
                # Try to understand why it's broken
                if img_src.startswith('../'):
                    print(f"      → Relative path pointing to parent directory")
                elif '/' in img_src:
                    dir_name = img_src.split('/')[0]
                    expected_dir = html_dir / dir_name
                    if not expected_dir.exists():
                        print(f"      → Expected directory doesn't exist: {expected_dir}")
                    else:
                        print(f"      → File missing from existing directory: {expected_dir}")
                else:
                    print(f"      → Missing from same directory as HTML file")
                    
            print()
            examples_found += 1
    
    print(f"Showed {examples_found} files with broken image examples")

if __name__ == "__main__":
    find_broken_examples()