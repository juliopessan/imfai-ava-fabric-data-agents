# Semantic Model: Sales Analytics
Generated: 2026-01-22 14:30
Agent: InsightForge v1.0

---

## Model Diagram (Star Schema)

```
                            ┌─────────────────┐
                            │   DIM_DATE      │
                            │─────────────────│
                            │ DateKey (PK)    │
                            │ Date            │
                            │ Year            │
                            │ Quarter         │
                            │ Month           │
                            │ MonthName       │
                            │ WeekOfYear      │
                            │ DayOfWeek       │
                            │ IsWeekend       │
                            └────────┬────────┘
                                     │
┌─────────────────┐         ┌────────┴────────┐         ┌─────────────────┐
│  DIM_PRODUCT    │         │  FACT_SALES     │         │  DIM_CUSTOMER   │
│─────────────────│         │─────────────────│         │─────────────────│
│ ProductKey (PK) │◄────────┤ SalesKey (PK)   ├────────►│ CustomerKey(PK) │
│ ProductID       │         │ DateKey (FK)    │         │ CustomerID      │
│ ProductName     │         │ ProductKey (FK) │         │ CustomerName    │
│ ProductCategory │         │ CustomerKey(FK) │         │ CustomerSegment │
│ SubCategory     │         │ RegionKey (FK)  │         │ Region          │
│ Brand           │         │ Quantity        │         │ Country         │
│ UnitCost        │         │ UnitPrice       │         │ City            │
│ ListPrice       │         │ Revenue         │         │ JoinDate        │
│ LaunchDate      │         │ Cost            │         └─────────────────┘
│ ProfitMargin    │         │ Profit          │
└─────────────────┘         │ SalesRepEmail   │         ┌─────────────────┐
                            └────────┬────────┘         │  DIM_REGION     │
                                     │                  │─────────────────│
                            ┌────────┴────────┐         │ RegionKey (PK)  │
                            │  FACT_BUDGET    │         │ Region          │
                            │─────────────────│         │ RegionManager   │
                            │ BudgetKey (PK)  ├────────►│ Timezone        │
                            │ DateKey (FK)    │         └─────────────────┘
                            │ RegionKey (FK)  │
                            │ CategoryKey(FK) │
                            │ BudgetAmount    │
                            │ TargetQuantity  │
                            └─────────────────┘
```

---

## Table Definitions

### FACT_SALES (Fact Table)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| SalesKey | INT | Surrogate primary key | Generated |
| DateKey | INT | FK to DIM_DATE | OrderDate |
| ProductKey | INT | FK to DIM_PRODUCT | ProductName lookup |
| CustomerKey | INT | FK to DIM_CUSTOMER | CustomerSegment lookup |
| RegionKey | INT | FK to DIM_REGION | Region lookup |
| Quantity | INT | Units sold | Quantity |
| UnitPrice | DECIMAL(10,2) | Sale price per unit | UnitPrice |
| Revenue | DECIMAL(12,2) | Quantity × UnitPrice | Calculated |
| Cost | DECIMAL(12,2) | Quantity × UnitCost | Lookup |
| Profit | DECIMAL(12,2) | Revenue - Cost | Calculated |
| SalesRepEmail | VARCHAR(100) | Sales rep identifier | SalesRepEmail |

**Row Count Estimate**: ~10,000/year

### FACT_BUDGET (Fact Table)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| BudgetKey | INT | Surrogate primary key | Generated |
| DateKey | INT | FK to DIM_DATE (Month grain) | Year, Month |
| RegionKey | INT | FK to DIM_REGION | Region |
| CategoryKey | INT | FK to DIM_PRODUCT (Category) | ProductCategory |
| BudgetAmount | DECIMAL(12,2) | Budget target | BudgetAmount |
| TargetQuantity | INT | Quantity target | TargetQuantity |

