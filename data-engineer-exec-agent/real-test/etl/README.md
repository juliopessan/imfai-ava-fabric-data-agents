# 🔄 Pipeline ETL - NYC Green Taxi Data

**Pipeline Completa: Landing → Silver → Gold (Arquitetura Medallion)**  
**Database:** TEST_PIPELINE  
**Fonte de Dados:** NYC Green Taxi Trip Records (Abril-Junho 2021)  
**Autor:** DataFlow Agent  
**Data:** 17 de Novembro de 2025

---

## 📋 Visão Geral

Esta pipeline ETL implementa **TODOS OS 8 REQUISITOS** do projeto, processando dados de táxi de NYC em múltiplos formatos (CSV, Parquet, JSON, TSV) através de uma arquitetura Medallion completa.

### Requisitos Implementados

| # | Requisito | Status | Arquivos |
|---|-----------|--------|----------|
| **1a** | CSV → LANDING (VARCHAR) | ✅ | `02-load-landing-csv.sql` |
| **1b** | LANDING → SILVER (tipos apropriados) | ✅ | `04-transform-to-silver-csv.sql` |
| **2a** | Parquet → LANDING (VARCHAR) | ✅ | `load_parquet_to_sql.py`, `03-load-landing-parquet.sql` |
| **2b** | LANDING → SILVER (tipos apropriados) | ✅ | `05-transform-to-silver-parquet.sql` |
| **3** | trip_type.tsv → REF.TRIP_TYPE | ✅ | `01-load-reference-data.sql` |
| **4** | rate_code.json → REF.RATE_CODE | ✅ | `01-load-reference-data.sql` |
| **5** | payment_type_array.json → REF.PAYMENT_TYPE | ✅ | `01-load-reference-data.sql` |
| **6** | Gold Enriched (CSV com JOINs) | ✅ | `06-build-gold-enriched.sql` |
| **7** | Gold Aggregated (por PULocationID) | ✅ | `07-build-gold-aggregated.sql` |
| **8** | Testes Unitários | ✅ | `08-unit-tests.sql` |

---

## 🗂️ Estrutura de Arquivos

```
real-test/
├── etl/
│   ├── 00-run-all-etl.sql                    # Script master (guia de execução)
│   ├── 01-load-reference-data.sql            # Requisitos 3, 4, 5
│   ├── 02-load-landing-csv.sql               # Requisito 1a
│   ├── 03-load-landing-parquet.sql           # Requisito 2a
│   ├── 04-transform-to-silver-csv.sql        # Requisito 1b
│   ├── 05-transform-to-silver-parquet.sql    # Requisito 2b
│   ├── 06-build-gold-enriched.sql            # Requisito 6
│   ├── 07-build-gold-aggregated.sql          # Requisito 7
│   └── load_parquet_to_sql.py                # Utilitário Python (Parquet)
│
├── 01-landing-tables.sql                     # DDL: Landing Layer
├── 02-silver-tables.sql                      # DDL: Silver Layer
├── 03-gold-tables.sql                        # DDL: Gold Layer
├── 04-reference-tables.sql                   # DDL: Reference Tables
└── REAL-DATA-PROFILE-REPORT.md               # Análise de Qualidade de Dados
```

---

## 🚀 Guia de Execução

### Pré-requisitos

1. **SQL Server** com permissões de BULK INSERT
2. **Python 3.8+** com bibliotecas (para Parquet):
   ```bash
   pip install pyarrow pandas pyodbc
   ```
3. **Arquivos de Dados** em `Files/`:
   - `green_tripdata_2021-04.csv`
   - `green_tripdata_2021-05.csv`
   - `green_tripdata_2021-06.csv`
   - `month=04/*.parquet`
   - `month=05/*.parquet`
   - `month=06/*.parquet`
   - `trip_type.tsv`
   - `rate_code.json`
   - `payment_type_array.json`

### Execução Passo a Passo

#### **FASE 1: DDL (Criar Estrutura)**

