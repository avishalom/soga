#!/usr/bin/env python3
import os
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import argparse

class SkydogLinkFixer:
    def __init__(self, skydog_root='.'):
        self.skydog_root = skydog_root
        self.fixes_applied = 0
        self.files_processed = 0
        
    def get_relative_path(self, from_dir, to_path):
        """Calculate correct relative path from current directory to target"""
        # Remove leading slashes and normalize
        to_path = to_path.lstrip('/')
        
        # If we're in root directory, direct path
        if from_dir == '.' or from_dir == '':
            return to_path
            
        # Count directory levels to go up
        levels_up = from_dir.count('/')
        if levels_up > 0:
            return '../' * levels_up + to_path
        else:
            return '../' + to_path
    
    def fix_href_in_file(self, filepath):
        """Process a single HTML file and fix all href attributes"""
        print(f"Processing: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return 0
            
        soup = BeautifulSoup(content, 'html.parser')
        fixes_in_file = 0
        
        # Get current directory relative to skydog root
        current_dir = os.path.dirname(os.path.relpath(filepath, self.skydog_root))
        
        # Process all elements with href attributes
        for element in soup.find_all(['a', 'link'], href=True):
            old_href = element['href']
            new_href = self.fix_single_href(old_href, current_dir)
            
            if new_href != old_href:
                element['href'] = new_href
                print(f"  Fixed: {old_href} -> {new_href}")
                fixes_in_file += 1
        
        # Write back the fixed content
        if fixes_in_file > 0:
            try:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print(f"  Applied {fixes_in_file} fixes to {filepath}")
            except Exception as e:
                print(f"Error writing {filepath}: {e}")
                return 0
        
        return fixes_in_file
    
    def fix_single_href(self, href, current_dir):
        """Fix a single href attribute"""
        # Skip external links (but not skydogsports.com)
        if href.startswith(('http://', 'https://')) and 'skydogsports.com' not in href:
            return href
            
        # Skip anchors, mailto, javascript, etc.
        if href.startswith(('#', 'mailto:', 'javascript:', 'tel:')):
            return href
            
        # Fix absolute skydogsports.com links
        if 'skydogsports.com' in href:
            # Extract path after domain
            path = href.split('skydogsports.com/')[-1] if '/' in href else ''
            return self.get_relative_path(current_dir, path)
        
        # Fix absolute paths that should be relative
        if href.startswith('/'):
            # Remove leading slash and make relative
            path = href.lstrip('/')
            return self.get_relative_path(current_dir, path)
        
        # Check if relative path needs fixing for cross-directory navigation
        if href.startswith('../'):
            # Verify this is correct for current directory depth
            return href
        
        # Direct file references - check if they exist
        if '/' not in href and href.endswith(('.html', '.htm', '.pdf', '.jpg', '.png', '.gif')):
            # This is a direct file reference, should work as-is
            return href
        
        # Directory references without ../ prefix that might need it
        known_dirs = ['A-HG', 'A-TRIKE', 'A-kayaks', 'RC', 'SKYNET', 'A-Windsurfing', 
                     'Inuksuk', 'A-JET-SKI', 'A-PARA', 'A-KITE-SKIERS', 'ROWBUST', 
                     'A-SNOWBOARD', 'bike', 'A-WATER-SKI', 'A-DOXIE-WEBSITE']
        
        for dir_name in known_dirs:
            if href.startswith(dir_name + '/'):
                # Cross-directory reference, needs proper relative path
                return self.get_relative_path(current_dir, href)
        
        return href
    
    def process_all_files(self):
        """Process all HTML files in the skydog directory"""
        for root, dirs, files in os.walk(self.skydog_root):
            for file in files:
                if file.endswith(('.html', '.htm')):
                    filepath = os.path.join(root, file)
                    fixes = self.fix_href_in_file(filepath)
                    self.fixes_applied += fixes
                    self.files_processed += 1
        
        print(f"\n✅ SUMMARY:")
        print(f"   Files processed: {self.files_processed}")
        print(f"   Total fixes applied: {self.fixes_applied}")

def main():
    parser = argparse.ArgumentParser(description='Fix href links in Skydog Sports website')
    parser.add_argument('--directory', '-d', default='.', 
                       help='Skydog directory path (default: current directory)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be changed without making changes')
    
    args = parser.parse_args()
    
    fixer = SkydogLinkFixer(args.directory)
    fixer.process_all_files()

if __name__ == "__main__":
    main()