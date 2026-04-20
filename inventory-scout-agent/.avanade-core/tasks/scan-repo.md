# Task: Scan Repository (*scan-repo)

**Command:** `*scan-repo`  
**Agent:** InventoryScout (Scout 🔍)  
**Phase:** UPSTREAM  
**Priority:** MANDATORY (First step)

---

## Purpose

Recursively scan a legacy data platform repository to identify all files, categorize by extension, calculate statistics, and generate the initial inventory map.

---

## When to Use

- ✅ **First step** in inventory process (always run this first)
- ✅ Starting a migration project
- ✅ Need complete file inventory
- ✅ Understanding repository structure
- ✅ Before any other Scout commands

---

## Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Repository Path | String | Yes | Absolute or relative path to repository root |
| Include Hidden | Boolean | No | Include hidden files/folders (default: false) |
| Max Depth | Integer | No | Maximum directory depth (default: unlimited) |
| Exclude Patterns | List | No | Patterns to exclude (e.g., node_modules, .git) |

---

## Process

### Step 1: Initialize Scan
```
1. Validate repository path exists
2. Initialize file counters
3. Set exclusion patterns (.git, node_modules, etc.)
4. Start recursive traversal
```

### Step 2: Traverse Directories
```
For each directory:
  1. List all files and subdirectories
  2. Apply exclusion patterns
  3. Record directory structure
  4. Track depth level
```

### Step 3: Categorize Files
```
For each file:
  1. Extract file extension
  2. Calculate file size
  3. Record full path
  4. Increment extension counter
  5. Detect file type (pipeline, config, code, etc.)
```

### Step 4: Calculate Statistics
```
1. Total files count
2. Total size (GB/MB)
3. Files by extension (with percentages)
4. Directory count
5. Maximum depth reached
6. Average files per directory
```

### Step 5: Identify Hot Spots
```
1. Directories with most files
2. Largest files (> 1000 lines or > 1 MB)
3. Duplicate file names
4. Unusual file types
```

### Step 6: Flag Issues
```
Scan for:
  ⚠️ Hard-coded credentials (patterns: password=, apiKey=)
  ⚠️ Large files (> 2000 lines)
  ⚠️ Binary files in source control
  ⚠️ Missing documentation (no README)
```

### Step 7: Generate Directory Tree
```
Create ASCII tree representation:
  repository/
  ├── folder1/
  │   ├── subfolder1/
  │   └── subfolder2/
  └── folder2/
```

---

## Outputs

### Primary Output
**File:** `inventory-outputs/inventory-map.md`

**Contents:**
```markdown
# Repository Inventory Map

## Summary Statistics
- Total Files: 1,247
- Total Size: 3.2 GB
- Directories: 89
- Max Depth: 7 levels

## Files by Extension
| Extension | Count | % | Purpose |
|-----------|-------|---|---------|
| .py | 342 | 27.4% | Python scripts |
| .json | 298 | 23.9% | ADF pipelines, configs |
| .sql | 186 | 14.9% | SQL scripts |
| .yaml | 127 | 10.2% | Airflow DAGs |
...

## Directory Structure
[ASCII tree]

## Hot Spots
[Critical areas with high file counts]

## Red Flags
[Security/technical debt issues]
```

### Secondary Outputs
- Console log with scan progress
- CSV export: `inventory-outputs/exports/file-inventory.csv`

---

## Technologies Detected

The scan identifies these file types:

### Pipelines
- `.json` → Azure Data Factory
- `.py` → Databricks notebooks, Python scripts
- `.yaml` → Airflow DAGs
- `.xml` → SAP BODS, SSIS
- `.scala` → Spark jobs
- `.sql` → SQL scripts

### Configurations
- `.properties` → Java configs
- `.yaml/.yml` → Various configs
- `.env` → Environment variables
- `.tf` → Terraform
- `.ini` → Legacy configs

---

## Security Checks

### Patterns Detected

```regex
# Credentials
password\s*=\s*['"][^'"]+['"]
apiKey\s*=\s*['"][^'"]+['"]
secret\s*=\s*['"][^'"]+['"]
token\s*=\s*['"][^'"]+['"]

# Connection Strings
Server=.*;Database=.*;User Id=.*;Password=.*
mongodb://.*:.*@

# AWS Keys
AKIA[0-9A-Z]{16}

# Azure Keys
DefaultEndpointsProtocol=https;AccountName=.*;AccountKey=.*
```

### Action Taken
- Flag files with matches
- DO NOT include actual credentials in output
- Show file path and line number only
- Recommend using vault services

---

## Example Usage

### Basic Scan
```
@inventory-scout *scan-repo /path/to/legacy-platform
```

### Scan with Exclusions
```
@inventory-scout *scan-repo /path/to/repo --exclude node_modules,dist,build
```

### Scan with Depth Limit
```
@inventory-scout *scan-repo /path/to/repo --max-depth 5
```

---

## Next Steps

After `*scan-repo` completes:

1. ✅ Review `inventory-map.md`
2. ⏭️ Run `*analyze-configs` to parse configuration files
3. ⏭️ Run `*detect-tech-stack` to identify technologies
4. ⏭️ Run `*map-dependencies` to build dependency graph

---

## Success Criteria

✅ **Complete when:**
- All files scanned successfully
- `inventory-map.md` generated
- No parsing errors (or errors logged separately)
- Statistics accurate and complete
- Red flags identified and documented

---

## Error Handling

| Error | Resolution |
|-------|-----------|
| Path not found | Validate repository path, check permissions |
| Permission denied | Run with appropriate permissions or skip file |
| Large repository (> 100k files) | Consider excluding build/output folders |
| Encoding errors | Log files with encoding issues, continue scan |

---

## Performance

| Repository Size | Expected Time |
|----------------|---------------|
| Small (< 1k files) | < 10 seconds |
| Medium (1k-10k files) | 10-60 seconds |
| Large (10k-50k files) | 1-5 minutes |
| Very Large (> 50k files) | 5-15 minutes |

**Tip:** Exclude build artifacts and node_modules to speed up scan.

---

## Validation

### Self-Check
- [ ] Repository path validated
- [ ] All directories traversed
- [ ] File counts accurate
- [ ] Extensions categorized correctly
- [ ] Size calculations correct
- [ ] Directory tree generated
- [ ] Red flags identified
- [ ] Output file created

---

**Status:** ✅ Ready for use  
**Last Updated:** 2026-02-12
