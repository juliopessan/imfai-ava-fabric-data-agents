# BI Requirements: Financial KPI Scorecard
**Generated:** January 28, 2026 12:00 PM  
**Agent:** InsightForge v1.0  
**Scenario:** Executive Financial Dashboard

---

## 📋 Executive Summary

This Financial KPI Scorecard provides executive leadership with real-time visibility into financial performance against budget targets. The dashboard enables rapid identification of variance trends, regional performance patterns, and category-level profitability analysis.

**Business Value:**
- **Immediate visibility** into budget variance across all business dimensions
- **Proactive alerts** for underperforming regions or categories
- **Data-driven decision making** with YTD and MTD performance tracking
- **Accountability** through clear metric ownership and targets

---

## 👥 User Personas

### 1. CFO (Chief Financial Officer)
- **Needs:** High-level financial health overview, board-ready metrics
- **Access:** All regions, all categories
- **Key Metrics:** Total revenue vs budget, profit margin, YTD performance
- **Frequency:** Daily morning review

### 2. Regional Finance Manager
- **Needs:** Regional performance details, drill-down to category level
- **Access:** Assigned region only (RLS)
- **Key Metrics:** Regional variance, category mix, trend analysis
- **Frequency:** Daily monitoring, weekly deep-dive

### 3. Controller
- **Needs:** Detailed variance analysis, forecast accuracy
- **Access:** All data with historical comparison
- **Key Metrics:** Budget utilization %, forecast variance, period-over-period
- **Frequency:** Weekly review, monthly close analysis

---

## 🎯 Functional Requirements

| ID | Requirement | Priority | Acceptance Criteria |
|----|-------------|----------|---------------------|
| FR-01 | Display actual vs budget variance by region | High | Show % variance with conditional formatting (red <90%, yellow 90-95%, green >95%) |
| FR-02 | Calculate YTD and MTD performance | High | Accurate cumulative calculations respecting fiscal calendar |
| FR-03 | Regional performance comparison | High | Side-by-side comparison of all 4 regions (West, East, Central, South) |
| FR-04 | Product category breakdown | Medium | Show top 3 categories with drill-through capability |
| FR-05 | Budget utilization tracking | High | Display % of budget consumed vs % of period elapsed |
| FR-06 | Trend visualization | Medium | Line chart showing 6-month trend of actuals vs budget |
| FR-07 | Alert indicators | High | Visual alerts for >10% negative variance |
| FR-08 | Mobile-responsive design | Medium | All KPIs visible on tablet and mobile devices |
| FR-09 | Export capability | Low | Export to Excel/PDF for board presentations |
| FR-10 | Row-level security | High | Regional managers see only their region |

---

## 📊 Key Performance Indicators (KPIs)

### Primary KPIs

1. **Total Revenue**
   - **Definition:** Sum of all sales transactions
   - **Target:** Budget amount from budget table
   - **Format:** Currency (USD)
   - **Alert:** <90% of budget = Red

2. **Budget Variance %**
   - **Definition:** (Actual - Budget) / Budget * 100
   - **Target:** ≥0% (at or above budget)
   - **Format:** Percentage with 1 decimal
   - **Alert:** <-10% = Critical

3. **YTD Revenue**
   - **Definition:** Cumulative revenue from fiscal year start
   - **Target:** Cumulative budget YTD
   - **Format:** Currency (USD)
   - **Alert:** <95% of YTD budget = Yellow

4. **Budget Utilization Rate**
   - **Definition:** % of annual budget consumed vs % of year elapsed
   - **Target:** Within ±5% of time elapsed
   - **Format:** Percentage
   - **Alert:** >110% of time ratio = Red (overspending)

### Secondary KPIs

5. **Average Transaction Value**
   - **Definition:** Total Revenue / Count of Transactions
   - **Format:** Currency (USD)

6. **Top Region Performance**
   - **Definition:** Region with highest % to budget
   - **Format:** Text with % indicator

7. **Category Mix %**
   - **Definition:** Each category as % of total revenue
   - **Format:** Percentage breakdown

---

## 🗄️ Data Sources

### Source Tables

| Table | Source | Grain | Refresh |
|-------|--------|-------|---------|
| **Sales Transactions** | sales-transactions.csv | One row per order line | Daily 6 AM |
| **Budget** | budget.csv | Month × Region × Category | Monthly |
| **Date Dimension** | Auto-generated | One row per day | Static |
| **Products** | products.csv | One row per product | Weekly |
| **Customers** | customers.csv | One row per customer | Weekly |

### Data Relationships
- Sales → Date (Many-to-One on OrderDate)
- Sales → Products (Many-to-One on ProductName)
- Sales → Budget (Many-to-One on Year, Month, Region, ProductCategory)

---

## 🎨 Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│ FINANCIAL KPI SCORECARD         Filters: YTD ▼     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐        │
│  │ Revenue   │ │ Variance  │ │ Budget    │        │
│  │ $1.2M ▲5% │ │ +$50K ✓   │ │ Util 47%  │        │
│  └───────────┘ └───────────┘ └───────────┘        │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ Revenue vs Budget Trend (6 Months)          │   │
│  │ [Line Chart: Actual vs Budget]              │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  ┌─────────────────┐  ┌──────────────────────┐    │
│  │ Regional Perf   │  │ Category Breakdown   │    │
│  │ [Bar Chart]     │  │ [Pie Chart]          │    │
│  └─────────────────┘  └──────────────────────┘    │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │ Variance Details Table                      │   │
│  │ [Grid with conditional formatting]          │   │
│  └─────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## ✅ Success Criteria

1. **Performance:** Dashboard loads in <3 seconds
2. **Accuracy:** Variance calculations match Excel validation within 0.01%
3. **Usability:** Executives can find key insights in <30 seconds
4. **Adoption:** 90% of target users access dashboard weekly within 1 month
5. **Data Quality:** No null values in KPI cards, budget data 100% complete

---

## 🚀 Implementation Phases

### Phase 1: Data Model (Week 1)
- [ ] Import source files
- [ ] Create star schema with fact and dimensions
- [ ] Define relationships
- [ ] Build Date table with fiscal calendar

### Phase 2: DAX Calculations (Week 1-2)
- [ ] Base measures (Revenue, Budget, Quantity)
- [ ] Variance measures (Absolute, Percentage)
- [ ] Time intelligence (YTD, MTD, PY)
- [ ] KPI measures with formatting

### Phase 3: Dashboard Design (Week 2)
- [ ] Layout wireframe approval
- [ ] Visual selection and configuration
- [ ] Interactivity (cross-filtering, drill-through)
- [ ] Conditional formatting rules

### Phase 4: Testing & UAT (Week 3)
- [ ] Data validation testing
- [ ] Performance testing
- [ ] User acceptance testing with CFO
- [ ] Mobile responsiveness testing

### Phase 5: Deployment (Week 4)
- [ ] Publish to Power BI Service
- [ ] Configure scheduled refresh
- [ ] Implement RLS roles
- [ ] User training sessions

---

## 📝 Assumptions & Constraints

**Assumptions:**
- Budget is set at month/region/category grain
- Sales data is complete and accurate in source system
- Fiscal year aligns with calendar year
- All transactions are in USD

**Constraints:**
- Historical data limited to 2024-2025
- Budget refresh is manual (monthly Excel upload)
- No real-time data connectivity
- Power BI Pro licenses required for all users

---

**Document Owner:** InsightForge BI Developer Agent  
**Approval Required:** CFO, Controller  
**Next Steps:** Review and approve requirements → Proceed to semantic model design
