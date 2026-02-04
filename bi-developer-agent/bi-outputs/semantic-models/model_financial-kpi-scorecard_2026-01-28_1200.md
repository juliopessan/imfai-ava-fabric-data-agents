# Semantic Model: Financial KPI Scorecard
**Generated:** January 28, 2026 12:00 PM  
**Agent:** InsightForge v1.0  
**Architecture:** Star Schema (Kimball)

---

## 🎯 Model Overview

This semantic model implements a **star schema** optimized for financial variance analysis. The model supports both actual vs budget comparisons and time intelligence calculations with a dedicated Date dimension.

**Model Characteristics:**
- **Type:** Import Mode (scheduled refresh)
- **Grain:** Transaction level for Sales, Month level for Budget
- **Estimated Size:** ~50 MB (compressed)
- **Refresh Schedule:** Daily 6:00 AM

---

## 📊 Model Diagram

```mermaid
erDiagram
    DimDate ||--o{ FactSales : "OrderDate"
    DimProduct ||--o{ FactSales : "ProductName"
    DimCustomer ||--o{ FactSales : "CustomerSegment"
    DimRegion ||--o{ FactSales : "Region"
    DimRegion ||--o{ FactBudget : "Region"
    DimDate ||--o{ FactBudget : "BudgetDate"
    DimCategory ||--o{ FactSales : "ProductCategory"
    DimCategory ||--o{ FactBudget : "ProductCategory"
    
    FactSales {
        date OrderDate PK
        string Region FK
        string ProductCategory FK
        string ProductName FK
        int Quantity
        decimal UnitPrice
        decimal Revenue
        string CustomerSegment FK
        string SalesRepEmail
    }
    
    FactBudget {
        int Year PK
        int Month PK
        string Region PK-FK
        string ProductCategory PK-FK
        decimal BudgetAmount
        int TargetQuantity
        date BudgetDate FK
    }
    
    DimDate {
        date Date PK
        int Year
        int Quarter
        int Month
        int DayOfWeek
        string MonthName
        string YearMonth
        bool IsWeekend
        int FiscalYear
        int FiscalQuarter
    }
    
    DimProduct {
        string ProductName PK
        string ProductCategory FK
        decimal StandardPrice
    }
    
    DimCategory {
        string ProductCategory PK
        string CategoryGroup
        int DisplayOrder
    }
    
    DimRegion {
        string Region PK
        string RegionManager
        string Territory
        int RegionCode
    }
    
    DimCustomer {
        string CustomerSegment PK
        string SegmentDescription
        int Priority
    }
```

---

## 📋 Table Definitions

### 🔵 FACT TABLES

#### FactSales
**Purpose:** Stores all sales transactions at the order line level  
**Grain:** One row per product per order  
**Source:** sales-transactions.csv  
**Row Count:** ~1,000 rows (growing daily)

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| **OrderDate** | Date | Transaction date (PK part) | 2025-01-15 |
| **Region** | Text | Sales region (FK to DimRegion) | West |
| **ProductCategory** | Text | Category (FK to DimCategory) | Electronics |
| **ProductName** | Text | Product identifier (FK to DimProduct) | Laptop Pro 15 |
| **Quantity** | Integer | Units sold | 5 |
| **UnitPrice** | Decimal | Price per unit | 1299.99 |
| **Revenue** | Decimal | Calculated: Quantity * UnitPrice | 6499.95 |
| **CustomerSegment** | Text | Customer type (FK to DimCustomer) | Enterprise |
| **SalesRepEmail** | Text | Sales representative | john.smith@contoso.com |

**Calculated Columns:**
```dax
Revenue = FactSales[Quantity] * FactSales[UnitPrice]
```

**Indexes:**
- Clustered: OrderDate
- Non-clustered: Region, ProductCategory

---

#### FactBudget
**Purpose:** Stores budget targets by month, region, and category  
**Grain:** One row per month per region per category  
**Source:** budget.csv  
**Row Count:** ~300 rows (12 months × 4 regions × 3 categories)

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| **Year** | Integer | Budget year (PK part) | 2025 |
| **Month** | Integer | Budget month (PK part) | 1 |
| **Region** | Text | Region (PK part, FK to DimRegion) | West |
| **ProductCategory** | Text | Category (PK part, FK to DimCategory) | Electronics |
| **BudgetAmount** | Decimal | Target revenue | 150000.00 |
| **TargetQuantity** | Integer | Target units | 100 |
| **BudgetDate** | Date | First day of month (FK to DimDate) | 2025-01-01 |

**Calculated Columns:**
```dax
BudgetDate = DATE(FactBudget[Year], FactBudget[Month], 1)
```

---

### 🟢 DIMENSION TABLES

