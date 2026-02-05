# 🛡️ DQ Initial - Requisitos Iniciais de Data Quality

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 📊 Mary (BusinessAnalyst)  
> **Referências:** [sttm.md](sttm.md) | [kpis.md](../strategy/kpis.md)

---

## 1. Visão Geral

Este documento define os requisitos iniciais de qualidade de dados para o projeto. Será refinado pelo DataSteward (Gaia) na fase MIDSTREAM.

### 1.1 Dimensões de Qualidade Aplicáveis

| Dimensão | Descrição | Aplicável |
|----------|-----------|-----------|
| **Completeness** | Dados não nulos onde esperado | ✅ Sim |
| **Validity** | Valores dentro de ranges/formatos válidos | ✅ Sim |
| **Uniqueness** | Sem duplicatas onde PK | ✅ Sim |
| **Consistency** | Dados consistentes entre campos | ✅ Sim |
| **Timeliness** | Dados atualizados no prazo | ✅ Sim |
| **Accuracy** | Dados corretos vs realidade | ⚠️ Parcial |

### 1.2 Thresholds Globais

| Métrica | Target | Threshold Crítico | Ação |
|---------|--------|-------------------|------|
| Taxa de Qualidade Geral | ≥99% | <95% | ALERTA |
| Completeness | ≥99% | <98% | ALERTA |
| Validity | ≥99% | <97% | QUARANTINE |
| Uniqueness | 100% | <100% | REJECT |

---

## 2. Campos Críticos

### 2.1 Identificação de Campos Críticos

| Campo | Tabela | Criticidade | Justificativa |
|-------|--------|-------------|---------------|
| pickup_datetime | trips | 🔴 CRÍTICO | Base para análise temporal |
| dropoff_datetime | trips | 🔴 CRÍTICO | Cálculo de duração |
| total_amount | trips | 🔴 CRÍTICO | KPI principal (receita) |
| trip_distance | trips | 🔴 CRÍTICO | Cálculo de eficiência |
| pu_location_id | trips | 🟡 ALTO | Análise geográfica |
| do_location_id | trips | 🟡 ALTO | Análise geográfica |
| payment_type | trips | 🟡 ALTO | Análise de comportamento |
| passenger_count | trips | 🟢 MÉDIO | Análise secundária |
| tip_amount | trips | 🟢 MÉDIO | Métrica derivada |

---

## 3. Regras de Qualidade por Campo

### 3.1 Campos de Data/Hora

#### pickup_datetime

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-001 | NOT NULL | 🔴 CRITICAL | REJECT |
| DQ-002 | VALID_DATE (parseable) | 🔴 CRITICAL | REJECT |
| DQ-003 | BETWEEN '2021-01-01' AND '2021-12-31' | 🟡 HIGH | QUARANTINE |
| DQ-004 | <= CURRENT_DATE | 🟡 HIGH | QUARANTINE |

```sql
-- Validação
CASE 
    WHEN pickup_datetime IS NULL THEN 'DQ-001: NULL'
    WHEN TRY_CONVERT(DATETIME, pickup_datetime) IS NULL THEN 'DQ-002: INVALID_FORMAT'
    WHEN pickup_datetime < '2021-01-01' OR pickup_datetime > '2021-12-31' THEN 'DQ-003: OUT_OF_RANGE'
    ELSE 'VALID'
END
```

#### dropoff_datetime

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-005 | NOT NULL | 🔴 CRITICAL | REJECT |
| DQ-006 | VALID_DATE (parseable) | 🔴 CRITICAL | REJECT |
| DQ-007 | >= pickup_datetime | 🔴 CRITICAL | QUARANTINE |
| DQ-008 | <= pickup_datetime + 24 HOURS | 🟡 HIGH | FLAG |

---

### 3.2 Campos Financeiros

#### total_amount

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-009 | NOT NULL | 🔴 CRITICAL | REJECT |
| DQ-010 | >= 0 | 🔴 CRITICAL | QUARANTINE |
| DQ-011 | <= 1000 (threshold razoável) | 🟡 HIGH | FLAG |
| DQ-012 | = fare + extra + mta_tax + tip + tolls + improvement + congestion (±$0.01) | 🟢 MEDIUM | FLAG |

```sql
-- Validação de consistência
CASE
    WHEN ABS(total_amount - (fare_amount + extra + mta_tax + tip_amount + 
         tolls_amount + COALESCE(ehail_fee,0) + improvement_surcharge + 
         COALESCE(congestion_surcharge,0))) > 0.01 
    THEN 'DQ-012: INCONSISTENT_TOTAL'
    ELSE 'VALID'
END
```

