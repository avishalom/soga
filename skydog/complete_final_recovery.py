#!/usr/bin/env python3

import os
import time
import subprocess
import urllib.parse
from pathlib import Path

def download_image_curl(img_url, local_path):
    """Download image using curl with proper URL encoding"""
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Handle URL encoding properly
        parsed_url = urllib.parse.urlparse(img_url)
        # Encode the path component properly, preserving / and handling special characters
        encoded_path = urllib.parse.quote(parsed_url.path.encode('utf-8'), safe='/~')
        final_url = f"{parsed_url.scheme}://{parsed_url.netloc}{encoded_path}"
        
        # Download with curl
        cmd = ['curl', '-k', '-s', '-f', final_url, '-o', local_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(local_path) and os.path.getsize(local_path) > 0:
            return True, "Success"
        else:
            return False, f"Curl error: {result.stderr}"
            
    except Exception as e:
        return False, f"Exception: {str(e)}"

def process_complete_recovery():
    """
    Process ALL 2,134 remaining broken images systematically.
    This will not stop until every single image is recovered or confirmed unavailable.
    """
    base_dir = "/Users/vishshalit/gith/soga/skydog"
    recovery_file = os.path.join(base_dir, "complete_broken_recovery.txt")
    
    if not os.path.exists(recovery_file):
        print("❌ Recovery file not found. Run complete_recovery_mapping.py first.")
        return
    
    print("🚀 STARTING COMPLETE RECOVERY OF ALL 2,134 BROKEN IMAGES")
    print("=" * 70)
    
    # Load all broken images
    all_broken_images = []
    with open(recovery_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            
            parts = line.split('|')
            if len(parts) == 5:
                all_broken_images.append({
                    'html_file': parts[0],
                    'img_src': parts[1],
                    'local_path': parts[2],
                    'source_url': parts[3],
                    'section': parts[4]
                })
    
    total_images = len(all_broken_images)
    print(f"📊 Total broken images to recover: {total_images}")
    
    # Group by section for progress tracking
    sections = {}
    for img in all_broken_images:
        section = img['section']
        if section not in sections:
            sections[section] = []
        sections[section].append(img)
    
    print(f"📁 Sections to process:")
    for section, images in sections.items():
        print(f"   - {section}: {len(images)} images")
    print()
    
    # Process each section systematically
    total_success = 0
    total_failed = 0
    
    for section_name, section_images in sections.items():
        print(f"\n=== PROCESSING SECTION: {section_name} ===")
        print(f"Images in this section: {len(section_images)}")
        
        section_success = 0
        section_failed = 0
        
        for i, img in enumerate(section_images, 1):
            print(f"[{i}/{len(section_images)}] Downloading: {img['img_src']}")
            
            # Check if already exists
            if os.path.exists(img['local_path']):
                print(f"✅ ALREADY EXISTS: {img['local_path']}")
                section_success += 1
                continue
            
            # Download the image
            success, message = download_image_curl(img['source_url'], img['local_path'])
            
            if success:
                print(f"✅ SUCCESS: {img['local_path']}")
                section_success += 1
                total_success += 1
            else:
                print(f"❌ FAILED: {img['img_src']} - {message}")
                section_failed += 1
                total_failed += 1
            
            # Progress update every 10 images
            if i % 10 == 0:
                success_rate = (section_success / i) * 100
                print(f"  Progress: {i}/{len(section_images)} attempted, {section_success} successful ({success_rate:.1f}%)")
            
            # Rate limiting - be respectful to the server
            time.sleep(0.1)
        
        # Section summary
        section_rate = (section_success / len(section_images)) * 100
        print(f"\nSection {section_name} results: {section_success}/{len(section_images)} successful ({section_rate:.1f}%)")
        print("-" * 50)
    
    # Final comprehensive summary
    print(f"\n🎯 COMPLETE RECOVERY SUMMARY")
    print("=" * 50)
    print(f"Total images processed: {total_success + total_failed}")
    print(f"Successfully recovered: {total_success}")
    print(f"Failed to recover: {total_failed}")
    overall_rate = (total_success / (total_success + total_failed)) * 100 if (total_success + total_failed) > 0 else 0
    print(f"Overall success rate: {overall_rate:.2f}%")
    
    # Verify final site-wide success rate
    print(f"\n🔍 VERIFYING FINAL SITE-WIDE SUCCESS RATE...")
    os.system("python3 comprehensive_broken_analysis.py")
    
    return total_success, total_failed

if __name__ == "__main__":
    success, failed = process_complete_recovery()
    
    if failed > 0:
        print(f"\n⚠️  {failed} images still failed - investigating...")
    else:
        print(f"\n🎉 MISSION ACCOMPLISHED! All images recovered successfully!")