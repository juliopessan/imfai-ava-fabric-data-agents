---
task: setup-monitoring
version: 1.0
elicit: true
description: Define and implement monitoring, alerting, and observability for data pipelines
---

# Setup Pipeline Monitoring & Observability

## Purpose
Implement comprehensive monitoring and observability for data pipelines including metrics collection, alerting rules, dashboards, and operational runbooks.

## Process

### Step 1: Gather Monitoring Requirements
ASK the user:

1. **Platform**: Azure Monitor, Datadog, Prometheus, CloudWatch?
2. **Critical Metrics**: What needs to be monitored?
3. **SLAs**: What are the service level agreements?
4. **Alert Recipients**: Who should receive alerts?
5. **Existing Tools**: Any current monitoring in place?

### Step 2: Define Key Metrics

**Pipeline Health Metrics:**
```markdown
## Metric Definitions

### Pipeline Execution Metrics
| Metric Name | Description | Type | Unit | Alert Threshold |
|-------------|-------------|------|------|-----------------|
| pipeline_duration_seconds | Total pipeline execution time | Gauge | seconds | > 7200 (2h) |
| pipeline_status | Success/Failure status | Gauge | enum | = FAILED |
| records_processed | Total records processed | Counter | count | < 1000 (too low) |
| records_rejected | Records failed validation | Counter | count | > 5% of total |
| data_freshness_hours | Hours since last successful load | Gauge | hours | > 24 |

### Data Quality Metrics
| Metric Name | Description | Type | Unit | Alert Threshold |
|-------------|-------------|------|------|-----------------|
| null_rate_percent | % of null values in critical columns | Gauge | percent | > 1% |
| duplicate_rate_percent | % of duplicate records | Gauge | percent | > 0.1% |
| schema_drift_detected | Schema changes detected | Gauge | boolean | = true |
| referential_integrity_failures | FK violations count | Counter | count | > 0 |

### Infrastructure Metrics
| Metric Name | Description | Type | Unit | Alert Threshold |
|-------------|-------------|------|------|-----------------|
| storage_used_gb | Data storage consumption | Gauge | GB | > 80% capacity |
| query_duration_p95 | 95th percentile query time | Gauge | seconds | > 60 |
| compute_utilization_percent | CPU/memory usage | Gauge | percent | > 90% |
| job_queue_depth | Pending jobs in queue | Gauge | count | > 10 |
```

### Step 3: Create Logging Framework

**Structured Logging Schema:**
```sql
-- Create pipeline audit/logging table
CREATE TABLE AUDIT.pipeline_execution_log (
    log_id BIGINT IDENTITY PRIMARY KEY,
    pipeline_name VARCHAR(100) NOT NULL,
    execution_id VARCHAR(50) NOT NULL,
    stage VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    duration_seconds INT,
    records_read BIGINT,
    records_written BIGINT,
    records_rejected BIGINT,
    error_message TEXT,
    error_stack_trace TEXT,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index for common queries
CREATE INDEX idx_pipeline_log_name_time 
ON AUDIT.pipeline_execution_log(pipeline_name, start_time DESC);

CREATE INDEX idx_pipeline_log_status 
ON AUDIT.pipeline_execution_log(status) WHERE status = 'FAILED';
```

