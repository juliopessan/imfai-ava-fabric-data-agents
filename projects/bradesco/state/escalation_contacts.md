# 📞 ESCALATION CONTACTS — Bradesco Einstein Migration

**Production Support Hierarchy & On-Call Schedule**

---

## SEVERITY MATRIX & RESPONSE TIMES

| Severity | Definition | Response Time | Resolution Target | Escalation Path |
|----------|-----------|---|---|---|
| **🔴 SEV 1** | Critical system down, data loss, security breach | **15 minutes** | 4 hours | L1 → L2 → L3 → VP Eng |
| **🟠 SEV 2** | Major feature broken, significant performance degradation | **1 hour** | 8 hours | L1 → L2 → Architect |
| **🟡 SEV 3** | Minor issues, workaround available, low user impact | **4 hours** | 24 hours | L1 → L2 (if needed) |
| **🟢 SEV 4** | Requests, documentation, non-critical questions | **24 hours** | 5 business days | L1 only |

---

## PRIMARY SUPPORT TEAM (L1 — Frontline)

### Primary On-Call Lead (24/7)

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Data Engineer** | julio.cesar.d.pessan | julio.cesar.d.pessan@avanade.com | +55 11 98765-4321 | 24/7 on-call |

**Backup (if primary unavailable):**
| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Data Engineer** | data-engineer-backup@avanade.com | data-engineer-backup@avanade.com | +55 11 98765-4322 | 24/7 on-call |

**Escalation if both unavailable:**
- Contact: SOC (Security Operations Center) — +55 11 4004-4000 ext. 5555
- Email: soc-alerts@avanade.com
- Ticket system: DevOps Alert Channel (Microsoft Teams)

---

## SECONDARY SUPPORT TEAM (L2 — Escalation)

### Data Architecture Lead

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Principal Data Architect** | data-architect@avanade.example | data-architect@avanade.example | +55 11 98765-4330 | Business hours + on-call (Sev 1) |

### Database Administration Lead

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Senior DBA** | dba-lead@avanade.example | dba-lead@avanade.example | +55 11 98765-4331 | Business hours + on-call (Sev 1) |

### Data Quality Lead

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **QA Engineer** | qa-lead@avanade.example | qa-lead@avanade.example | +55 11 98765-4332 | Business hours + on-call (Sev 1/2) |

### Databricks Solution Architect

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Databricks CSA** | databricks-csa@avanade.example | databricks-csa@avanade.example | +55 11 98765-4333 | Business hours (email), 24h Sev 1 |

---

## TERTIARY SUPPORT TEAM (L3 — Expert Resources)

### Infrastructure & Cloud

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Azure Cloud Architect** | azure-architect@avanade.example | azure-architect@avanade.example | +55 11 98765-4340 | Business hours + on-call (Sev 1) |
| **Network Engineer** | network-team@avanade.example | network-team@avanade.example | +55 11 98765-4341 | Business hours + on-call (Sev 1) |

### Security & Compliance

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Security Officer** | security-officer@avanade.example | security-officer@avanade.example | +55 11 98765-4350 | Business hours + on-call (Sec breach) |
| **Compliance Lead** | compliance@avanade.example | compliance@avanade.example | +55 11 98765-4351 | Business hours |

### Finance & Cost Management

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Finance Lead** | finance-lead@avanade.example | finance-lead@avanade.example | +55 11 98765-4360 | Business hours (cost overruns) |
| **FinOps Engineer** | finops@avanade.example | finops@avanade.example | +55 11 98765-4361 | Business hours |

---

## EXECUTIVE ESCALATION (L4 — Management)

### Project Sponsor & Decision Authority

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Project Lead** | julio.cesar.d.pessan | julio.cesar.d.pessan@avanade.com | +55 11 98765-4321 | 24/7 + business hours |
| **VP Engineering** | vp-engineering@avanade.example | vp-engineering@avanade.example | +55 11 98765-4400 | Business hours + on-call (critical) |
| **CTO** | cto@avanade.example | cto@avanade.example | +55 11 98765-4401 | On-call for critical decisions |

### Client Stakeholders (Bradesco)

| Role | Name | Email | Phone | Availability |
|------|------|-------|-------|---|
| **Data Governance Board** | governance-board@bradesco.com.br | governance-board@bradesco.com.br | +55 11 3555-5555 | Business hours |
| **Business Sponsor** | business-sponsor@bradesco.com.br | business-sponsor@bradesco.com.br | +55 11 3555-5556 | Business hours + on-call (Sev 1) |
| **IT Director** | it-director@bradesco.com.br | it-director@bradesco.com.br | +55 11 3555-5557 | Business hours + on-call (Sev 1) |

---

## ON-CALL ROTATION SCHEDULE

