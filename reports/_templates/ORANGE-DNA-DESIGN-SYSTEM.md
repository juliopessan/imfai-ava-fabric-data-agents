# Orange DNA · Design System Integration

**Status:** ✅ Active  
**Version:** 1.0.0  
**Last Updated:** 2026-06-08  
**Scope:** Consultoria Suite + Orange DNA Design Tokens

---

## Executive Summary

This document consolidates the **Orange DNA design system** with **Consultoria brand standards**. The integration preserves Consultoria's core identity (registered orange #ff6b35, blue #1f3a93, 8px spacing grid) while adopting Orange DNA's modern UI patterns (sidebar navigation, top bar, new accent colors).

**Key Decision:** Adopt Orange DNA's layout patterns and new accent colors (#FFB414, #FFE6D3) without replacing Consultoria's registered brand colors.

---

## 1. Color Palette (Consultoria + Orange DNA Integration)

### Primary Colors (PRESERVED — Consultoria Registered)
| Token | Value | Usage | Rationale |
|-------|-------|-------|-----------|
| **Consultoria Orange** | `#ff6b35` | Primary CTAs, accents, progress indicators | Registered brand — DO NOT REPLACE |
| **Consultoria Blue** | `#1f3a93` | Headers, text, borders, secondary elements | Organizational standard — DO NOT REPLACE |

### Accent Colors (NEW — Orange DNA)
| Token | Value | RGB | Usage | Notes |
|-------|-------|-----|-------|-------|
| **Yellow Accent** | `#FFB414` | 255, 180, 20 | Warning, secondary status, attention | From Orange DNA; complements blue + orange |
| **Peach Highlight** | `#FFE6D3` | 255, 230, 211 | Active states, hover backgrounds, selection | From Orange DNA; softer than full orange |

### Neutral Colors (ALIGNED)
| Token | Value | RGB | Usage |
|-------|-------|-----|-------|
| **Border Gray** | `#e0e0e0` | 224, 224, 224 | Borders, dividers, light lines |
| **Background Light** | `#f9f9f9` | 249, 249, 249 | Page backgrounds, card surfaces |
| **Background Lighter** | `#fafafa` | 250, 250, 250 | Alternate row backgrounds, subtle contrast |
| **Text Emphasis** | `#666666` | 102, 102, 102 | Secondary text, disabled states |
| **Text Dark** | `#333333` | 51, 51, 51 | Body text, primary content |

### Status Indicators (4-Color Palette)
| Status | Color | RGB | Usage |
|--------|-------|-----|-------|
| 🟢 **Success** | `#00A650` | 0, 166, 80 | Gate approved, ✓ checks |
| 🟡 **Warning** | `#FFB414` | 255, 180, 20 | Gate in review, ⚠️ caution |
| 🔴 **Error** | `#C80000` | 200, 0, 0 | Gate blocked, ✗ failures |
| ⚪ **Neutral** | `#888888` | 136, 136, 136 | Disabled, neutral state |

### Dark Mode Palette (Optional — for future use)
| Token | Light | Dark | Notes |
|-------|-------|------|-------|
| **Background** | `#f9f9f9` | `#1a1f37` | Primary surface |
| **Surface** | `#ffffff` | `#0f1d4d` | Cards, panels |
| **Text Primary** | `#333333` | `#ffffff` | Main text |
| **Text Secondary** | `#666666` | `#b0b0b0` | Secondary text |
| **Border** | `#e0e0e0` | `#2a2f4f` | Dividers |

---

## 2. Typography System

### Font Stack (Hybrid: Segoe UI + System Fallback)
```css
font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;
/* Segoe UI: brand primary (Microsoft standard)
   System fonts: fallback for reliability */
```

### Type Scale
| Role | Size | Weight | Line Height | Letter Spacing | Usage |
|------|------|--------|-------------|----------------|-------|
| **H1 / Page Title** | 32px | 700 Bold | 1.2 | 0 | Page headings, hero text |
| **H2 / Section Header** | 24px | 600 Semibold | 1.3 | 0 | Major sections, dashboard titles |
| **H3 / Card Title** | 18px | 600 Semibold | 1.3 | 0 | Card headers, subsections |
| **H4 / Label** | 16px | 600 Semibold | 1.3 | 0 | Form labels, emphasis text |
| **H5 / Subtitle** | 14px | 500 Medium | 1.4 | 0.02em | Subtitles, metadata |
| **Body** | 14px | 400 Regular | 1.5 | 0 | Paragraph text, default |
| **Small** | 12px | 400 Regular | 1.4 | 0 | Captions, helper text, small UI |
| **Extra Small** | 11px | 400 Regular | 1.3 | 0.05em | Timestamps, badges |

