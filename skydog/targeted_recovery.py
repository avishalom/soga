#!/usr/bin/env python3
"""
Targeted recovery of specific high-value broken images
Focus on files with many broken images that are likely recoverable
"""

import os
import re
import subprocess
from pathlib import Path
import time

def download_image_curl(base_url, img_path, local_path):
    """Download a single image using curl"""
    try:
        clean_img_path = img_path.replace('&amp;', '&')
        img_url = f"{base_url.rstrip('/')}/{clean_img_path}"
        
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'curl', '-k', '--connect-timeout', '8', '--max-time', '15',
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

def download_images_for_file(html_file, max_images=20):
    """Download missing images for a specific HTML file"""
    section_name = html_file.parent.name
    base_url = f"http://skydogsports.com/{section_name}/"
    
    try:
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return 0
    
    img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
    matches = re.findall(img_pattern, content, re.IGNORECASE)
    
    html_dir = html_file.parent
    downloaded = 0
    
    for match in matches[:max_images]:
        img_src = match[0]
        
        if img_src.startswith('http'):
            continue
        
        local_path = html_dir / img_src
        if not local_path.exists():
            if download_image_curl(base_url, img_src, local_path):
                downloaded += 1
                print(f"✅ {local_path}")
            time.sleep(0.1)
    
    return downloaded

def main():
    """Target specific high-value files for recovery"""
    print("=== TARGETED IMAGE RECOVERY ===")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    # Target files known to have many missing images
    target_files = [
        # Windsurfing files with many images
        Path('A-Windsurfing/2009.htm'),
        Path('A-Windsurfing/2017-W-Surf.htm'),
        Path('A-Windsurfing/2018-W-Surf.htm'),
        
        # Kayak files
        Path('A-kayaks/Kayak-P4.htm'),
        Path('A-kayaks/KAYAK-Photos-2.htm'),
        
        # High-value HG files
        Path('A-HG/2013-WW-DEMO-DAYS.htm'),
        Path('A-HG/2014-March-WW.htm'), 
        Path('A-HG/2016-TOGA.htm'),
        Path('A-HG/Wallaby-Feb-08.htm'),
        
        # RC files
        Path('RC/rcairplanes.htm'),
        Path('RC/rccombat.htm'),
        
        # Doxie files
        Path('A-DOXIE-WEBSITE/dfest06.htm'),
    ]
    
    total_downloaded = 0
    
    for html_file in target_files:
        if html_file.exists():
            print(f"\nProcessing: {html_file}")
            downloaded = download_images_for_file(html_file, max_images=30)
            total_downloaded += downloaded
            print(f"Downloaded {downloaded} images")
        else:
            print(f"File not found: {html_file}")
    
    print(f"\n=== TARGETED RECOVERY COMPLETE ===")
    print(f"Total images downloaded: {total_downloaded}")

if __name__ == "__main__":
    main()