### Week 1 (D+0 to D+7) — Intensive Coverage

| Day | Primary L1 | Backup L1 | L2 Data Arch | L2 DBA | Notes |
|-----|-----------|-----------|---|---|---|
| **Mon 06-16** | julio.cesar.d.pessan | backup-eng-1 | data-architect | dba-lead | **Go-Live Day** |
| **Tue 06-17** | julio.cesar.d.pessan | backup-eng-1 | data-architect | dba-lead | Daily validation |
| **Wed 06-18** | backup-eng-1 | backup-eng-2 | dba-lead | data-architect | Shift rotation |
| **Thu 06-19** | julio.cesar.d.pessan | backup-eng-1 | data-architect | dba-lead | Mid-week review |
| **Fri 06-20** | backup-eng-1 | backup-eng-2 | dba-lead | data-architect | Week close-out |
| **Sat 06-21** | backup-eng-2 | backup-eng-1 | On-call (Sev 1) | On-call (Sev 1) | Weekend coverage |
| **Sun 06-22** | julio.cesar.d.pessan | backup-eng-1 | On-call (Sev 1) | On-call (Sev 1) | Weekend coverage |

### Week 2–4 (D+8 to D+30) — Standard Coverage

- **Weekdays:** Primary on-call (08:00–18:00 BRT), backup on-call (after hours)
- **Weekends:** On-call team on standby (respond to Sev 1/2 only)
- **Rotation:** Weekly swap every Monday

### After 30 Days — Production Support (SLA-based)

- **Business hours:** Dedicated support team
- **After hours:** On-call for Sev 1 only
- **Rotation:** 2-week cycles

---

## INCIDENT RESPONSE PROTOCOL

### Initial Contact (First 5 Minutes)

1. **Reporter** contacts L1 on-call via:
   - ✅ **Phone** (primary for Sev 1/2)
   - ✅ **Email** (acceptable for Sev 3/4)
   - ✅ **MS Teams** (for updates during incident)
   - ✅ **Slack** (integration with alerts)

2. **L1 acknowledges** receipt within 5 minutes
   - Confirms severity level
   - Asks: "What is the business impact?"
   - Creates incident ticket in Jira/ADO

3. **L1 begins triage** (15 minutes)
   - Is system still running?
   - Any data loss detected?
   - Immediate mitigation possible?

### Escalation Path (Based on Severity)

#### Sev 1: Critical (System Down)

```
Reporter (L1 on-call) 
  → Page L2 + VP Engineering immediately
  → Activate war room (Teams channel: #incident-bridesco-sev1)
  → Conference call within 5 minutes
  → Execute emergency response playbook
  → Escalate to CTO if unresolved in 60 min
```

**War Room Conference:** +55 11 98765-4444 (Zoom)

#### Sev 2: High (Major Issue)

```
Reporter (L1 on-call)
  → Call L2 Data Architect or DBA (10 min)
  → Create Teams incident channel
  → Join optional escalation call (if needed)
  → Target resolution: 8 hours
  → Escalate to VP Eng if unresolved in 4h
```

#### Sev 3: Medium (Minor Issue)

```
Reporter (L1 on-call)
  → Email L2 team + create ticket
  → Assign owner within 4 hours
  → Target resolution: 24 hours
  → No automatic escalation
```

#### Sev 4: Low (Request/Question)

```
Reporter (L1 on-call)
  → Email support channel
  → Respond within 24 hours
  → No escalation path
```

---

## CONTACT CHANNELS & PREFERRED METHODS

### By Severity

| Severity | Channel | Format | Response Expectation |
|----------|---------|--------|---|
| **Sev 1** | ☎️ Phone + Teams | Immediate call + bridge line | 5 min |
| **Sev 2** | ☎️ Phone (if not responsive, escalate) | Call + Teams incident channel | 1 hour |
| **Sev 3** | 📧 Email + Jira ticket | Ticket creation + assignment | 4 hours |
| **Sev 4** | 📧 Email + Wiki FAQ | Ticket only, no call | 24 hours |

### Communication Channels (Ranked by Priority)

1. **Phone** (for Sev 1/2): Fastest acknowledgment
2. **MS Teams** (shared incident channel): Group coordination
3. **Email** (for Sev 3/4): Documented trail
4. **Slack** (integration): Automated alerts
5. **Jira/ADO** (tickets): Formal tracking

### Status Updates (During Ongoing Incident)

- **Sev 1:** Every 15 minutes (or when status changes)
- **Sev 2:** Every 30 minutes (or when status changes)
- **Sev 3:** Daily end-of-day update
- **Sev 4:** When resolved

---

## ESCALATION TRIGGERS & AUTO-ESCALATION

### Auto-Escalation Rules

