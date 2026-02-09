# ❓ Analytical Questions - Perguntas Analíticas

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 📊 Mary (BusinessAnalyst)  
> **Referências:** [problem-statement.md](../strategy/problem-statement.md) | [kpis.md](../strategy/kpis.md) | [sttm.md](sttm.md)

---

## 1. Visão Geral

Este documento define as perguntas analíticas que o projeto deve responder. Cada pergunta está vinculada a KPIs, stakeholders e requisitos de dados.

### 1.1 Categorias de Perguntas

| Categoria | Qtd | Foco |
|-----------|-----|------|
| 💰 Financeiro | 5 | Receita, custos, margens |
| 🚕 Operacional | 5 | Eficiência, utilização, tempo |
| 👤 Cliente | 3 | Satisfação, comportamento |
| 📍 Geográfico | 4 | Zonas, rotas, demanda |
| 📅 Temporal | 3 | Sazonalidade, tendências |

**Total: 20 perguntas analíticas**

---

## 2. Perguntas Financeiras

### AQ-01: Qual é a receita média por corrida?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual é a receita média por corrida (total_amount) e como varia por zona, tipo de pagamento e período? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | KPI-01: Receita Média por Corrida |
| **Stakeholder** | Sarah Chen (Diretora de Operações) |
| **Dimensões** | Zona (PU/DO), Tipo Pagamento, Dia da Semana, Hora |
| **Medidas** | AVG(total_amount), COUNT(trips), SUM(total_amount) |
| **Grain** | Por corrida |
| **Fontes** | fact_trips, dim_payment, dim_date, dim_location |

```sql
-- Query de exemplo
SELECT 
    d.day_name,
    p.payment_type_desc,
    AVG(f.total_amount) as avg_revenue,
    COUNT(*) as total_trips
FROM fact_trips f
JOIN dim_date d ON f.date_sk = d.date_sk
JOIN dim_payment p ON f.payment_type_sk = p.payment_type_sk
GROUP BY d.day_name, p.payment_type_desc
ORDER BY avg_revenue DESC
```

---

### AQ-02: Qual é a composição da receita por tipo de tarifa?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Como a receita total se distribui entre os componentes (fare, tip, tolls, surcharges)? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | KPI-01 |
| **Stakeholder** | Michael Rodriguez (CFO) |
| **Dimensões** | Componente de receita, Período |
| **Medidas** | SUM(fare_amount), SUM(tip_amount), SUM(tolls_amount), etc. |
| **Grain** | Por período (dia/semana/mês) |
| **Fontes** | fact_trips |

---

### AQ-03: Qual é o ticket médio por tipo de pagamento?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Existe diferença significativa no valor médio das corridas entre pagamentos em cartão vs dinheiro? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | KPI-01 |
| **Stakeholder** | Michael Rodriguez (CFO) |
| **Dimensões** | Tipo de Pagamento |
| **Medidas** | AVG(total_amount), AVG(tip_amount), COUNT(*) |
| **Grain** | Por tipo de pagamento |
| **Fontes** | fact_trips, dim_payment |

**Hipótese:** Corridas pagas com cartão têm gorjeta maior.

---

### AQ-04: Qual é a receita por milha e por minuto?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual a eficiência de receita considerando distância percorrida e tempo gasto? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | Métricas derivadas |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Zona, Hora do dia, Rate code |
| **Medidas** | AVG(revenue_per_mile), AVG(revenue_per_minute) |
| **Grain** | Por corrida agregada |
| **Fontes** | fact_trips, dim_rate |

---

### AQ-05: Qual é o impacto das gorjetas na receita total?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual percentual da receita vem de gorjetas? Quais fatores influenciam gorjetas maiores? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | Métricas derivadas (tip_percentage) |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Tipo pagamento, Zona, Distância, Hora |
| **Medidas** | SUM(tip_amount), AVG(tip_percentage), % de corridas com gorjeta |
| **Grain** | Por corrida |
| **Fontes** | fact_trips, dim_payment |

**Nota:** Gorjetas só são registradas para pagamentos com cartão.

---

## 3. Perguntas Operacionais

### AQ-06: Qual é a taxa de utilização da frota?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual percentual do tempo os táxis estão em corrida vs ociosos? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | KPI-02: Taxa de Utilização da Frota |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Hora, Dia da semana, Zona |
| **Medidas** | SUM(trip_duration), COUNT(DISTINCT vendor_id) |
| **Grain** | Por hora/zona |
| **Fontes** | fact_trips, dim_date |