**Python Logging Implementation:**
```python
import logging
import json
from datetime import datetime
from typing import Optional, Dict, Any

class PipelineLogger:
    """Structured logging for data pipelines"""
    
    def __init__(self, pipeline_name: str, execution_id: str):
        self.pipeline_name = pipeline_name
        self.execution_id = execution_id
        self.logger = logging.getLogger(f"pipeline.{pipeline_name}")
        
        # Configure JSON formatter
        handler = logging.StreamHandler()
        handler.setFormatter(self.JsonFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)
    
    class JsonFormatter(logging.Formatter):
        def format(self, record):
            log_obj = {
                "timestamp": datetime.utcnow().isoformat(),
                "level": record.levelname,
                "message": record.getMessage(),
                "pipeline": getattr(record, 'pipeline_name', None),
                "execution_id": getattr(record, 'execution_id', None),
                "stage": getattr(record, 'stage', None),
                "metrics": getattr(record, 'metrics', {}),
            }
            return json.dumps(log_obj)
    
    def log_stage_start(self, stage: str, metadata: Dict[str, Any] = None):
        """Log start of a pipeline stage"""
        self.logger.info(
            f"Stage {stage} started",
            extra={
                "pipeline_name": self.pipeline_name,
                "execution_id": self.execution_id,
                "stage": stage,
                "event": "STAGE_START",
                "metrics": metadata or {}
            }
        )
    
    def log_stage_complete(self, stage: str, records_processed: int, 
                           records_rejected: int = 0, duration_seconds: float = 0):
        """Log completion of a pipeline stage"""
        self.logger.info(
            f"Stage {stage} completed",
            extra={
                "pipeline_name": self.pipeline_name,
                "execution_id": self.execution_id,
                "stage": stage,
                "event": "STAGE_COMPLETE",
                "metrics": {
                    "records_processed": records_processed,
                    "records_rejected": records_rejected,
                    "duration_seconds": duration_seconds,
                    "reject_rate": round(records_rejected / max(records_processed, 1) * 100, 2)
                }
            }
        )
    
    def log_error(self, stage: str, error: Exception, context: Dict = None):
        """Log pipeline error"""
        self.logger.error(
            f"Stage {stage} failed: {str(error)}",
            extra={
                "pipeline_name": self.pipeline_name,
                "execution_id": self.execution_id,
                "stage": stage,
                "event": "STAGE_ERROR",
                "error_type": type(error).__name__,
                "error_message": str(error),
                "context": context or {}
            },
            exc_info=True
        )
    
    def log_data_quality_metric(self, table: str, metric: str, value: float, 
                                 threshold: float, status: str):
        """Log data quality check result"""
        self.logger.info(
            f"Data quality check: {metric}",
            extra={
                "pipeline_name": self.pipeline_name,
                "execution_id": self.execution_id,
                "event": "DATA_QUALITY_CHECK",
                "metrics": {
                    "table": table,
                    "metric_name": metric,
                    "metric_value": value,
                    "threshold": threshold,
                    "status": status
                }
            }
        )

# Usage example
logger = PipelineLogger("nyc_taxi_pipeline", "exec_20260126_001")
logger.log_stage_start("SILVER_TRANSFORM", {"source_table": "LND.trip_data"})
logger.log_stage_complete("SILVER_TRANSFORM", records_processed=785000, records_rejected=1250, duration_seconds=1847)
```

### Step 4: Define Alerting Rules

**Alert Configuration:**
```yaml
# alerts.yaml - Pipeline Alert Definitions

alerts:
  - name: pipeline_failure
    description: "Pipeline execution failed"
    severity: critical
    condition: pipeline_status == 'FAILED'
    notification:
      channels: [pagerduty, slack, email]
      message: |
        🚨 CRITICAL: Pipeline {{pipeline_name}} failed
        Execution ID: {{execution_id}}
        Stage: {{failed_stage}}
        Error: {{error_message}}
        Time: {{timestamp}}
    runbook: "runbooks/pipeline-failure.md"

  - name: high_reject_rate
    description: "Data rejection rate exceeds threshold"
    severity: warning
    condition: (records_rejected / records_processed) > 0.05
    notification:
      channels: [slack, email]
      message: |
        ⚠️ WARNING: High reject rate in {{pipeline_name}}
        Reject Rate: {{reject_rate}}%
        Records Rejected: {{records_rejected}}
        Stage: {{stage}}
    runbook: "runbooks/high-reject-rate.md"

  - name: data_freshness_breach
    description: "Data not refreshed within SLA"
    severity: critical
    condition: hours_since_last_refresh > 24
    notification:
      channels: [pagerduty, slack]
      message: |
        🚨 CRITICAL: Data freshness SLA breach
        Table: {{table_name}}
        Last Refresh: {{last_refresh_time}}
        Hours Stale: {{hours_since_last_refresh}}
    runbook: "runbooks/data-freshness.md"

  - name: schema_drift
    description: "Schema change detected in source"
    severity: warning
    condition: schema_drift_detected == true
    notification:
      channels: [slack, email]
      message: |
        ⚠️ WARNING: Schema drift detected
        Table: {{table_name}}
        Changes: {{schema_changes}}
        Action Required: Review and update pipeline
    runbook: "runbooks/schema-drift.md"

  - name: slow_query
    description: "Query execution time exceeds threshold"
    severity: warning
    condition: query_duration_seconds > 300
    notification:
      channels: [slack]
      message: |
        ⚠️ WARNING: Slow query detected
        Query: {{query_name}}
        Duration: {{query_duration_seconds}}s
        Table: {{table_name}}
    runbook: "runbooks/slow-queries.md"
```

### Step 5: Create Monitoring Dashboard

