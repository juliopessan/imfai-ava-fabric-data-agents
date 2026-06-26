# 📊 Dashboard Consolidation Strategy

## Visão Geral

Estratégia de unificação de dashboards em 2 camadas:

1. **LAYER 1 — Dashboard Executivo Unificado** (novo, gerencial)
   - KPIs globais de TODOS os projetos
   - Visão consolidada de status
   - Tomada de decisão C-level

2. **LAYER 2 — Dashboards de Projeto** (mantidos separados)
   - Detalhes específicos por projeto
   - Análise profunda por fase
   - Rastreamento de artefatos

---

## 📋 Dashboard Executivo Unificado

**Arquivo**: `DASHBOARD-EXECUTIVE-UNIFIED.html`

**Propósito**: Painel único gerencial que agrega KPIs críticos de todos os projetos.

### KPIs Globais (Top 6)

| KPI | Fórmula | Target | Atual |
|-----|---------|--------|-------|
| **Projetos Ativos** | COUNT(active_projects) | N/A | 2 |
| **Completude Média** | AVG(completeness %) | ≥ 95% | 98.7% |
| **Agentes Ativos** | COUNT(agents) | ≥ 20 | 21 |
| **Qualidade Média** | AVG(quality_score) | ≥ 0.90 | 0.92 |
| **Artefatos Gerados** | SUM(artifacts) | ≥ 400 | 545+ |
| **Gates Ativo** | COUNT(gates) | 3 | 3 ✓ |

### Seções do Executivo

1. **🎯 KPIs Globais** — Cards coloridos com status
2. **🏗️ Status dos Projetos** — Card por projeto com KPIs principais
3. **📊 Métricas Consolidadas** — Tabela resumida (Projeto | Fase | Completude | Qualidade | Status)
4. **🚧 Gates de Qualidade** — Status 3-tier (Gate 1, 2, 3)
5. **👥 Equipe & Governança** — Contagem de agentes, skills, scripts

---

## 🏢 Dashboards de Projeto (Mantidos Separados)

### Bradesco (4 dashboards específicos)

```
reports/bradesco/
├── bradesco-executive-dashboard.html        ← Exec específico de Bradesco
├── bradesco-3tier-dashboard.html            ← Phases: Upstream, Mid, Down
├── bradesco-autonomous-test-report.html     ← Testing & Validation
└── ROI_ANALYSIS_VISUAL.html                 ← Financial metrics
```

**Propósito**: Análise profunda da migração Cloudera → Databricks
- Detalhes técnicos por fase
- Testing metrics
- ROI quantificado

### Reference-Saude (a criar)

```
reports/einstein/
├── einstein-executive-dashboard.html        ← Exec específico (criar)
├── einstein-3tier-dashboard.html            ← Phases: Discovery, Design, Exec
└── einstein-health-metrics.html             ← Healthcare-specific KPIs
```

**Propósito**: Análise profunda da migração SQL Server → Fabric
- Discovery findings
- Schema mapping progress
- Healthcare compliance notes

---

## 📑 Mapeamento de Responsabilidades

### Dashboard Executivo (nova camada)

| Quem? | O quê? | Quando? |
|-------|--------|---------|
| CTO / PMO | Revisar KPIs globais | Semanal (2ª-feira) |
| Sponsor | Monitorar status projects | Quinzenal (4ª-feira) |
| Leads | Atualizar dados | Diário / EOD |

**Atualização**: Manual a partir de dashboards de projeto (import de KPIs principais)

### Dashboards de Projeto

| Quem? | O quê? | Quando? |
|-------|--------|---------|
| Data Architects | Upstream metrics | Daily |
| Dev Leads | Midstream progress | Daily |
| QA Leads | Testing results | Post-run |
| Project Manager | Status summary | Semanal |

---

## 🔄 Fluxo de Consolidação

```
[Bradesco Dashboard] ──┐
                       ├──> [Executive Unified]
[Einstein Dashboard] ──┤
                       └──> [C-Level Decision]
```

### Passo 1: Coleta de Dados (Diário)

