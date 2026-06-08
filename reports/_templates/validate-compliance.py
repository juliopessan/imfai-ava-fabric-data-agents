#!/usr/bin/env python3
"""
Validator: Avanade Style Guide Compliance Check
Audits executive-dashboard.html for brand compliance.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import List, Tuple


class AvanadeComplianceValidator:
    """Validate HTML against Avanade Style Guide."""

    REQUIRED_COLORS = {
        "#FF5800": "Avanade Orange (primary)",
        "#DC4600": "Dark Orange (hover)",
        "#890078": "Aurora (gradient end)",
        "#333333": "Grey 80 (text primary)",
        "#666666": "Grey 60 (body text)",
        "#00A650": "Success (green)",
        "#FFB414": "Warning (amber)",
        "#C80000": "Error (red)",
    }

    REQUIRED_FONTS = [
        "Segoe UI",
        "Segoe UI Variable",
    ]

    REQUIRED_COMPONENTS = [
        ("ava-header", ["<header"]),          # Header with logo
        ("ava-hero", ["ava-hero"]),           # Hero section with gradient
        ("ava-card", ["ava-card"]),           # Card component (border-top orange)
        ("ava-accent-bar", ["ava-accent-bar"]),  # Accent bar (gradient)
        ("ava-status", ["ava-status"]),       # Status indicators
        ("ava-tagline", ["ava-tagline"]),     # "Do what matters"
        ("buttons", ["ava-btn"]),             # Primary buttons (ava-btn variant)
        ("ava-pullquote", ["ava-pullquote"]), # Call-out boxes
        ("ava-flow", ["ava-flow"]),           # Flow diagram
        ("ava-footer", ["<footer"]),          # Footer with tagline
    ]

    REQUIRED_TEXT = [
        "Do what matters",      # Tagline (mandatory)
        "Avanade",              # Brand name
        "Data Migration Factory",  # Product
        "Executive Dashboard",  # Page title
    ]

    def __init__(self, html_path: str):
        """Initialize validator with HTML file."""
        self.path = Path(html_path)
        self.html = self.path.read_text(encoding='utf-8')
        self.issues: List[Tuple[str, str]] = []
        self.warnings: List[Tuple[str, str]] = []

    def validate(self) -> bool:
        """Run all compliance checks."""
        print(f"🔍 Validating: {self.path.name}\n")

        self._check_colors()
        self._check_fonts()
        self._check_components()
        self._check_text()
        self._check_spacing()
        self._check_accessibility()
        self._check_responsive()
        self._check_semantics()

        return self._report()

    def _check_colors(self):
        """Verify all required Avanade colors present."""
        print("🎨 Checking Colors...")
        missing = []
        for color, name in self.REQUIRED_COLORS.items():
            if color not in self.html:
                missing.append(f"{color} ({name})")

        if missing:
            self.warnings.append(("Colors", f"Missing colors: {', '.join(missing)}"))
        else:
            print("  ✅ All required colors found")

    def _check_fonts(self):
        """Verify Segoe UI font stack."""
        print("🔤 Checking Typography...")
        for font in self.REQUIRED_FONTS:
            if font not in self.html:
                self.warnings.append(("Typography", f"Missing font: {font}"))
                return

        # Check heading weights (H1/H2 should be Light 300, not Bold 700)
        if "font-weight: 300" not in self.html:
            self.warnings.append(
                ("Typography", "H1/H2 should use font-weight: 300 (Light), not Bold")
            )
            return

        print("  ✅ Font stack correct (Segoe UI + fallbacks)")

    def _check_components(self):
        """Verify all required components present."""
        print("🧩 Checking Components...")
        missing = []
        for component, variants in self.REQUIRED_COMPONENTS:
            found = any(v in self.html for v in variants)
            if not found:
                missing.append(component)

        if missing:
            self.warnings.append(("Components", f"Missing: {', '.join(missing)}"))
        else:
            print("  ✅ All components present")

    def _check_text(self):
        """Verify all required text present."""
        print("📝 Checking Required Text...")
        missing = []
        for text in self.REQUIRED_TEXT:
            if text not in self.html:
                missing.append(text)

        if missing:
            self.issues.append(("Content", f"Missing text: {', '.join(missing)}"))
        else:
            print("  ✅ All required text found")

    def _check_spacing(self):
        """Verify 8px base spacing system."""
        print("📐 Checking Spacing System...")
        spacing_vars = [
            "--ava-space-1: 4px",
            "--ava-space-2: 8px",
            "--ava-space-4: 16px",
            "--ava-space-6: 24px",
            "--ava-space-8: 32px",
        ]

        missing = []
        for var in spacing_vars:
            if var not in self.html:
                missing.append(var)

        if missing:
            self.issues.append(("Spacing", f"Missing vars: {', '.join(missing)}"))
        else:
            print("  ✅ Spacing system (8px base) complete")

    def _check_accessibility(self):
        """Check accessibility attributes."""
        print("♿ Checking Accessibility...")
        issues = []

        # Check for semantic HTML
        if "<h1" not in self.html:
            issues.append("Missing <h1> tag")
        if "<header" not in self.html:
            issues.append("Missing <header> semantic tag")
        if "<main" not in self.html:
            issues.append("Missing <main> semantic tag")
        if "<footer" not in self.html:
            issues.append("Missing <footer> semantic tag")
        if "lang=" not in self.html:
            issues.append("Missing lang attribute on <html>")

        # Check for viewport meta tag
        if 'viewport' not in self.html:
            issues.append("Missing viewport meta tag (responsive)")

        if issues:
            self.warnings.extend([("Accessibility", issue) for issue in issues])
        else:
            print("  ✅ Semantic HTML + accessibility features OK")

    def _check_responsive(self):
        """Verify responsive design."""
        print("📱 Checking Responsive Design...")
        issues = []

        if "@media (max-width:" not in self.html:
            issues.append("No responsive media queries found")
        if "box-sizing: border-box" not in self.html:
            issues.append("Missing box-sizing: border-box on *")

        if issues:
            self.warnings.extend([("Responsive", issue) for issue in issues])
        else:
            print("  ✅ Responsive breakpoints + mobile-first OK")

    def _check_semantics(self):
        """Verify semantic correctness."""
        print("✔️ Checking Semantics...")
        issues = []

        # Check for proper heading hierarchy
        h1_count = len(re.findall(r'<h1[^>]*>', self.html))
        if h1_count != 1:
            issues.append(f"Expected 1 <h1>, found {h1_count}")

        # Check for table headers
        if '<table' in self.html and '<thead>' not in self.html:
            issues.append("Tables should have <thead> element")

        # Check for button semantics (not divs with button styling)
        if '.ava-btn' in self.html and '<button' not in self.html:
            # OK — could be links with .ava-btn class
            pass

        if issues:
            self.warnings.extend([("Semantics", issue) for issue in issues])
        else:
            print("  ✅ Semantic HTML structure OK")

    def _report(self) -> bool:
        """Print compliance report."""
        print("\n" + "=" * 70)
        print("AVANADE COMPLIANCE REPORT")
        print("=" * 70 + "\n")

        # Issues (blocking)
        if self.issues:
            print("❌ CRITICAL ISSUES (Block Deployment):\n")
            for category, msg in self.issues:
                print(f"  [{category}] {msg}")
            print()

        # Warnings (non-blocking)
        if self.warnings:
            print("⚠️  WARNINGS (Non-blocking):\n")
            for category, msg in self.warnings:
                print(f"  [{category}] {msg}")
            print()

        # Summary
        print("=" * 70)
        if self.issues:
            print(f"❌ FAILED: {len(self.issues)} critical issue(s) found")
            return False
        elif self.warnings:
            print(f"⚠️  PASSED with {len(self.warnings)} warning(s)")
            return True
        else:
            print("✅ PASSED: 100% Avanade Style Guide Compliant")
            return True


def main():
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate HTML dashboard against Avanade Style Guide"
    )
    parser.add_argument(
        "html_file",
        nargs="?",
        default="executive-dashboard.html",
        help="HTML file to validate",
    )
    args = parser.parse_args()

    validator = AvanadeComplianceValidator(args.html_file)
    success = validator.validate()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