```sql
-- Executar na ordem:
sqlcmd -S localhost -d TEST_PIPELINE -i "01-landing-tables.sql"
sqlcmd -S localhost -d TEST_PIPELINE -i "02-silver-tables.sql"
sqlcmd -S localhost -d TEST_PIPELINE -i "03-gold-tables.sql"
sqlcmd -S localhost -d TEST_PIPELINE -i "04-reference-tables.sql"
```

#### **FASE 2: ETL (Processar Dados)**

```sql
-- PASSO 1: Carregar Referências (Requisitos 3, 4, 5)
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/01-load-reference-data.sql"

-- PASSO 2: Carregar CSV → Landing (Requisito 1a)
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/02-load-landing-csv.sql"

-- PASSO 3: [OPCIONAL] Carregar Parquet → Landing (Requisito 2a)
python etl/load_parquet_to_sql.py
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/03-load-landing-parquet.sql"

-- PASSO 4: Transformar CSV → Silver (Requisito 1b)
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/04-transform-to-silver-csv.sql"

-- PASSO 5: [OPCIONAL] Transformar Parquet → Silver (Requisito 2b)
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/05-transform-to-silver-parquet.sql"

-- PASSO 6: Construir Gold Enriched (Requisito 6)
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/06-build-gold-enriched.sql"

-- PASSO 7: Construir Gold Aggregated (Requisito 7)
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/07-build-gold-aggregated.sql"

-- PASSO 8: Executar Testes Unitários (Requisito 8)
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/08-unit-tests.sql"
```

#### **Execução Rápida (Script Master)**

```sql
-- Guia visual de toda a pipeline
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/00-run-all-etl.sql"
```

---

## 📊 Arquitetura de Dados

### **Landing Layer** (VARCHAR - Requisitos 1a, 2a)
- `LANDING.TRIP_DATA_CSV` - Dados CSV brutos
- `LANDING.TRIP_DATA_PARQUET` - Dados Parquet brutos
- `LANDING.DATA_LINEAGE` - Rastreamento de cargas
- **Características:** 
  - Todos os campos VARCHAR(50)
  - Dados não transformados
  - Audit columns (load_timestamp, source_file)

### **Silver Layer** (Tipos Tipados - Requisitos 1b, 2b)
- `SILVER.TRIP_DATA_CSV` - CSV com tipos apropriados
- `SILVER.TRIP_DATA_PARQUET` - Parquet com tipos apropriados
- `SILVER.TRIP_DATA_CSV_REJECTS` - Registros rejeitados
- **Características:**
  - Conversão VARCHAR → INT, DECIMAL, DATETIME2
  - 20+ regras de validação
  - Quality flags (VALID, INVALID, WARNING)
  - Computed columns (trip_duration, trip_month)
  - Reject tables para dados inválidos

### **Reference Layer** (Requisitos 3, 4, 5)
- `REF.TRIP_TYPE` - Tipos de viagem (TSV)
- `REF.RATE_CODE` - Códigos de tarifa (JSON)
- `REF.PAYMENT_TYPE` - Tipos de pagamento (JSON aninhado)
- `REF.VW_PAYMENT_TYPE_SIMPLE` - View simplificada
- **Características:**
  - Dados estáticos de referência
  - Suporte para JOINs
  - Atributos de negócio

### **Gold Layer** (Business-Ready - Requisitos 6, 7)

#### **Gold Enriched** (Requisito 6)
- `GOLD.TRIP_DATA_CSV` - Dados enriquecidos com JOINs
- **Features:**
  - ✅ JOIN com `REF.RATE_CODE` → descrições de tarifa
  - ✅ JOIN com `REF.PAYMENT_TYPE` → tipos de pagamento
  - ✅ JOIN com `REF.TRIP_TYPE` → tipos de viagem
  - 6 métricas de negócio (fare_per_mile, tip_percentage, etc)
  - 6 dimensões temporais (hour, day_of_week, month, quarter)
  - 3 categorizações (distance, fare, duration)
  - Data quality score

#### **Gold Aggregated** (Requisito 7)
- `GOLD.TRIP_DATA_PARQUET_AGG` - Agregação por localização
- **Métricas:**
  - ✅ `SUM(trip_distance)` por PULocationID
  - ✅ `SUM(fare_amount)` por PULocationID
  - ✅ `COUNT(*)` por PULocationID
  - 15+ KPIs de revenue e utilização
  - Location utilization score
  - Segmentação (airport trips, cash/card, weekend, rush hour)