#### fare_amount

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-013 | NOT NULL | 🟡 HIGH | QUARANTINE |
| DQ-014 | >= 0 | 🔴 CRITICAL | QUARANTINE |
| DQ-015 | >= 2.50 (tarifa mínima) OR = 0 (no charge) | 🟢 MEDIUM | FLAG |

#### tip_amount

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-016 | >= 0 | 🔴 CRITICAL | QUARANTINE |
| DQ-017 | IF payment_type = 2 (cash) THEN tip = 0 | 🟢 MEDIUM | INFO |
| DQ-018 | <= fare_amount * 1.0 (100% max) | 🟡 HIGH | FLAG |

---

### 3.3 Campos de Distância/Duração

#### trip_distance

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-019 | NOT NULL | 🟡 HIGH | QUARANTINE |
| DQ-020 | >= 0 | 🔴 CRITICAL | QUARANTINE |
| DQ-021 | <= 100 (milhas - threshold razoável NYC) | 🟡 HIGH | FLAG |
| DQ-022 | IF trip_distance > 0 THEN duration > 0 | 🟢 MEDIUM | FLAG |

#### trip_duration (calculado)

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-023 | > 0 minutos | 🔴 CRITICAL | QUARANTINE |
| DQ-024 | < 1440 minutos (24h) | 🟡 HIGH | FLAG |
| DQ-025 | Velocidade média < 100 mph | 🟢 MEDIUM | FLAG |

```sql
-- Validação de velocidade
CASE
    WHEN trip_duration_min > 0 AND trip_distance > 0 
         AND (trip_distance / (trip_duration_min / 60.0)) > 100
    THEN 'DQ-025: UNREALISTIC_SPEED'
    ELSE 'VALID'
END
```

---

### 3.4 Campos de Referência (FK)

#### payment_type

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-026 | NOT NULL | 🟡 HIGH | DEFAULT(5) |
| DQ-027 | IN (1, 2, 3, 4, 5, 6) | 🔴 CRITICAL | QUARANTINE |

#### ratecode_id

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-028 | IN (1, 2, 3, 4, 5, 6) | 🔴 CRITICAL | DEFAULT(1) |
| DQ-029 | IF rate = 2 (JFK) THEN fare >= $52 | 🟢 MEDIUM | FLAG |

#### trip_type

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-030 | IN (1, 2) | 🔴 CRITICAL | DEFAULT(1) |

#### pu_location_id / do_location_id

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-031 | NOT NULL | 🟡 HIGH | DEFAULT(264) |
| DQ-032 | BETWEEN 1 AND 265 | 🔴 CRITICAL | QUARANTINE |

---

### 3.5 Outros Campos

#### passenger_count

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-033 | BETWEEN 0 AND 9 | 🟢 MEDIUM | COALESCE(1) |

#### vendor_id

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-034 | IN (1, 2) | 🟡 HIGH | FLAG |

#### store_and_fwd_flag

| Regra ID | Regra | Severidade | Ação |
|----------|-------|------------|------|
| DQ-035 | IN ('Y', 'N', NULL) | 🟢 MEDIUM | DEFAULT('N') |

---

## 4. Estratégia de Quarentena

### 4.1 Estrutura da Tabela de Quarentena

```sql
CREATE TABLE quarantine.rejected_trips (
    quarantine_id       BIGINT IDENTITY(1,1) PRIMARY KEY,
    source_file         VARCHAR(100),
    source_row_number   BIGINT,
    rule_id             VARCHAR(10),       -- DQ-001, DQ-002, etc.
    rule_description    VARCHAR(200),
    severity            VARCHAR(20),       -- CRITICAL, HIGH, MEDIUM
    field_name          VARCHAR(50),
    field_value         NVARCHAR(MAX),
    record_json         NVARCHAR(MAX),     -- Registro completo em JSON
    quarantine_timestamp DATETIME DEFAULT GETDATE(),
    reprocess_status    VARCHAR(20) DEFAULT 'PENDING',
    reprocess_timestamp DATETIME NULL
);
```

### 4.2 Ações por Severidade

| Severidade | Ação | Destino | Reprocessamento |
|------------|------|---------|-----------------|
| 🔴 CRITICAL | REJECT | quarantine | Manual review |
| 🟡 HIGH | QUARANTINE | quarantine | Auto após correção |
| 🟢 MEDIUM | FLAG | target + flag | Não necessário |
| ℹ️ INFO | LOG | target | Não necessário |

### 4.3 Workflow de Quarentena

```
┌─────────────┐     ┌────────────────┐     ┌─────────────────┐
│   Source    │────▶│  DQ Validation │────▶│  VALID Records  │──▶ Silver
└─────────────┘     └───────┬────────┘     └─────────────────┘
                            │
                            │ FAILED
                            ▼
                    ┌───────────────┐
                    │  Quarantine   │
                    │    Table      │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │  Manual  │  │   Auto   │  │  Discard │
        │  Review  │  │  Reprocess│  │  (após N │
        │          │  │  (fix)   │  │   dias)  │
        └──────────┘  └──────────┘  └──────────┘
```

