# Delivery Lead Agent - DeliveryPro 📊

**Agent ID:** `delivery-lead`  
**Agent Name:** `DeliveryPro`  
**Version:** 1.0  
**Icon:** 📊

---

## 🎯 OVERVIEW

The **Delivery Lead Agent (DeliveryPro)** is an AI-powered assistant designed to help delivery leads, project managers, and program managers with:

- **Project Estimation** - Cost and timeline estimation with conservative, data-driven approaches
- **Roadmap Planning** - Multi-quarter roadmaps with phases, milestones, and dependencies
- **Delivery Planning** - Detailed WBS, sprint planning, and resource allocation
- **Risk Management** - Proactive risk identification, assessment, and mitigation
- **Issue Analysis** - Root cause analysis using 5 Whys and Fishbone diagrams
- **Executive Reporting** - RAG status reports and executive summaries
- **Budget Management** - Budget forecasting, burn rate analysis, and cost optimization
- **Project Health** - Comprehensive health assessments with actionable recommendations
- **Resource Planning** - Capacity planning and resource optimization

**Key Principle:** DeliveryPro provides **conservative, realistic estimates** and **transparent, data-driven insights** to help you deliver projects successfully.

---

## 🚀 HOW TO ACTIVATE

### Method 1: Mention the Agent (Recommended)

Simply mention the agent in your message:

```
@delivery-lead help me estimate this project
```

### Method 2: Use Commands Directly

DeliveryPro recognizes the following commands (all prefixed with `*`):

- `*estimate-project` - Get cost and timeline estimates
- `*create-roadmap` - Generate a project roadmap
- `*create-plan` - Create detailed delivery plan (WBS, sprints)
- `*assess-risks` - Identify and assess project risks
- `*analyze-issues` - Perform root cause analysis on issues
- `*exec-summary` - Generate executive status report
- `*forecast-budget` - Analyze budget burn and forecast
- `*health-check` - Comprehensive project health assessment
- `*resource-plan` - Create resource allocation plan
- `*yolo` - Quick estimate mode (use with caution!)
- `*exit` - Deactivate the agent

**Example:**

```
*estimate-project for a data platform migration
```

### Method 3: Activate Explicitly

```
I need help from the delivery lead agent
```

---

## 📚 AVAILABLE COMMANDS

### 1️⃣ \*estimate-project

**Purpose:** Estimate cost, timeline, and resources for a project

**What it does:**

- Gathers project information through 7 key questions
- Estimates development effort by role (Data Engineer, Data Scientist, etc.)
- Calculates infrastructure costs (Azure/AWS)
- Calculates ongoing operational costs
- Creates a timeline with phases and milestones
- Assesses risks and adds contingencies (15-20%)
- Shows AI impact (40-70% effort reduction)
- Generates comprehensive estimate document

**Usage:**

```
*estimate-project for building a real-time analytics platform
```

**Output:** Full project estimation in markdown format with:

- Budget breakdown by role and phase
- 5-year Total Cost of Ownership (TCO)
- Cost optimization opportunities
- ROI analysis
- Timeline with milestones
- Risk assessment

---

### 2️⃣ \*create-roadmap

**Purpose:** Create a multi-quarter project roadmap

**What it does:**

- Gathers project requirements and constraints
- Defines 4 phases: Foundation → Core → Enhancement → Go-Live
- Breaks down each phase into 2-week sprints
- Identifies key milestones with success criteria
- Maps dependencies (internal, external, cross-team)
- Allocates resources by quarter
- Defines success metrics (KPIs, business outcomes)

**Usage:**

```
*create-roadmap for our data modernization program
```

**Output:** Comprehensive roadmap document with:

- Quarterly breakdown with sprint-level detail
- Milestones with dates and dependencies
- Resource allocation table by quarter
- Dependency tracking
- Success metrics dashboard

---

### 3️⃣ \*create-plan

**Purpose:** Create detailed delivery plan with WBS and sprints

**What it does:**

- Creates Work Breakdown Structure (WBS) 4 levels deep
- Estimates effort using Three-Point estimation
- Sequences activities with dependencies
- Allocates resources (targeting 80-85% utilization)
- Creates sprint plan with user stories
- Identifies quality gates and phase transitions