---

## 🎯 Funcionalidades Principais

### Validação de Qualidade de Dados
- **20+ Regras de Validação:**
  - VendorID IN (1, 2)
  - Datas válidas e consistentes (dropoff > pickup)
  - Trip distance: 0 ≤ distance ≤ 500 mi
  - Passenger count: 0 ≤ count ≤ 8
  - Valores financeiros positivos
  - Integridade referencial

### Quality Flags
```sql
-- VALID: Passou todas as validações
-- INVALID: Falha crítica (movido para REJECT)
-- WARNING: Valores suspeitos mas processáveis
```

### Reject Tables
- Captura registros inválidos sem perder dados
- JSON completo do registro original
- Mensagens de erro detalhadas
- Rastreamento de fonte

### Data Lineage
- Tracking completo de arquivos carregados
- Status de sucesso/falha
- Contadores de registros
- Timestamps de processamento

---

## 📈 Métricas e KPIs

### **Gold Enriched** oferece:
- `trip_duration_minutes` - Duração da viagem
- `trip_speed_mph` - Velocidade média
- `fare_per_mile` - Tarifa por milha
- `fare_per_minute` - Tarifa por minuto
- `tip_percentage` - Percentual de gorjeta
- `total_surcharges` - Total de sobretaxas
- `is_weekend`, `is_rush_hour` - Flags temporais
- `data_quality_score` - Score de qualidade (0-100)

### **Gold Aggregated** oferece:
- `total_trips` - Total de viagens por localização
- `total_distance` - Distância total
- `total_revenue` - Receita total
- `avg_trip_distance` - Distância média
- `location_utilization_score` - Score de utilização
- `revenue_per_trip` - Receita por viagem
- `revenue_per_mile` - Receita por milha
- `total_airport_trips` - Viagens para aeroporto
- `total_weekend_trips` - Viagens em fim de semana

---

## 🔍 Consultas Úteis

### Verificar Carregamento Landing
```sql
SELECT 
    source_file,
    COUNT(*) as records,
    MIN(load_timestamp) as loaded_at
FROM LANDING.TRIP_DATA_CSV
GROUP BY source_file;
```

### Verificar Qualidade Silver
```sql
SELECT 
    quality_flag,
    COUNT(*) as count,
    CAST(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER() AS DECIMAL(5,2)) as percentage
FROM SILVER.TRIP_DATA_CSV
GROUP BY quality_flag;
```

### Top 10 Localizações por Receita
```sql
SELECT TOP 10
    PULocationID,
    total_trips,
    CAST(total_revenue AS MONEY) as revenue,
    location_utilization_score
FROM GOLD.TRIP_DATA_PARQUET_AGG
ORDER BY total_revenue DESC;
```

### Análise por Tipo de Pagamento
```sql
SELECT 
    payment_type_desc,
    COUNT(*) as trips,
    AVG(total_amount) as avg_fare,
    AVG(tip_percentage) as avg_tip_pct
FROM GOLD.TRIP_DATA_CSV
GROUP BY payment_type_desc
ORDER BY trips DESC;
```

---

## 🛠️ Troubleshooting

### Erro: "Cannot bulk load. Operating system error code 5"
**Solução:** Execute SQL Server Management Studio como Administrador ou ajuste permissões de arquivo.

### Erro: "Cannot open file 'xxx.csv'"
**Solução:** Verifique o caminho completo em `02-load-landing-csv.sql` (linhas 60-70).

### Aviso: "Nenhum dado Parquet"
**Normal:** Scripts Parquet são opcionais. Pipeline funciona apenas com CSV.

### Python: "Module 'pyarrow' not found"
**Solução:** 
```bash
pip install pyarrow pandas pyodbc
```

### Dados de Referência Ausentes
**Solução:** Execute primeiro `01-load-reference-data.sql` antes dos outros ETL.

---

## ✅ Checklist de Implementação

- [x] **DDL Scripts (4 arquivos)**
  - [x] Landing tables
  - [x] Silver tables
  - [x] Gold tables
  - [x] Reference tables