**Dashboard Specification:**
```markdown
## Pipeline Monitoring Dashboard

### Section 1: Executive Summary
┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐
│  Pipeline Status │  Data Freshness │  Quality Score  │   Alert Count   │
│     ✅ OK        │    2.5 hours    │     98.7%       │      0          │
└─────────────────┴─────────────────┴─────────────────┴─────────────────┘

### Section 2: Pipeline Execution Timeline
┌─────────────────────────────────────────────────────────────────────────┐
│  [Timeline chart showing last 7 days of pipeline executions]            │
│                                                                         │
│  ✅ ✅ ✅ ✅ ✅ ✅ ⚠️                                                    │
│  Mon Tue Wed Thu Fri Sat Sun                                           │
└─────────────────────────────────────────────────────────────────────────┘

### Section 3: Data Volume Trends
┌─────────────────────────────────────────────────────────────────────────┐
│  [Line chart: Records processed per day]                                │
│                                                                         │
│  Records: 785,234 | Rejected: 1,247 (0.16%) | Duration: 1h 45m         │
└─────────────────────────────────────────────────────────────────────────┘

### Section 4: Data Quality Metrics
┌───────────────────────┬───────────────────────┬───────────────────────┐
│   Completeness        │   Validity            │   Consistency         │
│   ████████░░ 98.5%    │   █████████░ 99.2%    │   █████████░ 99.8%    │
└───────────────────────┴───────────────────────┴───────────────────────┘

### Section 5: Table-Level Health
| Table | Rows | Last Update | Quality | Status |
|-------|------|-------------|---------|--------|
| GOLD.trip_enriched | 780,000 | 2h ago | 98.7% | ✅ |
| GOLD.daily_trip_agg | 90 | 2h ago | 100% | ✅ |
| SILVER.trip_data | 785,000 | 2h ago | 99.2% | ✅ |

### Section 6: Recent Alerts
| Time | Severity | Alert | Status |
|------|----------|-------|--------|
| 06:30 | ⚠️ Warning | High latency detected | Resolved |
| Yesterday | ✅ Info | Schema change detected | Acknowledged |
```

### Step 6: Create SQL Monitoring Queries

**Operational Monitoring Queries:**
```sql
-- ============================================
-- Pipeline Monitoring Queries
-- ============================================

-- 1. Pipeline execution summary (last 7 days)
CREATE OR REPLACE VIEW MONITOR.pipeline_summary AS
SELECT 
    pipeline_name,
    DATE(start_time) as execution_date,
    COUNT(*) as total_executions,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) as failed,
    ROUND(100.0 * SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END) / COUNT(*), 2) as success_rate,
    AVG(duration_seconds) as avg_duration_seconds,
    SUM(records_written) as total_records
FROM AUDIT.pipeline_execution_log
WHERE start_time >= CURRENT_DATE - INTERVAL '7 days'
GROUP BY pipeline_name, DATE(start_time)
ORDER BY execution_date DESC;

-- 2. Data freshness check
CREATE OR REPLACE VIEW MONITOR.data_freshness AS
SELECT 
    table_schema || '.' || table_name as table_name,
    MAX(load_timestamp) as last_refresh,
    EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(load_timestamp))) / 3600 as hours_since_refresh,
    CASE 
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(load_timestamp))) / 3600 > 24 
        THEN '🔴 STALE'
        WHEN EXTRACT(EPOCH FROM (CURRENT_TIMESTAMP - MAX(load_timestamp))) / 3600 > 12 
        THEN '🟡 WARNING'
        ELSE '🟢 FRESH'
    END as freshness_status
FROM information_schema.tables t
JOIN (
    SELECT 'SILVER' as schema_name, 'trip_data' as table_name, 
           MAX(processed_timestamp) as load_timestamp FROM SILVER.trip_data
    UNION ALL
    SELECT 'GOLD', 'trip_enriched', MAX(created_timestamp) FROM GOLD.trip_enriched
) loads ON t.table_schema = loads.schema_name AND t.table_name = loads.table_name
GROUP BY table_schema, table_name;

-- 3. Data quality summary
CREATE OR REPLACE VIEW MONITOR.quality_summary AS
SELECT 
    'SILVER.trip_data' as table_name,
    COUNT(*) as total_records,
    SUM(CASE WHEN quality_flag = 'VALID' THEN 1 ELSE 0 END) as valid_records,
    SUM(CASE WHEN quality_flag = 'INVALID' THEN 1 ELSE 0 END) as invalid_records,
    ROUND(100.0 * SUM(CASE WHEN quality_flag = 'VALID' THEN 1 ELSE 0 END) / COUNT(*), 2) as quality_score,
    CASE 
        WHEN 100.0 * SUM(CASE WHEN quality_flag = 'VALID' THEN 1 ELSE 0 END) / COUNT(*) >= 99 
        THEN '🟢 EXCELLENT'
        WHEN 100.0 * SUM(CASE WHEN quality_flag = 'VALID' THEN 1 ELSE 0 END) / COUNT(*) >= 95 
        THEN '🟡 ACCEPTABLE'
        ELSE '🔴 NEEDS ATTENTION'
    END as quality_status
FROM SILVER.trip_data;

-- 4. Recent failures investigation
CREATE OR REPLACE VIEW MONITOR.recent_failures AS
SELECT 
    execution_id,
    pipeline_name,
    stage,
    start_time,
    error_message,
    LEFT(error_stack_trace, 500) as stack_trace_preview
FROM AUDIT.pipeline_execution_log
WHERE status = 'FAILED'
  AND start_time >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY start_time DESC
LIMIT 20;

-- 5. Volume anomaly detection
CREATE OR REPLACE VIEW MONITOR.volume_anomalies AS
WITH daily_volumes AS (
    SELECT 
        DATE(start_time) as exec_date,
        SUM(records_written) as daily_records,
        AVG(SUM(records_written)) OVER (ORDER BY DATE(start_time) ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) as rolling_avg
    FROM AUDIT.pipeline_execution_log
    WHERE status = 'SUCCESS'
    GROUP BY DATE(start_time)
)
SELECT 
    exec_date,
    daily_records,
    rolling_avg,
    ROUND((daily_records - rolling_avg) / NULLIF(rolling_avg, 0) * 100, 2) as deviation_percent,
    CASE 
        WHEN ABS((daily_records - rolling_avg) / NULLIF(rolling_avg, 0)) > 0.20 
        THEN '🔴 ANOMALY'
        WHEN ABS((daily_records - rolling_avg) / NULLIF(rolling_avg, 0)) > 0.10 
        THEN '🟡 WARNING'
        ELSE '🟢 NORMAL'
    END as status
FROM daily_volumes
WHERE exec_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY exec_date DESC;
```