---

## 5. Regras de Reconciliação

### 5.1 Contagem de Registros

| Checkpoint | Validação | Threshold |
|------------|-----------|-----------|
| Source → Landing | COUNT match | 100% |
| Landing → Silver | COUNT (valid + quarantine) = landing | 100% |
| Silver → Gold | COUNT match (após dedup) | ≥99% |

### 5.2 Totais Financeiros

| Checkpoint | Validação | Threshold |
|------------|-----------|-----------|
| Source → Gold | SUM(total_amount) match | ±0.01% |

```sql
-- Reconciliação
SELECT 
    'Source' as layer, COUNT(*) as records, SUM(total_amount) as total
FROM landing.lnd_green_tripdata
UNION ALL
SELECT 
    'Silver', COUNT(*), SUM(total_amount)
FROM silver.slv_trips
WHERE dq_status = 'VALID'
UNION ALL
SELECT 
    'Quarantine', COUNT(*), NULL
FROM quarantine.rejected_trips
WHERE source_table = 'trips'
```

---

## 6. Métricas de Qualidade

### 6.1 KPIs de DQ

| Métrica | Fórmula | Target |
|---------|---------|--------|
| Overall Quality Rate | (valid / total) * 100 | ≥99% |
| Completeness Rate | (non_null / total) * 100 | ≥99% |
| Validity Rate | (valid_format / total) * 100 | ≥99% |
| Consistency Rate | (consistent / total) * 100 | ≥98% |
| Quarantine Rate | (quarantine / total) * 100 | <2% |

### 6.2 Dashboard de DQ

```
┌─────────────────────────────────────────────────────────────┐
│                    DQ DASHBOARD - BATCH 2021-04             │
├─────────────────┬─────────────────┬─────────────────────────┤
│  📊 QUALITY     │  ⚠️ QUARANTINE  │      ❌ REJECTED        │
│     98.7%       │      1.1%       │         0.2%            │
│   🟢 Target OK  │   🟡 Under 2%   │      🟢 Under 1%        │
├─────────────────┴─────────────────┴─────────────────────────┤
│  TOP 5 REGRAS VIOLADAS                                      │
│  1. DQ-003 (date range)     │ 4,521 records                 │
│  2. DQ-025 (speed)          │ 2,103 records                 │
│  3. DQ-012 (total mismatch) │ 1,847 records                 │
│  4. DQ-021 (distance)       │   892 records                 │
│  5. DQ-018 (tip > fare)     │   456 records                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 7. Alertas e Notificações

### 7.1 Triggers de Alerta

| Condição | Severidade | Destinatário | Canal |
|----------|------------|--------------|-------|
| Quality Rate < 95% | 🔴 CRÍTICO | Lisa Thompson | Email + Slack |
| Quality Rate < 99% | 🟡 WARNING | Lisa Thompson | Slack |
| Quarantine > 5% | 🔴 CRÍTICO | Lisa + Sarah | Email |
| Reconciliation fail | 🔴 CRÍTICO | Lisa Thompson | Email + Slack |
| New rule violation type | 🟡 WARNING | Lisa Thompson | Slack |

### 7.2 Template de Alerta

```
🚨 DQ ALERT - NYC Green Taxi Pipeline

Batch: 2021-04-15
Load Time: 2026-02-05 08:30:00

Issue: Quality Rate below threshold
Current: 94.2%
Target: 99%
Threshold: 95%

Top Violations:
- DQ-003: 15,234 records (date out of range)
- DQ-019: 3,456 records (null distance)

Action Required: Review quarantine table

Dashboard: [link]
```

---

## 8. Próximos Refinamentos (MIDSTREAM)

Este documento será expandido pelo **🛡️ DataSteward (Gaia)** com:

- [ ] Regras de DQ detalhadas por camada
- [ ] Implementação de Great Expectations / dbt tests
- [ ] Governance policies
- [ ] Data classification
- [ ] Lineage tracking

---

## 9. Resumo de Regras

| Categoria | Qtd Regras | Críticas | Altas | Médias |
|-----------|------------|----------|-------|--------|
| Data/Hora | 8 | 4 | 4 | 0 |
| Financeiro | 10 | 4 | 3 | 3 |
| Distância | 7 | 2 | 3 | 2 |
| Referência (FK) | 10 | 5 | 3 | 2 |
| Outros | 3 | 0 | 1 | 2 |
| **Total** | **38** | **15** | **14** | **9** |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Mary (BusinessAnalyst) | Versão inicial - 38 regras |

---

*Documento gerado pelo 📊 BusinessAnalyst Agent - Avanade™ Core*