---

### AQ-07: Qual é a duração média das corridas?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Quanto tempo em média dura uma corrida? Como varia por zona e horário? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | KPI-02 |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Zona origem/destino, Hora, Dia |
| **Medidas** | AVG(trip_duration_min), MIN, MAX, STDDEV |
| **Grain** | Por corrida |
| **Fontes** | fact_trips |

---

### AQ-08: Qual é a distância média das corridas?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual a distância média percorrida? Corridas mais longas são mais lucrativas? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | Métricas derivadas |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Rate code, Zona, Hora |
| **Medidas** | AVG(trip_distance), correlação com revenue |
| **Grain** | Por corrida |
| **Fontes** | fact_trips, dim_rate |

---

### AQ-09: Quantas corridas por hora por zona?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual o volume de corridas por hora em cada zona? Onde há maior/menor demanda? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | KPI-03: Tempo Médio de Espera (proxy) |
| **Stakeholder** | Sarah Chen, Jennifer Park |
| **Dimensões** | Hora, Zona |
| **Medidas** | COUNT(*), trips per hour |
| **Grain** | Por hora/zona |
| **Fontes** | fact_trips, dim_location |

---

### AQ-10: Qual é o número médio de passageiros?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Quantos passageiros em média por corrida? Corridas compartilhadas são comuns? |
| **Prioridade** | 🟢 Baixa |
| **KPI Vinculado** | - |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Hora, Dia, Zona |
| **Medidas** | AVG(passenger_count), % com >1 passageiro |
| **Grain** | Por corrida |
| **Fontes** | fact_trips |

---

## 4. Perguntas de Cliente

### AQ-11: Como se distribui o método de pagamento?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual a proporção de pagamentos em cartão vs dinheiro? Está mudando ao longo do tempo? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | Dashboard executivo |
| **Stakeholder** | Michael Rodriguez, Jennifer Park |
| **Dimensões** | Tipo pagamento, Mês, Zona |
| **Medidas** | COUNT(*) by payment_type, % distribution |
| **Grain** | Por período |
| **Fontes** | fact_trips, dim_payment |

---

### AQ-12: Qual tipo de corrida é mais comum?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Street-hail ou Dispatch? A tendência está mudando? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | - |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Trip type, Período, Zona |
| **Medidas** | COUNT(*) by trip_type, % distribution |
| **Grain** | Por período |
| **Fontes** | fact_trips, dim_trip_type |

---

### AQ-13: Quais corridas têm gorjeta zero?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual % de corridas não tem gorjeta? Está relacionado ao tipo de pagamento ou zona? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | KPI-06: NPS (proxy) |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Tipo pagamento, Zona, Hora |
| **Medidas** | % corridas com tip_amount = 0 |
| **Grain** | Por segmento |
| **Fontes** | fact_trips |

**Nota:** Corridas em dinheiro geralmente não registram gorjeta no sistema.

---

## 5. Perguntas Geográficas

### AQ-14: Quais são as top 10 zonas por receita?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Quais zonas de pickup geram mais receita total? E por receita média? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | Dashboard executivo |
| **Stakeholder** | Sarah Chen, Jennifer Park |
| **Dimensões** | Zona de pickup |
| **Medidas** | SUM(total_amount), AVG(total_amount), COUNT(*) |
| **Grain** | Por zona |
| **Fontes** | fact_trips, dim_location |

---

### AQ-15: Quais são as rotas mais frequentes?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Quais combinações origem-destino são mais comuns? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | - |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Zona pickup + Zona dropoff |
| **Medidas** | COUNT(*), AVG(total_amount), AVG(trip_distance) |
| **Grain** | Por par de zonas |
| **Fontes** | fact_trips, dim_location |

---

### AQ-16: Como é a demanda para aeroportos?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Qual o volume e receita de corridas JFK e LaGuardia? Padrões por horário? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | KPI-01 |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Rate code (JFK, Newark), Hora, Dia |
| **Medidas** | COUNT(*), AVG(total_amount), AVG(trip_distance) |
| **Grain** | Por aeroporto/período |
| **Fontes** | fact_trips, dim_rate |

---

