#!/usr/bin/env python3
"""
Phase 4: ClienteBanco Project Integration
Regenerates ClienteBanco dashboards with Orange DNA design patterns (sidebar + topbar)

Usage:
    python regenerate_clientebanco_dashboards.py
    
Output:
    - Updates all HTML dashboards in projects/clientebanco/outputs/
    - Applies new design system: 248px sidebar + 56px topbar
    - Preserves content, enhances layout
"""

import os
import glob
import re
from pathlib import Path
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
CLIENTEBANCO_OUTPUTS = PROJECT_ROOT / "projects" / "clientebanco" / "outputs"
TEMPLATES_DIR = PROJECT_ROOT / "reports" / "_templates"

DESIGN_TOKENS_LINK = '<link rel="stylesheet" href="../../reports/_templates/DESIGN-TOKENS.css">'

# ============================================================================
# TEMPLATE FRAGMENTS
# ============================================================================

TOPBAR_HTML = '''    <!-- TOP BAR (Orange DNA) -->
    <div class="topbar">
        <div class="topbar-logo">📊 Dashboard</div>
        <input type="text" class="topbar-search" placeholder="🔍 Buscar...">
        <div class="topbar-controls">
            <div class="topbar-avatar">RC</div>
        </div>
    </div>
'''

SIDEBAR_HTML = '''    <!-- SIDEBAR (Orange DNA 248px) -->
    <nav class="sidebar">
        <ul class="sidebar-nav">
            <li class="sidebar-nav-item active">📊 Dashboard</li>
            <li class="sidebar-nav-item">📈 Analytics</li>
            <li class="sidebar-nav-item">👥 Team</li>
            <li class="sidebar-nav-item">⚙️ Settings</li>
        </ul>
    </nav>
'''

# CSS for Orange DNA layout (to be added to <style> tag)
ORANGE_DNA_CSS = '''
        /* ===== ORANGE DNA LAYOUT (Phase 4) ===== */
        .topbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 56px;
            background: var(--color-white);
            border-bottom: 1px solid var(--color-border);
            z-index: 1000;
            display: flex;
            align-items: center;
            padding: 0 var(--spacing-lg);
            gap: var(--spacing-md);
            box-shadow: var(--shadow-sm);
        }

        .topbar-logo {
            font-weight: 700;
            font-size: 1.2em;
            color: var(--color-primary-orange);
            text-decoration: none;
            min-width: 200px;
        }

        .topbar-search {
            flex: 1;
            max-width: 400px;
            padding: var(--spacing-sm) var(--spacing-md);
            border: 1px solid var(--color-border);
            border-radius: var(--radius-md);
            font-family: var(--font-family);
            font-size: 0.95em;
        }

        .topbar-controls {
            display: flex;
            gap: var(--spacing-md);
            margin-left: auto;
            align-items: center;
        }

        .topbar-avatar {
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: var(--color-primary-orange);
            color: var(--color-white);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9em;
        }

        .app-container {
            display: flex;
            flex: 1;
            margin-top: 56px;
        }

        .sidebar {
            position: fixed;
            left: 0;
            top: 56px;
            width: 248px;
            height: calc(100vh - 56px);
            background: var(--color-white);
            border-right: 1px solid var(--color-border);
            padding: var(--spacing-lg) 0;
            overflow-y: auto;
            z-index: 999;
        }

        .sidebar-nav {
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .sidebar-nav-item {
            padding: var(--spacing-md) var(--spacing-lg);
            color: var(--color-text-primary);
            cursor: pointer;
            border-left: 3px solid transparent;
            transition: all 0.2s ease;
            font-size: 0.95em;
        }

        .sidebar-nav-item:hover {
            background: var(--color-light-bg);
        }

        .sidebar-nav-item.active {
            background: #FFE6D3;
            border-left-color: var(--color-primary-orange);
            color: var(--color-primary-orange);
            font-weight: 600;
        }

        .main-content {
            margin-left: 248px;
            padding: var(--spacing-lg);
            flex: 1;
        }

        @media (max-width: 768px) {
            .sidebar {
                display: none;
            }
            .main-content {
                margin-left: 0;
            }
            .topbar-search {
                display: none;
            }
        }
'''