**Usage:**

```
*create-plan for implementing MLOps platform
```

**Output:** Detailed delivery plan with:

- Complete WBS (Epic → Feature → User Story → Task)
- Sprint breakdown with story points
- Resource allocation by sprint and role
- Critical path analysis
- Quality gates and approval criteria

---

### 4️⃣ \*assess-risks

**Purpose:** Identify, assess, and mitigate project risks

**What it does:**

- Identifies risks across 5 categories (Technical, Resource, Process, External, Business)
- Assesses probability (1-5) and impact (1-5)
- Calculates risk scores (Probability × Impact)
- Performs 5 Whys root cause analysis
- Defines mitigation strategies (Avoidance, Transfer, Mitigation, Acceptance)
- Creates risk register with monitoring plan

**Usage:**

```
*assess-risks for cloud migration project
```

**Output:** Risk register with:

- Risk inventory by category
- Risk scores and priority (Critical/High/Medium/Low)
- Root cause analysis for each risk
- Mitigation plans with owners and dates
- Contingency plans
- Risk monitoring schedule

---

### 5️⃣ \*analyze-issues

**Purpose:** Perform root cause analysis on project issues

**What it does:**

- Gathers issue information and context
- Categorizes issue (Technical, Process, People, External)
- Performs 5 Whys root cause analysis
- Creates Fishbone (Ishikawa) diagram
- Assesses impact (Timeline, Cost, Quality, Team, Business)
- Recommends corrective actions (Immediate, Short-term, Long-term)
- Defines prevention strategies

**Usage:**

```
*analyze-issues: production deployment failures
```

**Output:** Issue analysis report with:

- Issue description and categorization
- 5 Whys root cause analysis
- Fishbone diagram identifying contributing factors
- Impact assessment across 5 dimensions
- Corrective action plan with priorities
- Prevention strategies and lessons learned

---

### 6️⃣ \*exec-summary

**Purpose:** Generate executive status report with RAG status

**What it does:**

- Gathers project status information
- Assesses RAG (Red/Amber/Green) status for 6 dimensions
- Highlights key metrics (Budget, Timeline, Scope, Quality)
- Identifies top 3 achievements this period
- Highlights top 3 risks and mitigation plans
- Highlights top 3 issues and corrective actions
- Provides clear recommendations for leadership

**Usage:**

```
*exec-summary for the monthly steering committee
```

**Output:** Executive summary (2-3 pages) with:

- Overall RAG status dashboard
- Key metrics (Budget: CPI/SPI, Schedule: Variance, Quality: Defects)
- Top 3 achievements with business impact
- Top 3 risks with mitigation status
- Top 3 issues with corrective actions
- Upcoming milestones (next 30 days)
- Decisions needed from leadership
- Clear recommendations

---

### 7️⃣ \*forecast-budget

**Purpose:** Analyze budget burn and forecast completion cost

**What it does:**

- Gathers budget information and actuals
- Calculates burn rate (actual spending per period)
- Calculates CPI (Cost Performance Index) and SPI (Schedule Performance Index)
- Identifies cost drivers (Labor, Infrastructure, Other)
- Forecasts using 3 methods: Linear, Earned Value, Bottom-Up
- Identifies budget risks and triggers
- Recommends cost optimization actions

**Usage:**

```
*forecast-budget for Q2 analysis
```

**Output:** Budget forecast report with:

- Budget summary (Approved, Spent, Remaining, Forecast)
- Burn rate analysis with trend chart
- Earned Value Management metrics (CPI, SPI, EAC, TCPI)
- Cost driver breakdown
- 3 forecast scenarios (Best/Expected/Worst)
- Risk-adjusted forecast
- Cost optimization recommendations

---

### 8️⃣ \*health-check

**Purpose:** Comprehensive project health assessment

**What it does:**

- Gathers status across 10 dimensions (Budget, Schedule, Scope, Quality, Resources, Risks, Stakeholders, Team, Technical, Governance)
- Calculates health scores (1-10 scale) with weighting
- Identifies root causes for any dimension scoring <7
- Assesses trends (Improving/Stable/Declining)
- Recommends corrective actions by priority (Immediate/High/Medium)
- Generates overall health scorecard

**Usage:**

```
*health-check for the data engineering program
```

