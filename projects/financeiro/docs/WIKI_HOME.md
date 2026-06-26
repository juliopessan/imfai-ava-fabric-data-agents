# 📚 Financeiro Data Migration Agents — Wiki

> Central de conhecimento técnico e operacional para o suite de agentes de migração de dados Financeiro.

---

## 🎯 Navegação Principal

### 📖 Documentação Técnica
- [Visão Geral Técnica](TECHNICAL_DOCUMENTATION.md) — Arquitetura geral, componentes, fluxos
- [Referência de APIs](API_REFERENCE.md) — Endpoints, payloads, autenticação, exemplos
- [Guia de Integração](INTEGRATION_GUIDE.md) — Padrões de conexão (Push/Pull/Private Link)
- [Arquitetura de Dashboards](DASHBOARD_ARCHITECTURE.md) — Design, componentes, KPIs

### 🔧 Guias Operacionais
- [Blueprint — 3 Padrões de Conexão](BLUEPRINT_GUIDE.md) — Especificações técnicas de cada padrão
- [Best Practices](BEST_PRACTICES.md) — Recomendações de segurança, performance, observabilidade
- [Troubleshooting](TROUBLESHOOTING.md) — Diagnóstico de problemas comuns

### 🛠️ Ferramentas & Calculadoras
- [Calculadora de Esforço](../EFFORT_CALCULATOR.html) — Estimativa de horas/custos
- [Proposta Comercial](../COMMERCIAL_PROPOSAL_ONE_PAGE.html) — ROI, timeline, padrões

### 📊 Dashboards
- [Portal Principal](../INDEX.html) — Hub central de navegação
- [Dashboard Consolidado](../00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html) — Relatório completo (Upstream/Midstream/Downstream)
- [Dashboard Financeiro](../Financeiro_MIGRATION_DASHBOARD.html) — Visão executiva
- [Dashboard Premium](../DATA_AI_OPERATIONS_PREMIUM_DASHBOARD.html) — Operações de dados e IA
- [Dashboard Factory](../EXECUTIVE_DATA_FACTORY_DASHBOARD.html) — Fábrica de dados
- [Dashboard Telemetria](../TELEMETRY_DEMO_DASHBOARD.html) — Métricas de observabilidade

---

## 📋 Índice Completo

### Seção 1: Arquitetura & Design
| Documento | Descrição | Público |
|-----------|-----------|---------|
| [Visão Geral Técnica](TECHNICAL_DOCUMENTATION.md) | Componentes, fluxos, stack Microsoft | Arquitetos, Devs |
| [Arquitetura de Dashboards](DASHBOARD_ARCHITECTURE.md) | Design, componentes reutilizáveis, tokens | UX/Devs |
| [Blueprint](BLUEPRINT_GUIDE.md) | 3 padrões de conexão, segurança, IP | Arquitetos, Engenheiros |

### Seção 2: Integração & APIs
| Documento | Descrição | Público |
|-----------|-----------|---------|
| [Guia de Integração](INTEGRATION_GUIDE.md) | Padrões A/B/C, setup, credenciais | Devs, Engenheiros |
| [Referência de APIs](API_REFERENCE.md) | Endpoints, payloads, exemplos cURL | Devs |
| [Best Practices](BEST_PRACTICES.md) | Segurança, performance, observabilidade | Devs, Ops |

### Seção 3: Operação & Suporte
| Documento | Descrição | Público |
|-----------|-----------|---------|
| [Troubleshooting](TROUBLESHOOTING.md) | Diagnóstico, logs, escalação | Ops, Suporte |
| [Calculadora](../EFFORT_CALCULATOR.html) | Estimativa de esforço | PMs, Executivos |
| [Proposta](../COMMERCIAL_PROPOSAL_ONE_PAGE.html) | ROI, timeline, valor | Executivos |

---

## 🏗️ Stack Técnico (100% Microsoft)

