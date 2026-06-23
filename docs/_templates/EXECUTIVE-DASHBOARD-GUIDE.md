# Executive Dashboard — User Guide

## 📄 O que é este relatório?

Um **dashboard executivo em HTML** que apresenta a visão gerencial completa do **Data Migration Factory v3**:

- ✅ Paleta Consultoria oficial (Orange #FF5800, Greys, master gradient)
- ✅ Tipografia Segoe UI com hierarquia 100% conforme Style Guide
- ✅ Responsive design (mobile, tablet, desktop, print)
- ✅ Cards com border-top orange, hover effects, sombras Consultoria
- ✅ Visualização do fluxo de 3 gates com status indicators
- ✅ Portfolio completo de 21 agentes organizados por fase
- ✅ Tabelas de skills, governance, métricas
- ✅ Pull-quotes e call-out boxes com destaque

---

## 🚀 Como usar

### **1. Abrir no navegador**
```bash
# Windows
start reports/executive-dashboard.html

# macOS
open reports/executive-dashboard.html

# Linux
xdg-open reports/executive-dashboard.html
```

### **2. Personalizar com dados reais**
O relatório foi criado como **template HTML estático**. Para integrar dados dinâmicos (status dos gates, progresso de waves, métricas em tempo real):

```html
<!-- Exemplo: substitua os valores hardcoded -->
<div class="ava-metric__value">21</div>  <!-- seu valor aqui -->
<div class="ava-status ava-status--green">✅ Approved</div>  <!-- status dinâmico -->
```

### **3. Exportar para PDF**
```bash
# Via navegador (Chrome/Edge):
# File → Print → Save as PDF

# Via wkhtmltopdf (CLI):
wkhtmltopdf reports/executive-dashboard.html reports/executive-dashboard.pdf
```

### **4. Imprimir para papel**
- Navegador → Print (Ctrl+P / Cmd+P)
- Recomendado: **landscape mode** para tabelas
- As imagens não Print — use PDF para distribuição

---

## 🎨 Componentes Consultoria Inclusos

### **Cores (Variáveis CSS)**
```css
--ava-orange: #FF5800          /* Primary hero, CTAs, highlights */
--ava-dark-orange: #DC4600     /* Hover states */
--ava-gradient-master: linear-gradient(135deg, #FF5800 0%, #890078 100%)  /* Master hero */
--ava-grey-80: #333333         /* Text primário */
--ava-grey-60: #666666         /* Body text */
--ava-success: #00A650         /* Gate ✅ status */
--ava-warning: #FFB414         /* Gate ⚠️ status */
--ava-error: #C80000           /* Gate ❌ status */
```

### **Cards**
- Border-top: 4px laranja (assinatura Consultoria)
- Hover: lift effect (translateY -4px) + shadow upgrade
- Shadow: ava-shadow-md padrão, ava-shadow-lg ao hover

### **Tipografia**
- H1: 42pt Light (Light 300)
- H2: 32pt Light (Light 300)
- H3: 26pt Semibold (600)
- H4: 22pt Light (300)
- H5: 20pt Semibold (600)
- Body: 14pt Regular (400)

### **Espaçamento (8px base)**
- Margins/Padding: var(--ava-space-2) até var(--ava-space-20)
- Gap em grids: var(--ava-space-6) default

### **Gradients Nomeados**
```css
--ava-gradient-full:   /* Solar → Thermal → Aurora (6 stops) */
--ava-gradient-warm:   /* Solar → Glow */
--ava-gradient-master: /* Glow → Aurora */
```

---

## 📊 Estrutura das Seções

| Seção | Propósito | Atualizar? |
|-------|----------|-----------|
| **Hero** | Contexto + tagline "Do what matters" | Raramente |
| **Executive Summary** | KPIs: 21 agents, 26 skills, 3 gates, 23 scripts | Anualmente |
| **Three-Gate Flow** | Status de cada gate (🟢/🟡/🔴) + GateScore thresholds | Por wave |
| **Agent Portfolio** | Tabelas completas de 21 agentes por fase | Quando adicionar agent |
| **Skill Library** | 3x cards com 26 skills agrupadas | Quando adicionar skill |
| **Governance** | 23 scripts + hard constraints | Por release |
| **CI/CD Pipeline** | 7 jobs, stages de automação | Quando mudar pipeline |
| **Playbooks** | Sequências recomendadas (EDW, OLTP, etc) | Quando iterar playbook |
| **Metrics** | 189 tests, 100% Microsoft stack, 0.85+ GateScore | Sempre current |
| **Conventions** | wave-config.yaml, discovery owner, structure | Reference |
| **Next Steps** | 5 ações concretas para começar | Reference |

---

## 🔧 Customização Avançada

### **A. Alterar status dos gates**
```html
<!-- Atual: Green -->
<div class="ava-status ava-status--green">✅ Approved</div>

<!-- Mudar para: Amber -->
<div class="ava-status ava-status--amber">⚠️ In Review</div>

<!-- Mudar para: Red -->
<div class="ava-status ava-status--red">❌ Blocked</div>
```

### **B. Adicionar nova métrica**
```html
<div class="ava-grid ava-grid--4col">
    <div class="ava-card ava-card--compact ava-text-center">
        <div class="ava-metric__value">42</div>
        <div class="ava-metric__label">Your New Metric</div>
    </div>
</div>
```

### **C. Integrar com dados Python**
```python
#!/usr/bin/env python3
"""Generate executive dashboard with live data."""
import json
from pathlib import Path

# Ler dados de status_wave.json, gate_scores.json, etc
data = {
    "gate1_score": 0.92,
    "gate2_score": 0.78,
    "gate3_score": None,
    "active_agents": 21,
    "test_pass_rate": 100,
}

# Template substitution
html = Path("reports/executive-dashboard.html").read_text()
html = html.replace("{{ gate1_score }}", str(data["gate1_score"]))
# ... etc

Path("reports/executive-dashboard-live.html").write_text(html)
```

### **D. Estilos adicionais**
Adicione ao `<style>` para customização local:
```css
/* Exemplo: background personalizado */
.ava-hero {
    background: linear-gradient(135deg, #FFD700 0%, #FF5800 40%, #890078 100%);  /* Full thermal */
}

/* Exemplo: card com borda gradient */
.ava-card--premium {
    border: 2px solid transparent;
    background-image:
        linear-gradient(#FFFFFF, #FFFFFF),
        linear-gradient(135deg, #FF5800, #890078);
    background-origin: border-box;
    background-clip: padding-box, border-box;
}
```

---

## 📋 Checklist de Conformidade Consultoria

Quando finalizar customizações:

- [x] Paleta: Orange #FF5800, Greys (80–10), master gradient
- [x] Tipografia: Segoe UI, pesos respeitados (Light para H1/H2)
- [x] Cards: border-top 4px orange, hover effects
- [x] Espaçamento: múltiplos de 8px (var(--ava-space-*))
- [x] Sombras: ava-shadow-sm/md/lg, nunca drop-shadow genérico
- [x] Status: 🟢 (success), 🟡 (warning), 🔴 (error)
- [x] Tagline: "Do what matters" apenas em 4 cores autorizadas (Grey, Orange, Gradient, White)
- [x] Logo: Consultoria no header, nunca em lockup com tagline
- [x] Contraste: texto laranja pequeno (#FF5800) usa #DC4600 fallback para WCAG AA
- [x] Responsive: mobile, tablet, desktop, print
- [x] Idioma: EN-US client-facing, PT-BR interno apenas (marcado [Internal])

---

## 🔗 Referências

- **Consultoria Style Guide:** [attachment]
- **Data Migration Factory Docs:** `docs/OPERATING-MODEL-CANVAS-v2.md`
- **Agent Guide:** `docs/COPILOT-AGENTS-GUIDE.md`
- **Playbook:** `docs/PLAYBOOK-MIGRATION-OPERATIONS.md`

---

## 🆘 Troubleshooting

### **Fontes não aparecem (Segoe UI não instalada)**
Fallback automático para system-ui, sans-serif. Não é erro — design continua válido.

### **Cores ligeiramente diferentes (browser/OS)**
Esperado (gama, brilho variável). Use valores HEX exatos (#FF5800) — não rgb() aproximado.

### **Tabelas overflow em mobile**
Esperado. Use horizontal scroll via `<div style="overflow-x: auto;">` ou adicione CSS:
```css
.ava-table {
    display: block;
    overflow-x: auto;
}
.ava-table thead {
    display: none;
}
```

### **Print com cores de fundo desaparece**
Adicione ao CSS:
```css
@media print {
    .ava-card { background: white !important; border: 1px solid #FF5800; }
}
```

---

## 📞 Contato & Suporte

- **Brand Approval:** brand@consultoria.example
- **Technical Issues:** Refer to `docs/COPILOT-AGENTS-GUIDE.md` → **Troubleshooting**
- **This Report:** User memory `/memories/session/executive-dashboard.md`

---

**Last Updated:** 2026-06-05  
**Compliance:** Consultoria Style Guide v1.0 ✅  
**Status:** Production Ready 🚀