**Output:** Health assessment report with:

- Overall health score (weighted average)
- Dimension-by-dimension breakdown with scores
- Trend analysis (last 3 periods)
- Red flags and critical issues
- Root cause analysis for low scores
- Prioritized corrective action plan
- Monthly health tracking dashboard

---

### 9️⃣ \*resource-plan

**Purpose:** Create resource allocation and capacity plan

**What it does:**

- Gathers resource requirements by role and phase
- Identifies required roles and skills
- Calculates resource demand by sprint
- Assesses resource supply (available capacity)
- Performs gap analysis (demand vs supply)
- Optimizes allocation (resource leveling/smoothing)
- Creates staffing plan with ramp-up/ramp-down

**Usage:**

```
*resource-plan for next quarter
```

**Output:** Resource plan with:

- Resource demand by role and sprint
- Resource supply analysis (available capacity)
- Gap analysis with resolution strategies
- Optimized resource allocation table
- Resource loading charts (utilization by person)
- Staffing plan (onboarding/ramping dates)
- Contingency plans for resource risks

---

### 🚀 \*yolo

**Purpose:** Quick estimate mode (experimental)

**What it does:**

- Provides rapid, high-level estimates with minimal input
- Uses AI to infer missing details
- Applies industry benchmarks and heuristics
- **⚠️ Warning:** Less accurate than full \*estimate-project

**Usage:**

```
*yolo estimate for small data pipeline project
```

**Use with caution:** Best for rough order of magnitude (ROM) estimates, not for final budget approval.

---

### 🚪 \*exit

**Purpose:** Deactivate the agent

**Usage:**

```
*exit
```

---

## 💡 USAGE EXAMPLES

### Example 1: Project Estimation

```
@delivery-lead I need to estimate a project to build a customer 360 data platform.
We need to integrate 5 data sources, build a data lake, create dashboards,
and implement 3 ML models. Target completion is 9 months.

*estimate-project
```

DeliveryPro will ask you 7 questions and then generate a comprehensive estimate.

---

### Example 2: Risk Assessment

```
@delivery-lead We're starting a cloud migration project and I'm worried about risks.

*assess-risks
```

DeliveryPro will guide you through identifying risks across 5 categories and create a detailed risk register.

---

### Example 3: Executive Summary

```
@delivery-lead I need to prepare the monthly executive report for our analytics program.

*exec-summary
```

DeliveryPro will gather project status and generate a 2-3 page executive summary with RAG status.

---

### Example 4: Root Cause Analysis

```
@delivery-lead Our ETL pipeline keeps failing in production. Can you help analyze why?

*analyze-issues
```

DeliveryPro will perform 5 Whys and Fishbone analysis and recommend corrective actions.

---

## 🧠 HOW DELIVERPRO THINKS

### Conservative Estimation Approach

DeliveryPro follows these principles:

1. **Be conservative, not optimistic** - Hope is not a strategy
2. **Add buffers** - 15-20% development buffer, 20-25% testing buffer
3. **Plan for 80-85% utilization** - Not 100%, because meetings/emails/context-switching
4. **Include all activities** - Requirements, design, testing, documentation, deployment
5. **Use historical data** - Industry benchmarks and cost data
6. **Quantify AI impact** - 40-70% effort reduction with agentic AI

### Data-Driven Insights

DeliveryPro leverages:

- **Industry benchmarks** - Hourly rates, project costs, infrastructure pricing
- **Best practices** - 70+ best practices across estimation, planning, risk management
- **Templates** - Proven templates for estimates, roadmaps, risk registers, executive summaries
- **Agentic AI impact data** - From AGENTIC-AI-IMPACT-ASSESSMENT.md

### Transparency & Honesty

DeliveryPro believes:

- Bad news doesn't get better with age
- Transparency builds trust
- Show your work (assumptions, calculations, risks)
- Provide options, let stakeholders decide

---

## 📁 AGENT STRUCTURE

DeliveryPro consists of the following files:

### Agent Definition

- `.avanade-core/agents/delivery-lead.md` - Agent configuration and persona

### Tasks (9 files)

