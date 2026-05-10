#!/usr/bin/env bash
set -u

echo "=== Python Textbook Website - Quality Check ==="
echo ""
missing=0

check_file() {
  local path="$1"
  if [ -f "$path" ]; then
    echo "  ✓ $path exists"
  else
    echo "  ✗ $path MISSING"
    missing=1
  fi
}

echo "1. Checking chapter pages..."
for week in {01..14}; do
  check_file "src/app/week-$week/page.tsx"
done

echo ""
echo "2. Checking markdown files..."
for week in {01..14}; do
  file="public/chapters/week-$week.md"
  if [ -f "$file" ]; then
    size=$(wc -c < "$file")
    echo "  ✓ Week $week.md exists ($size bytes)"
  else
    echo "  ✗ Week $week.md MISSING"
    missing=1
  fi
done

echo ""
echo "3. Checking components..."
for comp in src/components/collapsible-code.tsx src/components/chapter-nav.tsx src/components/chapter-footer.tsx; do
  check_file "$comp"
done

echo ""
echo "4. Checking config files..."
for cfg in package.json package-lock.json tsconfig.json tailwind.config.ts next.config.js postcss.config.js; do
  check_file "$cfg"
done

echo ""
echo "=== Summary ==="
echo "- Total chapter pages: $(find src/app/week-* -name 'page.tsx' 2>/dev/null | wc -l | tr -d ' ')"
echo "- Total markdown files: $(find public/chapters -name '*.md' 2>/dev/null | wc -l | tr -d ' ')"
echo ""
if [ "$missing" -eq 0 ]; then
  echo "All checks passed! Ready to run: npm install && npm run dev"
else
  echo "Quality check failed: missing required files."
fi
exit "$missing"
