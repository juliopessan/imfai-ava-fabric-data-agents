# Reconciliation Evidence - WAVE-001

Date: 2026-03-21
Prepared by: downstream-executor
Target reviewer: reconciliation-agent

## Baseline Reconciliation Controls

- Row count parity checks between Bronze and Silver
- Aggregated metric parity checks between Silver and Gold
- Duplicate key scan on Silver business key
- Schema compatibility check by layer

## Baseline Results

- Bronze to Silver parity: PASS (pilot sample)
- Silver to Gold aggregate parity: PASS (pilot sample)
- Duplicate key scan: PASS
- Schema compatibility: PASS

## Outstanding Actions for Final Sign-off

1. Expand checks to full monthly batch windows.
2. Add checksum validation for high-risk tables.
3. Define tolerance bands for rounding-sensitive metrics.
