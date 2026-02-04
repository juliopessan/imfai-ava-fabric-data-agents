# DataFlow Agent - Core Configuration

## 📁 Structure Overview

This folder contains the complete instruction set for the DataFlow Agent v2.0.

```
.avanade-core/
├── core-config.yaml           # Main configuration & capability mapping
├── README.md                  # This file
│
├── agents/                    # Agent persona definitions
│   ├── data-engineer.md       # Main agent persona
│   └── DATA-ENGINEER-README.md
│
├── checklists/                # Quality & process checklists
│   └── data-engineer-checklist.md   # 85+ item comprehensive checklist
│
├── data/                      # Reference data & best practices
│   └── data-engineering-best-practices.md
│
├── tasks/                     # Task definitions & instructions
│   ├── create-data-pipeline.md    # End-to-end pipeline creation
│   ├── create-ddl-scripts.md      # Table definition generation
│   ├── create-etl-scripts.md      # ETL/ELT development
│   ├── create-data-tests.md       # Unit test generation
│   ├── profile-data-sources.md    # Data profiling
│   ├── validate-data-quality.md   # Quality framework
│   ├── optimize-pipeline.md       # Performance optimization
│   ├── document-data-pipeline.md  # Documentation generation
│   ├── execute-checklist.md       # Checklist execution
│   └── run-demo.md               # Demo workflow execution
│
└── templates/                 # YAML templates for outputs
    ├── data-pipeline-tmpl.yaml
    ├── ddl-scripts-tmpl.yaml
    ├── etl-scripts-tmpl.yaml
    └── data-tests-tmpl.yaml
```

## 🎯 Capabilities Mapping

| Capability | Command | Task File | Template |
|------------|---------|-----------|----------|
| Data Profiling | `*profile-data` | profile-data-sources.md | - |
| Pipeline Creation | `*create-pipeline` | create-data-pipeline.md | data-pipeline-tmpl.yaml |
| DDL Generation | `*create-ddl` | create-ddl-scripts.md | ddl-scripts-tmpl.yaml |
| ETL Development | `*create-etl` | create-etl-scripts.md | etl-scripts-tmpl.yaml |
| Data Quality | `*validate-quality` | validate-data-quality.md | - |
| Test Creation | `*create-tests` | create-data-tests.md | data-tests-tmpl.yaml |
| Optimization | `*optimize-pipeline` | optimize-pipeline.md | - |
| Documentation | `*document-pipeline` | document-data-pipeline.md | - |
| Checklist Audit | `*execute-checklist` | execute-checklist.md | - |
| **Demo Workflow** | `*run-demo` | run-demo.md | - |

## 📊 AI Impact Metrics (Indicative)

| Capability | Traditional | AI-Assisted | Improvement |
|------------|-------------|-------------|-------------|
| Data Profiling | 11 hours | 0.6 hours | 95% faster |
| DDL Generation | 14 hours | 1 hour | 93% faster |
| ETL Development | 29 hours | 3 hours | 90% faster |
| Data Quality | 16 hours | 0.75 hours | 95% faster |
| Testing | 21 hours | 1 hour | 95% faster |
| Documentation | 17 hours | 1.2 hours | 93% faster |
| **Complete Pipeline** | **152 hours** | **21 hours** | **86% faster** |

## 🚀 Quick Start Commands

```plaintext
# Activate agent
[Switch to data-engineer mode]

# Show available commands
*help

# Run interactive demo
*run-demo

# Profile data sources
*profile-data

# Create complete pipeline
*create-pipeline

# Generate DDL scripts
*create-ddl

# Build ETL scripts
*create-etl

# Quality validation
*validate-quality

# Generate tests
*create-tests

# Create documentation
*document-pipeline

# Run checklist audit
*execute-checklist
```

## 📋 Output Location

All generated artifacts are saved to:
```
data-outputs/
├── ddl/            # Table definitions
├── etl/            # Transformation scripts
├── tests/          # Unit tests
├── profiles/       # Data profiling reports
├── quality/        # Quality validation
├── documentation/  # Pipeline documentation
├── optimization/   # Performance analysis
└── audits/         # Checklist results
```

## 📝 Naming Convention

```
{artifact-type}_{name}_{YYYY-MM-DD_HHmm}.{ext}
```

Examples:
- `ddl_landing-tables_2026-01-26_1600.sql`
- `etl_transform-silver_2026-01-26_1600.sql`
- `profile_nyc-taxi_2026-01-26_1600.md`

---

**Agent Version:** DataFlow v2.0  
**Framework:** Avanade Method - Data Engineering Excellence  
**Last Updated:** 2026-01-26