### Step 7: Create Operational Runbooks

**Runbook Template:**
```markdown
# Runbook: Pipeline Failure Recovery

## Alert Trigger
- **Alert Name**: pipeline_failure
- **Severity**: Critical
- **Condition**: Pipeline status = FAILED

## Immediate Actions (0-5 minutes)

### Step 1: Acknowledge Alert
```bash
# Mark alert as acknowledged in monitoring system
curl -X POST "https://monitoring.example.com/api/alerts/{alert_id}/ack"
```

### Step 2: Identify Failure Point
```sql
-- Check latest execution log
SELECT * FROM AUDIT.pipeline_execution_log
WHERE execution_id = '{execution_id}'
ORDER BY start_time DESC;
```

### Step 3: Check Error Details
```sql
-- Get error message and stack trace
SELECT 
    stage,
    error_message,
    error_stack_trace,
    metadata
FROM AUDIT.pipeline_execution_log
WHERE execution_id = '{execution_id}'
  AND status = 'FAILED';
```

## Common Failure Scenarios

### Scenario A: Source File Missing
**Symptoms**: `FileNotFoundException` in landing stage
**Resolution**:
1. Check if source files arrived
2. Contact upstream team if files are late
3. If files exist, check file permissions
4. Manually trigger file refresh if needed

### Scenario B: Data Type Conversion Error
**Symptoms**: `CastException` in silver stage
**Resolution**:
1. Identify problematic records
2. Check for schema drift in source
3. Update transformation logic if needed
4. Re-run failed stage after fix

### Scenario C: Out of Memory
**Symptoms**: `OutOfMemoryError` or job killed
**Resolution**:
1. Check data volume vs. normal
2. Increase cluster resources temporarily
3. Review query for optimization opportunities
4. Consider partitioning large tables

## Recovery Steps

### Option 1: Retry Pipeline
```bash
# Retry full pipeline
python run_pipeline.py --execution-id {new_execution_id} --mode full

# Retry from failed stage
python run_pipeline.py --execution-id {new_execution_id} --start-stage {failed_stage}
```

### Option 2: Manual Data Load
```sql
-- If automated pipeline cannot be fixed quickly
-- Load data manually with validation
BEGIN TRANSACTION;
-- Manual load steps here
COMMIT;
```

## Escalation Path
| Time | Action | Contact |
|------|--------|---------|
| 0-15 min | On-call engineer investigates | DataOps Team |
| 15-30 min | Escalate to senior engineer | Senior Data Engineer |
| 30-60 min | Escalate to team lead | Data Engineering Lead |
| >1 hour | Escalate to management | Engineering Manager |

## Post-Incident
- [ ] Root cause identified
- [ ] Fix implemented and tested
- [ ] Incident report created
- [ ] Monitoring improved if needed
```

## Output

Generate the following artifacts:

1. **Metric Definitions** (YAML/Markdown)
   - All metrics with thresholds
   - Alert rules

2. **Logging Framework** (SQL + Python)
   - Audit table DDL
   - Logging classes

3. **Dashboard Specification** (Markdown)
   - Panel definitions
   - Query specifications

4. **Monitoring Queries** (SQL)
   - Health check views
   - Anomaly detection

5. **Runbooks** (Markdown)
   - Incident response procedures
   - Recovery steps

## Completion Criteria

Monitoring setup is complete when:
- ✅ All critical metrics defined
- ✅ Alert thresholds configured
- ✅ Logging framework implemented
- ✅ Dashboard specifications created
- ✅ Monitoring queries tested
- ✅ Runbooks documented
- ✅ Escalation paths defined
