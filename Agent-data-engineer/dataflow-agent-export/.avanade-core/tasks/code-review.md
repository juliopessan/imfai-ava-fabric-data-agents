---
task: code-review
version: 1.0
elicit: true
description: Perform comprehensive peer review of data pipeline code
---

# Data Pipeline Code Review

## Purpose
Conduct thorough code review of data pipeline scripts (SQL, PySpark, Python) to ensure quality, performance, security, and maintainability before deployment.

## Process

### Step 1: Gather Review Context
ASK the user:

1. **Code Location**: Which files/scripts to review?
2. **Review Type**: Full review, security-focused, performance-focused?
3. **Criticality**: Production, staging, or development code?
4. **Standards**: Any specific coding standards to follow?
5. **History**: Is this new code or modifications?

### Step 2: Code Review Checklist

**Execute comprehensive review against these criteria:**

```markdown
## Code Review Checklist

### A. Code Quality & Readability

#### A1. Naming Conventions
- [ ] Table names follow standard (LND.*, SILVER.*, GOLD.*, REF.*)
- [ ] Column names are descriptive and consistent
- [ ] Variable names are meaningful (not x, y, temp)
- [ ] Procedure/function names describe their purpose
- [ ] Constants are UPPER_CASE

#### A2. Code Structure
- [ ] Code is properly indented
- [ ] Line length is reasonable (<120 chars)
- [ ] Complex logic is broken into smaller functions
- [ ] No deeply nested conditions (max 3 levels)
- [ ] Related code is grouped together

#### A3. Comments & Documentation
- [ ] Header comments explain file purpose
- [ ] Complex transformations have inline comments
- [ ] Business logic is documented
- [ ] TODO items have associated tickets
- [ ] No commented-out code blocks

### B. SQL-Specific Review

#### B1. Query Structure
- [ ] SELECT columns are explicit (no SELECT *)
- [ ] JOINs specify type (LEFT, INNER, etc.)
- [ ] JOIN conditions use proper columns
- [ ] WHERE clauses are sargable (index-friendly)
- [ ] GROUP BY includes all non-aggregated columns

#### B2. Data Types
- [ ] Appropriate types for each column
- [ ] DECIMAL used for financial data (not FLOAT)
- [ ] VARCHAR lengths are appropriate
- [ ] Date/timestamp types are consistent
- [ ] No implicit type conversions

#### B3. Null Handling
- [ ] COALESCE/NULLIF used appropriately
- [ ] NULL comparisons use IS NULL (not = NULL)
- [ ] Nullable columns documented
- [ ] Default values specified where appropriate
- [ ] NULL handling in aggregations considered

### C. Performance Review

#### C1. Query Optimization
- [ ] Indexes exist for JOIN columns
- [ ] Indexes exist for frequently filtered columns
- [ ] No unnecessary DISTINCT operations
- [ ] Subqueries could be replaced with JOINs
- [ ] LIMIT used in exploratory queries

#### C2. Data Volume Handling
- [ ] Large table operations are partitioned
- [ ] Incremental loading where possible
- [ ] Unnecessary data not loaded into memory
- [ ] Temporary tables cleaned up
- [ ] Query explain plan reviewed for large tables

#### C3. PySpark Optimization
- [ ] Broadcast joins for small tables
- [ ] Appropriate number of partitions
- [ ] Caching used for reused DataFrames
- [ ] Actions minimized (count, collect)
- [ ] Shuffle operations minimized

### D. Security Review

#### D1. Data Protection
- [ ] No hardcoded passwords/secrets
- [ ] Sensitive columns identified
- [ ] PII data is masked/encrypted
- [ ] Access controls documented
- [ ] No sensitive data in logs

#### D2. SQL Injection Prevention
- [ ] Parameterized queries used
- [ ] User input is validated
- [ ] Dynamic SQL is avoided
- [ ] If dynamic SQL required, properly sanitized
- [ ] No string concatenation for queries

#### D3. Access Control
- [ ] Minimum necessary permissions
- [ ] Service accounts used appropriately
- [ ] No shared credentials
- [ ] Role-based access implemented
- [ ] Audit logging enabled

### E. Error Handling & Reliability

#### E1. Error Handling
- [ ] TRY/CATCH blocks for critical operations
- [ ] Errors are logged with context
- [ ] Meaningful error messages
- [ ] Transactions properly managed
- [ ] Rollback on failure

#### E2. Data Validation
- [ ] Input data validated before processing
- [ ] Data quality checks implemented
- [ ] Boundary conditions handled
- [ ] Invalid records captured (reject tables)
- [ ] Quality flags assigned

#### E3. Idempotency
- [ ] Scripts can be re-run safely
- [ ] INSERT uses MERGE or upsert pattern
- [ ] DROP/CREATE uses IF EXISTS
- [ ] No duplicate record creation
- [ ] Timestamps track processing
```

