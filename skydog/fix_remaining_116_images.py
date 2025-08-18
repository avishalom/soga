#!/usr/bin/env python3

import os
import re
import subprocess
import urllib.parse
from pathlib import Path

def try_download_variations(img_url, local_path, img_src):
    """Try multiple URL variations to handle encoding issues"""
    variations = []
    
    # Original URL
    variations.append(img_url)
    
    # Handle %20 spaces - try both encoded and decoded versions
    if '%20' in img_url:
        # Replace %20 with actual spaces
        space_url = img_url.replace('%20', ' ')
        variations.append(space_url)
        
        # Try with different space encodings
        plus_url = img_url.replace('%20', '+')
        variations.append(plus_url)
        
        # Try completely unencoded
        unencoded_url = urllib.parse.unquote(img_url)
        variations.append(unencoded_url)
    
    # Handle special characters
    if any(char in img_src for char in ['[', ']', '%', '&', '#']):
        # Try properly encoded version
        parsed = urllib.parse.urlparse(img_url)
        properly_encoded = f"{parsed.scheme}://{parsed.netloc}{urllib.parse.quote(parsed.path, safe='/~')}"
        variations.append(properly_encoded)
        
        # Try with brackets removed or replaced
        if '[' in img_src or ']' in img_src:
            bracket_fixed = img_url.replace('[', '(').replace(']', ')')
            variations.append(bracket_fixed)
            
            bracket_removed = img_url.replace('[', '').replace(']', '')
            variations.append(bracket_removed)
    
    # Handle snapshot filenames with special patterns
    if 'Snapshot' in img_src and '%' in img_src:
        # Try alternative snapshot naming patterns
        base_url = img_url.rsplit('/', 1)[0]
        filename = img_src.split('/')[-1]
        
        # Common snapshot variations
        alt_names = [
            filename.replace('%20', '-'),
            filename.replace('%20', '_'),
            filename.replace('Snapshot%20', 'Snapshot-'),
            filename.replace('Snapshot%20', 'Snapshot_'),
            re.sub(r'Snapshot%20\d+', 'Snapshot', filename),
        ]
        
        for alt_name in alt_names:
            variations.append(f"{base_url}/{alt_name}")
    
    # Try downloading each variation
    for i, url_variant in enumerate(variations):
        try:
            # Create directory if needed
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            print(f"  Trying variation {i+1}: {url_variant}")
            
            cmd = ['curl', '-k', '-s', '-f', url_variant, '-o', local_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(local_path) and os.path.getsize(local_path) > 0:
                print(f"  ✅ SUCCESS with variation {i+1}")
                return True, f"Success with variation: {url_variant}"
                
        except Exception as e:
            continue
    
    return False, "All variations failed"

def fix_remaining_images():
    """Fix the remaining 116 images using URL encoding fixes"""
    base_dir = "/Users/vishshalit/gith/soga/skydog"
    recovery_file = os.path.join(base_dir, "complete_broken_recovery.txt")
    
    if not os.path.exists(recovery_file):
        print("❌ Recovery file not found.")
        return
    
    print("🔧 FIXING REMAINING 116 IMAGES WITH URL ENCODING AND SPECIAL CHARACTER FIXES")
    print("=" * 80)
    
    # Load all broken images that still need fixing
    remaining_broken = []
    with open(recovery_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or not line:
                continue
            
            parts = line.split('|')
            if len(parts) == 5:
                img_data = {
                    'html_file': parts[0],
                    'img_src': parts[1], 
                    'local_path': parts[2],
                    'source_url': parts[3],
                    'section': parts[4]
                }
                
                # Only process images that still don't exist
                if not os.path.exists(img_data['local_path']):
                    remaining_broken.append(img_data)
    
    print(f"📊 Found {len(remaining_broken)} images still missing")
    
    if len(remaining_broken) == 0:
        print("🎉 All images already recovered!")
        return
    
    # Group by problem type for analysis
    space_issues = [img for img in remaining_broken if '%20' in img['img_src']]
    special_char_issues = [img for img in remaining_broken if any(char in img['img_src'] for char in ['[', ']', '%', '&', '#']) and '%20' not in img['img_src']]
    other_issues = [img for img in remaining_broken if img not in space_issues and img not in special_char_issues]
    
    print(f"🔍 Issue breakdown:")
    print(f"   - Space (%20) issues: {len(space_issues)}")
    print(f"   - Special character issues: {len(special_char_issues)}")
    print(f"   - Other issues: {len(other_issues)}")
    print()
    
    success_count = 0
    failed_images = []
    
    # Process each category
    for category, images in [("SPACE ISSUES", space_issues), ("SPECIAL CHARACTERS", special_char_issues), ("OTHER", other_issues)]:
        if not images:
            continue
            
        print(f"\n=== FIXING {category} ({len(images)} images) ===")
        
        for i, img in enumerate(images, 1):
            print(f"[{i}/{len(images)}] {img['img_src']}")
            
            success, message = try_download_variations(
                img['source_url'], 
                img['local_path'], 
                img['img_src']
            )
            
            if success:
                success_count += 1
            else:
                failed_images.append(img)
                print(f"  ❌ FAILED: {message}")
    
    # Results summary
    print(f"\n🎯 ADVANCED RECOVERY RESULTS")
    print("=" * 50)
    print(f"Images attempted: {len(remaining_broken)}")
    print(f"Successfully fixed: {success_count}")
    print(f"Still failing: {len(failed_images)}")
    
    if success_count > 0:
        improvement = (success_count / len(remaining_broken)) * 100
        print(f"Improvement rate: {improvement:.1f}%")
    
    # Show remaining problematic pages
    if failed_images:
        print(f"\n❌ REMAINING {len(failed_images)} PROBLEMATIC IMAGES:")
        
        # Group by HTML page for easier analysis
        by_page = {}
        for img in failed_images:
            page = img['html_file']
            if page not in by_page:
                by_page[page] = []
            by_page[page].append(img)
        
        for page, page_images in by_page.items():
            print(f"\n📄 {page} ({len(page_images)} broken images):")
            for img in page_images[:5]:  # Show first 5
                print(f"   ❌ {img['img_src']}")
                print(f"      URL: {img['source_url']}")
            if len(page_images) > 5:
                print(f"   ... and {len(page_images) - 5} more")
    
    return success_count, failed_images

if __name__ == "__main__":
    success_count, failed_images = fix_remaining_images()
    
    print(f"\n🏁 FINAL STATUS:")
    if success_count > 0:
        new_total = 14615 + success_count
        new_rate = (new_total / 14731) * 100
        print(f"   New working images: {new_total}/14731")
        print(f"   New success rate: {new_rate:.2f}%")
        print(f"   Remaining missing: {14731 - new_total}")
    
    if failed_images:
        print(f"   🔍 {len(failed_images)} images still need manual investigation")