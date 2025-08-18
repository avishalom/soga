#!/usr/bin/env python3
"""
ROOT CAUSE FIX: Download missing entire image directories
The issue is that many subdirectories with images were never downloaded from the original site
"""

import os
import re
import subprocess
from pathlib import Path
from collections import defaultdict
import time

def download_image_curl(img_url, local_path):
    """Download a single image using curl"""
    try:
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'curl', '-k', '--connect-timeout', '8', '--max-time', '20',
            '--retry', '1', '--user-agent', 'Mozilla/5.0',
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

def find_missing_directories():
    """Find all missing image directories that need to be downloaded"""
    print("=== ANALYZING MISSING DIRECTORIES ===")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    missing_dirs = defaultdict(list)
    
    # Analyze all HTML files for broken image patterns
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
            
            # Skip external URLs and relative parent paths
            if img_src.startswith('http') or img_src.startswith('../'):
                continue
            
            # Check if file exists locally
            local_img_path = html_dir / img_src
            if not local_img_path.exists():
                # Extract the directory part
                if '/' in img_src:
                    img_dir = img_src.split('/')[0]
                    dir_key = f"{section_name}/{img_dir}"
                    if dir_key not in missing_dirs:
                        missing_dirs[dir_key] = []
                    missing_dirs[dir_key].append(img_src)
    
    return missing_dirs

def download_missing_directory(section, img_dir, missing_images, max_downloads=50):
    """Download all missing images from a specific directory"""
    
    base_url = f"http://skydogsports.com/{section}/"
    
    print(f"\n=== DOWNLOADING DIRECTORY: {section}/{img_dir} ===")
    print(f"Missing images: {len(missing_images)}")
    
    downloaded = 0
    
    # Get unique image paths (remove duplicates)
    unique_images = list(set(missing_images))
    
    for img_src in unique_images[:max_downloads]:
        img_url = f"{base_url}{img_src}"
        local_path = Path(section) / img_src
        
        if download_image_curl(img_url, local_path):
            downloaded += 1
            print(f"✅ {local_path}")
        else:
            print(f"❌ FAILED: {img_src}")
        
        time.sleep(0.1)
    
    return downloaded

def main():
    """Fix the root cause by downloading missing directory structures"""
    print("=== ROOT CAUSE FIX: MISSING DIRECTORIES ===")
    
    # Find all missing directories
    missing_dirs = find_missing_directories()
    
    print(f"\nFound {len(missing_dirs)} missing directory structures:")
    for dir_key, images in missing_dirs.items():
        print(f"  {dir_key}: {len(images)} missing images")
    
    total_downloaded = 0
    
    # Download missing directories in priority order
    priority_sections = ['A-HG', 'A-Windsurfing', 'A-kayaks', 'A-JET-SKI', 'RC']
    
    for section in priority_sections:
        section_dirs = {k: v for k, v in missing_dirs.items() if k.startswith(section)}
        
        if section_dirs:
            print(f"\n=== PROCESSING SECTION: {section} ===")
            
            for dir_key, missing_images in section_dirs.items():
                section_name, img_dir = dir_key.split('/', 1)
                downloaded = download_missing_directory(section_name, img_dir, missing_images)
                total_downloaded += downloaded
                print(f"Downloaded {downloaded} images from {dir_key}")
                time.sleep(0.5)
    
    print(f"\n=== ROOT CAUSE FIX COMPLETE ===")
    print(f"Total images downloaded: {total_downloaded}")

if __name__ == "__main__":
    main()