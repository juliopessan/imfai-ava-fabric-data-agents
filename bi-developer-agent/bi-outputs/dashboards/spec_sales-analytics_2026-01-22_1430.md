# Dashboard Specification: Sales Analytics
Generated: 2026-01-22 14:30
Agent: InsightForge v1.0

---

## Dashboard Overview

| Property | Value |
|----------|-------|
| Dashboard Name | Sales Analytics Dashboard |
| Target Audience | Sales Leadership, Regional Managers |
| Primary Purpose | Monitor sales performance, track KPIs, identify trends |
| Refresh Schedule | Daily at 6:00 AM |
| Mobile Optimized | Yes |

---

## Page Layout

### Page 1: Executive Summary

```
┌────────────────────────────────────────────────────────────────────────┐
│  HEADER: Sales Analytics Dashboard                    [Date Slicer ▼]  │
├────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │ TOTAL REVENUE│ │ TOTAL QTY    │ │ AVG ORDER    │ │ VS BUDGET    │   │
│  │   $1.2M      │ │    2,450     │ │    $489      │ │   +12.3%     │   │
│  │   ▲ 15.2% YoY│ │   ▲ 8.1% YoY │ │   ▲ 6.5% YoY │ │   ● On Track │   │
│  └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘   │
├────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────┐ ┌────────────────────────────────┐ │
│  │                                │ │                                │ │
│  │   REVENUE TREND (Line Chart)  │ │   REVENUE BY REGION (Bar)      │ │
│  │                                │ │                                │ │
│  │   [Monthly trend with LY]     │ │   West  ████████████  $450K    │ │
│  │                                │ │   East  █████████    $380K    │ │
│  │                                │ │   Central ███████   $250K     │ │
│  │                                │ │   South ██████     $200K      │ │
│  └────────────────────────────────┘ └────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────┐ ┌────────────────────────────────┐ │
│  │                                │ │                                │ │
│  │  REVENUE BY CATEGORY (Donut)  │ │   TOP 10 PRODUCTS (Table)      │ │
│  │                                │ │                                │ │
│  │     ┌─────┐                   │ │   1. Laptop Pro 17    $48K     │ │
│  │    /  65%  \  Electronics     │ │   2. Desktop Station  $38K     │ │
│  │   │  20%   │  Software        │ │   3. Laptop Pro 15    $32K     │ │
│  │    \  15% /   Accessories     │ │   4. Office Suite     $28K     │ │
│  │     └─────┘                   │ │   5. Smartphone Z     $24K     │ │
│  │                                │ │   ...                          │ │
│  └────────────────────────────────┘ └────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  FOOTER: Last Updated: Jan 22, 2026 6:00 AM | InsightForge Dashboard   │
└────────────────────────────────────────────────────────────────────────┘
```

### Page 2: Regional Deep Dive

```
┌────────────────────────────────────────────────────────────────────────┐
│  HEADER: Regional Performance              [Region Slicer ▼] [Date ▼]  │
├────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                                                                  │  │
│  │                    REGIONAL MAP (Filled Map)                     │  │
│  │                    [USA map with revenue by region]              │  │
│  │                                                                  │  │
│  └──────────────────────────────────────────────────────────────────┘  │
├────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────┐ ┌──────────────────────────────────┐ │
│  │                              │ │                                  │ │
│  │  REGION PERFORMANCE MATRIX   │ │  SALES REP LEADERBOARD           │ │
│  │  (Matrix with conditional)   │ │  (Bar chart)                     │ │
│  │                              │ │                                  │ │
│  │  Region | Revenue | vs LY    │ │  john.smith    ████████  $180K   │ │
│  │  West   | $450K   | +18%     │ │  mary.jones    ██████    $145K   │ │
│  │  East   | $380K   | +12%     │ │  david.wilson  █████     $120K   │ │
│  │  ...                         │ │  lisa.brown    ████      $95K    │ │
│  └──────────────────────────────┘ └──────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

### Page 3: Product Analysis

```
┌────────────────────────────────────────────────────────────────────────┐
│  HEADER: Product Performance          [Category ▼] [Brand ▼] [Date ▼]  │
├────────────────────────────────────────────────────────────────────────┤
│  ┌────────────────────────────────┐ ┌────────────────────────────────┐ │
│  │                                │ │                                │ │
│  │  CATEGORY TREEMAP              │ │  PRODUCT SCATTER PLOT          │ │
│  │  [Hierarchical view]           │ │  [Revenue vs Margin]           │ │
│  │                                │ │                                │ │
│  │  ┌─────────────────┬─────────┐│ │        High Margin             │ │
│  │  │   Electronics   │Software ││ │     *         *                │ │
│  │  │                 │         ││ │  *      *  *                   │ │
│  │  │                 ├─────────┤│ │     Low Revenue ──► High Rev   │ │
│  │  │                 │ Access. ││ │                                │ │
│  │  └─────────────────┴─────────┘│ │                                │ │
│  └────────────────────────────────┘ └────────────────────────────────┘ │
├────────────────────────────────────────────────────────────────────────┤
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │                    PRODUCT DETAIL TABLE                          │  │
│  │  Product | Category | Revenue | Qty | Margin | YoY | Rank        │  │
│  │  ────────────────────────────────────────────────────────────    │  │
│  │  Laptop Pro 17 | Electronics | $48K | 45 | 34% | +22% | 1       │  │
│  │  Desktop Station | Electronics | $38K | 20 | 37% | +15% | 2     │  │
│  │  ...                                                             │  │
│  └──────────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## Visual Specifications

