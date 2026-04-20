# Task: Scan Source Platform

```yaml
task_id: scan-repo
agent: discovery-scout
version: "4.0"
command: "*scan-repo"
phase: UPSTREAM
gate: 1
output: "inventory.json"
output_folder: "./discovery-outputs/inventory/"
```

---

## Purpose

Scan the entire source platform to discover and catalog every object — databases, tables, views, stored procedures, pipelines, jobs, scripts, configurations, and connections. This task produces the foundational inventory that all subsequent agents depend on.

---

## Pre-Conditions

- [ ] Source platform connection configuration available (`source-connection-config.yaml`)
- [ ] Read-only access credentials validated
- [ ] Target output directory exists
- [ ] Migration plan received from Migration Coordinator (optional but recommended)

---

## Execution Steps

### Step 1 — Connect to Source Platform

```
1.1  Load connection configuration from source-connection-config.yaml
1.2  Identify platform type (Cloudera, SSIS, Airflow, Informatica, SAP BODS)
1.3  Initialize appropriate connector/parser
1.4  Test connectivity and validate permissions
1.5  Log connection status and metadata
```

### Step 2 — Scan Databases & Schemas

```
2.1  Enumerate all databases/schemas in the environment
2.2  For each database:
     - List all tables (with row counts, sizes, partitions)
     - List all views (with underlying queries)
     - List all stored procedures/functions
     - List all indexes and constraints
2.3  Record schema metadata (creation date, last modified, owner)
2.4  Log any access errors or restricted objects
```

### Step 3 — Scan Pipelines & Jobs

```
3.1  Enumerate all ETL pipelines/dataflows
3.2  For each pipeline:
     - Extract source and target connections
     - List all transformations/steps
     - Identify custom code (UDFs, scripts)
     - Record scheduling information
3.3  Enumerate all orchestration jobs
3.4  For each job:
     - Extract execution sequence
     - Record dependencies and triggers
     - Note last execution date and status
```

### Step 4 — Extract Metadata

```
4.1  For every discovered object, extract:
     - Object name, type, location
     - Creation date, last modified date
     - Owner/creator
     - Size (where applicable)
     - Dependencies (references to other objects)
     - Tags/labels/categories
4.2  Normalize metadata to standard schema
4.3  Assign unique IDs to each object
```

### Step 5 — Catalog & Persist

```
5.1  Compile all objects into inventory.json
5.2  Generate summary statistics:
     - Total objects by type
     - Total databases/schemas
     - Total pipelines and jobs
     - Total data volume (estimated)
5.3  Save inventory.json to ./discovery-outputs/inventory/
5.4  Log scan completion with metrics
```

---

## Output Schema

```json
{
  "scan_metadata": {
    "scan_id": "string",
    "scan_date": "YYYY-MM-DD",
    "platform": "string",
    "duration_seconds": 0,
    "total_objects": 0
  },
  "databases": [
    {
      "name": "string",
      "tables": [],
      "views": [],
      "procedures": []
    }
  ],
  "pipelines": [],
  "jobs": [],
  "scripts": [],
  "connections": []
}
```

---

## Error Handling

| Error                        | Action                                         |
|------------------------------|-------------------------------------------------|
| Connection timeout           | Retry 3x with exponential backoff, then log error |
| Permission denied            | Log object as restricted, continue scan         |
| Unsupported object type      | Log warning, add to inventory with type=UNKNOWN |
| Partial metadata             | Log warning, add with available fields          |

---

## Completion Criteria

- [ ] All databases/schemas enumerated
- [ ] All tables, views, procedures cataloged
- [ ] All pipelines and jobs discovered
- [ ] Metadata extracted for every object
- [ ] inventory.json generated and saved
- [ ] Summary statistics logged
- [ ] Zero unrecoverable errors (warnings acceptable)

---

> **Task**: `scan-repo` · **Agent**: Discovery Scout 🔍 · **Phase**: UPSTREAM · **Gate**: 1
