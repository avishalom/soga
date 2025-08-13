#!/bin/bash
set -e

echo "🔗 Fixing ALL remaining skydogsports.com absolute URLs..."

# Count files before fixing
before_count=$(find . -name "*.html" -o -name "*.htm" | xargs grep -l "skydogsports.com" 2>/dev/null | wc -l)
echo "📊 Files with skydogsports.com links before: $before_count"

# Fix all files systematically  
fixed_count=0
failed_count=0

for file in $(find . -name "*.html" -o -name "*.htm"); do
  if grep -q "skydogsports.com" "$file" 2>/dev/null; then
    echo "Fixing: $file"
    
    # Try to fix both variants of the URL
    if LC_ALL=C sed -i '' 's|http://www\.skydogsports\.com/||g' "$file" 2>/dev/null && \
       LC_ALL=C sed -i '' 's|http://skydogsports\.com/||g' "$file" 2>/dev/null; then
      ((fixed_count++))
    else
      echo "⚠️ Failed to fix: $file"
      ((failed_count++))
    fi
  fi
done

# Count files after fixing
after_count=$(find . -name "*.html" -o -name "*.htm" | xargs grep -l "skydogsports.com" 2>/dev/null | wc -l || echo "0")

echo ""
echo "✅ RESULTS:"
echo "   Files fixed: $fixed_count"
echo "   Files failed: $failed_count" 
echo "   Files with links remaining: $after_count"

if [ "$after_count" -eq 0 ]; then
  echo "🎉 SUCCESS! All skydogsports.com links converted to relative paths!"
else
  echo "⚠️ Some files still need manual fixing"
fi