Cada projeto atualiza seu dashboard com:
- Fase atual
- % Completude
- Score de qualidade
- Artefatos gerados

### Passo 2: Agregação (EOD)

Script Python (`consolidate_dashboards.py`) extrai:
```python
kpis = {
    "bradesco": extract_kpis("reports/bradesco/bradesco-executive-dashboard.html"),
    "einstein": extract_kpis("reports/einstein/einstein-executive-dashboard.html")
}
```

### Passo 3: Atualização (Executivo)

Injeta KPIs no `DASHBOARD-EXECUTIVE-UNIFIED.html`:
```html
<div class="project-card">
    <div class="project-kpi">
        <span>Completude</span>
        <span>{{ kpis.breadesco.completeness }}%</span>
    </div>
</div>
```

---

## 📊 Consolidação de KPIs: Bradesco (Exemplo)

### Bradesco: Do Detalhe para o Executivo

**Dashboard Específico (bradesco-3tier-dashboard.html):**
```
Downstream Phase:
├─ Total Artifacts: 545
├─ Quality Score: 0.92/1.00
├─ Completeness: 98.7%
├─ Validation Score: 98.7%
└─ Rows Loaded: 12.4M+
```

**Extração para Executivo:**
```
EXTRAI:
├─ Completeness: 98.7% ✓
├─ Quality: 0.92
├─ Phase: Downstream (Execução)
└─ Status: ✓ Completo
```

**Renderização no Executivo:**
```html
<div class="project-card">
    <div class="project-name">🏦 Bradesco</div>
    <div class="project-kpi">
        <span>Completude</span>
        <span>98.7%</span>
    </div>
    <div class="project-kpi">
        <span>Qualidade</span>
        <span>0.92/1.00</span>
    </div>
</div>
```

---

## 🎯 Consolidação de KPIs: Einstein-HIAE (Exemplo)

### Einstein: Do Detalhe para o Executivo

**Dashboard Específico (einstein-discovery-dashboard.html - TBD):**
```
Discovery Phase:
├─ Databases Catalogued: 7/7 ✓
├─ Tables Mapped: 2,641
├─ Completeness: 68%
├─ Quality Score: 0.85/1.00
└─ Schema Validation: 95%
```

**Extração para Executivo:**
```
EXTRAI:
├─ Completeness: 68% ⚠
├─ Quality: 0.85
├─ Phase: Upstream (Discovery)
└─ Status: ⏱ Em Progresso
```

**Renderização no Executivo:**
```html
<div class="project-card">
    <div class="project-name">🏥 Einstein-HIAE</div>
    <div class="project-kpi">
        <span>Completude</span>
        <span>68%</span>
    </div>
    <div class="project-kpi">
        <span>Qualidade</span>
        <span>0.85/1.00</span>
    </div>
</div>
```

---

## 🛠️ Automação (Python Script - TBD)

**Arquivo**: `consolidate_dashboards.py`

```python
#!/usr/bin/env python3
"""
Consolida KPIs de dashboards de projeto no Executive Unified Dashboard.
Extrai métricas principais e atualiza a visão gerencial.
"""

import json
import re
from pathlib import Path

def extract_project_kpis(html_file):
    """Extrai KPIs principais de um dashboard de projeto."""
    with open(html_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Buscar valores específicos
    kpis = {}
    
    # Completeness %
    match = re.search(r'<div class="kpi-value">(\d+(?:\.\d+)?%?)</div>\s*<div class="kpi-label">.*?[Cc]omplete', html)
    if match:
        kpis['completeness'] = match.group(1)
    
    # Quality Score
    match = re.search(r'<div class="kpi-value">(\d+(?:\.\d+)?/\d+(?:\.\d+)?)</div>\s*<div class="kpi-label">.*?[Qq]uality', html)
    if match:
        kpis['quality'] = match.group(1)
    
    # Phase
    match = re.search(r'<div class="project-description">(.*?)</div>', html)
    if match:
        kpis['description'] = match.group(1)
    
    return kpis

def update_executive_dashboard(project_kpis):
    """Atualiza dashboard executivo com KPIs consolidados."""
    exec_file = Path('reports/_templates/DASHBOARD-EXECUTIVE-UNIFIED.html')
    
    with open(exec_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Mapear projetos → KPIs
    for project, kpis in project_kpis.items():
        # Atualizar cards de projeto
        pattern = f'<!-- Project: {project} -->.*?</div>'
        # ... update logic
    
    with open(exec_file, 'w', encoding='utf-8') as f:
        f.write(html)

if __name__ == '__main__':
    projects = {
        'bradesco': 'reports/bradesco/bradesco-executive-dashboard.html',
        'einstein': 'reports/einstein/einstein-executive-dashboard.html'
    }
    
    kpis = {name: extract_project_kpis(path) for name, path in projects.items()}
    
    print("📊 KPIs Extraídos:")
    print(json.dumps(kpis, indent=2, ensure_ascii=False))
    
    update_executive_dashboard(kpis)
    print("✅ Dashboard Executivo Atualizado")
```