# ============================================================================
# FUNCTIONS
# ============================================================================

def has_orange_dna_markers(html_content: str) -> bool:
    """Check if HTML already has Orange DNA layout."""
    return 'class="topbar"' in html_content and 'class="sidebar"' in html_content


def extract_body_content(html_content: str) -> str:
    """Extract content between <body> tags."""
    match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1)
    return html_content


def add_orange_dna_layout(html_content: str) -> str:
    """
    Transform HTML to use Orange DNA layout (topbar + sidebar).
    
    Returns:
        Transformed HTML with Orange DNA patterns
    """
    if has_orange_dna_markers(html_content):
        print("  ⏭️  Skipping (already has Orange DNA markers)")
        return html_content

    # Add DESIGN-TOKENS.css import if not present
    if 'DESIGN-TOKENS.css' not in html_content:
        html_content = html_content.replace(
            '</title>',
            '</title>\n    <!-- Design System Tokens -->\n    <link rel="stylesheet" href="../../reports/_templates/DESIGN-TOKENS.css">'
        )

    # Add Orange DNA CSS to <style> tag if not present
    if 'ORANGE DNA LAYOUT' not in html_content:
        html_content = re.sub(
            r'(<style[^>]*>)',
            r'\1\n' + ORANGE_DNA_CSS,
            html_content,
            count=1
        )

    # Extract body content
    body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
    if body_match:
        body_content = body_match.group(1)
        
        # Wrap content in Orange DNA structure
        new_body = f'''<body>
{TOPBAR_HTML}
{SIDEBAR_HTML}
    <div class="app-container">
        <div class="main-content">
            <div class="page-wrapper">
{body_content}
            </div>
        </div>
    </div>
</body>'''
        
        html_content = html_content.replace(body_match.group(0), new_body)

    return html_content


def regenerate_dashboard(input_path: Path, output_path: Path = None) -> bool:
    """
    Regenerate single dashboard with Orange DNA layout.
    
    Args:
        input_path: Path to original HTML file
        output_path: Path to save updated file (default: overwrite input)
    
    Returns:
        True if successful, False otherwise
    """
    if not input_path.exists():
        print(f"  ❌ File not found: {input_path}")
        return False

    output_path = output_path or input_path

    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        updated_html = add_orange_dna_layout(html_content)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(updated_html)

        print(f"  ✅ Regenerated: {output_path.name}")
        return True

    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False


def main():
    """Main regeneration workflow."""
    print("\n" + "="*70)
    print("PHASE 4: ClienteBanco Project Integration")
    print("Regenerating dashboards with Orange DNA patterns")
    print("="*70 + "\n")

    if not CLIENTEBANCO_OUTPUTS.exists():
        print(f"❌ ClienteBanco outputs directory not found: {CLIENTEBANCO_OUTPUTS}")
        return

    # Find all HTML files in outputs
    html_files = sorted(CLIENTEBANCO_OUTPUTS.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in ClienteBanco outputs")
        return

    print(f"📁 Found {len(html_files)} dashboard(s) to regenerate:\n")

    success_count = 0
    for html_file in html_files:
        print(f"  🔄 {html_file.name}")
        if regenerate_dashboard(html_file):
            success_count += 1

    print(f"\n{'='*70}")
    print(f"✅ Phase 4 Complete: {success_count}/{len(html_files)} dashboards regenerated")
    print(f"{'='*70}\n")

    # Summary
    print("📝 Summary of Changes:")
    print("  • Added 56px fixed topbar with logo, search, user avatar")
    print("  • Added 248px fixed left sidebar with navigation")
    print("  • Content wrapped in app-container with proper spacing")
    print("  • Mobile responsive: sidebar hides on <768px")
    print("  • All dashboards now use DESIGN-TOKENS.css")
    print("  • Peach highlight (#FFE6D3) active states applied")
    print("\n✨ Orange DNA design patterns successfully integrated!\n")


if __name__ == "__main__":
    main()
