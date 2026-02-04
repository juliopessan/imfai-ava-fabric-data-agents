# Task: Create Data Model

**Command:** `*data-model` / `*DM`  
**Output:** `data-model.md`

---

## Objective

Create a comprehensive logical data model based on requirements from STTM and architecture documents.

---

## Prerequisites

- [ ] STTM document available
- [ ] Architecture document available
- [ ] KPIs defined
- [ ] Analytical questions documented

---

## Steps

### Step 1: Analyze Requirements

1. Load STTM document
2. Review analytical questions
3. Identify required entities
4. Understand metrics needs

### Step 2: Define Granularity

For each layer, define the grain:

| Layer | Question to Answer |
|-------|-------------------|
| Landing | What is one row from source? |
| Silver | What is one clean entity? |
| Gold Fact | What is one business event? |
| Gold Dim | What is one master entity? |

### Step 3: Design Facts

For each fact table:
- Define grain
- Identify measures
- Identify foreign keys
- Document aggregation rules

### Step 4: Design Dimensions

For each dimension:
- Define grain
- List attributes
- Determine SCD type
- Identify hierarchies

### Step 5: Map Relationships

- Connect facts to dimensions
- Specify cardinality
- Document relationship type
- Create bridge tables if needed

### Step 6: Document Model

Create `data-model.md` with:
- Model overview
- Entity definitions
- Relationships diagram (Mermaid)
- Granularity table
- SCD specifications

---

## Output Template

```markdown
# Data Model

## Overview
[Brief description of the model]

## Entities

### Facts
| Table | Grain | Measures | Keys |
|-------|-------|----------|------|
| fact_X | ... | ... | ... |

### Dimensions
| Table | Grain | SCD Type | Attributes |
|-------|-------|----------|------------|
| dim_X | ... | ... | ... |

## Relationships
[Mermaid ER diagram]

## Granularity
[Table showing grain per layer]
```

---

## Validation

- [ ] All STTM entities covered
- [ ] Granularity defined for all tables
- [ ] Relationships complete
- [ ] SCD types assigned
- [ ] Model supports all analytical questions
