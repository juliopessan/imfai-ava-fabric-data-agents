#!/usr/bin/env python3
"""
Phase 5: Visual Regression Testing via Playwright
Captures screenshots of all Financeiro dashboards at multiple breakpoints

Screenshots:
  • Mobile: 390x844 (iPhone 12)
  • Tablet: 768x1024 (iPad)
  • Desktop: 1920x1080 (Full HD)

Stores in: projects/Financeiro/outputs/screenshots/
"""

import subprocess
import sys
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
Financeiro_OUTPUTS = PROJECT_ROOT / "projects" / "Financeiro" / "outputs"
SCREENSHOTS_DIR = Financeiro_OUTPUTS / "screenshots"

# Dashboard files to screenshot
DASHBOARDS = [
    "00_CONSOLIDATED_MIGRATION_REPORT.html",
    "Financeiro_MIGRATION_DASHBOARD.html",
    "EXECUTIVE_DATA_FACTORY_DASHBOARD.html",
]

# Viewport sizes (name, width, height)
VIEWPORTS = [
    ("mobile", 390, 844),
    ("tablet", 768, 1024),
    ("desktop", 1920, 1080),
]

# ============================================================================
# PLAYWRIGHT SCRIPT TEMPLATE
# ============================================================================

PLAYWRIGHT_SCRIPT_TEMPLATE = '''
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def take_screenshots():
    """Take screenshots of dashboards at multiple breakpoints."""
    
    # Configuration
    dashboards = %DASHBOARDS%
    viewports = %VIEWPORTS%
    output_dir = Path(r'%OUTPUT_DIR%')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        for dashboard_name in dashboards:
            dashboard_path = Path(r'%Financeiro_OUTPUTS%') / dashboard_name
            if not dashboard_path.exists():
                print(f"⏭️  {{dashboard_name}} not found")
                continue
            
            dashboard_url = dashboard_path.as_uri()
            print(f"\\n📸 {{dashboard_name}}")
            
            for viewport_name, width, height in viewports:
                context = await browser.new_context(viewport={{"width": width, "height": height}})
                page = await context.new_page()
                
                try:
                    await page.goto(dashboard_url, wait_until="networkidle")
                    
                    # Wait for dashboard to render
                    await page.wait_for_timeout(1000)
                    
                    # Take screenshot
                    filename = f"{{dashboard_name.replace('.html', '')}}-{{viewport_name}}.png"
                    screenshot_path = output_dir / filename
                    await page.screenshot(path=str(screenshot_path), full_page=False)
                    
                    print(f"  ✅ {{viewport_name:8}} ({{width}}x{{height}}) → {{filename}}")
                    
                except Exception as e:
                    print(f"  ❌ {{viewport_name:8}} → Error: {{e}}")
                
                finally:
                    await context.close()
        
        await browser.close()
    
    print(f"\\n✨ Screenshots saved to: {{output_dir}}")

if __name__ == "__main__":
    asyncio.run(take_screenshots())
'''

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    """Generate and execute visual regression screenshot script."""
    
    print("\n" + "="*70)
    print("PHASE 5: Visual Regression Testing (Screenshots)")
    print("="*70 + "\n")
    
    # Create output directory
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Check if dashboards exist
    missing = []
    for dashboard in DASHBOARDS:
        if not (Financeiro_OUTPUTS / dashboard).exists():
            missing.append(dashboard)
    
    if missing:
        print(f"⚠️  Missing dashboards: {', '.join(missing)}")
        print("\nAvailable dashboards:")
        for f in sorted(Financeiro_OUTPUTS.glob("*.html")):
            print(f"  • {f.name}")
    
    print(f"\n📁 Output directory: {SCREENSHOTS_DIR}")
    print(f"\n📱 Viewport sizes:")
    for name, w, h in VIEWPORTS:
        print(f"  • {name:8} {w}x{h}")
    
    # Generate Playwright script using string replacement
    script_content = PLAYWRIGHT_SCRIPT_TEMPLATE
    script_content = script_content.replace('%DASHBOARDS%', repr(DASHBOARDS))
    script_content = script_content.replace('%VIEWPORTS%', repr(VIEWPORTS))
    script_content = script_content.replace('%OUTPUT_DIR%', str(SCREENSHOTS_DIR))
    script_content = script_content.replace('%Financeiro_OUTPUTS%', str(Financeiro_OUTPUTS))
    
    script_path = SCREENSHOTS_DIR / "take_screenshots.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    print(f"\n✅ Generated screenshot script: {script_path}")
    print("\n" + "="*70)
    print("TO RUN SCREENSHOT TESTS:")
    print("="*70)
    print(f"\n  1. Install Playwright (if needed):")
    print(f"     pip install playwright")
    print(f"     playwright install chromium")
    print(f"\n  2. Run screenshot script:")
    print(f"     python {script_path}")
    print(f"\n  3. Results will be saved to:")
    print(f"     {SCREENSHOTS_DIR}/*.png")
    print(f"\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
