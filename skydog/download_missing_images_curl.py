#!/usr/bin/env python3
"""
Download missing images from skydogsports.com using curl
"""

import os
import re
import subprocess
from pathlib import Path
import time

def download_image_curl(base_url, img_path, local_path):
    """Download a single image using curl"""
    try:
        # Construct full URL
        img_url = f"{base_url.rstrip('/')}/{img_path}"
        print(f"Downloading: {img_url}")
        
        # Ensure directory exists
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use curl to download with insecure flag for expired cert
        cmd = [
            'curl', '-k', '--connect-timeout', '15', '--max-time', '30',
            '-o', str(local_path), img_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 0:
            print(f"✅ Downloaded: {local_path} ({local_path.stat().st_size} bytes)")
            return True
        else:
            print(f"❌ Failed to download {img_url}: {result.stderr}")
            # Clean up empty file
            if local_path.exists():
                local_path.unlink()
            return False
            
    except Exception as e:
        print(f"❌ Error downloading {img_url}: {e}")
        return False

def find_broken_images_in_html(html_file):
    """Find all broken image references in an HTML file"""
    broken_images = []
    
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {html_file}: {e}")
        return []
    
    # Find all image src attributes
    img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
    matches = re.findall(img_pattern, content, re.IGNORECASE)
    
    html_dir = html_file.parent
    
    for match in matches:
        img_src = match[0]
        
        # Skip external URLs
        if img_src.startswith('http'):
            continue
        
        # Check if file exists locally
        local_img_path = html_dir / img_src
        if not local_img_path.exists():
            broken_images.append(img_src)
    
    return broken_images

def download_missing_images_for_file(html_file, max_images=10):
    """Download missing images for a specific HTML file"""
    section_name = html_file.parent.name
    base_url = f"http://skydogsports.com/{section_name}/"
    
    print(f"\nProcessing: {html_file}")
    broken_images = find_broken_images_in_html(html_file)
    
    if not broken_images:
        print(f"No broken images in {html_file}")
        return 0
        
    print(f"Found {len(broken_images)} broken images")
    images_downloaded = 0
    
    for img_src in broken_images[:max_images]:  # Limit per file
        local_path = html_file.parent / img_src
        
        if download_image_curl(base_url, img_src, local_path):
            images_downloaded += 1
        
        # Be respectful to the server
        time.sleep(0.5)
    
    return images_downloaded

def main():
    """Main function to download missing images from specific problematic files"""
    print("=== DOWNLOADING MISSING IMAGES FROM SKYDOGSPORTS.COM ===")
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Start with the specific file we know has missing images
    test_files = [
        Path('A-Windsurfing/2009.htm'),
        Path('A-Windsurfing/2010.htm'),
        Path('A-kayaks/Kayak-P5.htm'),
        Path('A-kayaks/KAYAK-PHOTO-GALLERY.htm'),
    ]
    
    total_downloaded = 0
    
    for html_file in test_files:
        if html_file.exists():
            downloaded = download_missing_images_for_file(html_file, max_images=5)
            total_downloaded += downloaded
            print(f"Downloaded {downloaded} images for {html_file}")
            time.sleep(1)  # Pause between files
        else:
            print(f"File not found: {html_file}")
    
    print(f"\n=== DOWNLOAD COMPLETE ===")
    print(f"Total images downloaded: {total_downloaded}")
    print("Run final_verification.py to see the improvement")

if __name__ == "__main__":
    main()