### Step 3: Perform Code Analysis

**SQL Code Analysis:**
```sql
-- ==========================================
-- Code Review: SQL Analysis Queries
-- ==========================================

-- Check 1: Find SELECT * usage (anti-pattern)
-- Review these and replace with explicit columns
SELECT 
    'SELECT * found' as issue,
    '{file_name}' as file,
    '{line_number}' as location,
    'Replace with explicit column list' as recommendation;

-- Check 2: Find missing table aliases in JOINs
SELECT 
    'Ambiguous column reference' as issue,
    '{column_name}' as column,
    'Add table alias prefix' as recommendation;

-- Check 3: Find potentially slow queries (no WHERE clause)
SELECT 
    'Full table scan possible' as issue,
    '{table_name}' as table,
    'Add WHERE clause or ensure index exists' as recommendation;

-- Check 4: Check for implicit type conversions
SELECT 
    'Implicit type conversion' as issue,
    '{expression}' as expression,
    'Add explicit CAST to prevent performance issues' as recommendation;

-- Check 5: Find missing NULL handling
SELECT 
    'Potential NULL handling issue' as issue,
    '{expression}' as expression,
    'Add COALESCE or IS NULL check' as recommendation;
```

**PySpark Code Analysis:**
```python
# ==========================================
# Code Review: PySpark Analysis Patterns
# ==========================================

class PipelineCodeReviewer:
    """Automated code review patterns for PySpark"""
    
    def __init__(self, code_content: str):
        self.code = code_content
        self.issues = []
    
    def check_collect_usage(self):
        """Flag potential memory issues from collect()"""
        if '.collect()' in self.code:
            self.issues.append({
                'severity': 'WARNING',
                'category': 'PERFORMANCE',
                'issue': 'collect() found - loads all data to driver memory',
                'recommendation': 'Use take() for samples, or process in distributed manner',
                'line_pattern': '.collect()'
            })
    
    def check_for_loop_over_dataframe(self):
        """Flag Python loops over DataFrames"""
        import re
        if re.search(r'for\s+\w+\s+in\s+\w+\.collect\(\)', self.code):
            self.issues.append({
                'severity': 'CRITICAL',
                'category': 'PERFORMANCE',
                'issue': 'Python loop over collected DataFrame',
                'recommendation': 'Use DataFrame operations instead of Python loops',
                'line_pattern': 'for ... in ... .collect()'
            })
    
    def check_missing_error_handling(self):
        """Check for try/except blocks"""
        if 'try:' not in self.code:
            self.issues.append({
                'severity': 'WARNING',
                'category': 'RELIABILITY',
                'issue': 'No try/except error handling found',
                'recommendation': 'Add error handling for critical operations'
            })
    
    def check_hardcoded_paths(self):
        """Flag hardcoded file paths"""
        import re
        hardcoded = re.findall(r'["\'][A-Za-z]:\\[^"\']+["\']', self.code)
        hardcoded += re.findall(r'["\']\/[a-z]+\/[^"\']+["\']', self.code)
        if hardcoded:
            self.issues.append({
                'severity': 'WARNING',
                'category': 'MAINTAINABILITY',
                'issue': f'Hardcoded paths found: {hardcoded[:3]}',
                'recommendation': 'Use configuration files or environment variables'
            })
    
    def check_hardcoded_credentials(self):
        """CRITICAL: Check for hardcoded secrets"""
        import re
        patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'connection_string\s*=\s*["\'][^"\']+["\']'
        ]
        for pattern in patterns:
            if re.search(pattern, self.code, re.IGNORECASE):
                self.issues.append({
                    'severity': 'CRITICAL',
                    'category': 'SECURITY',
                    'issue': 'Potential hardcoded credential found',
                    'recommendation': 'Use secret management (Key Vault, env vars)'
                })
                break
    
    def check_missing_logging(self):
        """Check for logging implementation"""
        if 'logging' not in self.code and 'logger' not in self.code:
            self.issues.append({
                'severity': 'INFO',
                'category': 'OBSERVABILITY',
                'issue': 'No logging implementation found',
                'recommendation': 'Add structured logging for troubleshooting'
            })
    
    def run_all_checks(self):
        """Execute all code review checks"""
        self.check_collect_usage()
        self.check_for_loop_over_dataframe()
        self.check_missing_error_handling()
        self.check_hardcoded_paths()
        self.check_hardcoded_credentials()
        self.check_missing_logging()
        return self.issues
    
    def generate_report(self):
        """Generate formatted review report"""
        issues = self.run_all_checks()
        
        report = "# Code Review Report\n\n"
        report += f"**Total Issues Found**: {len(issues)}\n\n"
        
        # Group by severity
        critical = [i for i in issues if i['severity'] == 'CRITICAL']
        warnings = [i for i in issues if i['severity'] == 'WARNING']
        info = [i for i in issues if i['severity'] == 'INFO']
        
        if critical:
            report += "## 🔴 Critical Issues\n"
            for issue in critical:
                report += f"- **{issue['category']}**: {issue['issue']}\n"
                report += f"  - Recommendation: {issue['recommendation']}\n"
        
        if warnings:
            report += "\n## 🟡 Warnings\n"
            for issue in warnings:
                report += f"- **{issue['category']}**: {issue['issue']}\n"
                report += f"  - Recommendation: {issue['recommendation']}\n"
        
        if info:
            report += "\n## 🔵 Suggestions\n"
            for issue in info:
                report += f"- **{issue['category']}**: {issue['issue']}\n"
                report += f"  - Recommendation: {issue['recommendation']}\n"
        
        return report
```

