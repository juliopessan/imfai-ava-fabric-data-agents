# ✅ Success Criteria - Critérios de Sucesso

> **Projeto:** NYC Green Taxi Analytics  
> **Versão:** 1.0  
> **Data:** 2026-02-05  
> **Autor:** 🎯 Alex (DataStrategist)  
> **Referências:** [problem-statement.md](problem-statement.md) | [kpis.md](kpis.md)

---

## 1. Visão Geral

Este documento define os critérios objetivos e mensuráveis que determinam o sucesso do projeto. Os critérios estão organizados em três categorias:

| Categoria | Descrição | Peso |
|-----------|-----------|------|
| 🔴 **Must Have** | Obrigatórios - projeto falha sem eles | 60% |
| 🟡 **Should Have** | Importantes - agregam valor significativo | 30% |
| 🟢 **Nice to Have** | Desejáveis - diferenciais | 10% |

---

## 2. Critérios Must Have (Obrigatórios)

### MH-01: Pipeline ETL Funcional

| Atributo | Valor |
|----------|-------|
| **Descrição** | Pipeline automatizado processando dados das 3 camadas (Landing → Silver → Gold) |
| **Métrica** | 100% das tabelas definidas no STTM criadas e populadas |
| **Evidência** | Scripts DDL/ETL executando sem erros |
| **Prazo** | Semana 8 |
| **Owner** | Lisa Thompson (Data Engineer Lead) |
| **Validação** | `SELECT COUNT(*) FROM gold.fact_trips` > 0 |

**Checklist de Aceitação:**
- [ ] Tabelas Landing criadas (4 tabelas)
- [ ] Tabelas Silver criadas (4 tabelas)
- [ ] Tabelas Gold criadas (Facts + Dims)
- [ ] Tabelas de referência populadas
- [ ] ETL executando em schedule (diário)
- [ ] Logs de execução disponíveis

---

### MH-02: Qualidade de Dados ≥ 99%

| Atributo | Valor |
|----------|-------|
| **Descrição** | Taxa de registros válidos após aplicação de regras de DQ |
| **Métrica** | `(registros_válidos / registros_totais) * 100 ≥ 99%` |
| **Evidência** | Relatório de DQ por batch |
| **Prazo** | Semana 10 |
| **Owner** | Lisa Thompson |
| **Validação** | Dashboard de DQ mostrando ≥99% por 5 dias consecutivos |

**Checklist de Aceitação:**
- [ ] Regras de DQ definidas e documentadas
- [ ] Quarentena implementada para registros rejeitados
- [ ] Alertas configurados para DQ < 95%
- [ ] Processo de correção/reprocessamento definido
- [ ] Auditoria de DQ disponível

---

### MH-03: Dashboard Operacional MVP

| Atributo | Valor |
|----------|-------|
| **Descrição** | Dashboard Power BI com KPIs principais acessível aos stakeholders |
| **Métrica** | 6 KPIs visualizados com dados reais |
| **Evidência** | Link do dashboard publicado |
| **Prazo** | Semana 12 |
| **Owner** | Jennifer Park (Head de BI) |
| **Validação** | Demonstração para stakeholders com aprovação formal |

**Checklist de Aceitação:**
- [ ] 6 KPIs principais exibidos
- [ ] Filtros por data, zona, tipo de pagamento
- [ ] Refresh automático configurado
- [ ] Acesso concedido a todos stakeholders
- [ ] Mobile-friendly

---

### MH-04: Documentação Completa

| Atributo | Valor |
|----------|-------|
| **Descrição** | Documentação técnica e de negócio completa |
| **Métrica** | 100% dos artefatos obrigatórios do Avanade Core criados |
| **Evidência** | Repositório com todos os documentos |
| **Prazo** | Semana 12 |
| **Owner** | Todos os agentes |
| **Validação** | Gate 3 aprovado |