- `.avanade-core/tasks/estimate-project.md`
- `.avanade-core/tasks/create-roadmap.md`
- `.avanade-core/tasks/assess-risks.md`
- `.avanade-core/tasks/analyze-issues.md`
- `.avanade-core/tasks/executive-summary.md`
- `.avanade-core/tasks/forecast-budget.md`
- `.avanade-core/tasks/create-delivery-plan.md`
- `.avanade-core/tasks/project-health-check.md`
- `.avanade-core/tasks/resource-planning.md`

### Checklist

- `.avanade-core/checklists/delivery-lead-checklist.md` - 85-item quality checklist

### Data Files

- `.avanade-core/data/delivery-best-practices.md` - 70 best practices
- `.avanade-core/data/cost-benchmarks.md` - Industry cost benchmarks and rates

### Templates

- `.avanade-core/templates/project-estimation-tmpl.yaml` - Estimation template
- `.avanade-core/templates/roadmap-tmpl.yaml` - Roadmap template
- `.avanade-core/templates/risk-register-tmpl.yaml` - Risk register template
- `.avanade-core/templates/exec-summary-tmpl.yaml` - Executive summary template

---

## ⚙️ AGENT CONFIGURATION

### Core Principles

1. **Conservative Estimates** - Better to overestimate than underestimate
2. **Transparency** - Show assumptions, calculations, and rationale
3. **Data-Driven** - Use benchmarks and historical data
4. **Risk Proactivity** - Identify risks early, mitigate continuously
5. **Quality Focus** - Build quality gates into plans
6. **Team Health** - Plan for sustainable pace (80-85% utilization)
7. **Clear Communication** - Tailor message to audience (executives vs technical)
8. **Stakeholder Management** - Engage early, update frequently
9. **Continuous Learning** - Track actuals vs estimates, improve over time
10. **Embrace AI** - Leverage agentic AI for 40-70% effort reduction

### Expertise Areas

- **Estimation:** Three-point, analogous, bottom-up, story points
- **Planning:** Roadmaps, WBS, sprint planning, resource allocation
- **Risk Management:** Risk identification, assessment, mitigation, monitoring
- **Reporting:** RAG status, executive summaries, dashboards
- **Financial:** Budget forecasting, burn rate, TCO, ROI, EVM
- **Agile/Scrum:** Sprint planning, velocity, retrospectives

---

## 📊 DELIVERPRO'S VALUE PROPOSITION

### With DeliveryPro, You Get:

✅ **60-75% faster estimation** - AI-powered estimates in minutes, not days  
✅ **Conservative, realistic plans** - No surprises, no heroic efforts  
✅ **Comprehensive risk management** - Proactive identification and mitigation  
✅ **Executive-ready reports** - Professional, data-driven status updates  
✅ **Best practices built-in** - 70+ best practices applied automatically  
✅ **Industry benchmarks** - Hourly rates, project costs, infrastructure pricing  
✅ **Proven templates** - Used in 100+ real projects  
✅ **Continuous learning** - Improve estimates with every project

### Expected Impact:

- **Estimation accuracy:** ±10-15% (vs ±30-50% manual)
- **Time savings:** 60-75% effort reduction on delivery lead activities
- **Risk reduction:** 40-60% fewer critical issues due to proactive risk management
- **Stakeholder satisfaction:** Higher trust due to transparency and realism

---

## 🛠️ CUSTOMIZATION

Want to customize DeliveryPro for your organization?

### Add Your Own Data

1. Update [cost-benchmarks.md](.avanade-core/data/cost-benchmarks.md) with your organization's rates
2. Add your own best practices to [delivery-best-practices.md](.avanade-core/data/delivery-best-practices.md)
3. Track actual vs estimated on your projects and update benchmarks

### Modify Templates

1. Edit YAML templates in `.avanade-core/templates/` to match your organization's formats
2. Add company branding and required sections

### Add New Commands

1. Create new task files in `.avanade-core/tasks/`
2. Update [delivery-lead.md](.avanade-core/agents/delivery-lead.md) to reference new tasks

---

## 🤝 BEST PRACTICES FOR USING DELIVERPRO

### 1. Start with Estimation

Use `*estimate-project` early in the project lifecycle to set realistic expectations.

### 2. Review Risks Weekly

Use `*assess-risks` at project kickoff, then review and update weekly.

### 3. Monthly Executive Reports

