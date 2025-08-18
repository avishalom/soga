#!/usr/bin/env python3
"""
Systematic recovery using broken.temp.txt mapping
Process broken links in organized batches from the source site
"""

import os
import subprocess
import time
from pathlib import Path
import urllib.parse

def download_image_curl(img_url, local_path):
    """Download a single image using curl with better error handling"""
    try:
        # URL encode the path properly
        parsed_url = urllib.parse.urlparse(img_url)
        encoded_path = urllib.parse.quote(parsed_url.path.encode('utf-8'), safe='/~')
        final_url = f"{parsed_url.scheme}://{parsed_url.netloc}{encoded_path}"
        
        local_path.parent.mkdir(parents=True, exist_ok=True)
        
        cmd = [
            'curl', '-k', '--connect-timeout', '10', '--max-time', '30',
            '--retry', '2', '--user-agent', 'Mozilla/5.0',
            '-o', str(local_path), final_url
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and local_path.exists() and local_path.stat().st_size > 100:
            return True
        else:
            if local_path.exists():
                local_path.unlink()
            return False
            
    except Exception as e:
        print(f"Exception downloading {img_url}: {e}")
        return False

def load_broken_links():
    """Load broken links from broken.temp.txt"""
    broken_links = []
    
    with open('broken.temp.txt', 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('##') or line.startswith('###'):
                continue
            
            parts = line.split('|')
            if len(parts) == 5:
                broken_links.append({
                    'html_file': parts[0],
                    'img_src': parts[1],
                    'local_path': parts[2],
                    'source_url': parts[3],
                    'section': parts[4]
                })
    
    return broken_links

def systematic_recovery(max_downloads_per_batch=200):
    """Systematically recover broken images using the mapping"""
    print("=== SYSTEMATIC RECOVERY FROM BROKEN.TEMP.TXT ===\n")
    
    os.chdir('/Users/vishshalit/gith/soga/skydog')
    
    broken_links = load_broken_links()
    print(f"Loaded {len(broken_links)} broken image links")
    
    # Group by section for systematic processing
    by_section = {}
    for link in broken_links:
        section = link['section']
        if section not in by_section:
            by_section[section] = []
        by_section[section].append(link)
    
    print(f"Processing by section:")
    for section, links in by_section.items():
        print(f"  {section}: {len(links)} broken images")
    
    total_recovered = 0
    total_attempted = 0
    
    # Process each section systematically
    for section, links in by_section.items():
        print(f"\n=== PROCESSING SECTION: {section} ===")
        print(f"Broken images in this section: {len(links)}")
        
        section_recovered = 0
        section_attempted = 0
        
        # Limit downloads per section to avoid overwhelming
        batch_size = min(max_downloads_per_batch, len(links))
        
        for i, link in enumerate(links[:batch_size]):
            if total_attempted >= max_downloads_per_batch * 4:  # Overall limit
                print(f"Reached overall download limit, stopping")
                break
                
            total_attempted += 1
            section_attempted += 1
            
            local_path = Path(link['local_path'])
            source_url = link['source_url']
            
            # Skip if file already exists (may have been recovered)
            if local_path.exists():
                continue
            
            print(f"[{section_attempted}/{batch_size}] Downloading: {link['img_src']}")
            
            if download_image_curl(source_url, local_path):
                total_recovered += 1
                section_recovered += 1
                print(f"✅ SUCCESS: {local_path}")
            else:
                print(f"❌ FAILED: {source_url}")
            
            # Rate limiting
            if i % 10 == 0 and i > 0:
                print(f"  Progress: {i}/{batch_size} attempted")
                time.sleep(1)
            else:
                time.sleep(0.2)
        
        print(f"Section {section} results: {section_recovered}/{section_attempted} successful")
    
    return total_recovered, total_attempted

def verify_improvement():
    """Check improvement after systematic recovery"""
    print(f"\n=== VERIFYING IMPROVEMENT ===")
    
    # Re-run comprehensive analysis
    os.system("python3 comprehensive_broken_analysis.py")

def main():
    """Main systematic recovery process"""
    print("SYSTEMATIC RECOVERY BASED ON BROKEN.TEMP.TXT MAPPING")
    
    if not Path('broken.temp.txt').exists():
        print("ERROR: broken.temp.txt not found. Run map_broken_links.py first.")
        return
    
    recovered, attempted = systematic_recovery()
    
    print(f"\n=== SYSTEMATIC RECOVERY COMPLETE ===")
    print(f"Images attempted: {attempted}")
    print(f"Images recovered: {recovered}")
    if attempted > 0:
        print(f"Recovery rate: {(recovered/attempted)*100:.1f}%")
    
    # Verify improvement
    verify_improvement()

if __name__ == "__main__":
    main()