**Artefatos Obrigatórios:**
- [ ] Problem Statement ✅
- [ ] KPIs ✅
- [ ] Success Criteria (este documento) ✅
- [ ] STTM (Source-to-Target Mapping)
- [ ] Architecture Document
- [ ] Data Model
- [ ] DQ Rules
- [ ] DDL Scripts
- [ ] ETL Scripts
- [ ] Unit Tests
- [ ] Pipeline Documentation

---

### MH-05: Tempo de Relatório < 4 horas

| Atributo | Valor |
|----------|-------|
| **Descrição** | Capacidade de gerar relatório regulatório em menos de 4 horas |
| **Métrica** | Tempo desde solicitação até entrega < 4h |
| **Evidência** | Teste cronometrado de geração de relatório |
| **Prazo** | Semana 10 |
| **Owner** | David Kim (Compliance) |
| **Validação** | 3 testes bem-sucedidos documentados |

**Checklist de Aceitação:**
- [ ] Template de relatório regulatório criado
- [ ] Query otimizada para extração
- [ ] Processo documentado
- [ ] Treinamento realizado
- [ ] Teste cronometrado < 4h

---

## 3. Critérios Should Have (Importantes)

### SH-01: Testes Automatizados > 80% Coverage

| Atributo | Valor |
|----------|-------|
| **Descrição** | Cobertura de testes unitários nas transformações críticas |
| **Métrica** | ≥ 80% das transformações testadas |
| **Evidência** | Relatório de cobertura de testes |
| **Prazo** | Semana 11 |
| **Owner** | Lisa Thompson |

**Checklist de Aceitação:**
- [ ] Testes de integridade de PK/FK
- [ ] Testes de transformações de negócio
- [ ] Testes de agregações
- [ ] Testes de edge cases
- [ ] CI/CD com execução automática de testes

---

### SH-02: Tempo de Refresh < 15 minutos

| Atributo | Valor |
|----------|-------|
| **Descrição** | Pipeline completo executando em menos de 15 minutos |
| **Métrica** | Duração end-to-end do ETL < 15 min |
| **Evidência** | Logs de execução |
| **Prazo** | Semana 10 |
| **Owner** | Lisa Thompson |

**Checklist de Aceitação:**
- [ ] Baseline de performance documentado
- [ ] Otimizações implementadas
- [ ] Monitoramento de duração
- [ ] Alertas para execuções > 20 min

---

### SH-03: Análise por Zona Geográfica

| Atributo | Valor |
|----------|-------|
| **Descrição** | Capacidade de analisar métricas por zona de pickup/dropoff |
| **Métrica** | 263 zonas de NYC mapeadas e analisáveis |
| **Evidência** | Visualização de mapa no dashboard |
| **Prazo** | Semana 12 |
| **Owner** | Jennifer Park |

**Checklist de Aceitação:**
- [ ] Tabela de zonas (dim_location) populada
- [ ] Lookup de nomes de bairros
- [ ] Visualização de mapa implementada
- [ ] Top N zonas por métrica

---

### SH-04: Alertas Proativos

| Atributo | Valor |
|----------|-------|
| **Descrição** | Sistema de alertas para anomalias em KPIs |
| **Métrica** | Alertas configurados para todos os 6 KPIs |
| **Evidência** | Configuração de alertas documentada |
| **Prazo** | Semana 11 |
| **Owner** | Jennifer Park |

**Checklist de Aceitação:**
- [ ] Thresholds definidos por KPI
- [ ] Canais de notificação configurados (email/Slack)
- [ ] Escalation matrix definida
- [ ] Teste de alertas realizado

---

## 4. Critérios Nice to Have (Desejáveis)

### NH-01: Histórico de 12 Meses

| Atributo | Valor |
|----------|-------|
| **Descrição** | Expandir análise para 12 meses de dados históricos |
| **Métrica** | Dados de Jan-Dez 2021 disponíveis |
| **Prazo** | Fase 2 |

---

### NH-02: Comparativo Yellow vs Green

| Atributo | Valor |
|----------|-------|
| **Descrição** | Incluir dados de táxis amarelos para comparação |
| **Métrica** | Dashboard comparativo disponível |
| **Prazo** | Fase 2 |