- [x] **ETL Scripts (8 arquivos)**
  - [x] Load reference data (REQ 3,4,5)
  - [x] Load CSV to Landing (REQ 1a)
  - [x] Load Parquet to Landing (REQ 2a)
  - [x] Transform CSV to Silver (REQ 1b)
  - [x] Transform Parquet to Silver (REQ 2b)
  - [x] Build Gold Enriched (REQ 6)
  - [x] Build Gold Aggregated (REQ 7)
  - [x] Master execution script

- [x] **Funcionalidades**
  - [x] Data validation (20+ rules)
  - [x] Quality flags (VALID/INVALID/WARNING)
  - [x] Reject tables
  - [x] Data lineage tracking
  - [x] Business metrics calculation
  - [x] Temporal dimensions
  - [x] Reference data JOINs

- [x] **Testes Unitários (REQ 8)**
  - [x] Estrutura DDL validada
  - [x] Dados de referência validados
  - [x] CSV vs tables comparison
  - [x] Transformações Silver validadas
  - [x] Gold Enriched com JOINs validados
  - [x] Gold Aggregated validado
  - [x] Integridade de dados validada
  - [x] 25+ testes automatizados

---

## 📞 Próximos Passos

1. ✅ **Executar DDL Scripts** - Criar estrutura de tabelas
2. ✅ **Executar ETL Scripts** - Carregar e transformar dados
3. ✅ **Criar Testes Unitários** - Implementar Requisito 8
4. ⏳ **Monitoramento** - Dashboards e alertas
5. ⏳ **Otimização** - Tuning de performance
6. ⏳ **Automação** - Azure Data Factory / Airflow

---

## 🧪 Testes Unitários (Requisito 8)

### Executar Testes

```powershell
sqlcmd -S localhost -d TEST_PIPELINE -i "etl/08-unit-tests.sql"
```

### Categorias de Testes

1. **Estrutura DDL** - Validar existência de tabelas
2. **Dados de Referência** - Validar REQ 3, 4, 5
3. **Carregamento CSV** - Validar REQ 1a
4. **Transformação Silver** - Validar REQ 1b
5. **Gold Enriched** - Validar REQ 6 (JOINs)
6. **Gold Aggregated** - Validar REQ 7 (Agregações)
7. **Integridade de Dados** - Validações cruzadas

### Testes Incluídos (25+ testes)

✅ Existência de todas as tabelas (Landing, Silver, Gold, Ref)  
✅ Contagem correta de dados de referência  
✅ Dados CSV carregados corretamente  
✅ Campos VARCHAR em Landing  
✅ Tipos de dados apropriados em Silver  
✅ Quality flags atribuídos (VALID/INVALID/WARNING)  
✅ Registros inválidos capturados em REJECT  
✅ Taxa de qualidade > 90%  
✅ JOINs com REF.RATE_CODE funcionando  
✅ JOINs com REF.PAYMENT_TYPE funcionando  
✅ JOINs com REF.TRIP_TYPE funcionando  
✅ Métricas de negócio calculadas  
✅ Agregações por PULocationID  
✅ SUM(trip_distance), SUM(fare_amount), COUNT(*)  
✅ Consistência Landing → Silver → Gold  
✅ Sem duplicatas  

### Resultados dos Testes

Os testes geram um relatório completo mostrando:
- Total de testes executados
- Taxa de sucesso
- Testes que passaram / falharam / warnings
- Detalhamento por categoria
- Valores esperados vs valores reais

---

## 📝 Notas Técnicas

### Performance
- **BULK INSERT** com `TABLOCK` para performance otimizada
- Indexes em campos de JOIN e filtro
- Batch processing em lotes de 1000 registros (Python)
- Partition pruning em data ranges

### Idempotência
- Todos os scripts podem ser re-executados com segurança
- `TRUNCATE` antes de carregar (evita duplicatas)
- Tracking de arquivos carregados via `DATA_LINEAGE`

### Extensibilidade
- Fácil adicionar novos meses de dados
- Estrutura pronta para incremental loads
- Modular: cada script é independente

---

**DataFlow Agent** 🔄  
*Especialista em Pipelines de Dados e Arquitetura Medallion*