Use `*exec-summary` for steering committee meetings and monthly status reports.

### 4. Root Cause Analysis for Issues

Don't just firefight - use `*analyze-issues` to understand and prevent recurring problems.

### 5. Track Actuals vs Estimates

After project completion, compare actual costs/timelines to DeliveryPro's estimates. Use learnings to improve future estimates.

### 6. Leverage AI Impact Data

Always include AI impact analysis in estimates to show cost savings potential.

### 7. Be Honest with Stakeholders

Use DeliveryPro's transparent, data-driven approach to build trust with executives and sponsors.

---

## ❓ FREQUENTLY ASKED QUESTIONS

### Q: Is DeliveryPro's estimate a guarantee?

**A:** No. DeliveryPro provides **realistic, conservative estimates** based on industry benchmarks and best practices. Actual results will vary based on team experience, technology choices, requirements changes, and unforeseen risks. Always include contingency buffers (15-20%).

### Q: Can I use DeliveryPro for Agile projects?

**A:** Yes! DeliveryPro supports Agile methodologies (Scrum, SAFe, etc.) and uses story points, velocity, and sprint planning concepts. Use `*create-plan` for sprint-level planning.

### Q: How accurate are the cost benchmarks?

**A:** Cost benchmarks are based on industry surveys (January 2026) and Avanade project data. Rates vary by region, company size, and market conditions. Update [cost-benchmarks.md](.avanade-core/data/cost-benchmarks.md) with your organization's actual rates for higher accuracy.

### Q: What's the difference between *estimate-project and *yolo?

**A:**

- **`*estimate-project`**: Thorough, interactive estimation with 7 questions. Best for formal estimates and budget approval.
- **`*yolo`**: Quick, rough estimate with minimal input. Best for initial conversations and rough order of magnitude (ROM).

### Q: Can DeliveryPro integrate with Jira/Azure DevOps?

**A:** Not directly in this version. DeliveryPro generates markdown outputs that you can copy into your project management tools. Future versions may include direct integration.

### Q: How does DeliveryPro calculate AI impact?

**A:** Based on data from [AGENTIC-AI-IMPACT-ASSESSMENT.md](../real-test/docs/AGENTIC-AI-IMPACT-ASSESSMENT.md), which shows 40-70% effort reduction across activities like requirements analysis (60%), ETL development (60%), data quality rules (67%), testing (67%), and documentation (75%).

---

## 📞 SUPPORT & FEEDBACK

### Getting Help

- Review this README
- Check [delivery-best-practices.md](.avanade-core/data/delivery-best-practices.md) for guidance
- Review templates in `.avanade-core/templates/`

### Providing Feedback

DeliveryPro is continuously improving. Please provide feedback on:

- Estimation accuracy (compare actual vs estimated)
- Usefulness of outputs
- Missing features or commands
- Best practices to add

---

## 📜 VERSION HISTORY

### Version 1.0 (January 22, 2026)

- Initial release
- 9 core commands
- 85-item quality checklist
- 70 best practices
- Industry cost benchmarks
- 4 professional templates
- AI impact analysis built-in

---

## 🎓 LEARNING RESOURCES

### Recommended Reading

1. **Project Management Body of Knowledge (PMBOK)** - PMI
2. **Agile Estimating and Planning** - Mike Cohn
3. **The Mythical Man-Month** - Fred Brooks
4. **Risk Up Front** - Adam Shostack

### Certifications

- **PMP** - Project Management Professional
- **CSM** - Certified Scrum Master
- **SAFe Agilist** - Scaled Agile Framework
- **AWS Certified Solutions Architect** - For cloud cost estimation

---

## 🚀 GET STARTED NOW

Ready to use DeliveryPro? Try this:

```
@delivery-lead I have a project to estimate. It's a customer analytics platform
that will integrate data from Salesforce, SAP, and Google Analytics. We need
to build a data lake, create dashboards in Power BI, and implement 2 ML models
for customer segmentation and churn prediction. Timeline is 6-9 months.

*estimate-project
```

DeliveryPro will guide you through the estimation process and generate a comprehensive project estimate.

---

**Happy Delivering! 📊**

_"Hope is not a strategy. Data-driven delivery is."_ - DeliveryPro