---

### NH-03: Previsão de Demanda (ML)

| Atributo | Valor |
|----------|-------|
| **Descrição** | Modelo de ML para prever demanda por zona/hora |
| **Métrica** | Accuracy > 85% |
| **Prazo** | Fase 3 |

---

## 5. Matriz de Validação por Gate

### Gate 1 (UPSTREAM → MIDSTREAM)

| Critério | Status | Validador |
|----------|--------|-----------|
| Problem Statement aprovado | ✅ | Sarah Chen |
| KPIs definidos e validados | ✅ | Sarah Chen |
| Success Criteria documentados | ✅ | Sarah Chen |
| STTM criado | ⏳ Pendente | Jennifer Park |
| Analytical Questions definidas | ⏳ Pendente | Jennifer Park |
| DQ Initial documentado | ⏳ Pendente | Lisa Thompson |

### Gate 2 (MIDSTREAM → DOWNSTREAM)

| Critério | Status | Validador |
|----------|--------|-----------|
| Architecture aprovada | ⏳ Pendente | Lisa Thompson |
| Data Model finalizado | ⏳ Pendente | Jennifer Park |
| DQ Rules completas | ⏳ Pendente | David Kim |
| Tech stack definido | ⏳ Pendente | Lisa Thompson |

### Gate 3 (DOWNSTREAM → PRODUCTION)

| Critério | Status | Validador |
|----------|--------|-----------|
| DDL Scripts validados | ⏳ Pendente | Lisa Thompson |
| ETL Scripts testados | ⏳ Pendente | Lisa Thompson |
| Unit Tests passando | ⏳ Pendente | Lisa Thompson |
| Dashboard funcional | ⏳ Pendente | Jennifer Park |
| Documentação completa | ⏳ Pendente | Todos |
| DQ ≥ 99% | ⏳ Pendente | Lisa Thompson |

---

## 6. Critérios de Aceite Final

O projeto será considerado **SUCESSO** quando:

```
✅ TODOS os critérios Must Have atendidos (5/5)
✅ ≥ 75% dos critérios Should Have atendidos (3/4)
✅ Gate 3 aprovado formalmente
✅ Stakeholders assinaram aceite
```

O projeto será considerado **SUCESSO PARCIAL** quando:

```
⚠️ TODOS os Must Have atendidos
⚠️ < 75% dos Should Have atendidos
⚠️ Plano de ação para pendências
```

O projeto será considerado **FALHA** quando:

```
❌ Qualquer Must Have não atendido no prazo
❌ Sem plano de recuperação viável
```

---

## 7. Processo de Validação

### 7.1 Revisões Programadas

| Semana | Revisão | Participantes | Foco |
|--------|---------|---------------|------|
| 4 | Checkpoint 1 | Tech team | MH-01 progresso |
| 8 | Checkpoint 2 | Todos | MH-01, MH-02 |
| 10 | Checkpoint 3 | Todos | MH-03, MH-05 |
| 12 | Final Review | Todos + Sponsor | Todos os critérios |

### 7.2 Evidências Requeridas

Cada critério deve ter:
1. **Screenshot/Demo** - Prova visual
2. **Métricas** - Números que comprovam
3. **Sign-off** - Aprovação do owner

---

## 8. Aprovações

| Critério | Owner | Aprovado | Data |
|----------|-------|----------|------|
| Must Have (todos) | Sarah Chen | ⬜ | ___/___/___ |
| Should Have (todos) | Jennifer Park | ⬜ | ___/___/___ |
| Projeto Completo | Michael Rodriguez | ⬜ | ___/___/___ |

---

## Histórico de Versões

| Versão | Data | Autor | Alterações |
|--------|------|-------|------------|
| 1.0 | 2026-02-05 | Alex (DataStrategist) | Versão inicial |

---

*Documento gerado pelo 🎯 DataStrategist Agent - Avanade™ Core*
