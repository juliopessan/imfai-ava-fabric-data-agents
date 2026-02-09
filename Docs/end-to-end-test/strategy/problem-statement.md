# 📋 Problem Statement

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 🎯 Alex (DataStrategist)  
> **Status:** ✅ Aprovado

---

## 1. Sumário Executivo

A NYC Taxi & Limousine Commission (TLC) enfrenta desafios críticos na análise de dados operacionais dos táxis verdes (boro taxis). A falta de uma infraestrutura de dados moderna impede a tomada de decisões baseada em evidências, resultando em perdas estimadas de **$3M/ano** entre receita não otimizada e multas regulatórias.

---

## 2. Contexto do Negócio

### 2.1 Background

Os **Green Taxis** (táxis verdes) foram introduzidos em 2013 para atender bairros externos de Nova York (Brooklyn, Queens, Bronx, Staten Island) onde táxis amarelos tradicionalmente não operavam. A TLC é responsável por regular e monitorar aproximadamente **50.000 veículos** e **100.000 motoristas** licenciados.

### 2.2 Situação Atual

| Aspecto | Estado Atual | Problema |
|---------|--------------|----------|
| **Dados** | CSVs mensais isolados | Sem consolidação ou histórico |
| **Análise** | Planilhas manuais | Demorada, propensa a erros |
| **Relatórios** | Ad-hoc, reativo | Sem visão proativa |
| **Decisões** | Baseadas em intuição | Falta de evidências |

### 2.3 Drivers de Mudança

- 📈 Pressão por **eficiência operacional** pós-pandemia
- 📊 Exigências regulatórias de **relatórios trimestrais**
- 🎯 Competição com **rideshare** (Uber, Lyft)
- 💡 Iniciativa de **modernização digital** da cidade

---

## 3. Declaração do Problema

### 3.1 Problema Principal

> **"A TLC não consegue analisar de forma eficiente os dados operacionais dos táxis verdes, impedindo a identificação de padrões de demanda, otimização de rotas e tomada de decisões estratégicas baseadas em dados."**

### 3.2 Problemas Específicos

| ID | Problema | Impacto |
|----|----------|---------|
| P1 | Dados fragmentados em múltiplos CSVs sem integração | Análises inconsistentes |
| P2 | Ausência de métricas padronizadas de desempenho | Impossível comparar períodos |
| P3 | Falta de visibilidade por zona geográfica | Má alocação de veículos |
| P4 | Tempo excessivo para gerar relatórios regulatórios | Risco de multas |
| P5 | Dados de qualidade duvidosa (erros não tratados) | Decisões incorretas |

### 3.3 Perguntas de Negócio Não Respondidas

1. Quais são as **top 10 zonas** com maior demanda por horário do dia?
2. Qual o **ticket médio** por tipo de pagamento e por zona?
3. Qual a **eficiência** das corridas (receita por milha/minuto)?
4. Quais são os **padrões sazonais** de demanda?
5. Qual o **impacto** de gorjetas na receita total?

---

## 4. Impacto Quantificado

### 4.1 Impacto Financeiro

| Categoria | Valor Anual | Detalhamento |
|-----------|-------------|--------------|
| Receita perdida por má alocação | **$2.5M** | 15% de corridas não atendidas |
| Multas regulatórias | **$500K** | Atrasos em relatórios obrigatórios |
| Custo de análise manual | **$200K** | 4 FTEs dedicados |
| **Total** | **$3.2M/ano** | |

### 4.2 Impacto Operacional

| Métrica | Atual | Meta | Gap |
|---------|-------|------|-----|
| Tempo médio de espera | 12 min | 7 min | -42% |
| Utilização da frota | 65% | 80% | +23% |
| Tempo para relatório | 5 dias | 1 hora | -99% |
| Taxa de erros de dados | 8% | <1% | -87% |

### 4.3 Impacto no Cliente

| Indicador | Atual | Meta |
|-----------|-------|------|
| NPS (Net Promoter Score) | 45 | 70 |
| Reclamações/mês | 2.500 | 500 |
| Tempo de resposta a issues | 48h | 4h |

---

## 5. Escopo do Projeto

### 5.1 ✅ In Scope

