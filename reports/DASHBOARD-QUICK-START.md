# 🎯 Quick Reference — Dashboard Consolidation

## O Que Foi Feito

Criada estratégia 2-layer para dashboards:

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: Dashboard Executivo Unificado (novo)              │
│  ├─ KPIs globais de todos os projetos                       │
│  ├─ Visão consolidada de status                             │
│  └─ Tomada de decisão C-level                               │
└─────────────────────────────────────────────────────────────┘
                           ↑
                    Extração automática
                           ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: Dashboards de Projeto (mantidos separados)        │
│  ├─ Bradesco (4 dashboards)                                 │
│  │  └─ Detalhes técnicos, testing, ROI                      │
│  └─ Einstein-HIAE (a criar)                                 │
│     └─ Discovery, design, healthcare-specific               │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Arquivos Criados

```
reports/
├── _templates/
│   ├── DASHBOARD-EXECUTIVE-UNIFIED.html          ✅ NOVO
│   ├── consolidate_dashboards.py                 ✅ NOVO (automação)
│   └── README-GOLDEN-STANDARD.md                 (referência)
├── DASHBOARD-CONSOLIDATION-STRATEGY.md           ✅ NOVO (docs)
│
└── bradesco/
    ├── bradesco-executive-dashboard.html         (fonte de KPIs)
    ├── bradesco-3tier-dashboard.html             (fase técnica)
    ├── bradesco-autonomous-test-report.html      (testes)
    └── ROI_ANALYSIS_VISUAL.html                  (financeiro)
```

---

## 🚀 Como Usar

### 1️⃣ **Visualizar Dashboard Executivo (agora)**

```bash
# Abrir no navegador
open reports/_templates/DASHBOARD-EXECUTIVE-UNIFIED.html
```

**O que você vê**:
- ✅ 6 KPIs globais (Projetos, Completude, Agentes, Qualidade, Artefatos, Gates)
- ✅ 2 Cards de projeto (Bradesco + Einstein-HIAE)
- ✅ Tabela consolidada de métricas
- ✅ Status dos 3 Gates de qualidade

---

### 2️⃣ **Atualizar Dashboard com KPIs Novos (automação)**

```bash
# Executar script de consolidação (SEM modificar)
python reports/_templates/consolidate_dashboards.py --dry-run

# Executar script de consolidação (COM atualização)
python reports/_templates/consolidate_dashboards.py

# Filtrar projeto específico
python reports/_templates/consolidate_dashboards.py --projects=bradesco
```

**O que faz**:
1. Extrai KPIs do dashboard de Bradesco (completude, qualidade, etc)
2. Calcula métricas globais (médias)
3. Atualiza cards de projeto no Executivo
4. Gera relatório JSON com timestamp

**Output esperado**:
```
======================================================================
📊 CONSOLIDATE DASHBOARDS — KPI Extraction & Aggregation
======================================================================

🔍 Extraindo KPIs de 2 projeto(s)...

   📁 🏦 Bradesco
      ✓ Completude: 98.7%
      ✓ Qualidade: 0.92/1.00
      ✓ Status: ✓ Completo

📊 Calculando métricas globais...
   ✓ Projetos Ativos: 1
   ✓ Completude Média: 98.7%
   ✓ Qualidade Média: 0.92

✅ Dashboard Executivo Atualizado
```

---

### 3️⃣ **Manter Dashboards de Projeto Separados**

**Bradesco** (4 dashboards — não consolidam):
```
reports/bradesco/bradesco-executive-dashboard.html
reports/bradesco/bradesco-3tier-dashboard.html
reports/bradesco/bradesco-autonomous-test-report.html
reports/bradesco/ROI_ANALYSIS_VISUAL.html
```

**Cada um tem**:
- Detalhes técnicos da fase específica
- KPIs expandidos (não apenas sumários)
- Gráficos e tabelas profundas

---

### 4️⃣ **Criar Dashboard para Novo Projeto (Einstein)**

```bash
# 1. Copiar template base
cp reports/_templates/DASHBOARD-EXECUTIVE-UNIFIED.html \
   reports/einstein/einstein-executive-dashboard.html

# 2. Editar título, descrição, KPIs
# 3. Executar consolidação
python reports/_templates/consolidate_dashboards.py --projects=einstein
```

