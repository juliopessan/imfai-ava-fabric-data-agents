# Orchestration Best Practices

**Document:** Best Practices for Pipeline Orchestration  
**Agent:** Orchestrator  
**Version:** 1.0

---

## Pipeline Lifecycle Management

### Phase Discipline

**Principle:** Complete each phase thoroughly before moving to the next.

**UPSTREAM Phase:**
- Focus on understanding the business problem
- Define measurable success criteria
- Document all data sources and requirements
- Establish quality expectations early
- **Gate 1 validates:** Problem understanding and requirements clarity

**MIDSTREAM Phase:**
- Design before implementation
- Document architectural decisions
- Create logical data models
- Define quality rules in detail
- **Gate 2 validates:** Design completeness and feasibility

**DOWNSTREAM Phase:**
- Follow the design specifications
- Test incrementally
- Document as you build
- Validate quality continuously
- **Gate 3 validates:** Implementation completeness and production readiness

---

## Gate Validation Best Practices

### Preparation

1. **Review checklist before validation**
   - Know what artifacts are expected
   - Understand quality criteria
   - Prepare for common gaps

2. **Self-assess before formal validation**
   - Run `*artifacts` to see current state
   - Address obvious gaps first
   - Request validation when confident

### During Validation

1. **Be thorough, not rushed**
   - Quality over speed
   - Document all findings
   - Provide actionable feedback

2. **Consider cross-references**
   - Artifacts should be consistent
   - Later artifacts should reference earlier ones
   - Look for contradictions

### After Validation

1. **On PASS:**
   - Record the milestone
   - Celebrate progress
   - Brief next phase team

2. **On FAIL:**
   - Focus on remediation, not blame
   - Prioritize critical gaps
   - Set clear timeline for re-validation

---

## Routing Best Practices

### Agent Selection

1. **Match expertise to need**
   - DataStrategist for "why" questions
   - BusinessAnalyst for "what" mapping
   - DataArchitect for "how" design
   - DataSteward for quality/governance
   - DataFlow for implementation
   - InsightForge for visualization

2. **Consider context continuity**
   - Same agent for related tasks
   - Handoff with full context
   - Document decisions for next agent

### Handoff Communication

1. **Provide context**
   - Current phase and status
   - Relevant artifacts
   - Specific request/goal

2. **Set expectations**
   - What output is needed
   - Any constraints or preferences
   - Timeline if relevant

---

## Audit Trail Best Practices

### Recording

1. **Be consistent**
   - Use standard action types
   - Include all required fields
   - Timestamp accurately

2. **Be complete**
   - Record both successes and failures
   - Include context for decisions
   - Link to related artifacts

### Reviewing

1. **Regular reviews**
   - Check audit before gate validations
   - Review for patterns and issues
   - Use for status reporting

2. **Compliance**
   - Maintain trail integrity
   - Don't modify historical entries
   - Archive appropriately

---

## Status Reporting Best Practices

### Frequency

1. **Regular cadence**
   - Weekly for active projects
   - At each gate validation
   - On significant milestones

2. **On-demand**
   - When stakeholders request
   - Before major decisions
   - After significant changes

### Content

1. **Be accurate**
   - Base on actual artifact state
   - Don't overstate progress
   - Highlight real blockers

2. **Be actionable**
   - Clear next steps
   - Assigned to specific agents
   - Prioritized recommendations

---

## Common Pitfalls to Avoid

### Phase Discipline

❌ **Skipping phases:** "We already know what we need, let's start coding"
✅ **Solution:** Document even "obvious" requirements for future reference

❌ **Incomplete gates:** "Close enough, let's move on"
✅ **Solution:** Address gaps before proceeding; they compound later

❌ **Gold-plating:** "Let's add more features to STTM"
✅ **Solution:** Stay focused on defined scope; iterate in future phases

### Routing

❌ **Wrong agent:** "DataFlow, help me define KPIs"
✅ **Solution:** Use `*route` to get correct agent recommendation

❌ **Context loss:** "Continue from where we left off"
✅ **Solution:** Always provide context; agents don't remember previous sessions

### Documentation

❌ **Skipping documentation:** "I'll document later"
✅ **Solution:** Document as you go; use agent automation

❌ **Inconsistent artifacts:** "The STTM says X but model says Y"
✅ **Solution:** Cross-reference during gate validation

---

## Orchestration Patterns

### Pattern 1: New Project Initialization

```
1. *status          → Establish baseline
2. Route to DataStrategist
3. Define problem and KPIs
4. Route to BusinessAnalyst
5. Create STTM and questions
6. *gate-1          → Validate UPSTREAM
```

### Pattern 2: Design Phase

```
1. Route to DataArchitect
2. Create architecture
3. Create data model
4. Route to DataSteward
5. Define DQ rules
6. *gate-2          → Validate MIDSTREAM
```

### Pattern 3: Implementation Phase

```
1. Route to DataFlow
2. Generate DDL
3. Generate ETL
4. Run tests
5. Route to InsightForge (if needed)
6. Create dashboards
7. *gate-3          → Validate DOWNSTREAM
```

### Pattern 4: Issue Resolution

```
1. *status          → Understand current state
2. *gate-{n}        → Identify specific gaps
3. Route to appropriate agent
4. Address gaps
5. *gate-{n}        → Re-validate
```

---

## Metrics to Track

### Project Health

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Gate pass rate | > 80% | 60-80% | < 60% |
| Days per phase | < 14 | 14-21 | > 21 |
| Rework rate | < 10% | 10-20% | > 20% |

### Artifact Quality

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Completeness | > 95% | 80-95% | < 80% |
| Consistency | > 90% | 75-90% | < 75% |
| Documentation | Complete | Partial | Missing |

---

*Best practices maintained by Orchestrator Agent*