### Step 4: Generate Review Report

**Review Report Template:**
```markdown
# Code Review Report

## Summary
| Metric | Value |
|--------|-------|
| **Files Reviewed** | {count} |
| **Lines of Code** | {loc} |
| **Review Date** | {date} |
| **Reviewer** | DataFlow Agent |
| **Review Type** | Comprehensive / Security / Performance |

## Severity Summary
| Severity | Count | Status |
|----------|-------|--------|
| 🔴 Critical | {count} | Must fix before deployment |
| 🟡 Warning | {count} | Should fix before deployment |
| 🔵 Info | {count} | Consider fixing |
| ✅ Pass | {count} | No issues found |

---

## 🔴 Critical Issues

### CR-001: Hardcoded Database Credentials
**File**: etl/load_data.py  
**Line**: 45  
**Category**: Security  

**Code**:
```python
# ❌ CRITICAL: Hardcoded credentials
connection_string = "Server=prod-db;User=admin;Password=secret123"
```

**Issue**: Hardcoded credentials expose security risk and make rotation difficult.

**Recommendation**:
```python
# ✅ Use environment variables or secret management
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
secret_client = SecretClient(vault_url="https://myvault.vault.azure.net/", credential=credential)
connection_string = secret_client.get_secret("db-connection-string").value
```

**References**: 
- [Azure Key Vault Best Practices](https://docs.microsoft.com)
- Security Checklist Item S-001

---

## 🟡 Warnings

### WR-001: Missing Error Handling in ETL
**File**: etl/transform_silver.sql  
**Line**: 120  
**Category**: Reliability  

**Code**:
```sql
-- ❌ No error handling
INSERT INTO SILVER.trip_data
SELECT CAST(fare AS DECIMAL) FROM LND.trip_data;
```

**Issue**: Type conversion may fail without proper error handling.

**Recommendation**:
```sql
-- ✅ Add TRY_CAST and error capture
INSERT INTO SILVER.trip_data
SELECT 
    TRY_CAST(fare AS DECIMAL(10,2)) as fare,
    CASE 
        WHEN TRY_CAST(fare AS DECIMAL(10,2)) IS NULL 
        THEN 'INVALID' 
        ELSE 'VALID' 
    END as quality_flag
FROM LND.trip_data;

