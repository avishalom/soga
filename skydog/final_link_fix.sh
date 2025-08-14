#!/bin/bash
set -e

echo "🔗 FINAL comprehensive skydogsports.com link fix"
echo ""

# Process ALL files with skydogsports.com links
files_to_fix=($(find . -name "*.html" -o -name "*.htm" -exec grep -l 'http.*skydogsports.com' {} \; 2>/dev/null))

echo "📊 Found ${#files_to_fix[@]} files to fix"
echo ""

fixed=0
failed=0

for file in "${files_to_fix[@]}"; do
    echo "Fixing: $file"
    
    # Fix the different patterns
    if LC_ALL=C sed -i '' \
        -e 's|href="http://www\.skydogsports\.com/">|href="index.html">|g' \
        -e 's|href="http://www\.skydogsports\.com/index\.html">|href="index.html">|g' \
        -e 's|href="http://www\.skydogsports\.com">|href="index.html">|g' \
        -e 's|href="http://skydogsports\.com/">|href="index.html">|g' \
        -e 's|href="http://skydogsports\.com/index\.html">|href="index.html">|g' \
        -e 's|href="http://skydogsports\.com">|href="index.html">|g' \
        "$file" 2>/dev/null; then
        ((fixed++))
    else
        echo "⚠️  Failed: $file"
        ((failed++))
    fi
done

echo ""
echo "✅ RESULTS:"
echo "   Files fixed: $fixed"
echo "   Files failed: $failed"

# Final verification
remaining=$(find . -name "*.html" -o -name "*.htm" -exec grep -l 'href=.*http.*skydogsports.com' {} \; 2>/dev/null | grep -v mailto | wc -l || echo "0")
echo "   Files with HTTP skydogsports links remaining: $remaining"

if [ "$remaining" -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! All skydogsports.com navigation links are now relative!"
    echo "✅ Website ready for sogaclub.ca/skydog/ deployment"
else
    echo ""
    echo "⚠️  Some files may need manual attention"
fi