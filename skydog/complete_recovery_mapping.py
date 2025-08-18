#!/usr/bin/env python3

import os
import re
from collections import defaultdict

def map_all_remaining_broken_images():
    """
    Comprehensively map ALL remaining broken images by directory/section.
    This will create a complete recovery plan for every single broken image.
    """
    base_dir = "/Users/vishshalit/gith/soga/skydog"
    all_broken_images = []
    section_breakdown = defaultdict(lambda: defaultdict(list))
    
    print("=== COMPREHENSIVE MAPPING OF ALL REMAINING BROKEN IMAGES ===\n")
    
    # Find all HTML files
    html_files = []
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith('.htm') or file.endswith('.html'):
                if 'skydog' in root:  # Only process skydog subdirectory
                    html_files.append(os.path.join(root, file))
    
    print(f"Analyzing {len(html_files)} HTML files...\n")
    
    # Process each HTML file
    for html_file in html_files:
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract section name
            rel_path = os.path.relpath(html_file, base_dir)
            if '/' in rel_path:
                section = rel_path.split('/')[0]
            else:
                section = "ROOT"
            
            # Find all image src attributes
            img_pattern = r'src="([^"]*\.(jpg|jpeg|png|gif|bmp))"'
            matches = re.findall(img_pattern, content, re.IGNORECASE)
            
            for match in matches:
                img_src = match[0]
                
                # Skip absolute URLs and data URIs
                if img_src.startswith(('http:', 'https:', 'data:', '//', 'mailto:')):
                    continue
                
                # Construct the full local path
                html_dir = os.path.dirname(html_file)
                if img_src.startswith('/'):
                    # Absolute path from base
                    local_path = os.path.join(base_dir, img_src.lstrip('/'))
                else:
                    # Relative path from HTML file
                    local_path = os.path.normpath(os.path.join(html_dir, img_src))
                
                # Check if image exists locally
                if not os.path.exists(local_path):
                    # This is a broken image - add to our comprehensive list
                    html_filename = os.path.basename(html_file)
                    source_url = f"http://skydogsports.com/{section}/{img_src}"
                    
                    broken_entry = {
                        'html_file': html_filename,
                        'img_src': img_src,
                        'local_path': local_path,
                        'source_url': source_url,
                        'section': section
                    }
                    
                    all_broken_images.append(broken_entry)
                    
                    # Group by directory within section
                    if '/' in img_src:
                        img_dir = img_src.split('/')[0]
                    else:
                        img_dir = "ROOT_IMAGES"
                    
                    section_breakdown[section][img_dir].append(broken_entry)
        
        except Exception as e:
            print(f"Error processing {html_file}: {e}")
            continue
    
    # Generate comprehensive report
    print(f"**TOTAL BROKEN IMAGES FOUND: {len(all_broken_images)}**\n")
    
    total_directories = 0
    
    for section, directories in section_breakdown.items():
        section_total = sum(len(images) for images in directories.values())
        print(f"📁 **{section}** - {len(directories)} directories, {section_total} broken images")
        
        for directory, images in directories.items():
            print(f"   📂 {directory}/ - {len(images)} broken images")
            total_directories += 1
            
            # Show first few examples
            for i, img in enumerate(images[:3]):
                print(f"      ❌ {img['img_src']}")
            if len(images) > 3:
                print(f"      ... and {len(images) - 3} more")
        print()
    
    print(f"**RECOVERY PLAN SUMMARY:**")
    print(f"- Total Sections: {len(section_breakdown)}")
    print(f"- Total Directories: {total_directories}")
    print(f"- Total Broken Images: {len(all_broken_images)}")
    
    # Write comprehensive recovery file
    recovery_file = os.path.join(base_dir, "complete_broken_recovery.txt")
    with open(recovery_file, 'w') as f:
        f.write("# COMPREHENSIVE BROKEN IMAGE RECOVERY LIST\n")
        f.write(f"# Total broken images: {len(all_broken_images)}\n")
        f.write("# Format: HTML_FILE|IMG_SRC|LOCAL_PATH|SOURCE_URL|SECTION\n\n")
        
        for img in all_broken_images:
            f.write(f"{img['html_file']}|{img['img_src']}|{img['local_path']}|{img['source_url']}|{img['section']}\n")
    
    print(f"\n✅ Complete recovery mapping written to: {recovery_file}")
    
    # Create directory-specific recovery batches
    batch_dir = os.path.join(base_dir, "recovery_batches")
    os.makedirs(batch_dir, exist_ok=True)
    
    batch_count = 0
    for section, directories in section_breakdown.items():
        for directory, images in directories.items():
            batch_count += 1
            batch_file = os.path.join(batch_dir, f"batch_{batch_count:03d}_{section}_{directory.replace('/', '_')}.txt")
            
            with open(batch_file, 'w') as f:
                f.write(f"# BATCH {batch_count}: {section}/{directory}\n")
                f.write(f"# Images to recover: {len(images)}\n")
                f.write("# Format: HTML_FILE|IMG_SRC|LOCAL_PATH|SOURCE_URL|SECTION\n\n")
                
                for img in images:
                    f.write(f"{img['html_file']}|{img['img_src']}|{img['local_path']}|{img['source_url']}|{img['section']}\n")
    
    print(f"✅ Created {batch_count} recovery batches in: {batch_dir}")
    
    return all_broken_images, section_breakdown

if __name__ == "__main__":
    map_all_remaining_broken_images()