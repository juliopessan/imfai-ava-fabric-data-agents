# Task: Create Data Value Proposition

**Command:** `*value-prop`  
**Agent:** DataStrategist (Alex)  
**Output:** `value-proposition.md`

---

## Objective

Create a compelling data value proposition that articulates the business value, benefits, and ROI of the data initiative to stakeholders.

---

## Prerequisites

- [ ] Problem statement defined
- [ ] KPIs identified
- [ ] Stakeholders mapped
- [ ] Understanding of current state

---

## Steps

### Step 1: Understand Current State

Document the "Before" scenario:

| Aspect | Current State |
|--------|---------------|
| **Data Access** | How do users access data today? |
| **Decision Making** | How are decisions made? |
| **Time to Insight** | How long does it take? |
| **Data Quality** | What's the confidence level? |
| **Cost** | What are current data costs? |

### Step 2: Define Future State

Document the "After" scenario:

| Aspect | Future State |
|--------|--------------|
| **Data Access** | How will users access data? |
| **Decision Making** | How will decisions be made? |
| **Time to Insight** | Target time to insight |
| **Data Quality** | Target confidence level |
| **Cost** | Projected cost savings/investments |

### Step 3: Identify Value Drivers

For each stakeholder group, identify value:

| Stakeholder | Primary Value | Secondary Value |
|-------------|---------------|-----------------|
| **Executives** | Strategic insight | Risk reduction |
| **Managers** | Operational efficiency | Cost savings |
| **Analysts** | Time savings | Data accuracy |
| **Users** | Self-service | Real-time access |

### Step 4: Quantify Benefits

Calculate tangible benefits:

```yaml
benefits:
  revenue_impact:
    description: "Revenue increase from better decisions"
    calculation: "{formula}"
    estimated_value: "$X"
    timeframe: "12 months"
    
  cost_savings:
    description: "Cost reduction from automation"
    calculation: "{formula}"
    estimated_value: "$Y"
    timeframe: "12 months"
    
  time_savings:
    description: "Hours saved per analyst"
    calculation: "hours/week * analysts * weeks"
    estimated_value: "Z hours"
    timeframe: "yearly"
    
  quality_improvement:
    description: "Reduction in data errors"
    calculation: "current_errors - target_errors"
    estimated_value: "X% reduction"
    timeframe: "6 months"
```

### Step 5: Identify Intangible Benefits

Document qualitative benefits:
- Improved decision confidence
- Enhanced collaboration
- Better governance
- Reduced risk
- Competitive advantage

### Step 6: Calculate ROI

```yaml
roi_calculation:
  investment:
    implementation: "$X"
    maintenance: "$Y/year"
    total_3_year: "$Z"
    
  returns:
    year_1: "$A"
    year_2: "$B"
    year_3: "$C"
    total_3_year: "$D"
    
  roi:
    simple_roi: "(Returns - Investment) / Investment"
    payback_period: "X months"
    npv: "$E"
```

---

## Output Template

```markdown
# Data Value Proposition

**Project:** {project_name}  
**Date:** {date}  
**Author:** DataStrategist  
**Version:** 1.0

---

## Executive Summary

{2-3 sentence value proposition statement}

**Key Message:** {one-liner that captures the value}

---

## The Problem

### Current State
{Description of current challenges}

### Impact of the Problem
- Financial: {cost of current state}
- Operational: {inefficiencies}
- Strategic: {missed opportunities}

---

## The Solution

### Future State Vision
{Description of future state with this initiative}

### Key Capabilities
1. {Capability 1}: {benefit}
2. {Capability 2}: {benefit}
3. {Capability 3}: {benefit}

---

## Value for Stakeholders

### For Executives
- {Value 1}
- {Value 2}

### For Managers
- {Value 1}
- {Value 2}

### For Analysts/Users
- {Value 1}
- {Value 2}

---

## Quantified Benefits

| Benefit Category | Metric | Value | Timeframe |
|------------------|--------|-------|-----------|
| Revenue Impact | {metric} | ${value} | {time} |
| Cost Savings | {metric} | ${value} | {time} |
| Time Savings | {metric} | {hours} | {time} |
| Quality | {metric} | {%} | {time} |

### Total Expected Value
- **Year 1:** ${X}
- **Year 2:** ${Y}
- **Year 3:** ${Z}
- **3-Year Total:** ${Total}

---

## ROI Analysis

| Metric | Value |
|--------|-------|
| Total Investment | ${X} |
| Total Returns (3 years) | ${Y} |
| Simple ROI | {X}% |
| Payback Period | {X} months |

---

## Risk Mitigation Value

| Risk | Current Exposure | After Implementation |
|------|-----------------|---------------------|
| {Risk 1} | {exposure} | {mitigated} |
| {Risk 2} | {exposure} | {mitigated} |

---

## Success Metrics

| KPI | Baseline | Target | Timeline |
|-----|----------|--------|----------|
| {KPI 1} | {current} | {target} | {date} |
| {KPI 2} | {current} | {target} | {date} |

---

## Call to Action

{Clear next steps and decision required}
```

---

## Handoff

After completing value proposition:
- **Continue UPSTREAM:** Create strategy summary → `*strategy-summary`
- **Review KPIs:** Verify alignment → `*create-kpis`
- **Next phase:** Proceed to BusinessAnalyst → `@business-analyst *help`
