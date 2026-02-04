# Dashboard Specification: Financial KPI Scorecard
**Generated:** January 28, 2026 12:00 PM  
**Agent:** InsightForge v1.0  
**Dashboard Type:** Executive Financial Dashboard

---

## 📋 Overview

**Purpose:** Provide executives with at-a-glance visibility into financial performance against budget targets with drill-down capabilities for regional and category analysis.

**Audience:** CFO, Controllers, Regional Finance Managers  
**Update Frequency:** Daily (6:00 AM refresh)  
**Estimated Load Time:** <3 seconds  
**Mobile Optimized:** Yes (responsive layout)

---

## 🎨 Dashboard Layout

### Page 1: Executive Summary

```
┌────────────────────────────────────────────────────────────────────┐
│  FINANCIAL KPI SCORECARD                    📅 Period: YTD 2025   │
│  Updated: Today 6:00 AM                     🔍 Filter: All Regions │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │
│  │ REVENUE      │  │ VARIANCE     │  │ BUDGET UTIL  │            │
│  │              │  │              │  │              │            │
│  │  $1.24M ✓    │  │  +$52K ✓     │  │   47.2% →    │            │
│  │  +5.2% YoY   │  │  +4.3%       │  │  (48% time)  │            │
│  └──────────────┘  └──────────────┘  └──────────────┘            │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Revenue vs Budget Trend (Last 6 Months)                      │ │
│  │                                                              │ │
│  │  $250K ┤                                          ╭──●      │ │
│  │        │                               ╭──●──────╯          │ │
│  │  $200K ┤                    ╭──●──────╯                     │ │
│  │        │         ╭──●──────╯                                │ │
│  │  $150K ┤  ●──────╯                                          │ │
│  │        │                                                     │ │
│  │        └────┬─────┬─────┬─────┬─────┬─────                 │ │
│  │           Aug   Sep   Oct   Nov   Dec   Jan                │ │
│  │                                                              │ │
│  │  Legend: ● Actual   ▬ Budget                               │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌─────────────────────────┐  ┌──────────────────────────────┐   │
│  │ Regional Performance    │  │ Category Mix                 │   │
│  │                         │  │                              │   │
│  │ West    ████████ $402K  │  │  ┌─────────────┐            │   │
│  │ East    ██████ $318K    │  │  │             │ Electronics│   │
│  │ Central ████ $248K      │  │  │   58.3%     │    $723K   │   │
│  │ South   ███ $192K       │  │  │             │            │   │
│  │                         │  │  └─────┬───────┘            │   │
│  │ ✓ All above budget      │  │    25.1%│  Accessories      │   │
│  └─────────────────────────┘  │        │     $311K          │   │
│                                │    16.6% Software $206K     │   │
│                                └──────────────────────────────┘   │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │ Variance Details by Region & Category                       │ │
│  ├─────────┬──────────┬─────────┬───────────┬─────────┬────────┤ │
│  │ Region  │ Category │ Actual  │ Budget    │ Var ($) │ Var %  │ │
│  ├─────────┼──────────┼─────────┼───────────┼─────────┼────────┤ │
│  │ West    │ Electron │ $234K   │ $225K     │ +$9K    │ +4.0% ✓│ │
│  │ West    │ Accessor │ $98K    │ $95K      │ +$3K    │ +3.2% ✓│ │
│  │ East    │ Electron │ $186K   │ $180K     │ +$6K    │ +3.3% ✓│ │
│  │ Central │ Software │ $72K    │ $75K      │ -$3K    │ -4.0% ⚠│ │
│  │ ...     │ ...      │ ...     │ ...       │ ...     │ ...    │ │
│  └─────────┴──────────┴─────────┴───────────┴─────────┴────────┘ │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```

---

## 🎨 Visual Specifications

### Visual 1: Revenue KPI Card

**Type:** Card (KPI)  
**Size:** 300px × 200px  
**Position:** Top row, left