-- Capture failures
INSERT INTO REJECT.trip_data_errors
SELECT *, 'CAST_FAILED', GETDATE()
FROM LND.trip_data
WHERE TRY_CAST(fare AS DECIMAL(10,2)) IS NULL;
```

---

### WR-002: SELECT * Anti-Pattern
**File**: etl/build_gold.sql  
**Line**: 35  
**Category**: Maintainability  

**Code**:
```sql
-- ❌ SELECT * is fragile
SELECT * FROM SILVER.trip_data WHERE quality_flag = 'VALID';
```

**Issue**: SELECT * breaks when source schema changes and includes unnecessary columns.

**Recommendation**:
```sql
-- ✅ Explicit column list
SELECT 
    trip_id,
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    fare_amount,
    tip_amount,
    total_amount
FROM SILVER.trip_data 
WHERE quality_flag = 'VALID';
```

---

## 🔵 Suggestions

### SG-001: Add Comments for Complex Logic
**File**: etl/transform_silver.sql  
**Line**: 78-95  
**Category**: Maintainability  

**Issue**: Complex CASE statement without explanation of business logic.

**Recommendation**: Add comment explaining the business rule being implemented.

---

## ✅ Passed Checks

| Check | Status | Notes |
|-------|--------|-------|
| Table naming conventions | ✅ Pass | All tables follow LND/SILVER/GOLD pattern |
| Index coverage | ✅ Pass | JOIN columns are indexed |
| Null handling in aggregations | ✅ Pass | COALESCE used appropriately |
| Idempotent operations | ✅ Pass | MERGE statements used |
| Audit columns present | ✅ Pass | load_timestamp on all tables |

---

## Approval Status

| Reviewer | Decision | Date |
|----------|----------|------|
| DataFlow Agent | 🟡 **Conditional Approval** | 2026-01-26 |

**Conditions for Approval**:
1. ✅ Fix all Critical issues (CR-001)
2. ⬜ Address Warning WR-001 (error handling)
3. ⬜ Address Warning WR-002 (SELECT *)

---

## Next Steps

1. [ ] Developer addresses Critical issues
2. [ ] Developer addresses Warnings
3. [ ] Re-review after fixes
4. [ ] Final approval for deployment
```

### Step 5: Review Best Practices Reference

**Data Pipeline Coding Standards:**
```markdown
## Data Pipeline Coding Standards

### SQL Best Practices

1. **Always use explicit column lists**
   ```sql
   -- ❌ Bad
   SELECT * FROM table
   
   -- ✅ Good
   SELECT col1, col2, col3 FROM table
   ```

2. **Use table aliases consistently**
   ```sql
   -- ✅ Good
   SELECT 
       t.trip_id,
       r.rate_description
   FROM SILVER.trip_data t
   LEFT JOIN REF.rate_code r ON t.rate_code_id = r.rate_code_id
   ```

3. **Handle NULLs explicitly**
   ```sql
   -- ✅ Good
   COALESCE(fare_amount, 0) as fare_amount
   ```

4. **Use TRY_CAST for type safety**
   ```sql
   -- ✅ Good
   TRY_CAST(amount AS DECIMAL(10,2))
   ```

5. **Make operations idempotent**
   ```sql
   -- ✅ Good
   CREATE TABLE IF NOT EXISTS ...
   DROP TABLE IF EXISTS ...
   MERGE INTO target USING source ...
   ```

### PySpark Best Practices

1. **Avoid collect() on large DataFrames**
2. **Use broadcast() for small lookup tables**
3. **Cache DataFrames that are reused**
4. **Minimize shuffles (groupBy, join)**
5. **Use appropriate number of partitions**
```

## Output

Generate the following artifacts:

1. **Code Review Report** (Markdown)
   - Issue summary
   - Detailed findings
   - Recommendations
   - Approval status

2. **Review Checklist** (Markdown)
   - Completed checklist
   - Pass/Fail status

3. **Fix Recommendations** (Code samples)
   - Before/after examples
   - Implementation guidance

## Completion Criteria

Code review is complete when:
- ✅ All files reviewed against checklist
- ✅ Critical issues identified and documented
- ✅ Recommendations provided with examples
- ✅ Approval decision made
- ✅ Next steps defined
