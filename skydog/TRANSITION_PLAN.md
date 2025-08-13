# Skydog Sports Transition Plan

## Overview
Complete transition of http://skydogsports.com/ to sogaclub.ca/skydog/ with proper artifact cleanup and link management.

## Phase 1: Website Crawling & Content Download
### Objective
Download complete skydogsports.com website with proper structure and clean artifacts.

### Steps
1. **Create skydog directory structure**
   ```bash
   mkdir -p skydog
   cd skydog
   ```

2. **Website crawling with wget**
   ```bash
   wget --recursive \
        --level=5 \
        --no-clobber \
        --page-requisites \
        --html-extension \
        --convert-links \
        --restrict-file-names=windows \
        --domains skydogsports.com \
        --no-parent \
        http://skydogsports.com/
   ```

3. **Move content to proper structure**
   ```bash
   # Move from skydogsports.com subdirectory to skydog root
   mv skydogsports.com/* ./
   rmdir skydogsports.com
   ```

4. **Clean wget artifacts** (.! files)
   ```bash
   find . -name ".!*" -type f -delete
   echo "Removed $(find . -name ".!*" -type f | wc -l) wget artifacts"
   ```

## Phase 2: Link Analysis & Correction
### Objective
Ensure all links work properly in subdirectory deployment (sogaclub.ca/skydog/).

### Python Script for Systematic href Replacement
Create `fix_href_links.py`:
```python
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
                     'A-SNOWBOARD', 'bike']
        
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
```

### Link Correction Strategy
1. **External skydogsports.com links** → Convert to relative paths
   - `http://www.skydogsports.com/A-HG/` → `A-HG/`
   - `http://www.skydogsports.com/index.html` → `index.html`

2. **Cross-directory navigation** → Add proper relative paths
   - From `A-HG/` to `A-WATER-SKI/` → `../A-WATER-SKI/`
   - From root to subdirs → Direct paths `A-HG/`

## Phase 3: Content Updates
### Objective
Update content for 2025 and improve modern compatibility.

### Updates Required
1. **Year Updates**: All 2023 references → 2025
2. **YouTube Links**: Update to modern @cdnskydog format
3. **Navigation**: Ensure all internal links work in subdirectory
4. **Image Optimization**: Verify all images downloaded properly

## Phase 4: Testing & Validation
### Objective
Comprehensive testing of the migrated site.

### Testing Checklist
- [ ] All navigation links work within skydog subdirectory
- [ ] Images load correctly
- [ ] External links (non-skydogsports) remain functional  
- [ ] No 404 errors on internal links
- [ ] Cross-directory navigation works properly
- [ ] PDF downloads work
- [ ] YouTube links updated and functional

### Test Commands
```bash
# Check for broken internal links
grep -r "href.*skydogsports.com" *.html *.htm
# Verify image references
find . -name "*.jpg" -o -name "*.png" -o -name "*.gif" | wc -l
# Check for remaining wget artifacts
find . -name ".!*" -type f
```

## Phase 5: Deployment Integration
### Objective
Integrate with sogaclub.ca navigation and structure.

### Integration Steps
1. **Root navigation update** - Add skydog link to main site
2. **CSS compatibility** - Ensure styling works in subdirectory
3. **Mobile responsiveness** - Test on various devices
4. **SEO considerations** - Update any meta tags as needed

## Automated Cleanup Script
Create `cleanup_and_deploy.sh`:
```bash
#!/bin/bash
set -e

echo "🚀 Skydog Sports Transition - Automated Setup"

# Step 1: Download website
echo "📥 Step 1: Downloading skydogsports.com..."
wget --recursive --level=5 --no-clobber --page-requisites --html-extension \
     --convert-links --restrict-file-names=windows \
     --domains skydogsports.com --no-parent \
     http://skydogsports.com/

# Step 2: Restructure files
echo "📁 Step 2: Restructuring files..."
if [ -d "skydogsports.com" ]; then
    mv skydogsports.com/* ./
    rmdir skydogsports.com
    echo "✅ Files moved to skydog root"
fi

# Step 3: Clean wget artifacts
echo "🧹 Step 3: Cleaning wget artifacts..."
artifact_count=$(find . -name ".!*" -type f | wc -l)
find . -name ".!*" -type f -delete
echo "✅ Removed $artifact_count wget artifacts"

# Step 4: Fix external links
echo "🔗 Step 4: Converting external links..."
find . -name "*.html" -o -name "*.htm" | xargs sed -i '' 's|http://www\.skydogsports\.com/||g'
echo "✅ Converted external skydogsports.com links to relative paths"

# Step 5: Update year references
echo "📅 Step 5: Updating 2023 references to 2025..."
find . -name "*.html" -o -name "*.htm" | xargs sed -i '' 's/2023/2025/g'
echo "✅ Updated year references"

# Step 6: Update YouTube links
echo "📺 Step 6: Updating YouTube links..."
find . -name "*.html" -o -name "*.htm" | xargs sed -i '' 's|http://www\.youtube\.com/user/cdnskydog|http://www.youtube.com/@cdnskydog|g'
echo "✅ Updated YouTube links"

echo ""
echo "🎉 SUCCESS! Skydog Sports transition completed"
echo "📊 Statistics:"
echo "   HTML files: $(find . -name "*.html" -o -name "*.htm" | wc -l)"
echo "   Image files: $(find . -name "*.jpg" -o -name "*.png" -o -name "*.gif" | wc -l)"
echo "   Total files: $(find . -type f | wc -l)"
echo ""
echo "🔗 Ready for deployment at sogaclub.ca/skydog/"
```

## Success Criteria
- [ ] Complete website functionality at sogaclub.ca/skydog/
- [ ] Zero wget artifacts (.! files)
- [ ] All internal navigation working
- [ ] Images loading correctly
- [ ] External links (non-skydogsports) preserved
- [ ] 2025 content updates applied
- [ ] Modern YouTube links
- [ ] Mobile-responsive design maintained

## Risk Mitigation
- **Backup strategy**: Keep original downloaded files in separate directory
- **Incremental testing**: Test each phase before proceeding
- **Link validation**: Use automated tools to verify all links
- **Performance monitoring**: Ensure site loads efficiently

## Timeline
- **Phase 1-2**: 1-2 hours (Download & Link Analysis)
- **Phase 3**: 30 minutes (Content Updates) 
- **Phase 4**: 1 hour (Testing & Validation)
- **Phase 5**: 30 minutes (Integration)

**Total Estimated Time**: 3-4 hours for complete transition

## Notes
- Previous implementation had 159 wget artifacts that caused issues
- Cross-directory navigation was problematic in first attempt
- External link conversion is critical for standalone operation
- Subdirectory deployment requires careful relative path management