# 🎨 Quick Reference — Padrão Ouro Avanade

**Uso Rápido | Componentes | Cores | Troubleshooting**

---

## 📋 Copy-Paste: Dashboard Minimal

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Seu Dashboard | Avanade</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
    <style>
        /* Copiar CSS completo de GOLDEN-STANDARD-TEMPLATE.html */
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>📊 Seu Título</h1>
            <p class="subtitle">Descrição aqui</p>
        </div>
    </div>

    <div class="main">
        <!-- KPIs -->
        <div class="section-title">
            <div class="section-icon">📈</div> Indicadores
        </div>
        <div class="kpi-grid">
            <div class="kpi-card c-orange">
                <div class="kpi-value">42</div>
                <div class="kpi-label">Métrica</div>
            </div>
        </div>

        <!-- Conteúdo -->
    </div>

    <div class="footer">
        <strong class="brand-color">DMF</strong> — Avanade
    </div>

    <script>
        mermaid.initialize({startOnLoad: true, theme: 'base'});
        function togglePhase(el) { el.parentElement.classList.toggle('collapsed'); }
    </script>
</body>
</html>
```

---

## 🎨 Cores Rápidas

### Usar em Classes
```html
<div class="kpi-card c-orange">...</div>      <!-- #FF5800 -->
<div class="kpi-card c-magenta">...</div>     <!-- #CE0569 -->
<div class="kpi-card c-red">...</div>         <!-- #C80000 -->
<div class="kpi-card c-gold">...</div>        <!-- #FFB314 -->
<div class="kpi-card c-purple">...</div>      <!-- #890078 -->
<div class="kpi-card c-green">...</div>       <!-- #47800A -->
<div class="kpi-card c-blue">...</div>        <!-- #0057B8 -->
<div class="kpi-card c-dark">...</div>        <!-- #2D2D2D -->
<div class="kpi-card c-teal">...</div>        <!-- #05A870 -->
```

### Usar em Inline Styles
```html
<div style="background: var(--ava-orange);">...</div>
<div style="color: var(--ava-purple);">...</div>
<div style="border-left-color: var(--ava-gold);">...</div>
```

---

## 🧩 Componentes Prontos

### KPI Card
```html
<div class="kpi-card c-orange">
    <div class="kpi-value">123</div>
    <div class="kpi-label">Label</div>
    <div class="kpi-sub">Descrição</div>
</div>
```

### Phase Block (Colapsável)
```html
<div class="phase-block">
    <div class="phase-block-header" style="background: linear-gradient(135deg, var(--ava-purple), var(--ava-magenta));" onclick="togglePhase(this)">
        <div class="phase-badge-lg">🔷</div>
        <div class="phase-title-area">
            <h3>Título</h3>
            <p>Descrição</p>
        </div>
        <div class="chevron">▼</div>
    </div>
    <div class="phase-content">
        Conteúdo aqui...
    </div>
</div>
```

### Tabela
```html
<table>
    <thead>
        <tr><th>Col 1</th><th>Col 2</th></tr>
    </thead>
    <tbody>
        <tr><td>Data</td><td>Data</td></tr>
    </tbody>
</table>
```

### Mermaid Diagram
```html
<div class="mermaid-section">
    <pre class="mermaid">
graph LR
    A[Start] --> B[Process] --> C[End]
    </pre>
</div>
```

---

## 🎯 Gradients Personalizados

### Header
```css
background: linear-gradient(135deg, #1a0a00 0%, #3d1700 30%, var(--ava-orange) 100%);
```

### Purple Accent
```css
background: linear-gradient(135deg, var(--ava-purple), var(--ava-magenta));
```

### Table Header
```css
background: linear-gradient(135deg, var(--ava-purple), var(--ava-magenta));
```

### Custom
```css
background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
```

---

## 📱 Responsive Grid

### Desktop (4+ cols)
```html
<div class="kpi-grid">
    <!-- Auto 4+ colunas em telas grandes -->
</div>
```

### Mobile (1-2 cols)
```css
/* Automático! Media query em <768px reduz para 2-3 cols */
```

---

## 🌙 Dark Mode

**Automático** via `prefers-color-scheme: dark`

```css
@media (prefers-color-scheme: dark) {
    body { background: #1a1f37; }
    .content { color: #e0e0e0; }
}
```

Para testar:
1. Chrome DevTools → `Cmd/Ctrl + Shift + P`
2. "Render with dark media feature" ✓

---

## 🔧 Troubleshooting Rápido

| Problema | Solução |
|----------|---------|
| Cores erradas | Verificar `<head><style>` — copiar `:root` completo |
| Mobile não responsivo | Adicionar `<meta viewport>` |
| Mermaid quebrado | Verificar sintaxe diagram + `<script>` com `mermaid.initialize()` |
| Header background cortado | Aumentar padding ou revisar `overflow: hidden` |
| KPI cards não em grid | CSS Grid pode não estar ativo — inspecionar `.kpi-grid` |
| Dark mode não funciona | Testar em browser que suporta `prefers-color-scheme` |

---

## 📍 Arquivos para Referência

| Necessário | Arquivo |
|-----------|---------|
| **Template Completo** | `GOLDEN-STANDARD-TEMPLATE.html` |
| **Exemplos de Componentes** | `README-GOLDEN-STANDARD.md` |
| **Lista de Cores** | `:root` em qualquer `.html` padrão |
| **Automação de Dashboard** | `standardize_dashboards.py` |
| **Detalhes Implementação** | `IMPLEMENTATION-SUMMARY.md` |

---

## ⚡ Quick Wins

### Adicionar Logo
```html
<div class="brand">
    <img src="logo.png" alt="Logo">
</div>
```

### Mudar Cor do KPI
```html
<!-- Trocar apenas a classe de cor -->
<div class="kpi-card c-purple">  <!-- antes: c-orange -->
    ...
</div>
```

### Fazer Seção Colapsável
```html
<!-- Envolver em .phase-block + onclick handler -->
<div class="phase-block-header" onclick="togglePhase(this)">
```

### Dark Mode Testing
```javascript
// No console:
document.body.style.colorScheme = 'dark';
```

---

## 🎓 Exemplos em Repositório

```
reports/Financeiro/
├── Financeiro-executive-dashboard.html       ← Full example
├── Financeiro-3tier-dashboard.html           ← With charts
└── ROI_ANALYSIS_VISUAL.html                ← With metrics

reports/_templates/
├── example-dashboard.html                  ← Simple example
└── executive-dashboard.html                ← Complex example
```

---

**Última atualização:** 9 de Junho de 2026  
**Padrão:** Avanade Orange DNA v3.0.0