### DIM_DATE (Dimension)
| Column | Data Type | Description |
|--------|-----------|-------------|
| DateKey | INT | YYYYMMDD format (PK) |
| Date | DATE | Full date |
| Year | INT | Calendar year |
| Quarter | VARCHAR(2) | Q1-Q4 |
| Month | INT | 1-12 |
| MonthName | VARCHAR(20) | January-December |
| WeekOfYear | INT | 1-53 |
| DayOfWeek | INT | 1-7 (Sunday=1) |
| DayName | VARCHAR(20) | Sunday-Saturday |
| IsWeekend | BIT | 1 if Saturday/Sunday |
| FiscalYear | INT | Fiscal year (if different) |
| FiscalQuarter | VARCHAR(2) | Fiscal quarter |

### DIM_PRODUCT (Dimension)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| ProductKey | INT | Surrogate primary key | Generated |
| ProductID | VARCHAR(10) | Natural key | ProductID |
| ProductName | VARCHAR(100) | Product display name | ProductName |
| ProductCategory | VARCHAR(50) | Top-level category | ProductCategory |
| SubCategory | VARCHAR(50) | Sub-category | SubCategory |
| Brand | VARCHAR(50) | Brand name | Brand |
| UnitCost | DECIMAL(10,2) | Standard cost | UnitCost |
| ListPrice | DECIMAL(10,2) | MSRP | ListPrice |
| LaunchDate | DATE | Product launch date | LaunchDate |
| ProfitMargin | DECIMAL(5,2) | (ListPrice-UnitCost)/ListPrice | Calculated |

### DIM_CUSTOMER (Dimension)
| Column | Data Type | Description | Source |
|--------|-----------|-------------|--------|
| CustomerKey | INT | Surrogate primary key | Generated |
| CustomerID | VARCHAR(10) | Natural key | CustomerID |
| CustomerName | VARCHAR(100) | Company name | CustomerName |
| CustomerSegment | VARCHAR(50) | Enterprise/SMB/Consumer | CustomerSegment |
| Region | VARCHAR(50) | Geographic region | Region |
| Country | VARCHAR(50) | Country | Country |
| City | VARCHAR(100) | City | City |
| JoinDate | DATE | Customer since | JoinDate |

### DIM_REGION (Dimension)
| Column | Data Type | Description |
|--------|-----------|-------------|
| RegionKey | INT | Surrogate primary key |
| Region | VARCHAR(50) | West/East/Central/South |
| RegionManager | VARCHAR(100) | Manager name |
| Timezone | VARCHAR(50) | Primary timezone |

---

## Relationships

| From Table | From Column | To Table | To Column | Cardinality | Cross-Filter |
|------------|-------------|----------|-----------|-------------|--------------|
| FACT_SALES | DateKey | DIM_DATE | DateKey | Many-to-One | Single |
| FACT_SALES | ProductKey | DIM_PRODUCT | ProductKey | Many-to-One | Single |
| FACT_SALES | CustomerKey | DIM_CUSTOMER | CustomerKey | Many-to-One | Single |
| FACT_SALES | RegionKey | DIM_REGION | RegionKey | Many-to-One | Single |
| FACT_BUDGET | DateKey | DIM_DATE | DateKey | Many-to-One | Single |
| FACT_BUDGET | RegionKey | DIM_REGION | RegionKey | Many-to-One | Single |

---

## Hierarchies

### Date Hierarchy
```
Year
└── Quarter
    └── Month
        └── Date
```

### Product Hierarchy
```
ProductCategory
└── SubCategory
    └── ProductName
```

### Geography Hierarchy
```
Region
└── Country
    └── City
```

---

## Model Settings

| Setting | Value |
|---------|-------|
| Storage Mode | Import |
| Refresh Schedule | Daily 6:00 AM UTC |
| Row-Level Security | By Region |
| Aggregations | Monthly pre-aggregated table |

---

*Generated by InsightForge BI Developer Agent*
