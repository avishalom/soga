#!/bin/bash
set -e

echo "🏷️ Adding HTML Base Tag to Key Files"
echo "===================================="
echo ""

# Files to add base tag to (main index files)
key_files=(
    "./index.html"
    "./A-HG.html"
    "./A-TRIKE.html"
    "./Inuksuk.html"
    "./bike.html"
    "./A-HG/index.html"
    "./A-UKULELE/index.html"
    "./A-kayaks/index.htm"
    "./A-Windsurfing/index.htm"
    "./A-JET-SKI/index.htm"
    "./A-KITE-SKIERS/index.html"
    "./A-PARA/para.htm"
    "./A-SNOWBOARD/index.html"
    "./A-WATER-SKI/water-ski-video-index.htm"
    "./RC/index.htm"
    "./ROWBUST/index.htm"
    "./SKYNET/doxie-index.htm"
)

base_tag='<base href="https://sogaclub.ca/skydog/">'
files_updated=0

echo "📋 Processing key files for base tag insertion..."

for file in "${key_files[@]}"; do
    if [ -f "$file" ]; then
        # Check if base tag already exists
        if grep -q '<base href=' "$file" 2>/dev/null; then
            echo "  ⏭️ Base tag already exists in: $file"
            continue
        fi
        
        # Check if file has a <head> section
        if grep -q '<head>' "$file" 2>/dev/null; then
            echo "  📝 Adding base tag to: $file"
            
            # Create backup
            cp "$file" "${file}.backup" 2>/dev/null || true
            
            # Add base tag after <head>
            if LC_ALL=C sed -i '' "s|<head>|<head>\\
    $base_tag|" "$file" 2>/dev/null; then
                ((files_updated++))
                echo "    ✅ Added base tag successfully"
            else
                echo "    ⚠️ Failed to add base tag"
                # Restore backup if it failed
                [ -f "${file}.backup" ] && mv "${file}.backup" "$file"
            fi
        else
            echo "  ⏭️ No <head> section found in: $file"
        fi
    else
        echo "  ❌ File not found: $file"
    fi
done

echo ""
echo "✅ Base tag insertion complete!"
echo "   Files updated: $files_updated"
echo "   Base URL: https://sogaclub.ca/skydog/"
echo ""
echo "💡 Benefits of base tag:"
echo "   • All relative URLs automatically resolve to sogaclub.ca/skydog/"
echo "   • Cleaner URL management across the site"
echo "   • Better SEO and link consistency"