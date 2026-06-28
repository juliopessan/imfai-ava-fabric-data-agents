#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple trace test
"""

from trace_writer import get_trace_writer

writer = get_trace_writer()

# Try a simple write
trace = writer.write_agent_execution(
    agent_id='test',
    wave='test-wave',
    gate=1,
    operation_name='test_op',
    duration_sec=1.0,
    tokens_in=100,
    tokens_out=50,
    cost_usd=0.01,
    artifacts_generated=1,
    status='success',
    user='test'
)

print("Trace result:", trace)
if trace:
    print("[OK] Success! Trace ID:", trace['trace_id'])
else:
    print("[FAIL] Failed - trace is None")