**Compute & Orchestration:**
- Azure AI Foundry — Platform para agentes
- Semantic Kernel — Framework de orquestração
- Azure Container Apps — VNet-injected, stateless

**Data & Storage:**
- ADLS Gen2 — Landing zone para dados brutos
- Azure Service Bus — Job orchestration
- Azure Key Vault — Credential management

**Security & Identity:**
- Entra ID — Autenticação e service principals
- Managed Identity — Acesso sem senha
- Private Link — Conectividade air-gapped

**Observability:**
- Azure Monitor — Métricas e logs
- Application Insights — Telemetria de aplicação
- KQL — Consultas de diagnóstico

---

## 🔐 Padrões de Conexão (Quick Reference)

| Padrão | Modelo | Setup | Segurança | Custo |
|--------|--------|-------|-----------|-------|
| **A — Push** | SaaS default | 2h | Máxima (IP protegida) | Base |
| **B — Pull** | Compliance | 8h | Alta (credenciais efêmeras) | +20-30% |
| **C — Private Link** | Enterprise | 2-5d | Crítica (VNet privada) | +40-60% |

👉 [Detalhes completos →](BLUEPRINT_GUIDE.md)

---

## 📊 KPIs Principais

**Redução de Esforço:**
- ✅ 77% redução (Complexidade Baixa)
- ✅ 52% redução (Complexidade Média)
- ✅ 32% redução (Complexidade Alta)

**Timeline:**
- Semana 1-2: Setup & onboarding
- Semana 3-4: Configuração de agentes
- Semana 5-6: UAT
- Semana 7-8: Go-live

**ROI:**
- Payback < 6 meses
- Economia ~120h por pipeline
- Setup rápido: 2-8 horas

---

## 🚀 Quick Start

### Para Desenvolvedores
1. Leia [Visão Geral Técnica](TECHNICAL_DOCUMENTATION.md)
2. Escolha padrão: [Blueprint](BLUEPRINT_GUIDE.md)
3. Implemente: [Guia de Integração](INTEGRATION_GUIDE.md)
4. Valide: [APIs](API_REFERENCE.md)
5. Deploy: [Best Practices](BEST_PRACTICES.md)

### Para Arquitetos
1. Revise [Arquitetura de Dashboards](DASHBOARD_ARCHITECTURE.md)
2. Avalie [Padrões de Conexão](BLUEPRINT_GUIDE.md)
3. Verifique [Stack Técnico](TECHNICAL_DOCUMENTATION.md#stack-técnico)

### Para Executivos
1. Consulte [Proposta Comercial](../COMMERCIAL_PROPOSAL_ONE_PAGE.html)
2. Use [Calculadora de Esforço](../EFFORT_CALCULATOR.html)
3. Monitore [Dashboards](../INDEX.html)

---

## 📞 Suporte & Contato

| Função | Contato | Escalação |
|--------|---------|-----------|
| **Dev Support** | dev-team@avanade.com | Arquitetura |
| **Operations** | ops-team@avanade.com | Execução |
| **Emergências** | on-call@avanade.com | CTO |

---

## 📝 Changelog

| Versão | Data | Mudanças |
|--------|------|----------|
| 1.0.0 | 2026-06-12 | 🎉 Lançamento inicial — Documentação completa |
| 1.0.1 | — | Em breve: Dashboard dark mode, PDF export |

---

## 🔗 Links Rápidos

| Recurso | Link |
|---------|------|
| Proposta | [COMMERCIAL_PROPOSAL_ONE_PAGE.html](../COMMERCIAL_PROPOSAL_ONE_PAGE.html) |
| Calculadora | [EFFORT_CALCULATOR.html](../EFFORT_CALCULATOR.html) |
| Portal | [INDEX.html](../INDEX.html) |
| Dashboard Consolidado | [00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html](../00_CONSOLIDATED_MIGRATION_REPORT_tabbed.html) |

---

**Última atualização:** 2026-06-12 | **Mantido por:** Avanade Global AI Hub | **Status:** ✅ Atualizado