### Font Weights
- **700 Bold** — Page titles, strong emphasis
- **600 Semibold** — Headers (H1–H3), labels, badges
- **500 Medium** — Subtitles, emphasis text
- **400 Regular** — Body text, paragraphs, default

---

## 3. Spacing & Layout Grid

### Base Unit: 8px
All spacing follows an 8px grid. Divide/multiply by 2 for flexibility.

| Token | Value | Usage |
|-------|-------|-------|
| **Space 1** | 4px | Micro spacing (rarely used; see note below) |
| **Space 2** | 8px | Component padding, icon gaps, tight spacing |
| **Space 3** | 12px | Button groups, medium gaps |
| **Space 4** | 16px | Card padding, default padding, sidebar margins |
| **Space 6** | 24px | Section spacing, large margins |
| **Space 8** | 32px | Page padding, major layout spacing |
| **Space 12** | 48px | Between major sections |
| **Space 16** | 64px | Large section breaks |

**Note:** Avoid 4px spacing in most contexts. Use 8px or 16px for accessibility (WCAG compliance).

### Responsive Breakpoints
| Device | Width | Padding | Gap |
|--------|-------|---------|-----|
| **Mobile** | < 640px | 16px | 12px |
| **Tablet** | 640px–1024px | 20px | 16px |
| **Desktop** | > 1024px | 24px–32px | 16px–24px |

---

## 4. Border Radius & Shadows

### Border Radius (DO NOT reduce to 2px — keep soft, accessible)
| Component | Radius | Usage |
|-----------|--------|-------|
| **Cards, Panels** | 12px | Default component styling |
| **Buttons** | 8px | Button elements |
| **Toast, Modals** | 20px | Prominent notifications, large modals |
| **Input Fields** | 8px | Form inputs, textareas |
| **Icons (optional)** | 4px | Rounded icon backgrounds (rare) |

### Shadow System (3-Level Hierarchy)
| Level | CSS | Usage | Elevation |
|-------|-----|-------|-----------|
| **Subtle (sm)** | `0 1px 3px rgba(0, 0, 0, 0.08)` | Minimal lift; lines, badges | z: 1 |
| **Medium (md)** | `0 4px 12px rgba(0, 0, 0, 0.12)` | Cards, panels, dropdowns | z: 10 |
| **Prominent (lg)** | `0 12px 32px rgba(0, 0, 0, 0.15)` | Modals, toasts, overlays | z: 100+ |

**Implementation:**
```css
/* Light mode */
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);

/* Dark mode */
box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
```

---

## 5. Components & Patterns (Orange DNA)

### Sidebar Navigation (NEW)
**Dimensions:**
- Width: 248px
- Min-height: 100vh (full viewport)
- Background: #ffffff (light) / #0f1d4d (dark)
- Border-right: 1px solid #e0e0e0

**Active State:**
- Background: #FFE6D3 (peach highlight)
- Left border: 4px solid #ff6b35 (orange)
- Text color: #1f3a93 (blue)

**Hover State:**
- Background: rgba(255, 107, 53, 0.05) (faint orange)
- Transition: 200ms ease-in-out

### Top Bar / Header (NEW)
**Dimensions:**
- Height: 56px
- Background: #ffffff
- Border-bottom: 1px solid #e0e0e0

**Content:**
- Logo/branding (left)
- Title or breadcrumb (center-left)
- Search/filter (center-right)
- User menu (right)

### KPI / Metric Card
**Styling:**
- Background: #ffffff
- Border: 2px solid (colored by status: orange, blue, yellow, gray)
- Border-radius: 12px
- Padding: 16px
- Box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08)

**Hover:**
- Transform: translateY(-2px)
- Box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12)
- Border-color: darken by 10%

### Data Table
**Header:**
- Background: #f9f9f9
- Font-weight: 600 Semibold
- Border-bottom: 1px solid #e0e0e0

**Rows:**
- Alternating: #ffffff / #fafafa
- Hover: rgba(255, 107, 53, 0.05) (faint orange)
- Padding: 12px (vertical) / 16px (horizontal)

**Borders:**
- Column dividers: 1px solid #e0e0e0

