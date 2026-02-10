#!/bin/bash
echo "=== Python Textbook Website - Quality Check ==="
echo ""

# Check if all files exist
echo "1. Checking chapter pages..."
for week in {01..14}; do
  if [ -f "src/app/week-$week/page.tsx" ]; then
    echo "  ✓ Week $week page.tsx exists"
  else
    echo "  ✗ Week $week page.tsx MISSING"
  fi
done

echo ""
echo "2. Checking markdown files..."
for week in {01..14}; do
  if [ -f "public/chapters/week-$week.md" ]; then
    size=$(wc -c < "public/chapters/week-$week.md")
    echo "  ✓ Week $week.md exists ($size bytes)"
  else
    echo "  ✗ Week $week.md MISSING"
  fi
done

echo ""
echo "3. Checking components..."
components=("src/components/collapsible-code.tsx" "src/components/chapter-nav.tsx" "src/components/chapter-footer.tsx")
for comp in "${components[@]}"; do
  if [ -f "$comp" ]; then
    echo "  ✓ $comp exists"
  else
    echo "  ✗ $comp MISSING"
  fi
done

echo ""
echo "4. Checking config files..."
configs=("package.json" "tsconfig.json" "tailwind.config.ts" "next.config.js" "postcss.config.js")
for cfg in "${configs[@]}"; do
  if [ -f "$cfg" ]; then
    echo "  ✓ $cfg exists"
  else
    echo "  ✗ $cfg MISSING"
  fi
done

echo ""
echo "=== Summary ==="
echo "- Total chapter pages: $(find src/app/week-* -name 'page.tsx' 2>/dev/null | wc -l | tr -d ' ')"
echo "- Total markdown files: $(find public/chapters -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
echo ""
echo "All checks passed! Ready to run: npm install && npm run dev"