**Data:**
- **Primary Value:** `[Total Revenue]`
- **Secondary Value:** `[Revenue YoY Growth]` (with arrow indicator)
- **Status Icon:** `[Budget Alert Icon]`

**Formatting:**
- Primary: $#,##0.0K or $#,##0.0M
- Font: Segoe UI, Bold, 42pt
- Secondary: Percentage, 18pt
- Background: White with subtle shadow
- Border: Left border colored by variance status

**Conditional Formatting:**
```
IF [Total Revenue] >= [Total Budget]:
    Border Color: #107C10 (Green)
    Icon: ✓
ELSE IF [Variance (%)] >= -0.10:
    Border Color: #F7630C (Orange)
    Icon: ⚠
ELSE:
    Border Color: #D13438 (Red)
    Icon: ✖
```

**Tooltip:**
```
Revenue: $1,240,000
Budget: $1,188,000
Variance: +$52,000 (+4.3%)
Status: Above Target
```

---

### Visual 2: Variance KPI Card

**Type:** Card (KPI)  
**Size:** 300px × 200px  
**Position:** Top row, center

**Data:**
- **Primary Value:** `[Variance (Absolute)]`
- **Secondary Value:** `[Variance (%)]`
- **Status:** `[Variance Status]` text

**Formatting:**
- Primary: +$#,##0.0K (show sign)
- Color by value: Green if positive, Red if negative
- Font: Segoe UI Semibold, 36pt
- Background gradient based on variance %

---

### Visual 3: Budget Utilization Card

**Type:** Gauge Chart  
**Size:** 300px × 200px  
**Position:** Top row, right

**Data:**
- **Value:** `[Budget Utilization %]`
- **Target:** `[Time Elapsed %]`
- **Max:** 100%

