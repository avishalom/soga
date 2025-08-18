#!/usr/bin/env python3
"""
Download missing images from the original skydogsports.com site
"""

import os
import re
import requests
import urllib3
from pathlib import Path
from urllib.parse import urljoin, quote
import time

# Disable SSL warnings for the expired certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def download_image(base_url, img_path, local_path):
    """Download a single image from the original site"""
    try:
        # Construct full URL
        img_url = urljoin(base_url, img_path)
        print(f"Downloading: {img_url}")
        
        # Make request with SSL verification disabled
        response = requests.get(img_url, verify=False, timeout=30)
        
        if response.status_code == 200:
            # Ensure directory exists
            local_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write image file
            with open(local_path, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {local_path}")
            return True
        else:
            print(f"❌ Failed to download {img_url}: Status {response.status_code}")
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

def download_missing_images_for_section(section_name, max_files=5):
    """Download missing images for a specific section"""
    section_dir = Path(section_name)
    base_url = f"http://skydogsports.com/{section_name}/"
    
    if not section_dir.exists():
        print(f"Section directory {section_name} doesn't exist")
        return
    
    print(f"\n=== Processing {section_name} ===")
    
    # Find all HTML files in this section
    html_files = list(section_dir.glob('*.htm')) + list(section_dir.glob('*.html'))
    files_processed = 0
    
    for html_file in html_files:
        if files_processed >= max_files:
            print(f"Reached limit of {max_files} files for {section_name}")
            break
            
        print(f"\nProcessing: {html_file}")
        broken_images = find_broken_images_in_html(html_file)
        
        if not broken_images:
            print(f"No broken images in {html_file}")
            continue
            
        print(f"Found {len(broken_images)} broken images")
        images_downloaded = 0
        
        for img_src in broken_images[:10]:  # Limit to 10 images per file
            local_path = html_file.parent / img_src
            
            if download_image(base_url, img_src, local_path):
                images_downloaded += 1
            
            # Be respectful to the server
            time.sleep(1)
        
        if images_downloaded > 0:
            files_processed += 1
            print(f"Downloaded {images_downloaded} images for {html_file}")

def main():
    """Main function to download missing images"""
    print("=== DOWNLOADING MISSING IMAGES FROM SKYDOGSPORTS.COM ===")
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Process key sections with missing images
    sections = [
        'A-Windsurfing',
        'A-kayaks',
        'A-HG'
    ]
    
    for section in sections:
        download_missing_images_for_section(section, max_files=3)  # Start with 3 files per section
        print(f"Completed processing {section}")
        time.sleep(2)  # Pause between sections
    
    print("\n=== DOWNLOAD COMPLETE ===")
    print("Run final_verification.py to see the improvement in link success rate")

if __name__ == "__main__":
    main()