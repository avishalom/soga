#!/usr/bin/env python3
"""
Systematic fix for a specific page - download ALL missing images
Compare original site structure with local mirror and fix systematically
"""

import os
import re
import subprocess
from pathlib import Path
import time

def download_image_curl(img_url, local_path):
    """Download a single image using curl with better error handling"""
    try:
        print(f"Downloading: {img_url}")
        
        # Ensure directory exists
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use curl with better options
        cmd = [
            'curl', '-k', '--connect-timeout', '10', '--max-time', '30',
            '--retry', '2', '--user-agent', 'Mozilla/5.0 (compatible)',
            '-o', str(local_path), img_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 0:
            print(f"✅ SUCCESS: {local_path} ({local_path.stat().st_size} bytes)")
            return True
        else:
            print(f"❌ FAILED: {img_url}")
            print(f"   Error: {result.stderr}")
            if local_path.exists():
                local_path.unlink()
            return False
            
    except Exception as e:
        print(f"❌ EXCEPTION: {img_url} - {e}")
        return False

def fix_page_systematically(page_path, base_url):
    """Systematically fix ALL broken images on a specific page"""
    
    print(f"\n=== SYSTEMATIC FIX FOR {page_path} ===")
    
    # Read the local HTML file
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
            print(f"✅ EXISTS: {img_src}")
            continue
            
        # This image is missing - download it
        downloads_attempted += 1
        img_url = f"{base_url}/{img_src}"
        
        if download_image_curl(img_url, local_path):
            downloads_successful += 1
        
        # Be respectful to the server
        time.sleep(0.3)
    
    print(f"\n=== RESULTS ===")
    print(f"Images attempted: {downloads_attempted}")
    print(f"Images downloaded: {downloads_successful}")
    
    return downloads_successful

def main():
    """Fix the specific problematic page systematically"""
    print("=== SYSTEMATIC PAGE FIX ===")
    
    # Change to skydog directory  
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Fix the specific page we know has problems
    page_path = "A-HG/hg-07.htm"
    base_url = "http://skydogsports.com/A-HG"
    
    if not Path(page_path).exists():
        print(f"Page not found: {page_path}")
        return
    
    downloaded = fix_page_systematically(page_path, base_url)
    
    print(f"\n=== SYSTEMATIC FIX COMPLETE ===")
    print(f"Total new images downloaded: {downloaded}")

if __name__ == "__main__":
    main()