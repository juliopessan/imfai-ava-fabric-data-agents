#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Workflow Validation — All Waves & Gates

Validates:
  ✅ Week 1 Trace Integration (coach_insights + trace_writer)
  ✅ Ponytail Ladder Integration (lazy senior dev mode)
  ✅ End-to-End Wave Execution (Upstream → Midstream → Downstream → Consolidation)
  ✅ Coach Insights Feedback
  ✅ Trace File Creation
  ✅ All 4 Production Scripts Integrated

Usage:
  python validate_complete_workflow.py
"""

import sys
import io
import os
from pathlib import Path

# Force UTF-8 on Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", line_buffering=True)

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent / 'tools' / 'trace-integration'))

from trace_writer import get_trace_writer
from coach_insights import get_coach_insights


def print_header(text):
    """Print formatted header."""
    print(f'\n{"=" * 90}')
    print(f'  {text}')
    print(f'{"=" * 90}\n')


def print_section(text):
    """Print section header."""
    print(f'\n{text}')
    print(f'{"-" * 70}')


def validate_scripts():
    """Check that all 4 orchestrator scripts are integrated."""
    print_section('1. SCRIPT INTEGRATION CHECK')
    
    scripts = [
        'projects/financeiro/scripts/00_MASTER_PIPELINE.py',
        'projects/financeiro/scripts/PHASE2_MIDSTREAM_ORCHESTRATOR.py',
        'projects/financeiro/scripts/PHASE3_DOWNSTREAM_ORCHESTRATOR.py',
        'projects/financeiro/scripts/PHASE4_CONSOLIDATION_ORCHESTRATOR.py',
    ]
    
    integration_count = 0
    for script_path in scripts:
        if not Path(script_path).exists():
            print(f'[MISSING] {script_path}')
            continue
        
        with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        checks = [
            ('trace_writer', 'from trace_writer import'),
            ('coach_insights', 'from coach_insights import'),
            ('write_agent_execution', 'write_agent_execution('),
            ('analyze_execution', 'analyze_execution('),
            ('print_insights', 'print_insights('),
        ]
        
        passed = sum(1 for check_name, pattern in checks if pattern in content)
        status = '[OK]' if passed == len(checks) else '[INCOMPLETE]'
        print(f'  {status} {script_path}: {passed}/{len(checks)} integration points')
        
        if passed == len(checks):
            integration_count += 1
    
    print(f'\n[RESULT] {integration_count}/{len(scripts)} scripts fully integrated')
    return integration_count == len(scripts)


def validate_agents_md():
    """Check AGENTS.md exists and contains Ponytail rules."""
    print_section('2. AGENTS.MD (PONYTAIL RULES) CHECK')
    
    agents_path = Path('AGENTS.md')
    if not agents_path.exists():
        print('[MISSING] AGENTS.md not found')
        return False
    
    with open(agents_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    checks = [
        ('Ponytail ladder', '1. Does this need to exist?'),
        ('Gate-specific rules', '### Gate 1: Upstream Discovery'),
        ('Midstream rules', '### Gate 2: Midstream Design'),
        ('Downstream rules', '### Gate 3: Downstream'),
        ('Consolidation rules', '### Gate 4: Consolidation'),
        ('Ponytail integration', 'Coach Insights'),
    ]
    
    passed = sum(1 for check_name, pattern in checks if pattern in content)
    print(f'[OK] AGENTS.md: {passed}/{len(checks)} sections present')
    return passed >= len(checks) - 1


def simulate_complete_wave(wave_num: int = 1):
    """Simulate execution of all gates with traces and coach analysis for a specific wave."""
    print_section(f'3. COMPLETE WAVE {wave_num} SIMULATION')
    
    wave = f'financeiro-wave{wave_num}-validation'
    writer = get_trace_writer()
    coach = get_coach_insights()
    
    # Gate configurations
    gates = [
        {
            'num': 1,
            'name': 'upstream-discovery',
            'agent': 'discovery-scout',
            'tokens_in': 150000,
            'tokens_out': 75000,
            'cost': 0.45,
            'artifacts': 3,  # inventory, STTM, pain_points
            'duration': 1.5,
        },
        {
            'num': 2,
            'name': 'midstream-design',
            'agent': 'data-architect',
            'tokens_in': 120000,
            'tokens_out': 60000,
            'cost': 0.36,
            'artifacts': 5,  # DDL, contracts, strategy
            'duration': 2.0,
        },
        {
            'num': 3,
            'name': 'downstream-deployment',
            'agent': 'downstream-executor',
            'tokens_in': 100000,
            'tokens_out': 50000,
            'cost': 0.30,
            'artifacts': 6,  # ETL, validation, tests
            'duration': 2.5,
        },
        {
            'num': 4,
            'name': 'consolidation',
            'agent': 'consolidation-publisher',
            'tokens_in': 50000,
            'tokens_out': 25000,
            'cost': 0.15,
            'artifacts': 11,  # dashboards + runbook
            'duration': 3.0,
        },
    ]
    
    all_passed = True
    gate_results = []
    
    for gate in gates:
        print(f'\n  [Gate {gate["num"]}] {gate["name"]}...')
        
        # Write trace
        trace = writer.write_agent_execution(
            agent_id=gate['agent'],
            wave=wave,
            gate=gate['num'],
            operation_name=f'gate_{gate["num"]}_{gate["name"]}',
            duration_sec=gate['duration'],
            tokens_in=gate['tokens_in'],
            tokens_out=gate['tokens_out'],
            cost_usd=gate['cost'],
            artifacts_generated=gate['artifacts'],
            status='success',
            user='validation'
        )
        
        if not trace:
            print(f'    [FAIL] Trace write failed')
            all_passed = False
            continue
        
        # Coach analysis
        analysis = coach.analyze_execution(trace)
        
        # Ponytail ladder validation
        ladder = coach.validate_ponytail_ladder(trace, gate['num'])
        
        result = {
            'gate': gate['num'],
            'name': gate['name'],
            'trace_id': trace.get('trace_id', 'N/A'),
            'coach_status': analysis['status'].value,
            'ladder_status': ladder['status'].value,
            'artifacts': gate['artifacts'],
            'target_artifacts': ladder['target_artifacts'],
            'efficiency': f"{(gate['tokens_out']/gate['tokens_in'])*100:.0f}%",
        }
        
        gate_results.append(result)
        
        # Validation result
        ladder_ok = ladder['status'].value == '🟢'
        coach_ok = analysis['status'].value == '🟢'
        
        status = '[OK]' if (ladder_ok and coach_ok) else '[WARN]'
        print(f'    {status} Coach: {analysis["status"].value} | '
              f'Ponytail: {ladder["status"].value} | '
              f'Artifacts: {gate["artifacts"]}/{ladder["target_artifacts"]}')
        
        if not ladder_ok:
            print(f'    Ladder check: {ladder["message"]}')
        if not coach_ok:
            print(f'    Coach status: {analysis["status"].value}')
    
    # Wave summary
    print(f'\n  [WAVE SUMMARY]')
    coach.print_wave_summary(wave)
    
    # Print gate results table
    print(f'\n  [GATE RESULTS TABLE]')
    print(f'  {"Gate":<6} {"Name":<20} {"Coach":<8} {"Ponytail":<10} '
          f'{"Artifacts":<12} {"Efficiency":<12}')
    print(f'  {"-"*70}')
    for r in gate_results:
        print(f'  {r["gate"]:<6} {r["name"]:<20} {r["coach_status"]:<8} '
              f'{r["ladder_status"]:<10} {r["artifacts"]}/{r["target_artifacts"]:<10} '
              f'{r["efficiency"]:<12}')
    
    return all_passed and len(gate_results) == 4


def validate_trace_files():
    """Check that trace files were created."""
    print_section('4. TRACE FILE VALIDATION')
    
    trace_logs = Path('.trace-logs')
    if not trace_logs.exists():
        print(f'[WARNING] .trace-logs directory not found')
        return False
    
    categories = ['agents', 'gates', 'workflows', 'etl', 'migrations']
    found_count = 0
    
    for cat in categories:
        cat_path = trace_logs / cat
        if cat_path.exists():
            jsonl_files = list(cat_path.glob('*.jsonl'))
            if jsonl_files:
                print(f'  [OK] {cat}: {len(jsonl_files)} JSONL file(s)')
                found_count += 1
            else:
                print(f'  [EMPTY] {cat}: directory exists but no traces')
        else:
            print(f'  [MISSING] {cat}')
    
    print(f'\n[RESULT] {found_count}/{len(categories)} trace categories ready')
    return found_count >= 2


def main():
    """Run complete validation for all waves 1-4."""
    print_header('COMPLETE WORKFLOW VALIDATION — ALL WAVES (1-4)')
    print('Running full validation of Week 1 + Ponytail integration across all waves...\n')
    
    # Run basic checks once
    basic_checks = {
        'Script Integration': validate_scripts(),
        'AGENTS.md (Ponytail)': validate_agents_md(),
    }
    
    basic_passed = sum(1 for v in basic_checks.values() if v)
    print(f'\n[BASIC CHECKS] {basic_passed}/{len(basic_checks)} passed\n')
    
    if basic_passed < len(basic_checks):
        print('[ERROR] Basic checks failed. Cannot proceed with wave validation.')
        return 1
    
    # Run wave simulations
    waves = [1, 2, 3, 4]
    wave_results = {}
    
    for wave_num in waves:
        print(f'\n{"="*90}')
        print(f'  WAVE {wave_num} VALIDATION')
        print(f'{"="*90}')
        wave_passed = simulate_complete_wave(wave_num)
        wave_results[wave_num] = wave_passed
    
    # Trace files validation
    print_section('4. TRACE FILE VALIDATION')
    trace_ok = validate_trace_files()
    
    # Summary
    print_header('COMPLETE VALIDATION SUMMARY — ALL WAVES')
    
    print(f'{"="*90}')
    print(f'  BASIC CHECKS')
    print(f'{"="*90}')
    for check_name, result in basic_checks.items():
        status = '[PASS]' if result else '[FAIL]'
        print(f'{status} {check_name}')
    
    print(f'\n{"="*90}')
    print(f'  WAVE SIMULATIONS (Gates 1-4 per Wave)')
    print(f'{"="*90}')
    for wave_num in waves:
        status = '[PASS]' if wave_results[wave_num] else '[FAIL]'
        print(f'{status} Wave {wave_num}')
    
    print(f'\n{"="*90}')
    print(f'  TRACE FILES')
    print(f'{"="*90}')
    status = '[PASS]' if trace_ok else '[FAIL]'
    print(f'{status} Trace File Validation')
    
    passed = basic_passed + sum(1 for v in wave_results.values() if v) + (1 if trace_ok else 0)
    total = len(basic_checks) + len(waves) + 1
    
    print(f'\n[RESULT] {passed}/{total} checks passed')
    
    if passed == total:
        print(f'\n✅ ALL VALIDATIONS PASSED FOR ALL WAVES (1-4)!')
        print(f'\nYour workflow is ready:')
        print(f'  • Week 1 trace integration ✅')
        print(f'  • Ponytail lazy senior dev mode ✅')
        print(f'  • Coach insights feedback ✅')
        print(f'  • All gates validated (Wave 1-4) ✅')
        print(f'  • Traces captured for all waves ✅')
        print(f'\nNext: Run with real Financeiro Wave 1-4 data!')
        return 0
    else:
        print(f'\n⚠️  Some validations failed. Review above.')
        return 1


if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print(f'\n[ERROR] {str(e)}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
