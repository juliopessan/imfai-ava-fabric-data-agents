---
checklist: data-engineer-checklist
version: 1.0
description: Complete checklist for data pipeline development and deployment
---

# Data Engineering Pipeline Checklist

## 📋 Pre-Development

### Requirements Gathering
- [ ] Data sources identified (CSV, Parquet, JSON, TSV, etc.)
- [ ] Source schemas documented with sample data
- [ ] Business rules and transformations defined
- [ ] Data quality requirements specified
- [ ] Target state (Gold layer) requirements clear
- [ ] Performance/SLA requirements documented
- [ ] Technology stack selected (SQL/PySpark)
- [ ] Deployment environment identified

### Architecture Design
- [ ] Medallion architecture layers defined (Landing/Silver/Gold)
- [ ] Table naming conventions established
- [ ] Schema naming conventions established
- [ ] Data flow diagram created
- [ ] Error handling strategy defined
- [ ] Monitoring and alerting approach planned

## 🗄️ Database Objects

### DDL Scripts
- [ ] Landing tables created (VARCHAR columns)
- [ ] Silver tables created (proper data types)
- [ ] Gold tables created (denormalized/aggregated)
- [ ] Reference tables created
- [ ] Reject tables created for error handling
- [ ] Audit/logging tables created
- [ ] Primary keys defined
- [ ] Foreign keys defined (where applicable)
- [ ] Indexes created on join/filter columns
- [ ] Table and column comments added
- [ ] Scripts are idempotent (IF NOT EXISTS)

## 🔄 ETL/ELT Scripts

### Landing Layer
- [ ] File ingestion scripts created
- [ ] Source file path parameterized
- [ ] Load timestamp captured
- [ ] Source file name captured
- [ ] Raw data preserved exactly as source

### Silver Layer
- [ ] Type conversion logic implemented
- [ ] Data quality checks implemented
- [ ] NULL handling defined
- [ ] Range validation added
- [ ] Business rule validation added
- [ ] Quality flags assigned (VALID/INVALID)
- [ ] Rejects captured in reject tables
- [ ] Processed timestamp added

### Gold Layer
- [ ] Join logic implemented (enrichment)
- [ ] Aggregation logic implemented (summaries)
- [ ] Denormalization completed
- [ ] Query optimization applied
- [ ] Only VALID records promoted from Silver
- [ ] Business-ready columns created

### Reference Data
- [ ] Reference data load scripts created
- [ ] Reference data validated
- [ ] Foreign key relationships established

## ✅ Data Quality

### Validation Rules
- [ ] Type validation implemented
- [ ] NOT NULL checks on required fields
- [ ] Range checks on numeric fields
- [ ] Date validity checks
- [ ] Referential integrity checks
- [ ] Business rule validation
- [ ] Duplicate detection
- [ ] Format validation (emails, phone numbers, etc.)

### Error Handling
- [ ] Reject tables capture invalid records
- [ ] Error messages are descriptive
- [ ] Original data preserved in rejects
- [ ] Error timestamp captured
- [ ] Source file tracked in rejects

## 🧪 Testing

### Unit Tests
- [ ] Row count tests (file vs table)
- [ ] Schema validation tests
- [ ] NULL check tests
- [ ] Range validation tests
- [ ] Type conversion tests
- [ ] Join integrity tests
- [ ] Aggregation accuracy tests
- [ ] Data comparison tests (file vs table)
- [ ] Test runner script created
- [ ] All tests passing

### Integration Tests
- [ ] End-to-end pipeline execution tested
- [ ] Error scenarios tested
- [ ] Rerun/idempotency tested
- [ ] Performance benchmarks established

## 📊 Performance

### Optimization
- [ ] Partition strategy defined
- [ ] Indexes on frequently queried columns
- [ ] Statistics updated
- [ ] Query execution plans reviewed
- [ ] Broadcast joins used where appropriate
- [ ] Unnecessary transformations removed
- [ ] File formats optimized (Parquet for large data)

### Scalability
- [ ] Pipeline handles expected data volumes
- [ ] Incremental processing strategy defined
- [ ] Resource usage monitored
- [ ] Bottlenecks identified and addressed

## 📝 Documentation

### Technical Documentation
- [ ] Pipeline architecture documented
- [ ] Data flow documented
- [ ] Table relationships documented (ERD)
- [ ] Transformation logic explained
- [ ] Data quality rules documented
- [ ] Execution order documented
- [ ] Dependencies documented
- [ ] Parameter configuration documented

### Operational Documentation
- [ ] Deployment instructions created
- [ ] Execution instructions created
- [ ] Troubleshooting guide created
- [ ] Monitoring guide created
- [ ] Runbook for common issues
- [ ] Contact information for support

## 🔍 Monitoring & Observability

### Logging
- [ ] Pipeline execution logged
- [ ] Row counts logged
- [ ] Reject counts logged
- [ ] Execution time logged
- [ ] Error messages logged
- [ ] Audit trail maintained

### Alerting
- [ ] Failure alerts configured
- [ ] Data quality alerts configured
- [ ] Performance alerts configured
- [ ] Alert recipients defined

## 🚀 Deployment

### Pre-Deployment
- [ ] Code reviewed
- [ ] All tests passing in dev/test
- [ ] Performance validated
- [ ] Documentation complete
- [ ] Deployment plan reviewed
- [ ] Rollback plan prepared

### Deployment
- [ ] Database objects deployed
- [ ] ETL scripts deployed
- [ ] Test scripts deployed
- [ ] Configuration deployed
- [ ] Permissions granted
- [ ] Smoke tests executed

### Post-Deployment
- [ ] Pipeline executed successfully
- [ ] Data validated in production
- [ ] Monitoring confirmed working
- [ ] Alerts confirmed working
- [ ] Documentation updated
- [ ] Stakeholders notified

## 🔒 Security & Compliance

### Access Control
- [ ] Least privilege access implemented
- [ ] Service accounts created
- [ ] Credentials securely stored
- [ ] Audit logging enabled

### Data Governance
- [ ] PII data identified and protected
- [ ] Data retention policies applied
- [ ] Data lineage documented
- [ ] Compliance requirements met

## ✨ Best Practices

### Code Quality
- [ ] Code follows naming conventions
- [ ] Code is well-commented
- [ ] Code is modular and reusable
- [ ] Code is version controlled
- [ ] No hardcoded values
- [ ] Parameters externalized

### Maintainability
- [ ] Scripts are idempotent
- [ ] Error handling is comprehensive
- [ ] Logging is consistent
- [ ] Code is testable
- [ ] Dependencies are documented

---

## Completion Criteria

✅ **Pipeline is Ready for Production when:**
- All checklist items completed
- All tests passing
- Documentation complete
- Code reviewed and approved
- Successfully deployed to production
- Monitoring and alerts working
- Stakeholder sign-off obtained
