# 🚀 GO-LIVE CHECKLIST — Financeiro Reference Migration

**Production Deployment Readiness Verification**

---

## PRE-DEPLOYMENT FREEZE (T-7 days)

### Stakeholder Alignment

- [ ] **T-7:** Schedule pre-go-live review meeting with all stakeholders
  - Data Governance Board
  - Business Operations
  - IT Security
  - Finance (Cost Owner)
  - Escalation contacts (briefed)
  
- [ ] **T-7:** Distribute final deployment plan and rollback procedures
  - RTO: 4 hours
  - RPO: 15 minutes
  - Maintenance window: 20:00–06:00 BRT
  
- [ ] **T-7:** Obtain final stakeholder sign-off on go-live date

### Infrastructure Pre-Checks (T-7 to T-1)

- [ ] **T-5:** Verify Databricks cluster capacity
  - Worker count: 8 nodes (minimal SLA)
  - Driver: i3.2xlarge
  - Workers: i3.xlarge
  - Auto-scaling: Enabled (2–16 nodes)
  
- [ ] **T-5:** Confirm Azure networking (firewall, NSG, routes)
  - Cloudera → Databricks connectivity: Open
  - Application layer: Can reach Databricks SQL endpoints
  - DNS resolution: Both environments
  
- [ ] **T-5:** Validate storage accounts & Delta Lake paths
  - Databricks internal storage: 250 GB free
  - External Delta tables: 1.2 TB allocated
  - Backup storage (Azure): Healthy
  
- [ ] **T-3:** Perform final backup of source (Cloudera)
  - Full export timestamp: Record for audit
  - Verify backup integrity: 100%
  - Store backup metadata in versioning system
  
- [ ] **T-3:** Test rollback procedure end-to-end
  - Restore from backup: Success
  - Verify data consistency post-restore
  - Document rollback time: Actual vs. planned (target 4h)
  
- [ ] **T-1:** Verify all monitoring & alerting is active
  - Datadog/Azure Monitor: Connected
  - Data quality dashboards: Live
  - Escalation email/SMS: Tested

---

## DEPLOYMENT DAY (D+0)

### Pre-Deployment Window (18:00 BRT - 20:00 BRT)

#### Communication (18:00)

- [ ] **18:00:** Send "Deployment Starting" notification to all stakeholders
  - Incident channel (Teams, Slack, email)
  - Status page: Mark as "Maintenance"
  - Expected downtime: 4 hours (20:00–24:00 BRT)

- [ ] **18:15:** Confirm escalation team is on-call
  - Sev 1 lead: Available
  - Sev 2 lead: Available
  - Network/Infra team: Available

#### Final Validations (19:00)

- [ ] **19:00:** Freeze all application deployments
  - CI/CD pipelines: Paused (no new builds)
  - Database connections: Documented state
  - User sessions: Politely disconnected (if applicable)

- [ ] **19:15:** Final data reconciliation check
  - Cloudera → Target count match: 98.7% minimum
  - No truncations or corruptions detected
  - Quality rules pass: 100% critical rules

- [ ] **19:30:** Verify backup & rollback readiness
  - Backup timestamp: Recorded
  - Rollback scripts: Validated
  - Team briefed on abort procedure

- [ ] **19:45:** Final stakeholder confirmation
  - Go-ahead from Data Governance Board
  - Finance sign-off on costs
  - IT Security approval to proceed

#### Deployment Execution (20:00)

- [ ] **20:00:** DEPLOYMENT START — Begin migration window
  - Log deployment start timestamp (audit trail)
  - Notify all escalation contacts
  
- [ ] **20:05–22:00:** Data pipeline execution
  - Monitor ETL throughput: 100K–250K rows/min
  - Alert thresholds: If < 50K rows/min, escalate
  - Log all warnings/errors in real-time
  - **Checkpoint:** Record row count at 21:00 (midpoint)
  
- [ ] **22:00–23:00:** Data validation & reconciliation
  - Source vs. Target row counts: ≥ 98.7% match
  - Run data quality rules: 100% pass
  - Check referential integrity: All constraints satisfied
  - Review for NULL handling compliance
  
- [ ] **23:00–24:00:** Performance baseline & indexing
  - Build Databricks indexes on foreign keys
  - Run performance test queries: P95 < 3s
  - Collect baseline metrics (store for monitoring)
  - Enable query optimization

#### Post-Deployment Window (24:00+ BRT)

- [ ] **00:00:** DEPLOYMENT COMPLETE
  - Log final timestamp (audit trail)
  - Verify all 12.4M+ rows loaded successfully
  - Confirm zero data loss
  
- [ ] **00:15:** Smoke test from application layer
  - Connect application to Databricks SQL endpoints
  - Query critical tables: 5 test queries
  - Verify response times within SLA
  - **Result:** Record pass/fail
  
- [ ] **00:30:** Update status page
  - Status: "Deployment Successful"
  - Include metrics summary
  - Notify stakeholders of successful go-live

- [ ] **00:45:** Handoff to operational team
  - Daily monitoring schedule: Activated
  - Escalation contacts: Confirmed on-call
  - Incident response playbook: Briefed

---

## POST-DEPLOYMENT STABILIZATION (D+1 to D+7)

### Day 1 (D+1)

- [ ] **08:00:** Review overnight logs for any errors
  - Scan all error queues: Should be empty
  - Check data quality metrics: > 98% pass rate
  - Verify row counts haven't drifted
  - **Daily report:** Send to stakeholders

- [ ] **10:00:** First production validation run
  - Execute full reconciliation: 100% sample
  - Compare against Gate 3 baseline (98.7%)
  - Expected: No degradation

