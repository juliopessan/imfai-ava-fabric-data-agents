# 📊 KPIs - Key Performance Indicators

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 🎯 Alex (DataStrategist)  
> **Referência:** [problem-statement.md](problem-statement.md)

---

## 1. Sumário de KPIs

| # | KPI | Categoria | Baseline | Target | Prazo |
|---|-----|-----------|----------|--------|-------|
| 1 | Receita Média por Corrida | Financeiro | $12.50 | $14.00 | Q2/2026 |
| 2 | Taxa de Utilização da Frota | Operacional | 65% | 80% | Q2/2026 |
| 3 | Tempo Médio de Espera | Cliente | 12 min | 7 min | Q2/2026 |
| 4 | Taxa de Qualidade de Dados | Técnico | 92% | 99% | Semana 10 |
| 5 | Tempo de Geração de Relatório | Operacional | 5 dias | 1 hora | Semana 8 |
| 6 | NPS (Net Promoter Score) | Cliente | 45 | 70 | Q3/2026 |

---

## 2. Detalhamento dos KPIs

### 📈 KPI-01: Receita Média por Corrida

| Atributo | Valor |
|----------|-------|
| **Nome** | Receita Média por Corrida (Average Revenue per Trip) |
| **Categoria** | Financeiro |
| **Descrição** | Valor médio faturado por corrida completada, incluindo tarifa base, distância, tempo e gorjetas |
| **Fórmula** | `SUM(total_amount) / COUNT(trip_id)` |
| **Unidade** | USD ($) |
| **Baseline** | $12.50 (Q2/2021) |
| **Target** | $14.00 (+12%) |
| **Threshold** | 🔴 <$11.00 \| 🟡 $11-$13 \| 🟢 >$13 |
| **Frequência** | Diário |
| **Data Source** | `gold.fact_trips` |
| **Owner** | Sarah Chen (Diretora de Operações) |
| **Dimensões** | Zona, Tipo Pagamento, Dia da Semana, Hora |

```sql
-- Cálculo do KPI
SELECT 
    DATE(pickup_datetime) as data,
    AVG(total_amount) as receita_media_corrida,
    COUNT(*) as total_corridas
FROM gold.fact_trips
WHERE trip_status = 'completed'
GROUP BY DATE(pickup_datetime)
```

---

### 📈 KPI-02: Taxa de Utilização da Frota

| Atributo | Valor |
|----------|-------|
| **Nome** | Taxa de Utilização da Frota (Fleet Utilization Rate) |
| **Categoria** | Operacional |
| **Descrição** | Percentual de tempo que os veículos estão em corrida vs disponíveis |
| **Fórmula** | `SUM(trip_duration_minutes) / SUM(shift_duration_minutes) * 100` |
| **Unidade** | Percentual (%) |
| **Baseline** | 65% |
| **Target** | 80% (+23%) |
| **Threshold** | 🔴 <60% \| 🟡 60-75% \| 🟢 >75% |
| **Frequência** | Diário |
| **Data Source** | `gold.fact_trips`, `silver.driver_shifts` |
| **Owner** | Sarah Chen (Diretora de Operações) |
| **Dimensões** | Zona, Turno, Dia da Semana |

```sql
-- Cálculo aproximado (baseado em duração de corridas)
SELECT 
    DATE(pickup_datetime) as data,
    pu_location_id as zona,
    SUM(DATEDIFF(MINUTE, pickup_datetime, dropoff_datetime)) as minutos_em_corrida,
    COUNT(DISTINCT vendor_id) as veiculos_ativos
FROM gold.fact_trips
GROUP BY DATE(pickup_datetime), pu_location_id
```

---

### 📈 KPI-03: Tempo Médio de Espera

| Atributo | Valor |
|----------|-------|
| **Nome** | Tempo Médio de Espera do Passageiro (Avg Passenger Wait Time) |
| **Categoria** | Cliente |
| **Descrição** | Tempo médio entre solicitação e início da corrida |
| **Fórmula** | `AVG(pickup_datetime - request_datetime)` |
| **Unidade** | Minutos |
| **Baseline** | 12 minutos |
| **Target** | 7 minutos (-42%) |
| **Threshold** | 🔴 >15min \| 🟡 10-15min \| 🟢 <10min |
| **Frequência** | Horário |
| **Data Source** | `gold.fact_trips` (proxy: densidade de corridas por hora/zona) |
| **Owner** | Jennifer Park (Head de BI) |
| **Dimensões** | Zona, Hora do Dia, Dia da Semana |

> **Nota:** Dado que o dataset não tem timestamp de solicitação, este KPI será medido indiretamente pela densidade de táxis disponíveis por zona/hora.

---

### 📈 KPI-04: Taxa de Qualidade de Dados

| Atributo | Valor |
|----------|-------|
| **Nome** | Taxa de Qualidade de Dados (Data Quality Rate) |
| **Categoria** | Técnico |
| **Descrição** | Percentual de registros que passam em todas as validações de DQ |
| **Fórmula** | `(total_records - quarantine_records) / total_records * 100` |
| **Unidade** | Percentual (%) |
| **Baseline** | 92% (8% de erros identificados) |
| **Target** | 99% |
| **Threshold** | 🔴 <95% \| 🟡 95-98% \| 🟢 >98% |
| **Frequência** | Por carga (batch) |
| **Data Source** | `audit.dq_results`, `quarantine.rejected_records` |
| **Owner** | Lisa Thompson (Data Engineer Lead) |
| **Dimensões** | Fonte, Tipo de Erro, Regra DQ violada |

