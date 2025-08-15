#!/bin/bash
set -e

echo "🔗 COMPLETE skydogsports.com Link Fix - Smart Relative URLs"
echo "======================================================="
echo ""

# Function to calculate relative path from current directory to target
get_relative_path() {
    local from_dir="$1"
    local to_path="$2"
    
    # Clean up paths
    from_dir=$(echo "$from_dir" | sed 's|^\./||' | sed 's|/$||')
    to_path=$(echo "$to_path" | sed 's|^/||')
    
    # If we're in the root skydog directory
    if [ "$from_dir" = "." ] || [ -z "$from_dir" ]; then
        echo "$to_path"
        return
    fi
    
    # Count directory levels to go up
    levels=$(echo "$from_dir" | tr '/' '\n' | wc -l)
    
    # Build relative path
    rel_path=""
    for ((i=0; i<levels; i++)); do
        rel_path="../$rel_path"
    done
    
    echo "${rel_path}${to_path}"
}

# Count initial issues
echo "📊 Initial Analysis:"
href_links=$(find . -name "*.html" -o -name "*.htm" | xargs grep -c 'href=.*http.*skydogsports.com' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
src_links=$(find . -name "*.html" -o -name "*.htm" | xargs grep -c 'src=.*http.*skydogsports.com' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
display_text=$(find . -name "*.html" -o -name "*.htm" | xargs grep -c '>skydogsports\.com<' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
total_files=$(find . -name "*.html" -o -name "*.htm" | wc -l | tr -d ' ')

echo "   HTML files to process: $total_files"
echo "   href skydogsports.com links: $href_links"
echo "   src skydogsports.com links: $src_links"
echo "   display text to update: $display_text"
echo "   Total items to fix: $((href_links + src_links + display_text))"
echo ""

# Backup critical files
echo "💾 Creating backup..."
if [ ! -d "../backup-$(date +%Y%m%d)" ]; then
    mkdir -p "../backup-$(date +%Y%m%d)"
    find . -name "*.html" -o -name "*.htm" | head -10 | while read file; do
        cp "$file" "../backup-$(date +%Y%m%d)/" 2>/dev/null || true
    done
    echo "✅ Sample files backed up to ../backup-$(date +%Y%m%d)/"
fi

# Fix all href patterns with smart relative paths
echo "🔧 Phase 1: Fixing href links with proper relative paths..."
fixed_href=0
failed_href=0

for file in $(find . -name "*.html" -o -name "*.htm"); do
    if grep -q 'href=.*http.*skydogsports.com' "$file" 2>/dev/null; then
        echo "  Processing href links in: $file"
        
        # Get current directory relative to skydog root
        current_dir=$(dirname "$file")
        
        # Create temporary file for processing
        temp_file="${file}.tmp"
        
        # Process each skydogsports.com link intelligently
        python3 -c "
import re
import sys
import os

def get_relative_path(from_dir, to_path):
    from_dir = from_dir.lstrip('./').rstrip('/')
    to_path = to_path.lstrip('/')
    
    if not from_dir or from_dir == '.':
        return to_path or 'index.html'
    
    levels = len([x for x in from_dir.split('/') if x])
    rel_path = '../' * levels
    return rel_path + (to_path or 'index.html')

with open('$file', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

current_dir = '$current_dir'

# Fix different href patterns
content = re.sub(r'href=\"http://www\.skydogsports\.com/([^\"]*?)\"', 
                lambda m: f'href=\"{get_relative_path(current_dir, m.group(1))}\"', content)
content = re.sub(r'href=\"http://skydogsports\.com/([^\"]*?)\"', 
                lambda m: f'href=\"{get_relative_path(current_dir, m.group(1))}\"', content)
content = re.sub(r'href=\"http://www\.skydogsports\.com\"', 
                lambda m: f'href=\"{get_relative_path(current_dir, \"\")}\"', content)
content = re.sub(r'href=\"http://skydogsports\.com\"', 
                lambda m: f'href=\"{get_relative_path(current_dir, \"\")}\"', content)
content = re.sub(r'href=\"http://www\.skydogsports\.com/\"', 
                lambda m: f'href=\"{get_relative_path(current_dir, \"\")}\"', content)
content = re.sub(r'href=\"http://skydogsports\.com/\"', 
                lambda m: f'href=\"{get_relative_path(current_dir, \"\")}\"', content)

with open('$temp_file', 'w', encoding='utf-8') as f:
    f.write(content)
" 2>/dev/null
        
        if [ -f "$temp_file" ]; then
            mv "$temp_file" "$file"
            ((fixed_href++))
        else
            ((failed_href++))
            echo "    ⚠️ Failed to fix href in: $file"
        fi
    fi
done

echo "    ✅ href fixes: $fixed_href files, $failed_href failures"

# Fix all src patterns with smart relative paths
echo "🖼️ Phase 2: Fixing img src links with proper relative paths..."
fixed_src=0
failed_src=0

for file in $(find . -name "*.html" -o -name "*.htm"); do
    if grep -q 'src=.*http.*skydogsports.com' "$file" 2>/dev/null; then
        echo "  Processing src links in: $file"
        
        # Get current directory relative to skydog root
        current_dir=$(dirname "$file")
        
        # Create temporary file for processing
        temp_file="${file}.tmp"
        
        # Process each skydogsports.com src link intelligently
        python3 -c "
import re

def get_relative_path(from_dir, to_path):
    from_dir = from_dir.lstrip('./').rstrip('/')
    to_path = to_path.lstrip('/')
    
    if not from_dir or from_dir == '.':
        return to_path
    
    levels = len([x for x in from_dir.split('/') if x])
    rel_path = '../' * levels
    return rel_path + to_path

with open('$file', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

current_dir = '$current_dir'

# Fix different src patterns
content = re.sub(r'src=\"http://www\.skydogsports\.com/([^\"]+)\"', 
                lambda m: f'src=\"{get_relative_path(current_dir, m.group(1))}\"', content)
content = re.sub(r'src=\"http://skydogsports\.com/([^\"]+)\"', 
                lambda m: f'src=\"{get_relative_path(current_dir, m.group(1))}\"', content)

with open('$temp_file', 'w', encoding='utf-8') as f:
    f.write(content)
" 2>/dev/null
        
        if [ -f "$temp_file" ]; then
            mv "$temp_file" "$file"
            ((fixed_src++))
        else
            rm -f "$temp_file"
            ((failed_src++))
            echo "    ⚠️ Failed to fix src in: $file"
        fi
    fi
done

echo "    ✅ src fixes: $fixed_src files, $failed_src failures"

# Fix split/broken URLs (like the A-UKULELE issue)
echo "🔗 Phase 3: Fixing split/broken URLs..."
fixed_split=0

# Specific fix for the broken "Older Zoom Performan" + "ces" pattern
for file in $(find . -name "*.html" -o -name "*.htm"); do
    if grep -q "Older Zoom Performan.*ces" "$file" 2>/dev/null; then
        echo "  Fixing split URL in: $file"
        # Fix the specific broken pattern in A-UKULELE
        LC_ALL=C sed -i '' \
            -e 's|<a target="_blank" href="http://www\.skydogsports\.com/A-UKULELE/Zoom%20Performances\.htm">[^<]*Older Zoom Performan</font></a><font[^>]*><a target="_blank" href="http://www\.skydogsports\.com/A-UKULELE/Zoom%20Performances\.htm"><font[^>]*>ces</font></a>|<a target="_blank" href="Zoom%20Performances.htm">Older Zoom Performances</a>|g' \
            "$file" 2>/dev/null && ((fixed_split++)) || true
    fi
done

if [ $fixed_split -gt 0 ]; then
    echo "    ✅ Fixed split URLs in $fixed_split files"
fi

# Update display text to sogaclub.ca/skydog
echo "🏷️ Phase 4: Updating display text to sogaclub.ca/skydog..."
fixed_display=0

for file in $(find . -name "*.html" -o -name "*.htm"); do
    if grep -q '>skydogsports\.com<' "$file" 2>/dev/null; then
        echo "  Updating display text in: $file"
        if LC_ALL=C sed -i '' \
            -e 's|>www\.skydogsports\.com<|>sogaclub.ca/skydog<|g' \
            -e 's|>skydogsports\.com<|>sogaclub.ca/skydog<|g' \
            "$file" 2>/dev/null; then
            ((fixed_display++))
        fi
    fi
done

echo "    ✅ Updated display text in $fixed_display files"

# Preserve email links (don't change mailto: links)
echo "📧 Phase 5: Preserving email links..."
echo "    ℹ️ Email links (mailto:info@skydogsports.com) preserved"

# Final verification
echo ""
echo "🔍 FINAL VERIFICATION:"
remaining_href=$(find . -name "*.html" -o -name "*.htm" | xargs grep -c 'href=.*http.*skydogsports.com' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
remaining_src=$(find . -name "*.html" -o -name "*.htm" | xargs grep -c 'src=.*http.*skydogsports.com' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')
email_links=$(find . -name "*.html" -o -name "*.htm" | xargs grep -c 'mailto:.*skydogsports.com' 2>/dev/null | awk '{sum+=$1} END {print sum+0}')

echo "   Remaining href HTTP links: $remaining_href"
echo "   Remaining src HTTP links: $remaining_src"  
echo "   Email links (preserved): $email_links"
echo ""

if [ $((remaining_href + remaining_src)) -eq 0 ]; then
    echo "🎉 SUCCESS! All skydogsports.com HTTP/HTTPS links converted to relative paths!"
    echo "✅ Website is ready for deployment at sogaclub.ca/skydog/"
    echo "📧 Email links (mailto:) have been preserved"
else
    echo "⚠️  ATTENTION: $((remaining_href + remaining_src)) HTTP links still need manual review"
    echo ""
    echo "🔍 Files that still need attention:"
    find . -name "*.html" -o -name "*.htm" | xargs grep -l 'http.*skydogsports.com' 2>/dev/null | grep -v mailto || echo "   None found"
fi

echo ""
# Add HTML base tag suggestion
echo ""
echo "💡 OPTIONAL IMPROVEMENT: HTML Base Tag"
echo "   Consider adding <base href=\"https://sogaclub.ca/skydog/\"> to <head> sections"
echo "   This would make all relative URLs resolve correctly automatically"
echo ""

echo "📊 SUMMARY STATS:"
echo "   Files processed: $total_files"
echo "   href fixes applied: $fixed_href"
echo "   src fixes applied: $fixed_src"
echo "   Split URL fixes: $fixed_split"
echo "   Display text updates: $fixed_display"
echo "   Total transformations: $((fixed_href + fixed_src + fixed_split + fixed_display))"