---

## 📊 Fluxo de Consolidação Diário

```
┌───────────────────────────────────────────────────────────────┐
│ Data Teams: Atualizam dashboards de projeto (EOD)            │
│ ├─ Bradesco: completude, qualidade, artifacts               │
│ └─ Einstein: discovery%, schema%, validation%               │
└───────────────┬─────────────────────────────────────────────┘
                │
                ↓ Python Script (automático ou manual)
┌───────────────────────────────────────────────────────────────┐
│ consolidate_dashboards.py                                     │
│ ├─ Extrai KPIs de cada projeto                              │
│ ├─ Calcula agregações globais                               │
│ └─ Atualiza Dashboard Executivo                             │
└───────────────┬─────────────────────────────────────────────┘
                │
                ↓ PMO/CTO: Revisa visão unificada
┌───────────────────────────────────────────────────────────────┐
│ Dashboard Executivo                                           │
│ ├─ KPIs globais atualizados                                 │
│ ├─ Status de cada projeto                                  │
│ └─ Decisões estratégicas baseadas em dados                │
└───────────────────────────────────────────────────────────────┘
```

---

## 🔧 Técnico: Como O Script Funciona

### Extração de KPIs

```python
# Procura valores em tabelas (Bradesco format):
regex: <td><strong>Quality Score</strong></td>
       <td>0.92/1.00</td>

# Ou em KPI cards:
regex: <div class="kpi-value">98.7%</div>
       <div class="kpi-label">Completeness</div>
```

### Agregação

```python
avg_completeness = (98.7 + 68) / 2 = 83.35%
avg_quality = (0.92 + 0.85) / 2 = 0.885
```

### Atualização

```python
# Injeta HTML dos cards no Executivo
old_html: <!-- Project: bradesco -->...
new_html: <div class="project-card">...(com KPIs novos)
```

---

## 📈 KPIs Extraídos por Projeto

### Bradesco (Status Atual)

| KPI | Valor | Fonte |
|-----|-------|-------|
| Completude | 98.7% | bradesco-executive-dashboard.html |
| Qualidade | 0.92/1.00 | bradesco-3tier-dashboard.html |
| Entidades | 146 | (ou N/A se não encontrado) |
| Artefatos | 21+ | Dashboard principal |
| Status | ✓ Completo | HTML badge |

### Einstein-HIAE (Status Futuro)

| KPI | Valor | Fonte |
|-----|-------|-------|
| Completude | 68% | einstein-discovery-dashboard.html |
| Qualidade | 0.85/1.00 | (TBD) |
| Bases Mapeadas | 7/7 | wave-config.yaml |
| Tabelas Catalogadas | 2,641 | (TBD) |
| Status | ⏱ Discovery | (TBD) |

---

## ⚠️ Troubleshooting

| Problema | Solução |
|----------|---------|
| Script não encontra arquivo | ✓ Verificar caminho em PROJECTS_CONFIG |
| KPIs extraem "N/A" | ✓ Revisar regex patterns para novo HTML format |
| Arquivo já existe (erro) | ✓ Executar com `--dry-run` primeiro |
| Qual projeto está faltando? | ✓ `python consolidate_dashboards.py` mostra status |

---

## 📌 Próximas Ações

- [ ] Executar script para atualizar Executivo com Bradesco (agora)
- [ ] Integrar com CI/CD pipeline (CI: trigger daily)
- [ ] Criar dashboard Einstein-HIAE (próx. semana)
- [ ] Adicionar trending histórico (próx. 2 sem)
- [ ] Alertas automáticos se quality < threshold (próx. mês)

---

## 📞 Referências Completas

- **Dashboard Principal**: `DASHBOARD-EXECUTIVE-UNIFIED.html`
- **Documentação Estratégia**: `DASHBOARD-CONSOLIDATION-STRATEGY.md`
- **Design System**: `README-GOLDEN-STANDARD.md`
- **Script Automação**: `consolidate_dashboards.py`

---

**Avanade DMF** — Data Migration Factory v3  
**Last Updated**: 09 de Junho, 2026
