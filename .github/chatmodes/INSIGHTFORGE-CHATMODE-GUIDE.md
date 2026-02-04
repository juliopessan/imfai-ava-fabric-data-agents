# BI Developer Agent - Chatmode Guide

## Overview

The BI Developer chatmode (`bi-developer`) activates the **InsightForge** agent, a specialized Business Intelligence development assistant.

### Use Cases (Avanade Canada)

The BI Developer agent transforms data into actionable insights by:

- **Designing dashboards** - Visual layouts aligned with user personas
- **Generating reports** - Paginated and interactive reports for business needs
- **Creating visual narratives** - Storytelling through data aligned with business goals
- **Building semantic models** - Star schemas and optimized data models
- **Developing DAX measures** - Calculations, KPIs, and time intelligence

### Indicative Impact

| Benefit | Expected Impact |
|---------|-----------------|
| **Semantic Model Generation** | 70-80% faster model design with templates |
| **DAX Measures** | 60-70% reduction in measure development time |
| **Baseline Dashboards** | Auto-generated starter dashboards in minutes |
| **Performance Tuning** | 50-80% improvement in dataset load times |

## Activation

### Method 1: Chat Mode Selector
In VS Code Copilot Chat, use the chat mode selector dropdown and choose `bi-developer`.

### Method 2: Direct Mention
Type `@bi-developer` at the start of your message.

## Agent Details

| Property | Value |
|----------|-------|
| **Agent ID** | `bi-developer` |
| **Agent Name** | InsightForge |
| **Icon** | 📊 |
| **Role** | Senior BI Developer & Analytics Architect |

## Core Capabilities

### 1. Semantic Model Design
- Star schema creation
- Relationship configuration
- Hierarchy design
- Model documentation

### 2. DAX Development
- Base aggregations
- Time intelligence (YTD, MTD, PY, YoY)
- Comparisons and variances
- KPI calculations
- Ranking functions

### 3. Dashboard Design
- Visual hierarchy
- Chart selection
- Interactivity design
- Mobile layouts
- Accessibility compliance

### 4. Performance Optimization
- Model size reduction
- DAX efficiency improvements
- Query optimization
- Aggregation table design

### 5. Security Implementation
- Row-Level Security (RLS)
- Static and dynamic roles
- Manager hierarchies
- Testing scenarios

## Available Commands

| Command | Description |
|---------|-------------|
| `*help` | Show all available commands |
| `*create-semantic-model` | Design a Power BI data model |
| `*create-dax` | Generate DAX measures |
| `*create-dashboard` | Design dashboard layout |
| `*create-report` | Build reports |
| `*profile-requirements` | Gather BI requirements |
| `*optimize-dataset` | Tune performance |
| `*create-rls` | Implement Row-Level Security |
| `*document-bi` | Create documentation |
| `*validate-model` | Check model quality |
| `*execute-checklist` | Run validation checklist |
| `*demo` | Interactive demonstration |
| `*yolo` | Toggle autonomous mode |

## File Dependencies

The agent requires files from:
```
bi-developer-agent/.avanade-core/
├── core-config.yaml
├── tasks/
├── templates/
├── checklists/
└── data/
```

## Usage Examples

### Create a Sales Dashboard
```
@bi-developer I need to create a sales analytics dashboard for our retail business. 
We have data in SQL Server with sales, customers, and products tables.
```

### Generate DAX Measures
```
@bi-developer *create-dax
I need measures for:
- Total Sales
- Year-over-Year growth
- Rolling 12-month average
- Top 10 products ranking
```

### Optimize Slow Report
```
@bi-developer Our Power BI report takes 20 seconds to load. 
The dataset has 5 million rows in the fact table.
Can you help optimize it?
```

## Best Practices

1. **Be Specific**: Provide context about your business domain
2. **Describe Users**: Mention who will use the dashboards
3. **State Goals**: What decisions should be supported?
4. **Include Constraints**: Data volume, refresh frequency, security needs

## Integration

This agent integrates with:
- **DataFlow** (Data Engineer) - for source data preparation
- **Wilson** (Architect) - for solution architecture
- **Paula** (PO) - for requirements prioritization

## Troubleshooting

### Agent Not Loading?
1. Verify chatmode file exists at `.github/chatmodes/bi-developer.chatmode.md`
2. Check that `bi-developer-agent/.avanade-core/` folder exists
3. Restart VS Code if needed

### Commands Not Working?
1. Ensure you've activated the agent first
2. Check task files exist in `.avanade-core/tasks/`
3. Use `*help` to verify available commands

## Version

- **Version:** 1.0
- **Created:** January 2026
- **Author:** InsightForge Agent System