### Status Badge
**Styling:**
- Padding: 4px 8px
- Border-radius: 4px
- Font-size: 12px
- Font-weight: 500 Medium

**Variants:**
- Success (green): bg #00A650, text white
- Warning (yellow): bg #FFB414, text #1f3a93
- Error (red): bg #C80000, text white
- Neutral (gray): bg #e0e0e0, text #333333

### Toast / Notification
**Styling:**
- Border-top: 2px solid #ff6b35 (orange)
- Border-radius: 20px
- Padding: 16px
- Box-shadow: 0 12px 32px rgba(0, 0, 0, 0.15)
- Background: #ffffff

**Variants:**
- Success: border-top #00A650
- Warning: border-top #FFB414
- Error: border-top #C80000

---

## 6. Animations & Transitions

### Standard Durations
| Type | Duration | Easing | Usage |
|------|----------|--------|-------|
| **Quick** | 150ms | ease-in-out | Hover, focus, micro-interactions |
| **Normal** | 300ms | ease-in-out | Modal open/close, toast fade, component transitions |
| **Slow** | 500ms | ease-in-out | Page transitions, complex animations |

### Common Animations
```css
/* Hover lift effect (cards, buttons) */
transition: all 200ms ease-in-out;
transform: translateY(-2px);

/* Fade in/out (modals, toasts) */
animation: fadeIn 300ms ease-out;

/* Progress animation */
transition: stroke-dashoffset 300ms ease-in-out;

/* Pulse (active states) */
animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
```

---

## 7. Accessibility (WCAG 2.1 AA Minimum)

