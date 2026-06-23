# 🎨 Consultoria Golden Standard — Dashboard Design System

**Version:** v3.0.0  
**Last Updated:** June 9, 2026  
**Status:** ✅ All dashboards standardized

---

## 📋 Overview

Todos os dashboards do repositório agora usam o **Padrão Ouro (Golden Standard) da Consultoria**, garantindo:

- ✅ **Consistência visual** 100% fiel ao Orange DNA
- ✅ **Design tokens** Consultoria (cores, tipografia, spacing)
- ✅ **Responsividade** mobile-first
- ✅ **Acessibilidade** WCAG 2.1 AA
- ✅ **Performance** CSS otimizado, zero dependências externas

---

## 🎯 Design Tokens

### Cores Consultoria Primárias

```css
--ava-orange: #FF5800;      /* Primary brand color */
--ava-magenta: #CE0569;     /* Accent */
--ava-red: #C80000;         /* Critical/Error */
--ava-gold: #FFB314;        /* Highlight/Success */
--ava-purple: #890078;      /* Secondary brand */
--ava-green: #47800A;       /* Positive/Growth */
--ava-dark: #2D2D2D;        /* Text primary */
--ava-gray: #595959;        /* Text secondary */
--ava-light: #E7E6E6;       /* Borders/Dividers */
```

### Layout & Spacing

| Token | Value | Usage |
|-------|-------|-------|
| `--bg-body` | `#FAFAFA` | Page background |
| `--text-primary` | `#1A1A1A` | Main text color |
| `--text-secondary` | `#5A5A5A` | Secondary text |
| Header Padding | `48px 56px` | Desktop header |
| Main Padding | `44px` | Content area |
| KPI Gap | `18px` | Grid spacing |

---

## 🏗️ Component Library

### 1. Header

```html
<div class="header">
    <div class="header-content">
        <h1>📊 Dashboard Title</h1>
        <p class="subtitle">Subtitle or description</p>
    </div>
</div>
```

**Features:**
- Gradient background: `#1a0a00 → #3d1700 → #FF5800`
- Radial glow effect (top-right)
- Z-index layering for overlapping elements

---

### 2. KPI Cards

```html
<div class="kpi-grid">
    <div class="kpi-card c-orange">
        <div class="kpi-value">42</div>
        <div class="kpi-label">Total Agents</div>
        <div class="kpi-sub">Across 5 modules</div>
    </div>
</div>
```

**Color Variants:** `c-orange`, `c-magenta`, `c-red`, `c-gold`, `c-purple`, `c-green`, `c-blue`, `c-dark`, `c-teal`

**Responsive:** Auto-reflows to 1-column on mobile

---

### 3. Phase Blocks (Collapsible)

```html
<div class="phase-block">
    <div class="phase-block-header" style="background: linear-gradient(135deg, #890078, #5e0053);" 
         onclick="togglePhase(this)">
        <div class="phase-badge-lg">📊</div>
        <div class="phase-title-area">
            <h3>Core Coordination</h3>
            <p>3 agents managing wave orchestration</p>
        </div>
        <div class="chevron">▼</div>
    </div>
    <div class="phase-content">
        <!-- Content here -->
    </div>
</div>
```

**Features:**
- Click to toggle visibility
- Smooth chevron rotation
- Custom header gradients per section

---

### 4. Tables

```html
<table>
    <thead>
        <tr>
            <th>Column 1</th>
            <th>Column 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Data 1</td>
            <td>Data 2</td>
        </tr>
    </tbody>
</table>
```

**Styling:**
- Purple gradient header
- Hover effect on rows
- 1px borders between cells

---

### 5. Mermaid Diagrams

```html
<div class="mermaid-section">
    <pre class="mermaid">
        graph LR
            A[Start] --> B[Process] --> C[End]
    </pre>
</div>
```

**Mermaid Config:**
```javascript
mermaid.initialize({
    theme: 'base',
    themeVariables: {
        primaryColor: '#FFF5EE',
        primaryBorderColor: '#FF5800',
        lineColor: '#FFB314'
    }
});
```

---

## 📁 File Structure

```
reports/
├── _templates/
│   ├── GOLDEN-STANDARD-TEMPLATE.html      ← Master template
│   ├── DASHBOARD-TEMPLATE-MASTER.html     ← Production template
│   ├── DASHBOARD-TEMPLATE-ORANGE-DNA.html ← Standardized ✅
│   ├── DASHBOARD-ENTERPRISE-STANDARD.html ← Standardized ✅
│   ├── executive-dashboard.html           ← Standardized ✅
│   ├── dashboard-with-metrics.html        ← Standardized ✅
│   ├── example-dashboard.html             ← Standardized ✅
│   ├── standardize_dashboards.py          ← Automation script
│   └── README-GOLDEN-STANDARD.md          ← This file
│
└── clientebanco/
    ├── clientebanco-autonomous-test-report.html      ← Standardized ✅
    ├── clientebanco-3tier-dashboard.html             ← Standardized ✅
    ├── clientebanco-executive-dashboard.html         ← Standardized ✅
    └── ROI_ANALYSIS_VISUAL.html                  ← Standardized ✅
```

**Status:** ✅ **11/11 dashboards** standardized

---

## 🚀 Quick Start

### Creating a New Dashboard

**Option A: Use the Master Template**

1. Copy `DASHBOARD-TEMPLATE-MASTER.html`
2. Replace `{{TITLE}}`, `{{SUBTITLE}}`, `{{CONTENT}}`
3. Done! Design is automatic

