# 🔄 Data Engineer Agent - Chatmode Activation Guide

## ✅ Chatmode Successfully Created!

The `data-engineer.chatmode.md` chatmode has been created and is ready for use in GitHub Copilot!

## 🎯 How to Activate the Agent

### Method 1: Via Chatmode (Recommended)
```
@workspace /chatmode data-engineer
```

### Method 2: Via Agent Loader
```
@workspace /agent data-engineer
```

### Method 3: Direct Mention
```
@data-engineer [your question about data pipelines]
```

## 🚀 First Execution

After activation, the agent will:

1. **Greet you** as "DataFlow" 🔄
2. **Load project configuration**
3. **Show available commands** automatically
4. **Wait for** your instructions

Example greeting:
```
🔄 Hello! I'm DataFlow, your Data Engineering & Pipeline Specialist.

I'm here to help you with:
- Data ingestion pipelines (CSV, Parquet, JSON, TSV)
- DDL and ETL script generation
- Data quality validation
- Pipeline optimization
- Unit test creation

Available commands (* prefix required):

1. *help - Show all commands
2. *create-pipeline - Design complete data pipeline
3. *create-ddl - Generate DDL scripts
4. *create-etl - Generate ETL/ELT scripts
5. *create-tests - Generate unit tests
6. *profile-data - Analyze data sources
7. *validate-quality - Check data quality
8. *optimize-pipeline - Improve performance
9. *document-pipeline - Create documentation
10. *execute-checklist - Run quality checklist
11. *yolo - Toggle autonomous mode
12. *exit - Exit this agent

What would you like to work on today?
```

## 📋 Main Commands

| Command | Use when... |
|---------|-------------|
| `*create-pipeline` | Create complete pipeline from scratch |
| `*create-ddl` | Generate only table creation scripts |
| `*create-etl` | Generate only transformation scripts |
| `*create-tests` | Generate validation tests |
| `*profile-data` | Analyze files and determine data types |
| `*validate-quality` | Check data quality |
| `*optimize-pipeline` | Improve pipeline performance |
| `*document-pipeline` | Create complete documentation |

## 💡 Usage Example for Your Case

```
@workspace /chatmode data-engineer

*create-pipeline

I need to create a complete pipeline with:

MONTHLY INGESTION:
1. CSV with trip data → LND.TRIP_DATA_CSV → SILVER.TRIP_DATA_CSV
   Columns: trip_id, vendor_id, pickup_datetime, dropoff_datetime, 
   passenger_count, trip_distance, fare_amount, tip_amount, tolls_amount

2. Parquet with trip data → LND.TRIP_DATA_PARQUET → SILVER.TRIP_DATA_PARQUET
   Columns: same as CSV

REFERENCES:
3. TSV trip_type.tsv → REF.TRIP_TYPE
   Columns: trip_type (INT), trip_type_desc (VARCHAR)

4. JSON rate_code.json → REF.RATE_CODE  
   Columns: rate_code_id (INT), rate_code (VARCHAR)

5. JSON payment_type_array.json → REF.PAYMENT_TYPE
   Columns: payment_type (INT), payment_type_desc (VARCHAR)

GOLD LAYER:
6. GOLD.TRIP_DATA_CSV 
   - Join SILVER.TRIP_DATA_CSV with 3 reference tables
   - Add rate_code, payment_type_desc, trip_type_desc

7. GOLD.TRIP_DATA_PARQUET_AGG
   - Group by PULocationID
   - SUM(trip_distance), SUM(fare_amount), COUNT(trips)

TESTS:
8. Create SQL unit tests comparing:
   - Row counts (files vs tables)
   - Aggregations (Silver vs Gold)
   - Join integrity

TECHNOLOGY:
- Generate scripts in SQL and PySpark
- Databricks as platform
```

## 🎨 Chatmode Features

### 1. Specialized Persona
- Name: **DataFlow**
- Style: Precise, methodical, quality-focused
- Expertise: SQL, PySpark, Medallion Architecture

### 2. Enabled Tools
- ✅ File editing
- ✅ Notebook execution
- ✅ Semantic search in workspace
- ✅ New file creation
- ✅ Command execution
- ✅ VS Code API access
- ✅ Problem detection
- ✅ Change monitoring
- ✅ GitHub navigation
- ✅ External repository search

