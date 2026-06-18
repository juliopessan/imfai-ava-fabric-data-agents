#!/usr/bin/env python3
"""
integrate_agents_with_specs.py

Automatiza Phase 2: Integração de Agentes com Specs
- Adiciona campo 'spec:' no frontmatter YAML de cada agente
- Adiciona seção "🔗 Spec Reference" após o título
- Valida conformidade com specs
- Gera relatório de integração

Usage:
  python integrate_agents_with_specs.py --dry-run
  python integrate_agents_with_specs.py --execute
  python integrate_agents_with_specs.py --validate
  python integrate_agents_with_specs.py --status
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime


class AgentSpecIntegrator:
    def __init__(self, agents_dir=".github/agents", specs_dir=".github/specs"):
        self.agents_dir = Path(agents_dir)
        self.specs_dir = Path(specs_dir)
        self.results = {}
        self.spec_mapping = self._build_spec_mapping()
        
    def _build_spec_mapping(self) -> Dict[str, str]:
        """Map agent names to spec file numbers."""
        mapping = {
            "master-agent": "01-master-agent.md",
            "discovery-scout": "02-discovery-scout.md",
            "data-architect": "03-data-architect.md",
            "business-analyst": "04-business-analyst.md",
            "data-modeler": "05-data-modeler.md",
            "code-generator": "06-code-generator.md",
            "downstream-executor": "07-downstream-executor.md",
            "migration-coordinator": "08-migration-coordinator.md",
            "quality-gate": "09-quality-gate.md",
            "reconciliation": "10-reconciliation.md",
            "data-steward": "11-data-steward.md",
            "self-healing": "12-self-healing.md",
            "logic-extractor": "13-logic-extractor.md",
            "iteration-improvement": "14-iteration-improvement.md",
            "security-compliance": "15-security-compliance.md",
            "inventory-scout": "16-inventory-scout.md",
        }
        return mapping
    
    def dry_run(self):
        """Show what would be changed without modifying files."""
        print("🔍 DRY RUN: Showing what would be changed\n")
        
        for agent_file in sorted(self.agents_dir.glob("*.chatmode.md")):
            agent_name = agent_file.stem.replace(".chatmode", "")
            spec_file = self.spec_mapping.get(agent_name)
            
            if not spec_file:
                print(f"⚠️  {agent_file.name} → No spec mapping found")
                continue
            
            spec_path = self.specs_dir / spec_file
            if not spec_path.exists():
                print(f"❌ {agent_file.name} → Spec not found: {spec_file}")
                continue
            
            content = agent_file.read_text()
            has_spec_field = "spec:" in content
            has_spec_ref = "🔗 Spec Reference" in content
            
            status = "✅ Already integrated" if (has_spec_field and has_spec_ref) else "⏳ Would update"
            print(f"{status} {agent_file.name} → {spec_file}")
            
            if not has_spec_field:
                print(f"    → Would add: spec: .github/specs/{spec_file}")
            if not has_spec_ref:
                print(f"    → Would add: 🔗 Spec Reference section")
    
    def execute_integration(self):
        """Execute Phase 2: Integrate all agents with specs."""
        print("🚀 PHASE 2: Agent Integration — EXECUTING\n")
        
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        for agent_file in sorted(self.agents_dir.glob("*.chatmode.md")):
            agent_name = agent_file.stem.replace(".chatmode", "")
            spec_file = self.spec_mapping.get(agent_name)
            
            if not spec_file:
                print(f"⏭️  SKIP {agent_file.name} — No spec mapping")
                skipped_count += 1
                continue
            
            spec_path = self.specs_dir / spec_file
            if not spec_path.exists():
                print(f"❌ ERROR {agent_file.name} — Spec not found: {spec_file}")
                error_count += 1
                continue
            
            try:
                result = self._integrate_agent(agent_file, spec_file, spec_path)
                if result:
                    print(f"✅ UPDATED {agent_file.name} → {spec_file}")
                    updated_count += 1
                    self.results[agent_name] = "updated"
                else:
                    print(f"⏭️  SKIP {agent_file.name} — Already integrated")
                    skipped_count += 1
                    self.results[agent_name] = "skipped"
            except Exception as e:
                print(f"❌ ERROR {agent_file.name} — {e}")
                error_count += 1
                self.results[agent_name] = "error"
        
        print(f"\n📊 Results:")
        print(f"   Updated: {updated_count}/16")
        print(f"   Skipped: {skipped_count}/16")
        print(f"   Errors: {error_count}/16")
        
        return updated_count, skipped_count, error_count
    
    def _integrate_agent(self, agent_file: Path, spec_file: str, spec_path: Path) -> bool:
        """Integrate single agent file with spec."""
        content = agent_file.read_text()
        
        # Check if already integrated
        if "spec:" in content and "🔗 Spec Reference" in content:
            return False
        
        # Step 1: Add spec: field to frontmatter
        if "spec:" not in content:
            # Find YAML frontmatter
            yaml_match = re.match(r"^(---\n.*?\n)---\n", content, re.DOTALL)
            if yaml_match:
                yaml_end = yaml_match.end(1)
                # Find where to insert spec: (after description:)
                desc_match = re.search(r"description: [^\n]*\n", content[:yaml_end])
                if desc_match:
                    insert_pos = desc_match.end()
                    content = content[:insert_pos] + f"spec: .github/specs/{spec_file}\n" + content[insert_pos:]
        
        # Step 2: Add Spec Reference section after title
        title_match = re.search(r"^(# .*?\n)", content, re.MULTILINE)
        if title_match and "🔗 Spec Reference" not in content:
            title_end = title_match.end()
            
            # Extract spec number
            spec_num = spec_file.split("-")[0]
            
            spec_ref_section = f"""