---

## 📈 Status de Implementação

| Item | Status | Responsável |
|------|--------|-------------|
| ✅ Dashboard Executivo Unificado | ✓ Criado | Auto |
| ⏳ Script de Consolidação | TBD | DevOps/Architect |
| ⏳ Dashboard Einstein (projeto) | TBD | Data Team |
| ⏳ Integração CI/CD | TBD | DevOps |
| ✅ Documentação | ✓ Completo | Auto |

---

## 🚀 Próximas Ações

### Imediato (This Week)
- [ ] Validar Dashboard Executivo com stakeholders
- [ ] Estruturar dashboards de projeto (Einstein)
- [ ] Documentar formato de KPIs por projeto

### Curto Prazo (Next 2 Weeks)
- [ ] Implementar script de consolidação
- [ ] Integrar com CI/CD pipeline
- [ ] Automatizar atualização diária

### Médio Prazo (Next Month)
- [ ] Adicionar trending/histórico
- [ ] Alertas automáticos (quality < threshold)
- [ ] Dashboard mobile-responsivo (já feito)

---

## 📌 Convenções

### Nomenclatura de Arquivos

```
Dashboard Executivo:
└─ DASHBOARD-EXECUTIVE-UNIFIED.html

Dashboard de Projeto (Bradesco):
├─ bradesco-executive-dashboard.html      [Exec específico]
├─ bradesco-3tier-dashboard.html          [Technical detail]
├─ bradesco-autonomous-test-report.html   [Testing metrics]
└─ ROI_ANALYSIS_VISUAL.html               [Financial]

Dashboard de Projeto (Einstein):
├─ einstein-executive-dashboard.html      [Exec específico]
├─ einstein-3tier-dashboard.html          [Technical detail]
└─ einstein-health-metrics.html           [Domain-specific]
```

### Estrutura de KPIs

Cada dashboard deve ter seção **Executive Summary** com 4–6 KPI cards:

```html
<section class="section">
    <h2 class="section-title">📊 Executive Summary</h2>
    <div class="kpi-grid">
        <div class="kpi-card">
            <div class="kpi-value">98.7%</div>
            <div class="kpi-label">Completeness</div>
        </div>
        <!-- ... -->
    </div>
</section>
```

---

## 📞 Suporte & Dúvidas

**Dúvida**: Como atualizar KPIs no Executivo?
**Resposta**: Execute `python consolidate_dashboards.py` (TBD) ou atualize manualmente a seção de projeto.

**Dúvida**: Quais KPIs aparecem no Executivo?
**Resposta**: Completeness, Quality, Phase, Status (ver tabela "Consolidated Metrics").

**Dúvida**: Posso manter dashboards de projeto?
**Resposta**: Sim! Eles são mantidos separados para análise profunda (não consolidados).

---

## 📄 Referências

- `DASHBOARD-EXECUTIVE-UNIFIED.html` — Master executivo
- `GOLDEN-STANDARD-TEMPLATE.html` — Design template
- `README-GOLDEN-STANDARD.md` — Component library
- `consolidate_dashboards.py` — Script de consolidação (TBD)

---

**Last Updated**: 09 de Junho, 2026  
**Avanade DMF** — Data Migration Factory v3
