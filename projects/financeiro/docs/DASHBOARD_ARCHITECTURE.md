# 📊 Arquitetura de Dashboards

> Design, componentes reutilizáveis, tokens de design e boas práticas.

---

## 📑 Índice

1. [Overview](#overview)
2. [Design System — Avanade v2.0](#design-system--avanade-v20)
3. [Componentes Reutilizáveis](#componentes-reutilizáveis)
4. [Padrões de Layout](#padrões-de-layout)
5. [Tipos de Dashboards](#tipos-de-dashboards)
6. [Responsividade](#responsividade)

---

## Overview

### Filosofia de Design

```
┌─────────────────────────────────────┐
│  AVANADE DESIGN SYSTEM v2.0          │
├─────────────────────────────────────┤
│  Tokens (Colors, Typography,        │
│   Spacing, Shadows, Radius)         │
├─────────────────────────────────────┤
│  Components (Cards, Tables,         │
│   Grids, Charts)                    │
├─────────────────────────────────────┤
│  Patterns (Navigation, Forms,       │
│   Data Tables, Alerts)              │
├─────────────────────────────────────┤
│  Pages (Dashboard, Report,          │
│   Portal)                           │
└─────────────────────────────────────┘
```

### Objetivo

- ✅ Consistência visual across all 8 dashboards
- ✅ Acessibilidade (WCAG 2.1 AA)
- ✅ Performance (< 2s load time)
- ✅ Responsividade (mobile-first)
- ✅ Avanade brand compliance

---

## Design System — Avanade v2.0

### Color Tokens

```css
:root {
  /* Master Gradient */
  --ava-gradient-full: linear-gradient(135deg, #FFB414 0%, #FF5800 100%);
  --ava-gradient-warm: linear-gradient(135deg, #FF5800 0%, #C80000 100%);
  --ava-gradient-cool: linear-gradient(135deg, #890078 0%, #FFB414 100%);

  /* Primary Colors */
  --ava-orange: #FF5800;
  --ava-aurora: #890078;
  --ava-thermal: #C80000;
  --ava-success: #00A650;

  /* Grey Scale (8 steps) */
  --ava-grey-80: #333333;    /* Darkest */
  --ava-grey-70: #4D4D4D;
  --ava-grey-60: #666666;
  --ava-grey-50: #808080;
  --ava-grey-40: #999999;
  --ava-grey-30: #B3B3B3;
  --ava-grey-20: #CCCCCC;
  --ava-grey-10: #E5E5E5;    /* Lightest */

  /* Semantic Colors */
  --ava-bg-body: #F7F7F7;
  --ava-bg-card: #FFFFFF;
  --ava-border: #E5E5E5;
  --ava-text-primary: #333333;
  --ava-text-secondary: #5A5A5A;
}
```

### Typography Tokens

```css
:root {
  --ava-font: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Sizes */
  --ava-h1-size: 52px;     /* Main title */
  --ava-h2-size: 36px;     /* Section header */
  --ava-h3-size: 28px;     /* Subsection */
  --ava-h4-size: 20px;     /* Card title */
  --ava-h5-size: 16px;     /* Label */
  --ava-body-size: 14px;   /* Body text */
  --ava-small-size: 12px;  /* Helper text */

  /* Weights */
  --ava-font-light: 300;
  --ava-font-regular: 400;
  --ava-font-semibold: 600;
  --ava-font-bold: 700;

  /* Letter Spacing */
  --ava-tracking-tight: -0.02em;
  --ava-tracking-normal: 0;
  --ava-tracking-wide: 0.04em;
}
```

### Spacing Tokens

```css
:root {
  /* Scale: 8px base */
  --ava-space-xs: 4px;      /* 0.5 unit */
  --ava-space-sm: 8px;      /* 1 unit */
  --ava-space-md: 16px;     /* 2 units */
  --ava-space-lg: 24px;     /* 3 units */
  --ava-space-xl: 32px;     /* 4 units */
  --ava-space-2xl: 48px;    /* 6 units */
  --ava-space-3xl: 64px;    /* 8 units */
}
```

### Shadow Tokens

```css
:root {
  --ava-shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --ava-shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --ava-shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.15);
  --ava-shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.2);
}
```

### Border Radius Tokens

```css
:root {
  --ava-radius-sm: 4px;     /* Inputs, small elements */
  --ava-radius-md: 8px;     /* Cards, buttons */
  --ava-radius-lg: 12px;    /* Modals */
  --ava-radius-full: 9999px; /* Pills, avatars */
}
```

---

## Componentes Reutilizáveis

### 1. Card

```html
<div class="card">
  <!-- Optional top border (signature) -->
  <div class="card-header">
    <h4 class="card-title">Card Title</h4>
    <p class="card-subtitle">Subtitle or description</p>
  </div>
  <div class="card-body">
    <!-- Content here -->
  </div>
  <div class="card-footer">
    <!-- Optional footer action -->
  </div>
</div>
```

```css
.card {
  background: var(--ava-bg-card);
  border-top: 4px solid var(--ava-orange);  /* Signature */
  border-radius: var(--ava-radius-md);
  box-shadow: var(--ava-shadow-md);
  padding: var(--ava-space-lg);
  transition: box-shadow 0.2s, transform 0.2s;
}

.card:hover {
  box-shadow: var(--ava-shadow-lg);
  transform: translateY(-2px);
}
```

### 2. KPI Card

```html
<div class="kpi-card">
  <div class="kpi-label">Key Metric</div>
  <div class="kpi-value">77%</div>
  <div class="kpi-sublabel">Reduction in effort</div>
  <div class="kpi-sparkline">
    <canvas id="spark-1"></canvas>
  </div>
</div>
```

```css
.kpi-card {
  background: linear-gradient(135deg, var(--ava-bg-card) 0%, rgba(255,88,0,0.02) 100%);
  border: 1px solid var(--ava-border);
  border-radius: var(--ava-radius-md);
  padding: var(--ava-space-lg);
  text-align: center;
}

.kpi-value {
  font-size: 48px;
  font-weight: var(--ava-font-bold);
  color: var(--ava-orange);
  margin: var(--ava-space-md) 0;
}
```

### 3. Data Table

```html
<table class="data-table">
  <thead>
    <tr>
      <th>Coluna 1</th>
      <th>Coluna 2</th>
      <th>Coluna 3</th>
    </tr>
  </thead>
  <tbody>
    <tr class="row-hover">
      <td>Value 1</td>
      <td>Value 2</td>
      <td class="text-right">Value 3</td>
    </tr>
  </tbody>
</table>
```

```css
.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--ava-body-size);
}

.data-table thead {
  background: var(--ava-grey-10);
  border-bottom: 2px solid var(--ava-orange);
}

.data-table th {
  padding: var(--ava-space-md);
  text-align: left;
  font-weight: var(--ava-font-semibold);
  color: var(--ava-text-primary);
}

.data-table tbody tr:hover {
  background: rgba(255, 88, 0, 0.02);
}

.data-table td {
  padding: var(--ava-space-md);
  border-bottom: 1px solid var(--ava-border);
}
```

### 4. Navigation Menu

```html
<div class="nav-menu">
  <a href="#" class="nav-btn active">💼 Proposta</a>
  <a href="#" class="nav-btn">🏗️ Blueprint</a>
  <a href="#" class="nav-btn">🧮 Calculadora</a>
  <a href="#" class="nav-btn">📊 Portal</a>
</div>
```

```css
.nav-menu {
  display: flex;
  gap: var(--ava-space-sm);
  background: var(--ava-gradient-full);
  padding: var(--ava-space-md);
  border-radius: var(--ava-radius-md);
}

.nav-btn {
  padding: var(--ava-space-sm) var(--ava-space-md);
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: var(--ava-radius-sm);
  text-decoration: none;
  font-weight: var(--ava-font-semibold);
  font-size: 11px;
  text-transform: uppercase;
  transition: all 0.3s;
}

.nav-btn:hover,
.nav-btn.active {
  background: rgba(255, 255, 255, 0.3);
}
```

### 5. Chart Container

```html
<div class="chart-container">
  <div class="chart-header">
    <h4>Revenue by Quarter</h4>
    <div class="chart-legend">
      <span><span class="legend-dot" style="background: #FF5800;"></span> 2026</span>
      <span><span class="legend-dot" style="background: #890078;"></span> 2025</span>
    </div>
  </div>
  <canvas id="chart-revenue"></canvas>
</div>
```

```css
.chart-container {
  background: var(--ava-bg-card);
  border-top: 4px solid var(--ava-orange);
  border-radius: var(--ava-radius-md);
  padding: var(--ava-space-lg);
  box-shadow: var(--ava-shadow-md);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--ava-space-lg);
}

.legend-dot {
  display: inline-block;
  width: 12px;
  height: 12px;
  border-radius: var(--ava-radius-full);
  margin-right: var(--ava-space-xs);
}
```

---

## Padrões de Layout

### 1. Hero Section

```html
<section class="hero">
  <div class="hero-accent"></div>
  <div class="hero-eyebrow">Data Migration Agents · Azure AI Foundry</div>
  <h1>Redução de <strong>77% em esforço</strong></h1>
  <p class="hero-sub">Migração de dados com agentes inteligentes.</p>
  <div class="hero-pills">
    <span class="hero-pill">Azure AI Foundry</span>
    <span class="hero-pill">ADLS Gen2</span>
    <span class="hero-pill">Semantic Kernel</span>
  </div>
</section>
```

```css
.hero {
  background: var(--ava-grey-80);
  color: white;
  padding: 72px 40px 60px;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(255,88,0,.18) 0%, rgba(137,0,120,.14) 100%);
  pointer-events: none;
}

.hero-accent {
  width: 80px;
  height: 5px;
  background: var(--ava-gradient-full);
  margin-bottom: var(--ava-space-lg);
}

.hero h1 {
  font-size: clamp(28px, 4vw, 52px);
  font-weight: 300;
  line-height: 1.1;
  max-width: 720px;
}

.hero h1 strong {
  font-weight: 700;
  background: var(--ava-gradient-warm);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
```

### 2. Grid Layout (3-Coluna)

```html
<div class="grid-3">
  <div class="card">...</div>
  <div class="card">...</div>
  <div class="card">...</div>
</div>
```

```css
.grid-3 {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--ava-space-lg);
  margin-bottom: var(--ava-space-2xl);
}

@media (max-width: 1200px) {
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .grid-3 { grid-template-columns: 1fr; }
}
```

### 3. Tabbed Content

```html
<div class="tabs">
  <nav class="tab-nav">
    <button class="tab-btn active" data-target="tab-1">Tab 1</button>
    <button class="tab-btn" data-target="tab-2">Tab 2</button>
  </nav>
  <div class="tab-content">
    <section id="tab-1" class="tab-pane active">Content 1</section>
    <section id="tab-2" class="tab-pane">Content 2</section>
  </div>
</div>
```

```javascript
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', function() {
    const target = this.dataset.target;
    
    // Hide all panes
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    
    // Remove active from all buttons
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    
    // Show selected
    document.getElementById(target).classList.add('active');
    this.classList.add('active');
  });
});
```

---

## Tipos de Dashboards

### Executive Dashboard

**Propósito:** ROI, timeline, value proposition

**Componentes:**
- ✅ Hero with key metric (77% reduction)
- ✅ 3 KPI cards (ROI < 6 months, ~120h savings, 2-8h setup)
- ✅ Comparison table (Manual vs IA)
- ✅ Benefits grid (6 cards)
- ✅ Timeline (4 stages)
- ✅ CTA buttons

**Público:** C-level, sponsors

### Operational Dashboard

**Propósito:** Throughput, latency, errors

**Componentes:**
- ✅ Real-time metrics (rows/hour, MB/sec)
- ✅ Job status board (queued, running, completed)
- ✅ Error log (streaming)
- ✅ Resource utilization (CPU, memory)
- ✅ Alerts (P1, P2, P3)

**Público:** Ops team, SRE

### Technical Dashboard

**Propósito:** Agent logs, system health

**Componentes:**
- ✅ Agent status matrix
- ✅ Data lineage (interactive)
- ✅ Transformation rules (executed)
- ✅ Network metrics (latency, throughput)
- ✅ Cost breakdown (compute, storage)

**Público:** Devs, architects

---

## Responsividade

### Breakpoints

```css
/* Mobile: 375px */
@media (max-width: 375px) {
  .grid-3 { grid-template-columns: 1fr; }
  .hero { padding: 40px 20px; }
  h1 { font-size: 24px; }
}

/* Tablet: 768px */
@media (max-width: 768px) {
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .hero { padding: 48px 20px; }
  h1 { font-size: 32px; }
}

/* Desktop: 1024px+ */
@media (min-width: 1024px) {
  .grid-3 { grid-template-columns: repeat(3, 1fr); }
  .hero { padding: 72px 40px; }
  h1 { font-size: 52px; }
}
```

### Mobile-First Approach

```
1. Design for 375px (smallest)
2. Enhance for 768px (tablet)
3. Optimize for 1920px (desktop)
```

---

## Performance Checklist

- ✅ Critical CSS inline (< 50KB)
- ✅ Fonts: system stack (no web fonts)
- ✅ Images: optimized + lazy load
- ✅ JavaScript: deferred loading
- ✅ Chart.js: CDN (cached)
- ✅ Target: < 2s load time, < 100ms interaction

---

**Última atualização:** 2026-06-12 | **Status:** ✅ v2.0 (Production)