- [ ] **14:00:** Performance review with DBAs
  - Query latency (P50/P95): Within SLA?
  - Cluster CPU/memory utilization: Healthy?
  - Any slow queries: Identify & optimize
  - **Action:** Document optimizations

- [ ] **Close of Day:** Stakeholder update
  - Send daily digest email (Operations → Stakeholders)
  - Status: Green ✅
  - Metrics: Load time, row count, validation score

### Days 2–7 (D+2 to D+7)

#### Daily Tasks

- [ ] **Every morning (08:00):** Review 24-hour logs
  - Error count: Target = 0 critical
  - Data quality pass rate: Target ≥ 98%
  - Performance degradation: None detected
  
- [ ] **Every afternoon (16:00):** Weekly performance deep-dive
  - Query hotspots analysis
  - Cluster sizing review
  - Cost per GB processed
  - **Days 2, 4, 6:** Send metrics to Finance
  
- [ ] **Every evening (18:00):** Backup verification
  - Ensure daily backups are running
  - Test restore procedure (simulate once daily)
  - Backup storage: Sufficient?

#### Weekly Milestone Checklist

| Day | Milestone | Owner | Status |
|-----|-----------|-------|--------|
| D+1 | First production validation run | DBA | [ ] |
| D+1 | Stakeholder update: Day 1 summary | PM | [ ] |
| D+3 | Mid-week review: Any issues? | Architect | [ ] |
| D+5 | 5-day stability report | QA | [ ] |
| D+7 | Week 1 retrospective & metrics | Project Lead | [ ] |

---

## CRITICAL DECISION POINTS

### Abort Criteria (⛔ STOP & ROLLBACK IF ANY OCCUR)

| Scenario | Trigger | Action |
|----------|---------|--------|
| **Data loss** | Row count < 95% of expected | Activate rollback immediately |
| **Data corruption** | Quality rule pass rate < 90% | Abort deployment, investigate |
| **Performance failure** | Query P95 > 10s | Rollback, re-optimize offline |
| **Connectivity loss** | Cannot reach Cloudera/Databricks | Hold & troubleshoot (max 30 min) |
| **Security breach** | Unauthorized access detected | Isolate, escalate, rollback |

### Decision Authority

| Scenario | Authority | Escalation |
|----------|-----------|-----------|
| Data loss > 1% | DBA + Architect | CTO |
| Performance degradation > 50% | DBA | VP Engineering |
| Security incident | IT Security | CISO |
| Cost overrun > 20% | Finance | CFO |

---

## ROLLBACK PROCEDURE (If Needed)

### Rollback Decision (T+15 min)

- [ ] **Decision Gate:** Is the system recoverable within 4 hours?
  - YES → Proceed with automated rollback
  - NO → Manual intervention required (escalate to CTO)

### Automated Rollback (15–240 min)

- [ ] **Step 1 (15 min):** Stop all ETL pipelines
  - Pause Databricks jobs
  - Freeze application connections
  
- [ ] **Step 2 (30 min):** Restore from backup
  - Restore Cloudera to last known good state
  - Restore Databricks (if needed)
  - Verify backup integrity
  
- [ ] **Step 3 (60 min):** Run full reconciliation
  - Row count match: ≥ 98%
  - Data quality rules: 100% pass
  - Referential integrity: Confirmed
  
- [ ] **Step 4 (30 min):** Restore application connectivity
  - Redirect traffic back to Cloudera (if applicable)
  - Test critical application queries
  - Verify user authentication
  
- [ ] **Step 5 (30 min):** Post-rollback validation
  - Send "System Restored" notification to stakeholders
  - Document root cause
  - Schedule incident review (within 24 hours)

**Total Rollback Time: 4 hours (RTO = 4h, RPO = 15 min)**

---

## SIGN-OFF GATE

### Go-Live Authorization

| Person | Role | Sign-off | Date |
|--------|------|----------|------|
| [ ] | Project Lead | _____ | _____ |
| [ ] | Data Architect | _____ | _____ |
| [ ] | QA Lead | _____ | _____ |
| [ ] | Escalation (Sev 1) | _____ | _____ |
| [ ] | Business Sponsor | _____ | _____ |

### Pre-Deployment Meeting Notes

**Date:** _______________  
**Attendees:** _________________________________________________  
**Risks discussed:** ________________________________________  
**Final concerns:** __________________________________________  
**Go-ahead decision:** [ ] APPROVED [ ] DEFERRED [ ] REJECTED

---

## POST-GO-LIVE RETROSPECTIVE (D+14)

### Retrospective Meeting

- [ ] **Schedule:** 2 weeks after go-live (D+14)
- [ ] **Attendees:** Full deployment team + stakeholders
- [ ] **Agenda:**
  1. What went well?
  2. What challenges did we face?
  3. What would we do differently next time?
  4. Lessons learned → Update playbook

### Retrospective Output

- [ ] Document lessons learned (attach to wave status)
- [ ] Update runbooks based on actual vs. planned
- [ ] Record training needs for next wave
- [ ] Propose process improvements

---

## REFERENCE DOCUMENTS

- **Certificate of Production Readiness:** [certificate_production_ready.md](certificate_production_ready.md)
- **Escalation Contacts:** [escalation_contacts.md](escalation_contacts.md)
- **Wave Status:** [wave-status-consolidated.md](wave-status-consolidated.md)
- **Lessons Learned:** [lessons-learned-retrospective.md](lessons-learned-retrospective.md)

---

**Prepared by:** migration-coordinator (Orion)  
**Date:** 2026-06-16  
**Status:** ✅ Ready for review & sign-off
