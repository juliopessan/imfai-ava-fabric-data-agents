#!/usr/bin/env python3
"""
validate_agent_contracts.py

Validates that:
1. All specs follow SPEC-TEMPLATE.md structure
2. Agent files reference their corresponding specs
3. Specs are consistent (no conflicts between sequential agents)
4. All required sections present in each spec

Usage:
  python validate_agent_contracts.py --all-specs
  python validate_agent_contracts.py --spec 02-discovery-scout.md
  python validate_agent_contracts.py --validate-wave bradesco
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple


class SpecValidator:
    def __init__(self, specs_dir=".github/specs", agents_dir=".github/agents"):
        self.specs_dir = Path(specs_dir)
        self.agents_dir = Path(agents_dir)
        self.issues = []
        self.warnings = []
        
        # Required sections in every spec
        self.REQUIRED_SECTIONS = [
            "1. Agent Identity" if "Master" in str(specs_dir) else "Input Contract",
            "Task Definition",
            "Output Contract",
            "Constraints",
            "Success Criteria",
        ]
        
    def validate_all_specs(self) -> bool:
        """Validate all specs in specs directory."""
        print("🔍 Validating all specs...")
        print(f"   Location: {self.specs_dir}\n")
        
        specs = sorted(self.specs_dir.glob("*.md"))
        results = {}
        
        for spec_file in specs:
            if spec_file.name in ["SPEC-TEMPLATE.md", "README.md", "HOW-TO-USE-SPECS.md"]:
                continue
            
            result = self.validate_spec(spec_file)
            results[spec_file.name] = result
        
        # Print results
        passed = sum(1 for r in results.values() if r)
        total = len(results)
        
        for spec_name, result in results.items():
            status = "✅" if result else "❌"
            print(f"{status} {spec_name}")
        
        print(f"\n📊 Results: {passed}/{total} specs valid\n")
        
        if self.issues:
            print("❌ ISSUES FOUND:")
            for issue in self.issues:
                print(f"   • {issue}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"   • {warning}")
            print()
        
        return passed == total
    
    def validate_spec(self, spec_path: Path) -> bool:
        """Validate a single spec file."""
        try:
            content = spec_path.read_text(encoding="utf-8")
            
            # Check required sections
            missing_sections = []
            for section in self.REQUIRED_SECTIONS:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                self.issues.append(
                    f"{spec_path.name}: Missing sections: {', '.join(missing_sections)}"
                )
                return False
            
            # Check for valid Markdown structure
            if not re.search(r"^# SDD:", content, re.MULTILINE):
                self.warnings.append(f"{spec_path.name}: Missing '# SDD:' header")
            
            # Check for Input/Output contracts
            if "Input Contract" not in content:
                self.warnings.append(f"{spec_path.name}: No Input Contract section")
            
            if "Output Contract" not in content:
                self.warnings.append(f"{spec_path.name}: No Output Contract section")
            
            # Validate YAML blocks in Input Contract (if present)
            yaml_blocks = re.findall(r"```yaml\n(.*?)\n```", content, re.DOTALL)
            if yaml_blocks:
                for block in yaml_blocks:
                    if "Required:" not in block and "Optional:" not in block:
                        self.warnings.append(
                            f"{spec_path.name}: YAML block missing Required/Optional fields"
                        )
            
            return True
        
        except Exception as e:
            self.issues.append(f"{spec_path.name}: Read error — {e}")
            return False
    
    def validate_spec_workflow(self, wave: str = None) -> bool:
        """Validate that agent specs form a valid workflow."""
        print("🔄 Validating workflow...")
        
        # Load all specs
        specs = {}
        for spec_file in sorted(self.specs_dir.glob("*.md")):
            if spec_file.name.startswith(("01-", "02-", "03-", "04-", "05-", "06-", "07-", "08-", "09-", "10-")):
                content = spec_file.read_text()
                specs[spec_file.name] = content
        
        # Validate handoff chain
        prev_outputs = None
        for i in range(1, 11):  # Specs 01-10
            spec_file = f"{i:02d}-*.md"
            # Find matching spec
            matching = list(self.specs_dir.glob(spec_file))
            if not matching:
                self.warnings.append(f"Spec {i:02d} not found")
                continue
            
            spec_content = matching[0].read_text()
            
            # Extract "Passes To" field
            passes_to_match = re.search(r"Passes To:\s*(.+)", spec_content)
            if passes_to_match:
                next_agent = passes_to_match.group(1).strip()
                # Verify next agent exists
                next_spec_pattern = f"*-{next_agent.lower().replace(' ', '-')}.md"
                if not list(self.specs_dir.glob(next_spec_pattern)):
                    self.warnings.append(f"Spec {i:02d}: References unknown agent '{next_agent}'")
        
        print("✅ Workflow validation complete\n")
        return len(self.issues) == 0
    
    def check_agent_spec_references(self) -> bool:
        """Check that all agent files reference their specs."""
        print("🔗 Checking agent-spec links...\n")
        
        agents = list(self.agents_dir.glob("*.chatmode.md"))
        valid_count = 0
        
        for agent_file in agents:
            content = agent_file.read_text()
            
            # Extract agent name
            agent_name = agent_file.stem.replace(".chatmode", "")
            
            # Check if spec is referenced
            spec_ref_found = False
            for spec_file in self.specs_dir.glob("*.md"):
                if agent_name.lower() in spec_file.name.lower():
                    if f"specs/{spec_file.name}" in content or f"specs/{spec_file.name}" in agent_file.name:
                        spec_ref_found = True
                        break
            
            if spec_ref_found:
                print(f"✅ {agent_file.name} → spec found")
                valid_count += 1
            else:
                print(f"⚠️  {agent_file.name} → spec NOT referenced")
                self.warnings.append(f"Agent {agent_name} doesn't reference spec")
        
        print(f"\n✅ {valid_count}/{len(agents)} agents linked to specs\n")
        return valid_count == len(agents)
    
    def generate_report(self) -> Dict:
        """Generate validation report."""
        return {
            "timestamp": __import__("datetime").datetime.now().isoformat(),
            "total_issues": len(self.issues),
            "total_warnings": len(self.warnings),
            "issues": self.issues,
            "warnings": self.warnings,
            "status": "PASS" if len(self.issues) == 0 else "FAIL"
        }


def main():
    parser = argparse.ArgumentParser(description="Validate agent specs")
    parser.add_argument("--all-specs", action="store_true", help="Validate all specs")
    parser.add_argument("--spec", type=str, help="Validate specific spec")
    parser.add_argument("--validate-wave", type=str, help="Validate workflow for wave")
    parser.add_argument("--check-links", action="store_true", help="Check agent-spec links")
    parser.add_argument("--json", action="store_true", help="Output JSON report")
    
    args = parser.parse_args()
    
    validator = SpecValidator()
    
    if args.all_specs:
        result = validator.validate_all_specs()
        if args.json:
            print(json.dumps(validator.generate_report(), indent=2))
    elif args.spec:
        result = validator.validate_spec(Path(args.spec))
        print(f"{'✅' if result else '❌'} {args.spec}")
    elif args.validate_wave:
        result = validator.validate_spec_workflow(args.validate_wave)
    elif args.check_links:
        result = validator.check_agent_spec_references()
    else:
        result = validator.validate_all_specs()
    
    return 0 if result else 1


if __name__ == "__main__":
    exit(main())