```sql
-- Cálculo do KPI
SELECT 
    load_date,
    source_table,
    total_records,
    passed_records,
    failed_records,
    (passed_records * 100.0 / total_records) as quality_rate
FROM audit.dq_summary
ORDER BY load_date DESC
```

---

### 📈 KPI-05: Tempo de Geração de Relatório

| Atributo | Valor |
|----------|-------|
| **Nome** | Tempo de Geração de Relatório Regulatório |
| **Categoria** | Operacional |
| **Descrição** | Tempo total desde solicitação até entrega do relatório de compliance |
| **Fórmula** | `delivery_timestamp - request_timestamp` |
| **Unidade** | Horas |
| **Baseline** | 120 horas (5 dias) |
| **Target** | 1 hora |
| **Threshold** | 🔴 >24h \| 🟡 4-24h \| 🟢 <4h |
| **Frequência** | Por demanda |
| **Data Source** | Sistema de tickets / Pipeline logs |
| **Owner** | David Kim (Compliance Officer) |
| **Dimensões** | Tipo de Relatório, Complexidade |

---

### 📈 KPI-06: Net Promoter Score (NPS)

| Atributo | Valor |
|----------|-------|
| **Nome** | Net Promoter Score |
| **Categoria** | Cliente |
| **Descrição** | Índice de satisfação e lealdade dos passageiros |
| **Fórmula** | `%Promotores (9-10) - %Detratores (0-6)` |
| **Unidade** | Score (-100 a +100) |
| **Baseline** | 45 |
| **Target** | 70 (+55%) |
| **Threshold** | 🔴 <30 \| 🟡 30-60 \| 🟢 >60 |
| **Frequência** | Mensal |
| **Data Source** | Pesquisa de satisfação (externo) |
| **Owner** | Sarah Chen (Diretora de Operações) |
| **Dimensões** | Zona, Período |

> **Nota:** Este KPI é medido externamente. O projeto de dados habilitará análise correlacionada com métricas operacionais.

---

## 3. KPIs Derivados (Calculados)

Além dos KPIs principais, o pipeline calculará métricas derivadas:

| Métrica | Fórmula | Uso |
|---------|---------|-----|
| **Receita por Milha** | `total_amount / trip_distance` | Eficiência de pricing |
| **Receita por Minuto** | `total_amount / trip_duration` | Eficiência de tempo |
| **Taxa de Gorjeta** | `tip_amount / fare_amount * 100` | Satisfação do cliente |
| **Trips por Hora por Zona** | `COUNT(*) / hora / zona` | Demanda geográfica |
| **Ticket Médio por Pagamento** | `AVG(total_amount) GROUP BY payment_type` | Mix de pagamento |

---

## 4. Dashboard de KPIs

### 4.1 Visão Executiva (Power BI)

```
┌─────────────────────────────────────────────────────────────────┐
│                    NYC GREEN TAXI - KPI DASHBOARD               │
├─────────────────┬─────────────────┬─────────────────────────────┤
│   💰 RECEITA    │  🚕 UTILIZAÇÃO  │      📊 QUALIDADE           │
│   $13.75/trip   │     72%         │         98.5%               │
│   🟢 +10%       │   🟡 +7%        │       🟢 +6.5%              │
├─────────────────┴─────────────────┴─────────────────────────────┤
│                    📈 TENDÊNCIA (30 DIAS)                       │
│  ▁▂▃▄▅▆▇█▇▆▅▄▃▂▁▂▃▄▅▆▇█▇▆▅▄▃▂▁                                │
├─────────────────────────────────────────────────────────────────┤
│  TOP 5 ZONAS POR RECEITA    │  DISTRIBUIÇÃO PAGAMENTOS         │
│  1. JFK Airport   $18.50    │  💳 Card:  68%                   │
│  2. LaGuardia     $16.20    │  💵 Cash:  30%                   │
│  3. Downtown BK   $14.80    │  📱 Other:  2%                   │
│  4. Astoria       $13.90    │                                  │
│  5. Flushing      $13.20    │                                  │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 Alertas Configurados

| KPI | Condição | Ação |
|-----|----------|------|
| Receita Média | < $11.00 por 3 dias | Email para Sarah Chen |
| Qualidade Dados | < 95% em batch | Slack para Lisa Thompson |
| Tempo Relatório | > 24h pendente | Escalation para David Kim |

---

## 5. Governança de KPIs

### 5.1 Revisão e Atualização

| Frequência | Ação | Responsável |
|------------|------|-------------|
| Diário | Monitoramento de thresholds | Dashboard automático |
| Semanal | Revisão de tendências | Jennifer Park |
| Mensal | Análise de causa-raiz | Todos stakeholders |
| Trimestral | Revisão de targets | Sarah Chen + CFO |

### 5.2 Versionamento

Qualquer mudança em KPIs (fórmula, target, threshold) deve ser:
1. Documentada neste arquivo
2. Aprovada pelo Owner do KPI
3. Comunicada aos stakeholders
4. Registrada no histórico de versões

---

## 6. Mapeamento para Artefatos Técnicos

| KPI | Tabela Gold | Coluna | Agregação |
|-----|-------------|--------|-----------|
| KPI-01 | `fact_trips` | `total_amount` | AVG |
| KPI-02 | `fact_trips` | `trip_duration` | SUM/ratio |
| KPI-03 | `fact_trips` | (calculado) | AVG |
| KPI-04 | `audit.dq_summary` | `quality_rate` | Latest |
| KPI-05 | (externo) | - | - |
| KPI-06 | (externo) | - | - |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Alex (DataStrategist) | Versão inicial - 6 KPIs definidos |

---

*Documento gerado pelo 🎯 DataStrategist Agent - Avanade™ Core*
