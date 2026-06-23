
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

async def take_screenshots():
    """Take screenshots of dashboards at multiple breakpoints."""
    
    # Configuration
    dashboards = ['00_CONSOLIDATED_MIGRATION_REPORT.html', 'CLIENTEBANCO_MIGRATION_DASHBOARD.html', 'EXECUTIVE_DATA_FACTORY_DASHBOARD.html']
    viewports = [('mobile', 390, 844), ('tablet', 768, 1024), ('desktop', 1920, 1080)]
    output_dir = Path(r'~/projects/imfai-ava-fabric-data-agents\projects\clientebanco\outputs\screenshots')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        for dashboard_name in dashboards:
            dashboard_path = Path(r'~/projects/imfai-ava-fabric-data-agents\projects\clientebanco\outputs') / dashboard_name
            if not dashboard_path.exists():
                print(f"⏭️  {{dashboard_name}} not found")
                continue
            
            dashboard_url = dashboard_path.as_uri()
            print(f"\n📸 {{dashboard_name}}")
            
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
    
    print(f"\n✨ Screenshots saved to: {{output_dir}}")

if __name__ == "__main__":
    asyncio.run(take_screenshots())