## 🔗 Spec Reference

**Spec:** [.github/specs/{spec_file}](.github/specs/{spec_file})

This agent follows spec `{spec_file}` which defines:
- ✅ **Input Contract:** What inputs are valid
- ✅ **Task Definition:** Exactly what to do
- ✅ **Success Criteria:** How to measure success
- ✅ **Output Contract:** What to produce
- ✅ **Constraints:** Non-negotiable rules

### Key Requirements from Spec
See spec file for complete details.

---

"""
            
            content = content[:title_end] + spec_ref_section + content[title_end:]
        
        # Write updated content
        agent_file.write_text(content)
        return True
    
    def validate_integration(self):
        """Validate Phase 2 completion."""
        print("🔍 VALIDATION: Checking Phase 2 completion\n")
        
        valid_count = 0
        
        for agent_name, spec_file in self.spec_mapping.items():
            agent_file = self.agents_dir / f"{agent_name}.chatmode.md"
            
            if not agent_file.exists():
                print(f"❌ {agent_name} → Agent file not found")
                continue
            
            content = agent_file.read_text()
            
            # Check for spec: field
            has_spec_field = f"spec: .github/specs/{spec_file}" in content
            
            # Check for Spec Reference section
            has_spec_ref = "🔗 Spec Reference" in content
            
            # Check spec file exists
            spec_path = self.specs_dir / spec_file
            spec_exists = spec_path.exists()
            
            if has_spec_field and has_spec_ref and spec_exists:
                print(f"✅ {agent_name} → Fully integrated")
                valid_count += 1
            else:
                missing = []
                if not has_spec_field:
                    missing.append("spec: field")
                if not has_spec_ref:
                    missing.append("Spec Reference section")
                if not spec_exists:
                    missing.append("spec file")
                print(f"❌ {agent_name} → Missing: {', '.join(missing)}")
        
        print(f"\n📊 Validation: {valid_count}/16 agents fully integrated")
        return valid_count == 16
    
    def generate_report(self):
        """Generate Phase 2 integration report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "phase": "Phase 2: Agent Integration",
            "total_agents": 16,
            "integrated_agents": len([v for v in self.results.values() if v == "updated"]),
            "skipped_agents": len([v for v in self.results.values() if v == "skipped"]),
            "error_agents": len([v for v in self.results.values() if v == "error"]),
            "results": self.results,
            "spec_mapping": self.spec_mapping,
        }
        
        print("\n📄 PHASE 2 INTEGRATION REPORT")
        print("=" * 60)
        print(json.dumps(report, indent=2))
        
        return report


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Phase 2: Integrate agents with specs")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    parser.add_argument("--execute", action="store_true", help="Execute integration")
    parser.add_argument("--validate", action="store_true", help="Validate integration")
    parser.add_argument("--status", action="store_true", help="Show current status")
    parser.add_argument("--report", action="store_true", help="Generate report")
    
    args = parser.parse_args()
    
    integrator = AgentSpecIntegrator()
    
    if args.dry_run:
        integrator.dry_run()
    elif args.execute:
        updated, skipped, errors = integrator.execute_integration()
    elif args.validate:
        result = integrator.validate_integration()
        exit(0 if result else 1)
    elif args.report:
        integrator.generate_report()
    elif args.status:
        integrator.dry_run()
    else:
        # Default: dry-run
        integrator.dry_run()


if __name__ == "__main__":
    main()
