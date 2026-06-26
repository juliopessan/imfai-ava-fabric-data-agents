#!/usr/bin/env python3
"""
test_specs_system.py

Phase 3: Comprehensive Testing of Specs System
- Validates all specs structure
- Tests agent-spec compliance
- Measures token reduction
- Confirms zero hallucination
- Tests workflow with sample Financeiro data

Usage:
  python test_specs_system.py --all
  python test_specs_system.py --validate-specs
  python test_specs_system.py --test-workflow
  python test_specs_system.py --measure-tokens
  python test_specs_system.py --report
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime
import statistics

_SCRIPTS_DIR = Path(__file__).resolve().parents[2] / "src" / "shared" / "scripts"
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from real_compressor import count_tokens, tokenizer_method  # noqa: E402


def _read_text_safe(path: Path) -> str:
    """Read a repo doc that may be UTF-8 or legacy cp1252 (some PT-BR files are)."""
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="cp1252")


class SpecsSystemTester:
    def __init__(self, specs_dir=".github/specs", agents_dir=".github/agents", project_root="."):
        self.specs_dir = Path(specs_dir)
        self.agents_dir = Path(agents_dir)
        self.project_root = Path(project_root)
        self.test_results = {}
        self.metrics = {}
        
    def validate_all_specs(self) -> Tuple[int, int]:
        """Test 1: Validate all spec files are well-formed."""
        print("🧪 TEST 1: Validate All Specs")
        print("-" * 60)
        
        valid_count = 0
        invalid_count = 0
        
        required_sections = [
            "# SDD:",
            "Input Contract",
            "Task Definition",
            "Success Criteria",
            "Output Contract",
            "Constraints",
        ]
        
        for spec_file in sorted(self.specs_dir.glob("*.md")):
            if spec_file.name in ["README.md", "HOW-TO-USE-SPECS.md", "SPEC-INTEGRATION-GUIDE.md", "SPEC-TEMPLATE.md"]:
                continue
            
            content = _read_text_safe(spec_file)
            
            # Check all required sections
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                print(f"❌ {spec_file.name} — Missing: {', '.join(missing_sections)}")
                invalid_count += 1
            else:
                print(f"✅ {spec_file.name} — Valid")
                valid_count += 1
        
        self.test_results["validate_specs"] = {
            "valid": valid_count,
            "invalid": invalid_count,
            "total": valid_count + invalid_count,
            "passed": invalid_count == 0,
        }
        
        return valid_count, invalid_count
    
    def validate_agent_spec_links(self) -> Tuple[int, int]:
        """
        Test 2: Validate that agents covered by the Specs System reference
        their spec. Only the 16 agents with a numbered spec (01-16) are in
        scope — the Specs System never claimed to cover the other 5
        (agent-designer, bi-semantic, data-strategist, documentation,
        orchestrator — the last is explicitly DEPRECATED). Those are
        reported separately, not counted as failures of this system.
        """
        print("\n🧪 TEST 2: Validate Agent-Spec Links")
        print("-" * 60)

        specced_agent_names = {
            spec_file.stem.split("-", 1)[1]
            for spec_file in self.specs_dir.glob("*.md")
            if spec_file.name.startswith(tuple(f"{i:02d}-" for i in range(1, 17)))
        }

        linked_count = 0
        unlinked_count = 0
        out_of_scope = []

        for agent_file in sorted(self.agents_dir.glob("*.chatmode.md")):
            agent_name = agent_file.stem.replace(".chatmode", "")

            if agent_name not in specced_agent_names:
                out_of_scope.append(agent_name)
                continue

            content = _read_text_safe(agent_file)
            has_spec_field = re.search(r'spec:\s*\.github/specs/\d{2}-.*?\.md', content)

            if has_spec_field:
                print(f"✅ {agent_file.name} → spec field found")
                linked_count += 1
            else:
                print(f"❌ {agent_file.name} → spec field NOT found")
                unlinked_count += 1

        if out_of_scope:
            print(f"ℹ️  Out of Specs System scope (no numbered spec exists): {', '.join(out_of_scope)}")

        self.test_results["agent_links"] = {
            "linked": linked_count,
            "unlinked": unlinked_count,
            "total": linked_count + unlinked_count,
            "out_of_scope": out_of_scope,
            "passed": unlinked_count == 0,
        }
        
        return linked_count, unlinked_count
    
    def test_spec_workflow_chain(self) -> bool:
        """Test 3: Validate workflow handoff chain (01→02→...→10)."""
        print("\n🧪 TEST 3: Validate Workflow Handoff Chain")
        print("-" * 60)
        
        spec_files = [
            ("01-master-agent.md", None),  # Dynamic router (see "Routes To"), not a fixed handoff
            ("02-discovery-scout.md", "business-analyst"),
            ("03-data-architect.md", None),  # Receives from multiple
            ("04-business-analyst.md", "data-modeler"),
            ("05-data-modeler.md", "code-generator"),
            ("06-code-generator.md", "downstream-executor"),
            ("07-downstream-executor.md", "quality-gate"),
            ("08-migration-coordinator.md", None),  # Orchestrator
            ("09-quality-gate.md", None),  # Gate keeper
            ("10-reconciliation.md", None),  # Final check
        ]
        
        all_valid = True
        
        for spec_file, expected_next in spec_files:
            spec_path = self.specs_dir / spec_file
            if not spec_path.exists():
                print(f"❌ {spec_file} — File not found")
                all_valid = False
                continue
            
            content = _read_text_safe(spec_path)

            # Check if "Passes To" or a dynamic "Routes To" is documented
            passes_to_match = re.search(r"Passes To:\s*(.+)", content)
            routes_to_match = re.search(r"Routes To:\s*(.+)", content)

            if passes_to_match and expected_next:
                next_agent = passes_to_match.group(1).strip()
                status = "✅" if expected_next.lower() in next_agent.lower() else "⚠️ "
                print(f"{status} {spec_file} → Passes to: {next_agent}")
            elif expected_next is None and routes_to_match:
                print(f"✅ {spec_file} — Dynamic router: {routes_to_match.group(1).strip()}")
            elif expected_next is None and passes_to_match:
                print(f"ℹ️  {spec_file} — Endpoint or fork (OK)")
            elif expected_next is None:
                print(f"⚠️  {spec_file} — Endpoint/fork has no 'Passes To' or 'Routes To' documented")
                all_valid = False
            else:
                print(f"⚠️  {spec_file} — Missing 'Passes To' section")
                all_valid = False
        
        self.test_results["workflow_chain"] = {
            "passed": all_valid,
        }
        
        return all_valid
    
    def _resolve_agent_file_content(self, agent_file: Path) -> Tuple[str, bool]:
        """
        Resolve a chatmode.md's `@file <path>` include to the real prompt it
        points at. Returns (content, resolved). If the referenced file
        doesn't exist in this repo, returns the stub's own 6-line content
        and resolved=False — the stub is NOT a stand-in for "the real agent
        prompt"; callers must treat unresolved agents separately, not fold
        their stub size into a token comparison as if it were real.
        """
        stub_content = _read_text_safe(agent_file)
        match = re.search(r"^@file\s+(.+)$", stub_content, re.MULTILINE)
        if not match:
            return stub_content, True  # no include — stub IS the whole prompt

        included_path = self.project_root / match.group(1).strip()
        if included_path.exists():
            return _read_text_safe(included_path), True
        return stub_content, False

    def measure_token_reduction(self) -> Dict:
        """
        Test 4: Measure token reduction (before specs vs after specs).

        Real measurement, not a guess: "before" is the actual token count of
        the real agent prompt (resolving each chatmode.md's `@file` include)
        an agent would have to read without specs; "after" is the actual
        token count of the matching spec file it reads instead. Both sides
        use the same real tokenizer (real_compressor.count_tokens — tiktoken
        when available). No hardcoded per-task constants.

        Only the 16 agents that have a numbered spec (01-16) are compared —
        see validate_agent_spec_links() for the 5 agents out of scope.
        """
        print("\n🧪 TEST 4: Measure Token Reduction")
        print("-" * 60)

        spec_tokens_by_file: Dict[str, int] = {}
        for spec_file in self.specs_dir.glob("*.md"):
            if spec_file.name.startswith(tuple(f"{i:02d}-" for i in range(1, 17))):
                spec_tokens_by_file[spec_file.stem] = count_tokens(_read_text_safe(spec_file))

        agent_name_by_spec_num = {
            spec_file.stem.split("-", 1)[1]: spec_file.stem
            for spec_file in self.specs_dir.glob("*.md")
            if spec_file.name.startswith(tuple(f"{i:02d}-" for i in range(1, 17)))
        }

        agent_tokens_by_file: Dict[str, int] = {}
        unresolved_agents: List[str] = []
        for agent_name in agent_name_by_spec_num:
            agent_file = self.agents_dir / f"{agent_name}.chatmode.md"
            if not agent_file.exists():
                continue
            content, resolved = self._resolve_agent_file_content(agent_file)
            agent_tokens_by_file[agent_name] = count_tokens(content)
            if not resolved:
                unresolved_agents.append(agent_name)

        total_before = sum(agent_tokens_by_file.values())
        total_after = sum(spec_tokens_by_file.values())

        reduction = ((total_before - total_after) / total_before * 100) if total_before > 0 else 0.0

        print(f"📊 Token Analysis ({tokenizer_method()}):")
        if unresolved_agents:
            print(
                f"⚠️  {len(unresolved_agents)}/{len(agent_tokens_by_file)} agent prompts are unresolved "
                f"`@file` stubs (the real prompt file doesn't exist in this repo): "
                f"{', '.join(sorted(unresolved_agents))}"
            )
            print("   Their 6-line stub size is being counted as 'before' — this UNDER-counts the real")
            print("   baseline, so the reduction number below is not reliable until those prompts exist.")
        print(f"   Agent files (before specs):   {total_before:,} tokens across {len(agent_tokens_by_file)} files")
        print(f"   Spec files (after specs):     {total_after:,} tokens across {len(spec_tokens_by_file)} files")
        print(f"   Measured reduction:           {reduction:.1f}%")

        self.metrics["token_reduction"] = {
            "method": tokenizer_method(),
            "agent_tokens_total": total_before,
            "spec_tokens_total": total_after,
            "reduction_percent": reduction,
            "target_met": reduction >= 70 and not unresolved_agents,
            "unresolved_agents": unresolved_agents,
            "reliable": not unresolved_agents,
            "by_agent": agent_tokens_by_file,
            "by_spec": spec_tokens_by_file,
        }

        return self.metrics["token_reduction"]
    
    def test_hallucination_prevention(self) -> bool:
        """Test 5: Verify specs prevent hallucination."""
        print("\n🧪 TEST 5: Verify Hallucination Prevention")
        print("-" * 60)
        
        hallucination_keywords = [
            "GUESS",
            "ASSUME",
            "INFER",
            "PARTIAL",
            "NO GUESSING",
            "NO INFERRING",
            "Flag unknowns",
        ]
        
        prevention_found = True
        
        # Check discovery-scout spec (most hallucination-prone)
        spec_path = self.specs_dir / "02-discovery-scout.md"
        content = _read_text_safe(spec_path)
        
        found_keywords = []
        for keyword in hallucination_keywords:
            if keyword in content:
                found_keywords.append(keyword)
        
        if found_keywords:
            print(f"✅ Hallucination prevention found in specs:")
            for keyword in found_keywords:
                print(f"   • {keyword}")
        else:
            print(f"❌ Insufficient hallucination prevention")
            prevention_found = False
        
        # Check constraints section
        if "🔴 NO GUESSING" in content and "🔴 NO INFERRING" in content:
            print(f"✅ Hard constraints present: NO GUESSING, NO INFERRING")
        else:
            print(f"⚠️  Consider adding hard constraints")
        
        self.test_results["hallucination_prevention"] = {
            "passed": prevention_found,
            "keywords_found": len(found_keywords),
        }
        
        return prevention_found
    
    def test_workflow_with_Financeiro(self) -> Tuple[bool, str]:
        """Test 6: Test workflow with Financeiro sample data."""
        print("\n🧪 TEST 6: Test Workflow with Financeiro Wave")
        print("-" * 60)
        
        # Check if Financeiro wave config exists
        wave_config = self.project_root / "projects" / "Financeiro" / "wave-config.yaml"
        
        if not wave_config.exists():
            print(f"⚠️  Financeiro wave-config.yaml not found")
            return False, "Wave config missing"
        
        print(f"✅ Wave config found: {wave_config}")
        
        # Validate wave config structure
        import yaml
        try:
            with open(wave_config, encoding="utf-8") as f:
                config = yaml.safe_load(f)
            
            required_fields = ["project_name", "phases", "discovery_owner"]
            missing_fields = [f for f in required_fields if f not in config]
            
            if missing_fields:
                print(f"❌ Wave config missing fields: {missing_fields}")
                return False, f"Missing: {missing_fields}"
            
            print(f"✅ Wave config valid: {config.get('project_name')}")
            
            # Check legacy folder
            legacy_folder = self.project_root / "projects" / "Financeiro" / "legacy"
            if legacy_folder.exists():
                legacy_files = list(legacy_folder.glob("*"))
                print(f"✅ Legacy folder found: {len(legacy_files)} files")
            
            return True, "Workflow ready"
        
        except Exception as e:
            print(f"❌ Error parsing wave config: {e}")
            return False, str(e)
    
    def run_all_tests(self) -> bool:
        """Run all Phase 3 tests."""
        print("=" * 60)
        print("🧪 PHASE 3: COMPREHENSIVE TESTING")
        print("=" * 60)
        
        # Run all tests
        valid, invalid = self.validate_all_specs()
        linked, unlinked = self.validate_agent_spec_links()
        workflow_ok = self.test_spec_workflow_chain()
        token_metrics = self.measure_token_reduction()
        hallucination_ok = self.test_hallucination_prevention()
        workflow_ok_Financeiro, workflow_msg = self.test_workflow_with_Financeiro()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        all_passed = (
            invalid == 0 and
            unlinked == 0 and
            workflow_ok and
            token_metrics["target_met"] and
            hallucination_ok and
            workflow_ok_Financeiro
        )
        
        print(f"{'✅' if invalid == 0 else '❌'} Specs Valid: {valid}/16")
        print(f"{'✅' if unlinked == 0 else '❌'} Agents Linked: {linked}/16")
        print(f"{'✅' if workflow_ok else '❌'} Workflow Chain: Valid")
        reliability_note = "" if token_metrics["reliable"] else f" — UNRELIABLE: {len(token_metrics['unresolved_agents'])} agent prompt(s) don't exist in this repo"
        print(f"{'✅' if token_metrics['target_met'] else '❌'} Token Reduction: {token_metrics['reduction_percent']:.1f}% (target: 70%){reliability_note}")
        print(f"{'✅' if hallucination_ok else '❌'} Hallucination Prevention: Valid")
        print(f"{'✅' if workflow_ok_Financeiro else '❌'} Financeiro Workflow: {workflow_msg}")
        
        print("\n" + "=" * 60)
        if all_passed:
            print("🎉 PHASE 3 TESTING: ALL TESTS PASSED ✅")
        else:
            print("⚠️  PHASE 3 TESTING: Some tests failed — Review above")
        print("=" * 60)
        
        return all_passed
    
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "phase": "Phase 3: Testing",
            "test_results": self.test_results,
            "metrics": self.metrics,
            "all_passed": all(
                result.get("passed", True) for result in self.test_results.values()
            ),
        }
        
        return report


import re


def main():
    import argparse

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="Phase 3: Test Specs System")
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--validate-specs", action="store_true", help="Validate spec files")
    parser.add_argument("--test-workflow", action="store_true", help="Test workflow chain")
    parser.add_argument("--measure-tokens", action="store_true", help="Measure token reduction")
    parser.add_argument("--report", action="store_true", help="Generate test report")
    
    args = parser.parse_args()
    
    tester = SpecsSystemTester()
    
    if args.all:
        passed = tester.run_all_tests()
        exit(0 if passed else 1)
    elif args.validate_specs:
        tester.validate_all_specs()
    elif args.test_workflow:
        tester.test_spec_workflow_chain()
    elif args.measure_tokens:
        tester.measure_token_reduction()
    elif args.report:
        report = tester.generate_test_report()
        print(json.dumps(report, indent=2))
    else:
        # Default: run all tests
        passed = tester.run_all_tests()
        exit(0 if passed else 1)


if __name__ == "__main__":
    main()