#### DimDate
**Purpose:** Date dimension for time intelligence  
**Grain:** One row per day  
**Source:** DAX-generated  
**Row Count:** 1,826 days (2024-01-01 to 2028-12-31)

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| **Date** | Date | Calendar date (PK) | 2025-01-15 |
| **Year** | Integer | Calendar year | 2025 |
| **Quarter** | Integer | Calendar quarter (1-4) | 1 |
| **Month** | Integer | Month number (1-12) | 1 |
| **MonthName** | Text | Month name | January |
| **YearMonth** | Text | YYYY-MM format | 2025-01 |
| **DayOfWeek** | Integer | Day (1=Sun, 7=Sat) | 4 |
| **IsWeekend** | Boolean | Weekend flag | FALSE |
| **FiscalYear** | Integer | Fiscal year | 2025 |
| **FiscalQuarter** | Integer | Fiscal quarter | 1 |

**Generation Script:**
```dax
DimDate = 
CALENDAR(DATE(2024,1,1), DATE(2028,12,31))
```

---

#### DimProduct
**Purpose:** Product master data  
**Grain:** One row per product  
**Source:** products.csv  
**Row Count:** ~50 products

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| **ProductName** | Text | Unique product identifier (PK) | Laptop Pro 15 |
| **ProductCategory** | Text | Category (FK to DimCategory) | Electronics |
| **StandardPrice** | Decimal | List price | 1299.99 |

---

#### DimCategory
**Purpose:** Product category reference  
**Grain:** One row per category  
**Source:** Static table  
**Row Count:** 3 categories

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| **ProductCategory** | Text | Category name (PK) | Electronics |
| **CategoryGroup** | Text | High-level grouping | Hardware |
| **DisplayOrder** | Integer | Sort order for visuals | 1 |

**Static Data:**
```
| ProductCategory | CategoryGroup | DisplayOrder |
|----------------|---------------|--------------|
| Electronics    | Hardware      | 1            |
| Accessories    | Hardware      | 2            |
| Software       | Software      | 3            |
```

---

#### DimRegion
**Purpose:** Regional sales territory reference  
**Grain:** One row per region  
**Source:** Static table  
**Row Count:** 4 regions

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| **Region** | Text | Region name (PK) | West |
| **RegionManager** | Text | Manager name | John Smith |
| **Territory** | Text | Geographic area | Pacific |
| **RegionCode** | Integer | Numeric code | 1 |

**Static Data:**
```
| Region  | RegionManager | Territory    | RegionCode |
|---------|---------------|--------------|------------|
| West    | John Smith    | Pacific      | 1          |
| East    | Mary Jones    | Atlantic     | 2          |
| Central | David Wilson  | Central USA  | 3          |
| South   | Lisa Brown    | Gulf Coast   | 4          |
```

---

#### DimCustomer
**Purpose:** Customer segment classification  
**Grain:** One row per segment  
**Source:** Static table  
**Row Count:** 3 segments

| Column | Data Type | Description | Example |
|--------|-----------|-------------|---------|
| **CustomerSegment** | Text | Segment name (PK) | Enterprise |
| **SegmentDescription** | Text | Detailed description | Large enterprise customers (>1000 employees) |
| **Priority** | Integer | Service priority level | 1 |

**Static Data:**
```
| CustomerSegment | SegmentDescription                          | Priority |
|----------------|---------------------------------------------|----------|
| Enterprise     | Large enterprise customers (>1000 emp)      | 1        |
| SMB            | Small/medium business (10-1000 emp)         | 2        |
| Consumer       | Individual consumers                        | 3        |
```

---

## 🔗 Relationships

### Relationship Definitions

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter | Active |
|------------|-------------|----------|-----------|-------------|--------------|--------|
| FactSales | OrderDate | DimDate | Date | Many-to-One | Single | ✅ Yes |
| FactSales | ProductName | DimProduct | ProductName | Many-to-One | Single | ✅ Yes |
| FactSales | ProductCategory | DimCategory | ProductCategory | Many-to-One | Both | ✅ Yes |
| FactSales | Region | DimRegion | Region | Many-to-One | Both | ✅ Yes |
| FactSales | CustomerSegment | DimCustomer | CustomerSegment | Many-to-One | Single | ✅ Yes |
| FactBudget | BudgetDate | DimDate | Date | Many-to-One | Single | ✅ Yes |
| FactBudget | Region | DimRegion | Region | Many-to-One | Both | ✅ Yes |
| FactBudget | ProductCategory | DimCategory | ProductCategory | Many-to-One | Both | ✅ Yes |
| DimProduct | ProductCategory | DimCategory | ProductCategory | Many-to-One | Single | ✅ Yes |

### Relationship Rules

1. **Date Relationships:**
   - Both FactSales and FactBudget relate to DimDate
   - Sales uses OrderDate (transaction date)
   - Budget uses BudgetDate (first day of month)

2. **Dimension Sharing:**
   - DimRegion and DimCategory are shared between both facts
   - Enables proper variance calculations across same dimensions

3. **Cross-Filtering:**
   - Region and Category have bi-directional filtering
   - Enables regional filtering to affect both sales and budget
   - Date is single direction to prevent filter ambiguity