### AQ-17: Onde há desequilíbrio oferta/demanda?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Quais zonas têm mais pickups que dropoffs (e vice-versa)? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | KPI-02 |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Zona, Hora |
| **Medidas** | COUNT(pickups) - COUNT(dropoffs) por zona |
| **Grain** | Por zona/hora |
| **Fontes** | fact_trips |

---

## 6. Perguntas Temporais

### AQ-18: Qual é o padrão semanal de demanda?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Como o volume de corridas varia por dia da semana? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | Dashboard executivo |
| **Stakeholder** | Sarah Chen, Jennifer Park |
| **Dimensões** | Dia da semana |
| **Medidas** | COUNT(*), AVG(total_amount) by day_of_week |
| **Grain** | Por dia |
| **Fontes** | fact_trips, dim_date |

---

### AQ-19: Quais são os horários de pico?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | Em quais horas do dia há maior volume de corridas? |
| **Prioridade** | 🔴 Alta |
| **KPI Vinculado** | KPI-02, KPI-03 |
| **Stakeholder** | Sarah Chen |
| **Dimensões** | Hora do dia, Dia da semana |
| **Medidas** | COUNT(*) by hour, heatmap |
| **Grain** | Por hora |
| **Fontes** | fact_trips |

---

### AQ-20: Há tendência mensal (Abr→Mai→Jun)?

| Atributo | Valor |
|----------|-------|
| **Pergunta** | O volume e receita estão crescendo, estáveis ou diminuindo ao longo do Q2? |
| **Prioridade** | 🟡 Média |
| **KPI Vinculado** | Todos |
| **Stakeholder** | Michael Rodriguez, Sarah Chen |
| **Dimensões** | Mês |
| **Medidas** | Trend analysis, MoM growth |
| **Grain** | Por mês |
| **Fontes** | fact_trips, dim_date |

---

## 7. Matriz de Priorização

### 7.1 Por Prioridade

| Prioridade | Perguntas | Foco Principal |
|------------|-----------|----------------|
| 🔴 **Alta** | AQ-01, 03, 06, 09, 11, 14, 16, 18, 19 | KPIs principais, Dashboard |
| 🟡 **Média** | AQ-02, 04, 05, 07, 08, 12, 13, 15, 17, 20 | Análise secundária |
| 🟢 **Baixa** | AQ-10 | Nice to have |

### 7.2 Por Stakeholder

| Stakeholder | Perguntas |
|-------------|-----------|
| Sarah Chen | AQ-01, 04-10, 12-19 |
| Michael Rodriguez | AQ-02, 03, 05, 11, 20 |
| Jennifer Park | AQ-09, 11, 14, 18 |
| David Kim | (Relatórios regulatórios - todas) |

### 7.3 Por KPI

| KPI | Perguntas Relacionadas |
|-----|------------------------|
| KPI-01 (Receita/Trip) | AQ-01, 02, 03, 04, 05, 14, 16 |
| KPI-02 (Utilização) | AQ-06, 07, 08, 09, 17 |
| KPI-03 (Tempo Espera) | AQ-09 |
| KPI-04 (DQ) | - (técnico) |
| KPI-05 (Relatório) | Todas |
| KPI-06 (NPS) | AQ-13 |

---

## 8. Requisitos de Dashboard

### 8.1 Visualizações Necessárias

| Pergunta | Tipo de Visual | Descrição |
|----------|----------------|-----------|
| AQ-01 | KPI Card + Line | Receita média com trend |
| AQ-11 | Pie/Donut | Distribuição pagamentos |
| AQ-14 | Bar Chart | Top 10 zonas |
| AQ-18 | Column Chart | Volume por dia semana |
| AQ-19 | Heatmap | Hora x Dia da semana |

### 8.2 Filtros Globais Necessários

- Data (range picker)
- Zona de Pickup
- Zona de Dropoff
- Tipo de Pagamento
- Tipo de Tarifa (Rate Code)

---

## 9. Validação

Cada pergunta deve ser validada com:

- [ ] Query funcional no Gold layer
- [ ] Dados suficientes para resposta significativa
- [ ] Visualização apropriada definida
- [ ] Stakeholder aprovou interpretação

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Mary (BusinessAnalyst) | Versão inicial - 20 perguntas |

---

*Documento gerado pelo 📊 BusinessAnalyst Agent - Avanade™ Core*
