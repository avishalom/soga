#!/usr/bin/env python3
"""
Continue recovery - Batch 2 focusing on remaining high-priority pages
"""

import os
import re
import subprocess
from pathlib import Path
import time

def download_image_curl(img_url, local_path):
    """Download a single image using curl"""
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'curl', '-k', '--connect-timeout', '10', '--max-time', '30',
            '--retry', '2', '--user-agent', 'Mozilla/5.0',
            '-o', str(local_path), img_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 100:
            return True
        else:
            if local_path.exists():
                local_path.unlink()
            return False
            
    except Exception:
        return False

def fix_specific_page(page_path, base_url, max_downloads=50):
    """Fix broken images on a specific page with download limit"""
    print(f"\n=== FIXING: {page_path} ===")
    
    try:
        with open(page_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {page_path}: {e}")
        return 0
    
    # Extract all image src attributes
    img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
    matches = re.findall(img_pattern, content, re.IGNORECASE)
    
    html_dir = Path(page_path).parent
    downloads_successful = 0
    downloads_attempted = 0
    
    print(f"Found {len(matches)} image references")
    
    for match in matches[:max_downloads]:  # Limit downloads per page
        img_src = match[0]
        
        # Skip external URLs
        if img_src.startswith('http'):
            continue
        
        # Skip malformed filenames with brackets
        if '[' in img_src or ']' in img_src:
            continue
        
        # Check if file exists locally
        local_path = html_dir / img_src
        if local_path.exists():
            continue
            
        # This image is missing - download it
        downloads_attempted += 1
        img_url = f"{base_url}/{img_src}"
        
        print(f"Downloading: {img_src}")
        if download_image_curl(img_url, local_path):
            downloads_successful += 1
            print(f"✅ SUCCESS: {local_path}")
        else:
            print(f"❌ FAILED: {img_src}")
        
        time.sleep(0.2)
    
    print(f"Results: {downloads_successful}/{downloads_attempted} successful")
    return downloads_successful

def main():
    """Fix next batch of high-priority pages with many broken images"""
    print("=== BATCH 2 RECOVERY ===")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Next batch of high-priority pages
    priority_pages = [
        # A-HG NY and other problematic pages
        {
            'local': 'A-HG/2012 NY.htm',
            'base_url': 'http://skydogsports.com/A-HG'
        },
        {
            'local': 'A-HG/NY-09-01.htm', 
            'base_url': 'http://skydogsports.com/A-HG'
        },
        {
            'local': 'A-HG/quest-04.htm',
            'base_url': 'http://skydogsports.com/A-HG'
        },
        
        # More A-DOXIE-WEBSITE pages
        {
            'local': 'A-DOXIE-WEBSITE/dfest04.htm',
            'base_url': 'http://skydogsports.com/A-DOXIE-WEBSITE'
        },
        {
            'local': 'A-DOXIE-WEBSITE/dfest05.htm',
            'base_url': 'http://skydogsports.com/A-DOXIE-WEBSITE'
        },
        {
            'local': 'A-DOXIE-WEBSITE/Doggie-Treats.htm',
            'base_url': 'http://skydogsports.com/A-DOXIE-WEBSITE'
        },
        
        # More A-WATER-SKI pages
        {
            'local': 'A-WATER-SKI/Brett.htm',
            'base_url': 'http://skydogsports.com/A-WATER-SKI'
        },
        {
            'local': 'A-WATER-SKI/Waterski-2-2006.htm',
            'base_url': 'http://skydogsports.com/A-WATER-SKI'
        },
        
        # Remaining Windsurfing
        {
            'local': 'A-Windsurfing/2015-W-Surf.htm',
            'base_url': 'http://skydogsports.com/A-Windsurfing'
        },
        
        # RC with valid filenames only
        {
            'local': 'RC/indoor.htm',
            'base_url': 'http://skydogsports.com/RC'
        }
    ]
    
    total_recovered = 0
    
    for page_info in priority_pages:
        page_path = page_info['local']
        base_url = page_info['base_url']
        
        if Path(page_path).exists():
            recovered = fix_specific_page(page_path, base_url)
            total_recovered += recovered
        else:
            print(f"Page not found: {page_path}")
    
    print(f"\n=== BATCH 2 RECOVERY COMPLETE ===")
    print(f"Total additional images recovered: {total_recovered}")
    
    # Check final progress
    print(f"\nChecking final recovery progress...")
    
    # Re-run analysis to see improvement
    os.system("python3 comprehensive_broken_analysis.py")

if __name__ == "__main__":
    main()