### 3. Core Principles
1. **Data Quality First** - Never compromise integrity
2. **Layered Architecture** - Landing → Silver → Gold
3. **Idempotent Operations** - Re-executable pipelines
4. **Comprehensive Testing** - Test each transformation
5. **Clear Data Lineage** - Complete traceability

### 4. Supported Formats
- CSV (comma-delimited)
- Parquet (columnar)
- JSON (structured/semi-structured)
- TSV (tab-delimited)
- Avro, ORC, Delta Lake

## 📊 Implemented Architecture

```
┌─────────────────────────────────────────┐
│     SOURCE FILES (Monthly Batch)        │
│  CSV │ Parquet │ JSON │ TSV            │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  🥉 LANDING LAYER (Bronze - Raw Data)   │
│  - LND.TRIP_DATA_CSV                    │
│  - LND.TRIP_DATA_PARQUET                │
│  - All columns as VARCHAR               │
│  - No transformations                   │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  🥈 SILVER LAYER (Validated & Typed)    │
│  - SILVER.TRIP_DATA_CSV                 │
│  - SILVER.TRIP_DATA_PARQUET             │
│  - REF.TRIP_TYPE / RATE_CODE / PAYMENT  │
│  - Proper data types                    │
│  - Quality checks applied               │
│  - Rejects captured                     │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│  🥇 GOLD LAYER (Business Ready)         │
│  - GOLD.TRIP_DATA_CSV (enriched)        │
│  - GOLD.TRIP_DATA_PARQUET_AGG (agg)     │
│  - Joined with reference data           │
│  - Aggregated summaries                 │
│  - Query-optimized                      │
└──────────────┬──────────────────────────┘
               ↓
┌─────────────────────────────────────────┐
│   📊 ANALYTICS / BI TOOLS / REPORTS     │
└─────────────────────────────────────────┘
```

## 🗂️ Agent File Structure

```
.avanade-core/
├── agents/
│   ├── data-engineer.md              ← Agent definition
│   └── DATA-ENGINEER-README.md       ← Usage guide
├── tasks/
│   ├── create-data-pipeline.md       ← Complete pipeline
│   ├── create-ddl-scripts.md         ← DDL generation
│   ├── create-etl-scripts.md         ← ETL generation
│   ├── create-data-tests.md          ← Test generation
│   ├── profile-data-sources.md       ← Data analysis
│   ├── validate-data-quality.md      ← Quality validation
│   ├── optimize-pipeline.md          ← Optimization
│   └── document-data-pipeline.md     ← Documentation
├── templates/
│   └── data-pipeline-tmpl.yaml       ← Documentation template
├── checklists/
│   └── data-engineer-checklist.md    ← Quality checklist
└── data/
    └── data-engineering-best-practices.md ← Best practices

.github/
└── chatmodes/
    └── data-engineer.chatmode.md     ← CHATMODE (ESTE ARQUIVO!)
```

## 🔍 Troubleshooting

### Problem: Chatmode doesn't appear
**Solution:** Reload VS Code
```
Ctrl+Shift+P → "Developer: Reload Window"
```

### Problem: Commands don't work
**Solution:** Make sure to use the `*` prefix
```
❌ help
✅ *help
```

### Problem: Agent doesn't load files
**Solution:** Check if `.avanade-core/` exists and has the files

### Problem: Want to exit the agent
**Solution:** Use the exit command
```
*exit
```

## 🎯 Next Steps

1. **Activate the agent:**
   ```
   @workspace /chatmode data-engineer
   ```

2. **View available commands:**
   ```
   *help
   ```

3. **Start your pipeline:**
   ```
   *create-pipeline
   ```

4. **Or ask for direct help:**
   ```
   I need to create a pipeline to ingest monthly CSV files with trip data...
   ```

## 💪 What the Agent Can Do

✅ Create complete pipelines Landing → Silver → Gold  
✅ Generate DDL scripts for all tables  
✅ Generate ETL scripts in SQL and PySpark  
✅ Create comprehensive unit tests  
✅ Analyze files and suggest data types  
✅ Validate data quality  
✅ Optimize pipeline performance  
✅ Document complete architecture  
✅ Follow best practices (Medallion, ACID, etc.)  
✅ Implement data quality checks  
✅ Capture rejects without data loss  
✅ Create audit logs  

## 🎉 Everything is Ready!

The **data-engineer** chatmode is fully configured and ready to solve your data pipeline requirements!

**Start now:**
```
@workspace /chatmode data-engineer
```

🚀 Happy Data Engineering!