**Option B: Manual Integration**

Add this to your `<head>`:

```html
<link rel="stylesheet" href="golden-standard.css">
```

Or inline the CSS from `GOLDEN-STANDARD-TEMPLATE.html`

---

### Applying to Existing Dashboards

```bash
python reports/_templates/standardize_dashboards.py
```

This script:
- Extracts content from existing dashboards
- Wraps with Golden Standard HTML/CSS
- Preserves all original content
- Maintains responsive behavior

---

## 🎨 Using Consultoria Colors

### Orange DNA Color System

```html
<!-- KPI Card with Custom Color -->
<div class="kpi-card c-orange">
    <div class="kpi-value">100</div>
    <div class="kpi-label">Total Items</div>
</div>

<!-- Custom Gradient -->
<div class="phase-block-header" 
     style="background: linear-gradient(135deg, var(--ava-purple), var(--ava-magenta));">
    Content
</div>
```

### Color Mapping

| Color | Hex | Usage |
|-------|-----|-------|
| Orange | `#FF5800` | Primary CTA, icons |
| Magenta | `#CE0569` | Secondary accent |
| Red | `#C80000` | Errors, critical alerts |
| Gold | `#FFB314` | Success, highlights |
| Purple | `#890078` | Headers, titles |
| Green | `#47800A` | Growth, positive |
| Dark | `#2D2D2D` | Text, dark elements |

---

## 📱 Responsive Breakpoints

```css
/* Mobile (< 768px) */
@media (max-width: 768px) {
    .header { padding: 32px 24px; }
    .kpi-grid { grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }
    table { font-size: 12px; }
}
```

---

## ✨ Advanced Features

### Dark Mode Support

The Golden Standard includes built-in dark mode support via `prefers-color-scheme`:

```css
@media (prefers-color-scheme: dark) {
    body { background: linear-gradient(135deg, #0f1d4d 0%, #1a1f37 100%); }
    .content { background: #1a1f37; color: #e0e0e0; }
}
```

### Animation & Transitions

- Phase blocks: smooth collapse/expand
- KPI cards: hover lift effect (translateY -3px)
- Chevron: 0.3s rotation on toggle

---

## 🔧 Customization

### Adding Custom CSS

```html
<style>
    /* Your overrides here */
    .custom-section {
        background: var(--ava-orange);
        padding: 24px;
    }
</style>
```

### Modifying Colors

Update CSS variables in `:root`:

```css
:root {
    --ava-orange: #FF6B35; /* Your custom orange */
}
```

---

## 📊 Example Dashboard Markup

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>My Dashboard | Consultoria</title>
    <!-- Copy full <style> from GOLDEN-STANDARD-TEMPLATE.html -->
</head>
<body>
    <div class="header">
        <div class="header-content">
            <h1>📊 My Dashboard</h1>
            <p class="subtitle">Key metrics and insights</p>
        </div>
    </div>

    <div class="main">
        <!-- KPI Section -->
        <div class="section-title">
            <div class="section-icon">📈</div> Performance Indicators
        </div>
        <div class="kpi-grid">
            <div class="kpi-card c-orange">
                <div class="kpi-value">42</div>
                <div class="kpi-label">Total</div>
                <div class="kpi-sub">All items</div>
            </div>
        </div>

        <!-- Chart Section -->
        <div class="chart-container">
            <canvas id="myChart"></canvas>
        </div>

        <!-- Phase Block -->
        <div class="phase-block">
            <div class="phase-block-header" style="background: linear-gradient(135deg, #890078, #5e0053);">
                <div class="phase-badge-lg">🔄</div>
                <div class="phase-title-area">
                    <h3>Process Steps</h3>
                </div>
                <div class="chevron">▼</div>
            </div>
            <div class="phase-content">
                <p>Content here...</p>
            </div>
        </div>
    </div>

    <div class="footer">
        <strong class="brand-color">DMF</strong> &mdash; Data Migration Factory
    </div>

    <script>
        mermaid.initialize({...});
        function togglePhase(el) { el.parentElement.classList.toggle('collapsed'); }
    </script>
</body>
</html>
```

---

## ✅ Validation Checklist

Before deploying a dashboard, verify:

- [ ] Header has correct gradient (`#1a0a00 → #FF5800`)
- [ ] All colors use Consultoria palette
- [ ] KPI cards are responsive (4+ columns on desktop, 2+ on mobile)
- [ ] Tables have purple gradient headers
- [ ] Footer includes DMF branding
- [ ] Mermaid diagrams render correctly
- [ ] Dark mode CSS is applied
- [ ] No inline styles override design tokens
- [ ] Contrast ratios meet WCAG AA standards

---

## 🎓 References

| Asset | Location |
|-------|----------|
| Master Template | `GOLDEN-STANDARD-TEMPLATE.html` |
| Example Dashboards | `reports/_templates/example-dashboard.html` |
| Automation Script | `standardize_dashboards.py` |
| Design Tokens | `:root` CSS variables |
| Brand Guidelines | `BRAND-GUIDELINES.md` |

---

## 📞 Support

For dashboard design questions or improvements:

1. Check existing dashboards for patterns
2. Review CSS variables in `:root`
3. Test responsive behavior with Chrome DevTools
4. Validate with accessibility inspector

---

**Last Standardization:** June 9, 2026  
**Total Dashboards:** 11 ✅  
**Template Version:** v3.0.0  
**Orange DNA Alignment:** 100%