### KPI Cards

| KPI | Measure | Format | Trend Indicator |
|-----|---------|--------|-----------------|
| Total Revenue | [Total Revenue] | $#,##0 | [Revenue YoY %] with ▲/▼ |
| Total Quantity | [Total Quantity] | #,##0 | [Quantity YoY %] with ▲/▼ |
| Avg Order Value | [Average Order Value] | $#,##0 | [AOV YoY %] with ▲/▼ |
| Budget Variance | [Revenue vs Budget %] | +#0.0%;-#0.0% | [Budget Status] icon |

### Charts

| Visual | Type | X-Axis | Y-Axis | Legend |
|--------|------|--------|--------|--------|
| Revenue Trend | Line | DIM_DATE[Month] | [Total Revenue], [Revenue LY] | Current/Prior Year |
| Revenue by Region | Clustered Bar | DIM_REGION[Region] | [Total Revenue] | N/A |
| Revenue by Category | Donut | DIM_PRODUCT[ProductCategory] | [Total Revenue] | Category |
| Top 10 Products | Table | DIM_PRODUCT[ProductName] | [Total Revenue], [Revenue YoY %] | N/A |

### Conditional Formatting

| Visual | Condition | Color |
|--------|-----------|-------|
| YoY Change | >= 10% | Green (#107C10) |
| YoY Change | 0% to 10% | Teal (#008272) |
| YoY Change | -10% to 0% | Yellow (#FFB900) |
| YoY Change | < -10% | Red (#D13438) |
| Budget Status | >= 100% | Green (#107C10) |
| Budget Status | 90-100% | Teal (#008272) |
| Budget Status | 75-90% | Yellow (#FFB900) |
| Budget Status | < 75% | Red (#D13438) |

---

## Interactivity

### Slicers

| Slicer | Type | Field | Default |
|--------|------|-------|---------|
| Date Range | Date range picker | DIM_DATE[Date] | Current month |
| Region | Dropdown | DIM_REGION[Region] | All |
| Category | Checkbox | DIM_PRODUCT[ProductCategory] | All |
| Segment | Dropdown | DIM_CUSTOMER[CustomerSegment] | All |

### Cross-Filtering

| Source Visual | Target Visuals | Behavior |
|---------------|----------------|----------|
| Revenue by Region | All visuals | Filter |
| Revenue by Category | All visuals | Filter |
| Revenue Trend | KPIs only | Highlight |

### Drill-Through

| Source | Target Page | Fields Passed |
|--------|-------------|---------------|
| Region bar chart | Regional Deep Dive | DIM_REGION[Region] |
| Product table | Product Detail | DIM_PRODUCT[ProductKey] |

---

## Mobile Layout

The dashboard includes a dedicated mobile view with:
- Stacked KPI cards (vertical scroll)
- Full-width charts
- Collapsible slicer panel
- Touch-optimized interactions

---

## Color Palette

| Element | Color | Hex |
|---------|-------|-----|
| Primary | Blue | #0078D4 |
| Secondary | Teal | #008272 |
| Positive | Green | #107C10 |
| Negative | Red | #D13438 |
| Warning | Yellow | #FFB900 |
| Background | Light Gray | #F3F2F1 |
| Text | Dark Gray | #323130 |

---

*Generated by InsightForge BI Developer Agent*