| Item | Descrição |
|------|-----------|
| **Dados** | Green taxi trip data (Q2/2021: Abril, Maio, Junho) |
| **Fontes** | CSVs de corridas, JSONs de referência, TSVs de lookup |
| **Pipeline** | ETL batch com camadas Landing → Silver → Gold |
| **Plataforma** | Azure Synapse Analytics / Databricks |
| **Visualização** | Dashboards Power BI para stakeholders |
| **Qualidade** | Regras de DQ, quarentena, reconciliação |

### 5.2 ❌ Out of Scope

| Item | Justificativa |
|------|---------------|
| Yellow Taxis | Escopo futuro (Fase 2) |
| FHV (Uber/Lyft) | Dados não disponíveis |
| Streaming/Real-time | Complexidade, orçamento |
| Previsão (ML) | Após baseline estabelecido |
| Apps mobile | Fora da iniciativa atual |

### 5.3 Premissas

1. Dados históricos de Q2/2021 são representativos
2. Infraestrutura Azure já disponível
3. Stakeholders disponíveis para validação
4. Orçamento aprovado para 3 meses de projeto

### 5.4 Restrições

1. Prazo máximo: 12 semanas
2. Budget: $150K
3. Compliance com GDPR/CCPA para dados de localização
4. Uso exclusivo de ferramentas Microsoft/Azure

---

## 6. Stakeholders

### 6.1 Matriz RACI

| Stakeholder | Papel | R | A | C | I |
|-------------|-------|---|---|---|---|
| **Sarah Chen** | Diretora de Operações | | ✓ | ✓ | |
| **Michael Rodriguez** | CFO | | | ✓ | ✓ |
| **Jennifer Park** | Head de BI | ✓ | | ✓ | |
| **David Kim** | Compliance Officer | | | ✓ | ✓ |
| **Lisa Thompson** | Data Engineer Lead | ✓ | | | |

### 6.2 Necessidades por Stakeholder

| Stakeholder | Necessidade Principal | Frequência |
|-------------|----------------------|------------|
| Sarah Chen | Dashboard de operações em tempo quase-real | Diário |
| Michael Rodriguez | Relatório de receita e custos | Semanal |
| Jennifer Park | Dados limpos para análises | Contínuo |
| David Kim | Relatórios de compliance | Trimestral |
| Lisa Thompson | Pipeline automatizado e documentado | Contínuo |

---

## 7. Critérios de Sucesso

> Detalhado em: [`kpis.md`](kpis.md) e [`success-criteria.md`](success-criteria.md)

### 7.1 Critérios Obrigatórios

| ID | Critério | Meta | Prazo |
|----|----------|------|-------|
| S1 | Pipeline ETL funcional | 100% automatizado | Semana 8 |
| S2 | Qualidade de dados | >99% accuracy | Semana 10 |
| S3 | Dashboard operacional | MVP entregue | Semana 12 |

### 7.2 Critérios Desejáveis

| ID | Critério | Meta |
|----|----------|------|
| D1 | Tempo de refresh | <15 min |
| D2 | Documentação completa | 100% |
| D3 | Testes automatizados | >80% coverage |

---

## 8. Riscos Identificados

| ID | Risco | Probabilidade | Impacto | Mitigação |
|----|-------|---------------|---------|-----------|
| R1 | Qualidade dos dados fonte | Alta | Alto | Quarentena + DQ rules |
| R2 | Atraso em aprovações | Média | Médio | Escalation path definido |
| R3 | Mudança de escopo | Média | Alto | Change control rígido |
| R4 | Indisponibilidade de recursos | Baixa | Alto | Backup de conhecimento |

---

## 9. Próximos Passos

| # | Ação | Responsável | Prazo |
|---|------|-------------|-------|
| 1 | Validar problem statement | Sarah Chen | 1 dia |
| 2 | Definir KPIs detalhados | Alex (DataStrategist) | 2 dias |
| 3 | Criar STTM (Source-to-Target Mapping) | Mary (BusinessAnalyst) | 3 dias |
| 4 | Iniciar arquitetura técnica | Winston (DataArchitect) | 5 dias |

---

## 10. Aprovações

| Nome | Papel | Data | Assinatura |
|------|-------|------|------------|
| Sarah Chen | Sponsor | ____/____/____ | ___________ |
| Michael Rodriguez | CFO | ____/____/____ | ___________ |
| Jennifer Park | Head BI | ____/____/____ | ___________ |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Alex (DataStrategist) | Versão inicial |

---

*Documento gerado pelo 🎯 DataStrategist Agent - Avanade™ Core*