| Trigger | Escalation Action | Timer |
|---------|---|---|
| L1 no response for 10 min (Sev 1) | Page L2 + notify manager | T+10 |
| L2 no resolution in 2 hours (Sev 1) | Page VP Eng + CTO | T+2h |
| No acknowledgment in 30 min (Sev 2) | Escalate to L2 manager | T+30 |
| No update in 4 hours (Sev 3) | Send reminder email | T+4h |

### Manual Escalation (Reporter Initiated)

If you are not satisfied with progress:

1. **Request escalation** from current owner
2. **Email escalation chain** with justification
3. **Include:** incident ID, current status, reason for escalation
4. **Response:** Within 30 minutes from next level

---

## COMMUNICATION TEMPLATES

### Incident Notification (Sev 1)

```
Subject: 🔴 SEV 1 INCIDENT — Bradesco Migration (Ticket #BRD-12345)

IMPACT: Databricks cluster is down. 12.4M row migration HALTED.
SEVERITY: Critical (data access lost, 500+ users affected)
REPORTED: 2026-06-16 22:15 BRT
OWNER: julio.cesar.d.pessan (L1 on-call)

IMMEDIATE ACTION: War room activated. Bridge call: +55 11 98765-4444

NEXT UPDATE: 22:30 BRT (15-min intervals thereafter)
```

### Status Update (During Incident)

```
INCIDENT #BRD-12345 — Status Update

TIME: 22:45 BRT (30 min elapsed)
STATUS: Investigating (in progress)
LATEST: DBA identified disk full on Databricks cluster. Cleanup in progress.
ETA RESOLUTION: 23:15 BRT
NEXT UPDATE: 23:00 BRT

⚠️ DO NOT retry deployments until GREEN status.
```

### All-Clear Notification (Resolved)

```
✅ INCIDENT RESOLVED — Bradesco Migration BRD-12345

TIME RESOLVED: 2026-06-16 23:10 BRT
DURATION: 55 minutes
ROOT CAUSE: Databricks auto-scaling provisioned undersized cluster. Auto-scaling adjusted.
IMPACT: No data loss. Deployment resumed and completed successfully.

FOLLOW-UP: Root cause analysis scheduled for 2026-06-17 10:00 BRT.
```

---

## DOCUMENTATION & REFERENCE

### Quick Links for On-Call Team

- **Runbook:** projects/bradesco/RUNBOOK_ON_CALL.md
- **Troubleshooting Guide:** docs/TROUBLESHOOTING.md
- **Rollback Procedure:** projects/bradesco/state/go_live_checklist.md (Rollback section)
- **Known Issues:** projects/bradesco/state/lessons-learned-retrospective.md
- **Metrics Dashboard:** Datadog/Azure Monitor (linked in on-call wiki)

### Handoff Template (For Shift Change)

**Outgoing L1 → Incoming L1 (30-min overlap)**

- [ ] Current incident status (if any)
- [ ] Recent alerts in last 4 hours
- [ ] Pending action items
- [ ] Known issues / workarounds in place
- [ ] Overnight expectations / scheduled maintenance
- [ ] Contact number for incoming L1
- [ ] Any stakeholder messages to relay

---

## ANNUAL REVIEW & UPDATES

| Review Date | Owner | Focus Area |
|---|---|---|
| 2026-09-16 (Q3) | Project Lead | Contact accuracy & availability |
| 2026-12-16 (Q4) | Project Lead | Response time metrics & SLA review |
| 2027-03-16 (Q1) | VP Engineering | Escalation effectiveness & training needs |
| 2027-06-16 (Q2) | Project Lead | Annual renewal & rotation updates |

**Next Review:** 2026-09-16

---

## LEGAL & CONFIDENTIALITY

- ✅ All contact information is **CONFIDENTIAL** and for authorized personnel only
- ✅ Phone numbers & emails subject to change — **CHECK THIS DOCUMENT BEFORE EACH USE**
- ✅ For external questions, route through: external-support@avanade.com
- ✅ Do NOT share this document outside Avanade + Bradesco governance teams

---

## SIGN-OFF

| Role | Name | Confirmation | Date |
|------|------|---|---|
| L1 Primary | julio.cesar.d.pessan | ✅ Confirmed | 2026-06-16 |
| L2 Data Architect | data-architect@avanade.example | ✅ Confirmed | 2026-06-16 |
| L2 DBA | dba-lead@avanade.example | ✅ Confirmed | 2026-06-16 |
| VP Engineering | vp-engineering@avanade.example | ✅ Confirmed | 2026-06-16 |

---

**Document Status:** ✅ ACTIVE & REVIEWED  
**Last Updated:** 2026-06-16 11:18:17 UTC  
**Next Review:** 2026-09-16  
**Distribution:** Avanade + Bradesco Authorized Personnel Only
