#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper para rodar demo_week1_trace_integration.py com encoding correto.
"""

import sys
import os

# Set encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

# Add tools to path
sys.path.insert(0, str(os.path.join(os.path.dirname(__file__), '..', '..', 'tools', 'trace-integration')))

# Now import and run
if __name__ == '__main__':
    # Import directly
    from trace_writer import get_trace_writer
    from coach_insights import get_coach_insights
    import time
    
    def print_header(text):
        print(f'\n{"=" * 80}')
        print(f'  {text}')
        print(f'{"=" * 80}\n')
    
    def simulate_phase(phase_name, phase_num, wave):
        print(f"⏱️  Simulating {phase_name}...")
        
        writer = get_trace_writer()
        coach = get_coach_insights()
        
        time.sleep(0.5)
        
        phase_config = {
            1: {'agent_id': 'upstream-orchestrator', 'tokens_in': 150000, 'tokens_out': 75000, 'cost_usd': 0.45, 'artifacts': 7},
            2: {'agent_id': 'midstream-designer', 'tokens_in': 120000, 'tokens_out': 60000, 'cost_usd': 0.36, 'artifacts': 5},
            3: {'agent_id': 'downstream-deployer', 'tokens_in': 100000, 'tokens_out': 50000, 'cost_usd': 0.30, 'artifacts': 6},
            4: {'agent_id': 'consolidation-publisher', 'tokens_in': 50000, 'tokens_out': 25000, 'cost_usd': 0.15, 'artifacts': 11}
        }
        
        config = phase_config[phase_num]
        
        trace = writer.write_agent_execution(
            agent_id=config['agent_id'],
            wave=wave,
            gate=phase_num,
            operation_name=f'phase_{phase_num}_{phase_name.lower()}',
            duration_sec=1.0 + phase_num * 0.5,
            tokens_in=config['tokens_in'],
            tokens_out=config['tokens_out'],
            cost_usd=config['cost_usd'],
            artifacts_generated=config['artifacts'],
            status='success',
            user='demo-simulation'
        )
        
        print(f"✅ Trace ID: {trace['trace_id']}")
        
        # Coach analysis
        analysis = coach.analyze_execution(trace)
        coach.print_insights(analysis)
        
        # Ponytail ladder validation
        ladder_check = coach.validate_ponytail_ladder(trace, phase_num)
        print(f"\n[PONYTAIL] {ladder_check['message']}")
        if ladder_check['violations']:
            print(f"  Violations: {', '.join(ladder_check['violations'])}")
        if ladder_check['suggestions']:
            for i, sugg in enumerate(ladder_check['suggestions'], 1):
                print(f"  Suggestion {i}: {sugg}")
        
        return trace, analysis, ladder_check
    
    # Main
    print_header('🎬 WEEK 1 TRACE INTEGRATION DEMO')
    print('Executing all 4 phases with trace capture and coach analysis...\n')
    
    wave = 'financeiro-wave2-demo'
    
    phases = [
        ('UPSTREAM DISCOVERY', 1),
        ('MIDSTREAM DESIGN', 2),
        ('DOWNSTREAM DEPLOYMENT', 3),
        ('CONSOLIDATION', 4),
    ]
    
    traces = []
    for phase_name, phase_num in phases:
        print_header(f'PHASE {phase_num} - {phase_name}')
        trace, analysis, ladder = simulate_phase(phase_name, phase_num, wave)
        traces.append(trace)
    
    coach = get_coach_insights()
    print_header('📊 WAVE SUMMARY - ALL PHASES COMPLETE')
    coach.print_wave_summary(wave)
    
    print_header('✨ DEMO COMPLETE')
    
    total_duration = sum(t.get('duration_sec', 0) for t in traces)
    total_cost = sum(t.get('cost_usd', 0) for t in traces)
    total_artifacts = sum(t.get('artifacts_generated', 0) for t in traces)
    
    print('📈 AGGREGATED METRICS:\n')
    print(f'   Wave ...................... {wave}')
    print(f'   Phases Executed .......... {len(traces)}')
    print(f'   Total Duration ........... {total_duration:.2f}s')
    print(f'   Total Cost ............... ${total_cost:.2f}')
    print(f'   Total Artifacts .......... {total_artifacts}')
    print(f'\n📂 Traces saved to: .trace-logs/')
    print(f'\n✅ Week 1 Demo Complete!\n')
