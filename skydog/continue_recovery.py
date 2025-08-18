#!/usr/bin/env python3
"""
Continue systematic recovery of specific missing images
Focus on high-priority pages with many broken images
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

def fix_specific_page(page_path, base_url):
    """Fix all broken images on a specific page"""
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
    
    for match in matches:
        img_src = match[0]
        
        # Skip external URLs
        if img_src.startswith('http'):
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
    """Fix high-priority pages with many broken images"""
    print("=== CONTINUING SYSTEMATIC RECOVERY ===")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # High-priority pages to fix
    priority_pages = [
        # A-HG pages with many broken images
        {
            'local': 'A-HG/ridge.htm',
            'base_url': 'http://skydogsports.com/A-HG'
        },
        {
            'local': 'A-HG/2013-Quest.htm', 
            'base_url': 'http://skydogsports.com/A-HG'
        },
        {
            'local': 'A-HG/2013-Florida-A.htm',
            'base_url': 'http://skydogsports.com/A-HG'
        },
        
        # A-DOXIE-WEBSITE pages
        {
            'local': 'A-DOXIE-WEBSITE/dfest07.htm',
            'base_url': 'http://skydogsports.com/A-DOXIE-WEBSITE'
        },
        {
            'local': 'A-DOXIE-WEBSITE/dfest06.htm',
            'base_url': 'http://skydogsports.com/A-DOXIE-WEBSITE'
        },
        
        # A-WATER-SKI pages
        {
            'local': 'A-WATER-SKI/Waterski-2002.htm',
            'base_url': 'http://skydogsports.com/A-WATER-SKI'
        },
        {
            'local': 'A-WATER-SKI/Waterski-2006.htm',
            'base_url': 'http://skydogsports.com/A-WATER-SKI'
        },
        
        # A-Windsurfing pages  
        {
            'local': 'A-Windsurfing/2009.htm',
            'base_url': 'http://skydogsports.com/A-Windsurfing'
        },
        {
            'local': 'A-Windsurfing/2014-W-Surf.htm',
            'base_url': 'http://skydogsports.com/A-Windsurfing'
        },
        
        # RC pages
        {
            'local': 'RC/rcairplanes.htm',
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
    
    print(f"\n=== RECOVERY COMPLETE ===")
    print(f"Total additional images recovered: {total_recovered}")

if __name__ == "__main__":
    main()