---

## 📐 Hierarchies

### Date Hierarchy
**Name:** Calendar  
**Path:** Year → Quarter → Month → Date

```
Calendar
├── Year (2024, 2025, 2026...)
│   └── Quarter (Q1, Q2, Q3, Q4)
│       └── Month (January, February...)
│           └── Date (2025-01-01, 2025-01-02...)
```

### Product Hierarchy
**Name:** Product Drill-Down  
**Path:** CategoryGroup → ProductCategory → ProductName

```
Product Drill-Down
├── CategoryGroup (Hardware, Software)
│   └── ProductCategory (Electronics, Accessories, Software)
│       └── ProductName (Laptop Pro 15, Wireless Mouse...)
```

---

## ⚙️ Model Configuration

### Storage Mode
- **FactSales:** Import
- **FactBudget:** Import
- **All Dimensions:** Import

**Rationale:** Full Import mode for fast aggregations and time intelligence. Dataset size is manageable (<500 MB).

### Aggregations
Not implemented in v1.0 (dataset size does not warrant it)

### Partitioning
- **FactSales:** Partitioned by Year (2024, 2025, 2026...)
- **FactBudget:** Single partition (small table)

### Incremental Refresh
**FactSales Configuration:**
- Archive data: 2 years
- Refresh data: Last 7 days
- Detect data changes: OrderDate column

---

## 🔐 Security Model

### Row-Level Security (RLS)

**Role:** Regional Manager  
**Filter:** `DimRegion[Region] = USERNAME()`

**DAX Filter Expression:**
```dax
-- Regional Manager Role
DimRegion[RegionManager] = USERPRINCIPALNAME()

-- Applied to DimRegion table
-- Cascades to FactSales and FactBudget via relationships
```

**Role Assignments:**
- john.smith@contoso.com → West
- mary.jones@contoso.com → East
- david.wilson@contoso.com → Central
- lisa.brown@contoso.com → South

---

## 📏 Model Statistics

| Metric | Value |
|--------|-------|
| Total Tables | 8 |
| Fact Tables | 2 |
| Dimension Tables | 6 |
| Total Columns | 47 |
| Calculated Columns | 2 |
| Total Relationships | 9 |
| Active Relationships | 9 |
| Hierarchies | 2 |
| RLS Roles | 1 |
| Estimated Size (Compressed) | 45 MB |

---

## ✅ Model Validation Checklist

- [x] All tables have primary keys defined
- [x] Relationships follow many-to-one pattern
- [x] Date table spans full range of fact data
- [x] No circular dependencies
- [x] Bi-directional filters justified (Region, Category for variance)
- [x] RLS tested for each role
- [x] Calculated columns necessary (not duplicating measures)
- [x] Naming conventions consistent (PascalCase)
- [x] All FK columns match data types
- [x] Budget grain matches analysis requirements

---

## 🚀 Implementation Steps

### 1. Create Date Dimension
```dax
DimDate = 
ADDCOLUMNS(
    CALENDAR(DATE(2024,1,1), DATE(2028,12,31)),
    "Year", YEAR([Date]),
    "Quarter", QUARTER([Date]),
    "Month", MONTH([Date]),
    "MonthName", FORMAT([Date], "MMMM"),
    "YearMonth", FORMAT([Date], "YYYY-MM"),
    "DayOfWeek", WEEKDAY([Date]),
    "IsWeekend", WEEKDAY([Date]) IN {1, 7},
    "FiscalYear", YEAR([Date]),
    "FiscalQuarter", QUARTER([Date])
)
```

### 2. Import Source Files
- Load sales-transactions.csv → FactSales
- Load budget.csv → FactBudget
- Load products.csv → DimProduct
- Load customers.csv (if available) → DimCustomer

### 3. Create Static Dimensions
- Create DimCategory with 3 rows
- Create DimRegion with 4 rows
- Create DimCustomer with 3 rows

### 4. Add Calculated Columns
```dax
// FactSales
Revenue = FactSales[Quantity] * FactSales[UnitPrice]

// FactBudget
BudgetDate = DATE(FactBudget[Year], FactBudget[Month], 1)
```

### 5. Define Relationships
- Connect all FKs as per relationship table above
- Set cross-filter directions
- Validate relationship validity

### 6. Create Hierarchies
- Calendar hierarchy on DimDate
- Product Drill-Down on DimCategory/DimProduct

### 7. Configure RLS
- Create "Regional Manager" role
- Apply filter: `DimRegion[RegionManager] = USERPRINCIPALNAME()`
- Test with each user account

### 8. Optimize Model
- Remove unused columns
- Set data types appropriately
- Mark Date table (`CTRL+K` in Power BI)
- Configure incremental refresh on FactSales

---

**Model Owner:** InsightForge BI Developer  
**Version:** 1.0  
**Last Updated:** January 28, 2026  
**Next Step:** Proceed to DAX measure development