**Formatting:**
- Gauge color: Blue (#0078D4)
- Target line: Dashed black
- Value label: ##0.0% format
- Secondary label: "vs X% of year elapsed"

**Threshold Colors:**
- 0-40%: Blue (on track)
- 41-50%: Green (healthy pacing)
- 51-110%: Orange (monitor)
- >110%: Red (overspending)

---

### Visual 4: Revenue vs Budget Trend

**Type:** Line and Clustered Column Chart  
**Size:** 1200px × 350px  
**Position:** Second row, full width

**Axis:**
- **X-Axis:** `DimDate[YearMonth]` (last 6 months)
- **Y-Axis:** Currency, 0 to max(Revenue) * 1.1

**Series:**
- **Line 1 (Actual):** `[Total Revenue]` - Solid blue line, 3px, with data markers
- **Line 2 (Budget):** `[Total Budget]` - Dashed gray line, 2px
- **Column:** `[Variance (Absolute)]` - Conditional color (green/red)

**Formatting:**
- Grid lines: Horizontal only, light gray
- Legend: Top right
- Data labels: On columns only
- Tooltips: Show all series with variance %

**Interactivity:**
- Cross-highlight with region/category visuals
- Drill-down from month to week to day

---

### Visual 5: Regional Performance Bar Chart

**Type:** Horizontal Bar Chart  
**Size:** 500px × 350px  
**Position:** Third row, left

**Axis:**
- **Y-Axis:** `DimRegion[Region]` (sorted by revenue descending)
- **X-Axis:** `[Total Revenue]`

**Bars:**
- Color: Conditional by `[Variance (%)]`
  - Green: ≥0%
  - Orange: -5% to 0%
  - Red: <-5%
- Data labels: Revenue amount and variance %

**Formatting:**
- Bar height: 40px
- Spacing: 10px
- Data labels: Inside end, white text
- Title: "Regional Performance - YTD"

**Interactivity:**
- Click to filter entire dashboard
- Tooltip shows: Revenue, Budget, Variance ($), Variance (%), Rank

---

### Visual 6: Category Mix Pie Chart

**Type:** Donut Chart  
**Size:** 500px × 350px  
**Position:** Third row, right

**Data:**
- **Values:** `[Total Revenue]`
- **Legend:** `DimCategory[ProductCategory]`
- **Detail Labels:** `[% of Total Revenue]`

**Formatting:**
- Colors: 
  - Electronics: #0078D4 (Blue)
  - Accessories: #50E6FF (Cyan)
  - Software: #8764B8 (Purple)
- Inner radius: 60% (donut)
- Data labels: Outside with leader lines
- Center text: "Total Revenue" with amount

**Interactivity:**
- Click to filter dashboard
- Hover shows breakdown by region

---

### Visual 7: Variance Detail Table

**Type:** Matrix (Table)  
**Size:** 1200px × 300px  
**Position:** Fourth row, full width

**Rows:**
- `DimRegion[Region]`
- `DimCategory[ProductCategory]`

**Values:**
- `[Total Revenue]`
- `[Total Budget]`
- `[Variance (Absolute)]`
- `[Variance (%)]`

**Formatting:**
- Header: Bold, dark background
- Alternating row colors: White/Light gray
- Number formatting:
  - Revenue/Budget: $#,##0
  - Variance ($): +$#,##0;-$#,##0
  - Variance (%): +0.0%;-0.0%

**Conditional Formatting:**
- Variance (%) column:
  - Background color gradient: Red (-10%) → Yellow (0%) → Green (+5%)
  - Font color: White if background dark
  - Icon set: ✖ (red), ⚠ (yellow), ✓ (green)

**Interactivity:**
- Sort by any column
- Drill-down to product level
- Right-click for "Analyze" options

---

## 🎛️ Filters & Slicers

### Filter Panel (Left Sidebar)

**Width:** 200px  
**Background:** Light gray (#F3F2F1)

#### Slicer 1: Date Range
**Type:** Relative Date Slicer  
**Options:** YTD, MTD, Last 6 Months, Last 12 Months, Custom Range  
**Default:** YTD

#### Slicer 2: Region
**Type:** Dropdown (multi-select)  
**Values:** `DimRegion[Region]`  
**Default:** All  
**RLS Applied:** Yes (managers see only their region)

#### Slicer 3: Category
**Type:** Checkbox List  
**Values:** `DimCategory[ProductCategory]`  
**Default:** All selected

#### Slicer 4: Customer Segment
**Type:** Dropdown  
**Values:** `DimCustomer[CustomerSegment]`  
**Default:** All

---

## 📱 Mobile Layout

### Portrait Mode (Phone)

```
┌────────────────────┐
│ KPI SCORECARD      │
│ Period: YTD        │
├────────────────────┤
│ Revenue      $1.2M │
│ Variance     +$52K │
│ Budget Util   47%  │
├────────────────────┤
│ [Trend Chart]      │
│ (6M simplified)    │
├────────────────────┤
│ [Regional Bars]    │
│ (Top 4 regions)    │
├────────────────────┤
│ [Category Donut]   │
├────────────────────┤
│ [Summary Table]    │
│ (Collapsed view)   │
└────────────────────┘
```

**Mobile Optimizations:**
- KPI cards stacked vertically
- Trend chart shows 3 months instead of 6
- Table shows top 5 rows with "View More" button
- Filters collapse to hamburger menu
- Touch-friendly tap targets (min 44px)

---

## 🎨 Color Palette

### Primary Colors
- **Primary Blue:** #0078D4 (Microsoft Blue)
- **Success Green:** #107C10
- **Warning Orange:** #F7630C
- **Error Red:** #D13438

### Background Colors
- **Page Background:** #FAFAFA
- **Card Background:** #FFFFFF
- **Table Header:** #E1DFDD
- **Alternate Row:** #F3F2F1

### Text Colors
- **Primary Text:** #201F1E
- **Secondary Text:** #605E5C
- **Disabled Text:** #A19F9D

### Data Colors (Categories)
- **Electronics:** #0078D4
- **Accessories:** #50E6FF
- **Software:** #8764B8

---

## 🔧 Interactivity Design

### Cross-Filtering Rules

| Source Visual | Filters Target Visuals | Behavior |
|---------------|------------------------|----------|
| Trend Chart (month click) | All except date slicer | Highlight |
| Regional Bars | All | Filter |
| Category Donut | All | Filter |
| Detail Table (row click) | All | Filter |

### Drill-Through Configuration

**From:** Variance Detail Table  
**To:** New page "Category Deep Dive"  
**Pass Filters:** Region, Category, Date Range  
**Button:** Right-click on row → "Drill through to details"

### Tooltips

**Custom Tooltip Page:** "Variance Tooltip"

**Contains:**
- Sparkline of 3-month trend
- YoY comparison
- Rank within dimension
- Top 3 contributing products

**Applied To:** All charts (except KPI cards)

---

## 🚀 Performance Optimization

### Visual-Level Filters
- Apply category filter at visual level to avoid query overhead
- Limit detail table to top 20 rows, use "See More" button

### Query Reduction
- Use common date filter across all visuals
- Avoid bi-directional relationships in visuals when possible
- Pre-aggregate variance calculations in measures (not visual filters)

### Rendering
- Load KPI cards first (priority rendering)
- Lazy load detail table (below fold)
- Optimize images (PNG compressed, max 100KB)

---

## ✅ Accessibility Standards

### WCAG 2.1 AA Compliance

**Color Contrast:**
- Text on background: Minimum 4.5:1 ratio
- KPI values: 7:1 ratio (AAA)
- Avoid color as only indicator (use icons + color)

**Screen Reader Support:**
- Alt text for all visuals
- Proper heading hierarchy (H1 → H2 → H3)
- Keyboard navigation enabled
- Tab order optimized

**Responsive Design:**
- Minimum font size: 12pt
- Touch targets: Minimum 44×44 pixels
- No horizontal scrolling on mobile

---

## 📊 Dashboard Metadata

| Property | Value |
|----------|-------|
| **Creator** | InsightForge BI Developer |
| **Version** | 1.0 |
| **Last Updated** | January 28, 2026 |
| **Refresh Schedule** | Daily 6:00 AM |
| **Data Sensitivity** | Confidential (Financial) |
| **Certification** | Pending |
| **Workspace** | Finance Analytics |
| **Endorsement** | CFO Approved |

---

## 📝 User Guide Summary

### Getting Started
1. Dashboard opens to YTD view (default)
2. All regions and categories selected
3. Scroll down for detailed variance table

### Key Actions
- **Filter by date:** Use date range slicer (top right)
- **Drill into region:** Click region bar in regional chart
- **View details:** Right-click table row → Drill through
- **Export data:** Click "..." menu on visual → Export data

### Understanding KPIs
- **Green ✓:** Performance above target
- **Yellow ⚠:** Within acceptable range (±5%)
- **Red ✖:** Critical variance (>10% below target)

---

## 🔍 Testing Checklist

- [ ] All visuals render correctly on desktop
- [ ] Mobile layout displays properly on phone/tablet
- [ ] Cross-filtering works as expected
- [ ] Drill-through navigates correctly
- [ ] Tooltips display complete information
- [ ] Filters apply across all visuals
- [ ] RLS restricts data appropriately per user
- [ ] Export to Excel/PDF functions work
- [ ] Performance: Dashboard loads in <3 seconds
- [ ] Accessibility: Screen reader compatible
- [ ] Color contrast meets WCAG AA standards
- [ ] Data accuracy: Variance calculations match Excel

---

**Dashboard Owner:** InsightForge BI Developer  
**Stakeholder Approval:** CFO, Finance Controller  
**Next Step:** Build dashboard in Power BI Desktop using this specification
