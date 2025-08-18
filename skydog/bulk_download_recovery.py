#!/usr/bin/env python3
"""
Comprehensive bulk image recovery from skydogsports.com
Downloads many missing images systematically across all sections
"""

import os
import re
import subprocess
from pathlib import Path
import time
from collections import defaultdict

def download_image_curl(base_url, img_path, local_path):
    """Download a single image using curl"""
    try:
        # Handle encoded ampersands and other URL issues
        clean_img_path = img_path.replace('&amp;', '&')
        img_url = f"{base_url.rstrip('/')}/{clean_img_path}"
        
        # Ensure directory exists
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Use curl with more options for better success
        cmd = [
            'curl', '-k', '--connect-timeout', '10', '--max-time', '20',
            '--retry', '2', '--user-agent', 'Mozilla/5.0',
            '-o', str(local_path), img_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 100:
            return True
        else:
            # Clean up failed downloads
            if local_path.exists():
                local_path.unlink()
            return False
            
    except Exception as e:
        return False

def find_all_broken_images():
    """Find ALL broken images across the entire site"""
    broken_images_by_section = defaultdict(list)
    
    print("Analyzing all HTML files for broken images...")
    
    # Process all HTML files
    html_files = list(Path('.').rglob('*.html')) + list(Path('.').rglob('*.htm'))
    
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
            
            # Skip external URLs
            if img_src.startswith('http'):
                continue
            
            # Check if file exists locally
            local_img_path = html_dir / img_src
            if not local_img_path.exists():
                broken_images_by_section[section_name].append({
                    'html_file': html_file,
                    'img_src': img_src,
                    'local_path': local_img_path
                })
    
    return broken_images_by_section

def bulk_download_section(section_name, broken_images, max_downloads=50):
    """Download missing images for a specific section"""
    base_url = f"http://skydogsports.com/{section_name}/"
    
    print(f"\n=== BULK DOWNLOADING: {section_name} ===")
    print(f"Found {len(broken_images)} broken images")
    
    downloads_attempted = 0
    downloads_successful = 0
    
    for item in broken_images[:max_downloads]:
        if downloads_attempted >= max_downloads:
            break
            
        img_src = item['img_src']
        local_path = item['local_path']
        
        print(f"Downloading: {base_url}{img_src}")
        
        if download_image_curl(base_url, img_src, local_path):
            downloads_successful += 1
            print(f"✅ Success: {local_path} ({local_path.stat().st_size} bytes)")
        else:
            print(f"❌ Failed: {img_src}")
        
        downloads_attempted += 1
        
        # Be respectful to server
        time.sleep(0.2)
    
    return downloads_successful

def main():
    """Main bulk recovery process"""
    print("=== BULK IMAGE RECOVERY FROM SKYDOGSPORTS.COM ===")
    
    # Change to skydog directory
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Find all broken images organized by section
    broken_images_by_section = find_all_broken_images()
    
    total_broken = sum(len(images) for images in broken_images_by_section.values())
    print(f"\nTotal broken images found: {total_broken}")
    
    # Priority sections (most likely to have recoverable images)
    priority_sections = [
        'A-HG',
        'A-Windsurfing', 
        'A-kayaks',
        'A-JET-SKI',
        'A-WATER-SKI',
        'RC',
        'A-DOXIE-WEBSITE',
        'A-TRIKE',
        'SKYNET',
        'Inuksuk'
    ]
    
    total_downloaded = 0
    
    # Process priority sections first
    for section in priority_sections:
        if section in broken_images_by_section:
            images = broken_images_by_section[section]
            
            # Download more images for high-priority sections
            max_downloads = 100 if section in ['A-HG', 'A-Windsurfing', 'A-kayaks'] else 50
            
            downloaded = bulk_download_section(section, images, max_downloads)
            total_downloaded += downloaded
            print(f"Downloaded {downloaded} images for {section}")
            
            # Brief pause between sections
            time.sleep(1)
    
    # Process remaining sections
    for section, images in broken_images_by_section.items():
        if section not in priority_sections:
            downloaded = bulk_download_section(section, images, max_downloads=25)
            total_downloaded += downloaded
            print(f"Downloaded {downloaded} images for {section}")
            time.sleep(0.5)
    
    print(f"\n=== BULK RECOVERY COMPLETE ===")
    print(f"Total images downloaded: {total_downloaded}")
    print("Run final_verification.py to see the improvement!")

if __name__ == "__main__":
    main()