# 🎯 Best Practices

> Recomendações de segurança, performance, observabilidade e operação.

---

## 📑 Índice

1. [Segurança](#segurança)
2. [Performance](#performance)
3. [Observabilidade](#observabilidade)
4. [Operação](#operação)
5. [Compliance](#compliance)

---

## Segurança

### Princípios Fundamentais

```
Zero Trust:
├─ Never trust, always verify
├─ Least privilege access
├─ Encrypt everything (in transit + at rest)
└─ Audit all actions

Defense in Depth:
├─ Network layer (NSG, firewall, private link)
├─ Identity layer (Managed Identity, Entra)
├─ Data layer (encryption, masking)
└─ Application layer (validation, rate limiting)
```

### 1. Credenciais & Secrets

✅ **FAZER:**
- Store all secrets in Azure Key Vault
- Use Managed Identity (no passwords)
- Rotate credentials every 30-90 days
- Enable Key Vault logging
- Use short-lived tokens (TTL ≤ 1h)

❌ **NÃO FAZER:**
- Hardcode credentials in code/config
- Store in environment variables
- Share credentials across teams
- Use same credential for multiple purposes

**Implementação:**
```csharp
// ✅ Good: Use Managed Identity
var credential = new DefaultAzureCredential();
var client = new BlobContainerClient(
    new Uri("https://storage.azure.com/container"),
    credential
);

// ❌ Bad: Hardcoded connection string
var client = new BlobContainerClient(
    new Uri("https://storage.azure.com/container"),
    new StorageSharedKeyCredential("account", "hardcodedkey")
);
```

### 2. Network Security

**NSG Rules (Least Privilege):**
```yaml
Inbound:
  ├─ Allow: Consultoria IPs (10.100.0.0/8) → Port 1433 (SQL)
  ├─ Allow: Consultoria IPs (10.100.0.0/8) → Port 10000 (Hive)
  ├─ Deny: Everything else
  └─ Audit: All denied attempts

Outbound:
  ├─ Allow: 443 (HTTPS only)
  ├─ Allow: 10.0.0.0/8 (Private IPs)
  ├─ Deny: 80 (HTTP, force HTTPS)
  └─ Deny: Everything else
```

**VNet Isolation:**
```
├─ Separate subnets per function
│  ├─ Agents (10.100.1.0/24)
│  ├─ Storage (10.100.2.0/24)
│  └─ Monitoring (10.100.3.0/24)
├─ Service endpoints for Azure services
├─ Private endpoints for storage/databases
└─ No direct Internet access (NAT gateway for egress)
```

### 3. Data Protection

**Encryption:**
```yaml
In Transit:
  ├─ TLS 1.2+ (never 1.0 or 1.1)
  ├─ Certificate pinning (for sensitive endpoints)
  ├─ mTLS for service-to-service
  └─ VPN/Private Link (no public Internet)

At Rest:
  ├─ ADLS Gen2: SMB encryption (automatic)
  ├─ Key Vault: AES-256
  ├─ Cosmos DB: AWS KMS (transparent)
  ├─ Databases: TDE (Transparent Data Encryption)
  └─ Backups: Same encryption as primary
```

**Data Masking:**
```sql
-- Mask PII in staging zone
ALTER TABLE staging.customers
ADD MASKED WITH (FUNCTION = 'email()') FOR email_address
ADD MASKED WITH (FUNCTION = 'partial(2,"XXX",2)') FOR ssn;
```

### 4. IAM & RBAC

**Service Principal Roles (Least Privilege):**

| Service | Role | Scope | Purpose |
|---------|------|-------|---------|
| **Connector Agent** | Read | Client DB | Extract data |
| **Landing Zone** | Storage Blob Data Contributor | `/landing/{tenant}/` | Upload |
| **Foundry Agents** | Storage Blob Data Reader/Contributor | `/landing/{tenant}/` | Process |
| **Monitoring** | Reader | Subscription | View logs |

**Avoid:**
- ❌ Owner role (too broad)
- ❌ Shared service principals
- ❌ Permanent role assignments (use PIM)

### 5. Audit & Compliance

**Enable Logging:**
```powershell
# Key Vault audit
Set-AzKeyVaultAccessPolicy -VaultName consultoria-vault `
  -EnabledForDisableBypolicyAudit

# ADLS Gen2 audit
Set-AzStorageAccount -ResourceGroupName consultoria-prod `
  -Name consultoriaadls `
  -EnableDetailedLogging

# Azure Monitor
New-AzActionGroupReceiver -Name SecurityTeam `
  -EmailReceiver -EmailAddress security@consultoria.example
```

**Compliance Checklist:**
```
[ ] All secrets encrypted (Key Vault)
[ ] Network isolated (VNet, NSG, Private Link)
[ ] Data encrypted (in transit + at rest)
[ ] Access logged (audit trail)
[ ] Credentials rotated (< 90 days)
[ ] Vulnerabilities scanned (Defender)
[ ] Compliance checked (Azure Policy)
```

---

## Performance

### 1. Throughput Optimization

**Benchmark Targets:**
- ✅ Hive extraction: > 1M rows/min (100 MB/s)
- ✅ SQL extraction: > 500K rows/min (50 MB/s)
- ✅ Dashboard load: < 2 seconds
- ✅ API response: < 200ms (p95)

**Techniques:**
```
├─ Parallel connections (5-10 per source)
├─ Batch size tuning (100K-1M rows per batch)
├─ Connection pooling (keep-alive)
├─ Compression (gzip, level 6)
├─ Caching (CDN for static assets)
└─ Indexes (create on join columns)
```

### 2. Memory Management

**Container Resource Limits:**
```yaml
requests:
  cpu: 1      # minimum guaranteed
  memory: 2Gi
limits:
  cpu: 2      # maximum allowed
  memory: 4Gi
```

**Avoid Memory Leaks:**
```python
# ❌ Bad: Accumulates rows in memory
all_rows = []
for batch in cursor.fetchall():
    all_rows.append(batch)  # Memory grows unbounded

# ✅ Good: Stream batches
for batch in cursor.fetch_batch(size=100000):
    process(batch)  # Fixed memory footprint
    batch = None    # Garbage collect immediately
```

### 3. Database Query Optimization

**Query Best Practices:**
```sql
-- ❌ Bad: Full table scan + joins
SELECT * FROM large_table t1
JOIN another_table t2 ON t1.id = t2.id

-- ✅ Good: Indexed, filtered, projected
SELECT t1.id, t1.name, t2.status
FROM large_table t1
INNER JOIN another_table t2 ON t1.id = t2.id
WHERE t1.year = 2026
AND t2.status = 'ACTIVE'
```

**Parallel Execution:**
```python
# Execute queries in parallel (10 concurrent)
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [
        executor.submit(extract_table, table)
        for table in source_tables
    ]
    results = [f.result() for f in concurrent.futures.as_completed(futures)]
```

### 4. API Rate Limiting

**Implement Backoff:**
```python
# Exponential backoff with jitter
import time
import random

max_retries = 5
for attempt in range(max_retries):
    try:
        response = api.request(...)
        break
    except RateLimitExceeded:
        wait_time = (2 ** attempt) + random.uniform(0, 1)
        time.sleep(wait_time)
```

---

## Observabilidade

### 1. Logging

**Structured Logging:**
```json
{
  "timestamp": "2026-06-12T14:30:45.123Z",
  "level": "INFO",
  "service": "pull-agent",
  "job_id": "job-20260612-001",
  "connector_id": "c-clientebanco-001",
  "event": "extraction_started",
  "metadata": {
    "source": "cloudera_main",
    "table_count": 127,
    "estimated_rows": 52487234
  }
}
```

**Log Levels:**
```
CRITICAL: System down, immediate action required
ERROR:    Function failed, requires investigation
WARNING:  Anomaly detected, monitor
INFO:     Key milestones, normal operation
DEBUG:    Detailed traces (dev only)
```

**Log to Azure Monitor:**
```csharp
var logger = new LogAnalyticsLogger("consultoria-workspace");
logger.Log(new {
    Level = "INFO",
    JobId = "job-12345",
    Event = "extraction_complete",
    Metrics = new {
        RowsProcessed = 52487234,
        DurationSeconds = 480,
        ThroughputMbSec = 45.2
    }
});
```

### 2. Metrics & Tracing

**Key Metrics to Track:**
```
Job Metrics:
├─ Jobs queued / running / completed / failed
├─ Average job duration (by stage)
├─ Error rate (% failed jobs)
├─ Data throughput (rows/min, MB/sec)
└─ Cost per job

Resource Metrics:
├─ CPU utilization (%, p99)
├─ Memory usage (MB, p99)
├─ Disk I/O (MB/sec)
├─ Network bandwidth (Mbps)
└─ Database connection pool (% used)

Business Metrics:
├─ ROI % (savings vs. baseline)
├─ Time-to-value (days to production)
├─ User adoption rate
└─ Customer satisfaction (NPS)
```

**Distributed Tracing:**
```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("extract_hive") as span:
    span.set_attribute("table_count", 127)
    span.set_attribute("estimated_rows", 52487234)
    
    # Code inside span
    rows = extract_hive_tables()
    
    span.set_attribute("actual_rows", len(rows))
```

### 3. Alerts & Escalation

**Alert Rules:**

| Condition | Severity | Action |
|-----------|----------|--------|
| Job running > 1h | P2 | Email ops@consultoria.example |
| Error rate > 5% | P1 | Slack + PagerDuty |
| Cost > budget | P2 | Email finance@consultoria.example |
| API response > 1s (p99) | P3 | Log investigation |

**Implement:**
```yaml
# Azure Monitor alert rule
alerts:
  - name: JobTimeout
    metric: job_duration_seconds
    condition: value > 3600
    threshold_count: 1
    evaluation_frequency: 5m
    action_group: emergency_response
    severity: P1
```

### 4. Dashboards & Reports

**Create in Azure Monitor:**
```
├─ Executive Dashboard (1-page, daily)
│  ├─ ROI % (vs. baseline)
│  ├─ Jobs completed this week
│  └─ Cost vs. budget
├─ Operations Dashboard (real-time)
│  ├─ Running jobs (%)
│  ├─ Error rate (%)
│  └─ Throughput (rows/min)
└─ Technical Dashboard (hourly)
   ├─ Agent resource utilization
   ├─ Database query latency
   └─ Network bandwidth
```

---

## Operação

### 1. Deployment Checklist

```
Pre-Deployment:
[ ] Code review passed
[ ] Unit tests passing
[ ] Integration tests passing
[ ] Security scan passed (no CVEs)
[ ] Performance baseline established
[ ] Documentation updated
[ ] Rollback plan prepared

Deployment:
[ ] Blue-green setup ready
[ ] Database migrations tested (if any)
[ ] Secrets imported to Key Vault
[ ] RBAC roles assigned
[ ] Monitoring alerts configured

Post-Deployment:
[ ] Health checks passing
[ ] Metrics flowing to dashboards
[ ] No elevated error rates
[ ] Team notified
[ ] 30-minute active monitoring
```

### 2. Incident Response

**Severity Levels:**
```
P1 (Critical): System down, customer impact
└─ Response: < 15 minutes, escalate immediately

P2 (High): Degraded performance, workaround exists
└─ Response: < 1 hour, assign senior engineer

P3 (Medium): Minor issue, low impact
└─ Response: < 24 hours, schedule for sprint

P4 (Low): Enhancement, future release
└─ Response: Backlog, no SLA
```

**Runbook Template:**
```
Service: Pull Agent
Issue: Authentication failures

Symptoms:
├─ Error logs show "Token request failed"
├─ No data flowing to staging zone
└─ Job status stuck at "pending"

Root Cause Analysis:
├─ Check credential broker health
├─ Verify SP certificate not expired
├─ Confirm Entra ID token endpoint reachable

Resolution:
├─ Manual: Rotate SP certificate
├─ Automatic: Restart credential broker pod
├─ Escalate: Contact Entra ID team if persists

Prevention:
├─ Monitor certificate expiry (30 days before)
├─ Test credential refresh weekly
└─ Add automated certificate rotation
```

### 3. Backup & Disaster Recovery

**Backup Strategy:**
```
ADLS Gen2 (Landing Zone):
├─ Snapshot: Daily (7 day retention)
├─ Geo-replication: GRS (automatic failover)
└─ Restore time: < 1 hour

Cosmos DB (Metadata):
├─ Backup: Continuous (35 day retention)
├─ Region: 3 replicas (strong consistency)
└─ RTO: < 15 minutes

Key Vault:
├─ Backup: Automated daily
├─ Retention: 90 days
└─ Restore: < 30 minutes
```

**Recovery Tests:**
```
Monthly:
├─ Restore from snapshot (test environment)
├─ Verify data integrity (row count, hash)
├─ Test failover to secondary region
└─ Document results
```

### 4. Capacity Planning

**Monitor & Forecast:**
```
Current Usage:
├─ Data size: 2.3 TB/month
├─ Transactions: 10M jobs/month
├─ Storage growth: 15% MoM
└─ Cost: $45K/month

Forecast (12 months):
├─ Data size: ~55 TB (if growth continues)
├─ Storage upgrade: Needed in Q3 2026
├─ Compute upgrade: Needed in Q4 2026
└─ Estimated cost: ~$150K/month

Actions:
├─ Order hardware 60 days before upgrade
├─ Test scaling in dev environment
├─ Plan maintenance window
└─ Communicate to stakeholders
```

---

## Compliance

### 1. Data Governance

**Classification:**
```
Data Class:
├─ Public: No PII, no restrictions
├─ Internal: Company confidential
├─ Confidential: PII or sensitive
└─ Restricted: Highly sensitive (financial, legal)

Handling:
├─ Public: No encryption required
├─ Internal: Encrypted in transit
├─ Confidential: Encrypted in transit + at rest
└─ Restricted: Encrypted + access logs + audit
```

### 2. GDPR Compliance

**Data Subject Rights:**
```
Right to Access:
└─ Implement API to retrieve all data for a customer

Right to Deletion:
└─ Cascade delete across all systems (3-day SLA)

Right to Portability:
└─ Export to standard format (JSON, CSV)

Data Minimization:
├─ Only collect necessary data
├─ Retention: 7 years max
└─ Auto-delete after expiry
```

### 3. SOC 2 Compliance

**Key Controls:**
```
Security:
├─ Network isolation (VNet, NSG)
├─ Encryption (in transit + at rest)
├─ Access control (RBAC, Managed Identity)
└─ Incident response (runbooks, SLA)

Availability:
├─ 99.95% SLA
├─ Multi-region failover
├─ Automated health checks
└─ Incident tracking

Confidentiality:
├─ Data masking (PII)
├─ Audit logs (encrypted)
├─ Access restrictions (least privilege)
└─ Data retention policies

Integrity:
├─ Checksums (MD5/SHA256)
├─ Transactional consistency
├─ Change tracking
└─ Backup verification
```

---

## Checklist de Implementação

```
Security ✅
[ ] Secrets in Key Vault
[ ] Managed Identity enabled
[ ] Network NSG rules configured
[ ] Encryption enabled (in transit + at rest)
[ ] Audit logging active

Performance ✅
[ ] Throughput > 100 MB/s
[ ] API response < 200ms (p95)
[ ] Dashboard load < 2s
[ ] Memory usage < 80%

Observability ✅
[ ] Structured logging enabled
[ ] Metrics flowing to Monitor
[ ] Alerts configured (P1, P2, P3)
[ ] Dashboards created
[ ] Tracing implemented

Operations ✅
[ ] Deployment pipeline tested
[ ] Rollback plan documented
[ ] Runbooks created
[ ] Team trained
[ ] DR tested
```

---

**Última atualização:** 2026-06-12 | **Status:** ✅ v1.0 (Recommended)
