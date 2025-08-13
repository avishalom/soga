#!/bin/bash

# Shell script to create clean PR - removing skydog and keeping root changes
# Run this from the soga repository root directory

set -e  # Exit on any error

echo "🧹 Creating clean PR - removing skydog directory and keeping root changes..."

# 1. Switch to master and create clean branch
echo "📋 Step 1: Creating clean branch from master..."
git checkout master
git pull origin master
git checkout -b clean-root-only-changes

# 2. Remove skydog directory and related files completely
echo "🗑️ Step 2: Removing skydog directory..."
if [ -d "skydog" ]; then
    rm -rf skydog/
    echo "✅ Removed skydog directory"
else
    echo "ℹ️ No skydog directory found"
fi

# Remove any PDF generation artifacts
if [ -f "SOGA-Waiver-Form-2025.pdf" ]; then rm -f "SOGA-Waiver-Form-2025.pdf"; fi
if [ -f "SOGA-Waiver-Form-2025.html" ]; then rm -f "SOGA-Waiver-Form-2025.html"; fi  
if [ -f "update_pdf_to_2025.py" ]; then rm -f "update_pdf_to_2025.py"; fi
if [ -d "pdf_env" ]; then rm -rf "pdf_env/"; fi

echo "✅ Cleanup complete"

# 3. Apply 2023→2025 updates to root files
echo "📅 Step 3: Updating 2023 references to 2025..."
sed -i '' 's/2023/2025/g' membership.htm membership2.htm membership3.html joining.htm
echo "✅ Updated year references"

# 4. Rename PDF file
echo "📄 Step 4: Updating PDF filename..."
if [ -f "SOGA-Waiver-Form-2023.pdf" ]; then
    mv "SOGA-Waiver-Form-2023.pdf" "SOGA-Waiver-Form-2025.pdf"
    echo "✅ Renamed PDF file to 2025"
else
    echo "ℹ️ No 2023 PDF file found"
fi

# 5. Add visitor membership section to membership.htm
echo "👥 Step 5: Adding visitor membership section..."
cat > temp_visitor_section.txt << 'EOF'
            <p>
                <strong>Glider Storage: </strong>Membership includes storage for one glider. If you have a second glider, 
                there is an additional fee of $75.
            </p>
            
            <div class="notification is-warning mt-5 mb-5" style="background-color: #ffeb3b; border-left: 5px solid #ff9800;">
                <h3><span class="tag is-danger is-medium mr-2">NEW</span>Visitor Membership</h3>
                <p>
                    <strong>For Remote Visitors and Out-of-Province Pilots</strong>
                </p>
                <p>
                    We now offer flexible membership options for pilots coming from out of province or traveling more than 3 hours drive within Ontario:
                </p>
                
                <h4><strong>Associate Membership</strong></h4>
                <ul class="custom-list">
                    <li><strong>Cost:</strong> $50 CAD for the year</li>
                    <li><strong>Who:</strong> Remote visitors coming from out of province or more than 3 hours drive in Ontario</li>
                    <li><strong>2025 Special Offer:</strong> Your $50 associate membership fee counts as your first day membership fee for the rest of 2025!</li>
                </ul>
                
                <h4><strong>Day Membership</strong></h4>
                <ul class="custom-list">
                    <li><strong>Cost:</strong> $50 CAD per day</li>
                    <li><strong>Who:</strong> Out-of-province pilots who prefer daily rates instead of full membership</li>
                    <li><strong>Perfect for:</strong> Occasional visits or trying out SOGA before committing to full membership</li>
                    <li><strong>2025 Weekend Special:</strong> Due to the success of having many remote pilots visit during the August long weekend, for the rest of 2025, one day rate will cover up to 3 consecutive weekend days!</li>
                </ul>
                
                <p class="has-text-weight-semibold">
                    Both options still require current HPAC membership, signed waiver, and meeting our pilot requirements.
                </p>
            </div>
            
            <h3>Club Organization</h3>
EOF

# Replace the section in membership.htm
if grep -q "Glider Storage" membership.htm; then
    # Create temp file with replacement
    sed '/Glider Storage.*there is an additional fee of \$75\./r temp_visitor_section.txt' membership.htm | \
    sed '/Glider Storage.*there is an additional fee of \$75\./,/^[[:space:]]*<h3>Club Organization<\/h3>/d' > temp_membership.htm
    mv temp_membership.htm membership.htm
    echo "✅ Added visitor membership section"
else
    echo "⚠️ Could not find Glider Storage section in membership.htm"
fi

rm -f temp_visitor_section.txt

# 6. Stage, commit and push
echo "📤 Step 6: Creating commit and PR..."
git add -A
git status

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "ℹ️ No changes to commit"
else
    git commit -m "Clean up: Remove skydog directory and add 2025 membership updates

- Removed entire skydog directory (messy wget artifacts)  
- Updated all 2023 references to 2025 in membership files
- Renamed PDF: SOGA-Waiver-Form-2023.pdf → SOGA-Waiver-Form-2025.pdf
- Added NEW Visitor Membership section with:
  - Associate Membership: \$50 CAD/year for remote visitors
  - Day Membership: \$50 CAD/day for out-of-province pilots  
  - 2025 Weekend Special: One day rate covers 3 consecutive weekend days
  - 2025 Special Offer: Associate fee counts as first day membership
- Clean slate for proper skydogsports.com transition implementation

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

    echo "✅ Committed changes"
    
    # Push branch
    git push -u origin clean-root-only-changes
    echo "✅ Pushed branch"
    
    # Create PR
    if command -v gh &> /dev/null; then
        gh pr create --title "Clean up: Remove skydog directory and keep 2025 membership updates" --body "## Summary

Remove the messy skydog directory implementation and keep only valuable root changes.

### 🧹 **Cleanup Actions**
- **Removed skydog directory** - contained wget artifacts and improper structure  
- **Removed generated files** - PDF scripts and temporary files
- **Clean slate** for proper transition implementation

### 📅 **2025 Membership Updates**  
- **Updated all 2023→2025** in membership files (membership.htm, membership2.htm, etc.)
- **Renamed PDF**: SOGA-Waiver-Form-2023.pdf → SOGA-Waiver-Form-2025.pdf
- **NEW Visitor Membership** section with highlighted styling

### ✨ **Visitor Membership Features**
- **Associate Membership**: \$50 CAD/year for remote visitors (out-of-province or 3+ hours drive)
- **Day Membership**: \$50 CAD/day for out-of-province pilots  
- **2025 Special Offers**:
  - Associate membership fee counts as first day membership fee
  - Weekend Special: One day rate covers up to 3 consecutive weekend days
- **Success story**: References August long weekend with remote pilots

### 🎯 **Next Steps**
This creates a clean foundation for proper skydogsports.com transition:
1. Proper website crawling with artifact cleanup
2. Directory structure maintenance  
3. Python script for href link analysis
4. YouTube link corrections

**Ready for review and merge!**"
        echo "✅ Created PR"
        echo ""
        echo "🎉 SUCCESS! Clean PR created successfully."
        echo "📋 The PR removes skydog directory and keeps valuable root changes."
    else
        echo "⚠️ GitHub CLI not found. Please create PR manually."
        echo "   Branch: clean-root-only-changes"
    fi
fi

echo ""
echo "✅ Script completed successfully!"
echo "📁 Current branch: $(git branch --show-current)"
echo "🔗 Ready for proper skydogsports.com transition implementation"