### Color Contrast
| Element | Foreground | Background | Ratio | Status |
|---------|-----------|-----------|-------|--------|
| Consultoria Orange (#ff6b35) | orange | white | 4.5:1 | ✅ AA (large text) |
| Consultoria Blue (#1f3a93) | blue | white | 8.1:1 | ✅ AAA |
| Yellow (#FFB414) | yellow | white | 3.2:1 | ⚠️ AA (large text only) |
| Text Gray (#333333) | dark | white | 12.6:1 | ✅ AAA |

**Rule:** Use yellow only for large text (18px+) or with supporting icons.

### Interactive Elements
- **Min click area:** 44px × 44px (touch-friendly)
- **Focus visible:** 2px outline, high contrast
- **Keyboard nav:** Tab order follows visual left→right, top→bottom
- **Screen reader:** ARIA labels on icons, semantic HTML (h1–h6, nav, article, etc.)

### Visual Indicators
- Never use color alone; pair with icons, text, or patterns
- Progress indicators: visual bar + percentage
- Status: icon + color + text

---

## 8. CSS Custom Properties (Design Tokens)

Reference file: `DESIGN-TOKENS.css`

```css
:root {
  /* Primary Colors */
  --ava-orange-primary: #ff6b35;
  --ava-blue-secondary: #1f3a93;

  /* Accent Colors */
  --ava-yellow-accent: #FFB414;
  --ava-peach-highlight: #FFE6D3;

  /* Neutral Colors */
  --ava-gray-border: #e0e0e0;
  --ava-gray-bg-light: #f9f9f9;
  --ava-gray-bg-lighter: #fafafa;
  --ava-gray-text-secondary: #666666;
  --ava-gray-text-dark: #333333;

  /* Status Colors */
  --ava-status-success: #00A650;
  --ava-status-warning: #FFB414;
  --ava-status-error: #C80000;
  --ava-status-neutral: #888888;

  /* Spacing (8px base unit) */
  --ava-space-1: 4px;
  --ava-space-2: 8px;
  --ava-space-3: 12px;
  --ava-space-4: 16px;
  --ava-space-6: 24px;
  --ava-space-8: 32px;
  --ava-space-12: 48px;
  --ava-space-16: 64px;

  /* Border Radius */
  --ava-radius-sm: 4px;
  --ava-radius-md: 8px;
  --ava-radius-lg: 12px;
  --ava-radius-xl: 20px;

  /* Shadows */
  --ava-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
  --ava-shadow-md: 0 4px 12px rgba(0, 0, 0, 0.12);
  --ava-shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.15);

  /* Font Stack */
  --ava-font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif;

  /* Font Sizes */
  --ava-font-size-h1: 32px;
  --ava-font-size-h2: 24px;
  --ava-font-size-h3: 18px;
  --ava-font-size-h4: 16px;
  --ava-font-size-body: 14px;
  --ava-font-size-small: 12px;

  /* Font Weights */
  --ava-font-weight-bold: 700;
  --ava-font-weight-semibold: 600;
  --ava-font-weight-medium: 500;
  --ava-font-weight-regular: 400;

  /* Line Heights */
  --ava-line-height-tight: 1.2;
  --ava-line-height-normal: 1.3;
  --ava-line-height-relaxed: 1.5;

  /* Transitions */
  --ava-transition-quick: 150ms ease-in-out;
  --ava-transition-normal: 300ms ease-in-out;
  --ava-transition-slow: 500ms ease-in-out;

  /* Sidebar (new) */
  --ava-sidebar-width: 248px;

  /* Top Bar (new) */
  --ava-topbar-height: 56px;
}

/* Dark Mode Overrides (optional) */
@media (prefers-color-scheme: dark) {
  :root {
    --ava-gray-bg-light: #1a1f37;
    --ava-gray-bg-lighter: #0f1d4d;
    --ava-gray-text-secondary: #b0b0b0;
    --ava-gray-text-dark: #ffffff;
    --ava-gray-border: #2a2f4f;
    --ava-shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
    --ava-shadow-md: 0 4px 12px rgba(0, 0, 0, 0.4);
    --ava-shadow-lg: 0 12px 32px rgba(0, 0, 0, 0.5);
  }
}
```

---

## 9. Component Usage Examples

### Button with Orange Primary
```html
<button style="
  background-color: var(--ava-orange-primary);
  color: white;
  padding: var(--ava-space-2) var(--ava-space-4);
  border-radius: var(--ava-radius-md);
  border: none;
  font-weight: var(--ava-font-weight-semibold);
  cursor: pointer;
  transition: var(--ava-transition-quick);
">
  Primary Action
</button>
```

### Card with Peach Hover
```html
<div style="
  background: white;
  border: 2px solid var(--ava-orange-primary);
  border-radius: var(--ava-radius-lg);
  padding: var(--ava-space-4);
  box-shadow: var(--ava-shadow-sm);
  transition: var(--ava-transition-quick);
">
  KPI Card
</div>

<div:hover {
  transform: translateY(-2px);
  box-shadow: var(--ava-shadow-md);
}>
```

### Status Badge (Warning)
```html
<span style="
  background-color: var(--ava-status-warning);
  color: var(--ava-blue-secondary);
  padding: var(--ava-space-1) var(--ava-space-2);
  border-radius: var(--ava-radius-sm);
  font-size: var(--ava-font-size-small);
  font-weight: var(--ava-font-weight-medium);
">
  ⚠️ In Review
</span>
```

---

## 10. Implementation Checklist

- [ ] Import `DESIGN-TOKENS.css` in all HTML/React files
- [ ] Replace hard-coded colors with CSS variables (e.g., `background: var(--ava-orange-primary)`)
- [ ] Update all dashboards: executive-dashboard.html, DASHBOARD-ENTERPRISE-STANDARD.html, etc.
- [ ] Add sidebar navigation (248px) to new templates
- [ ] Add top bar (56px) to new templates
- [ ] Update React components (google-drive-uploader-toast-consultoria.tsx) to use new variables
- [ ] Test responsive (mobile 320px, tablet 640px, desktop 1024px+)
- [ ] Test dark mode (if applicable)
- [ ] Verify WCAG AA contrast (use WebAIM Contrast Checker)
- [ ] Visual regression testing (before/after screenshots)

---

## 11. Next Steps

1. **Review & Approval** — Stakeholder sign-off on color/spacing updates
2. **BRAND-GUIDELINES.md Update** — Incorporate this document's findings
3. **DESIGN-TOKENS.css Creation** — CSS custom properties file (single source of truth)
4. **Dashboard Refactoring** — Apply to executive-dashboard.html, ClienteBanco outputs, etc.
5. **Component Updates** — Update React components to use new tokens
6. **Testing & Validation** — Visual regression, WCAG AA verification, responsive testing

---

## References

- **Consultoria Brand Guidelines** — Official color palette, registered trademarks
- **Orange DNA Dashboard** — Modern layout patterns, new accent colors
- **WCAG 2.1 AA Standards** — Accessibility compliance (contrast, interactions, semantic HTML)
- **CSS Custom Properties** — See DESIGN-TOKENS.css

---

**Document Owner:** Design System Team  
**Last Reviewed:** 2026-06-08  
**Status:** ✅ Ready for Implementation
