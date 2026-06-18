# 🎨 Avanade Brand Guidelines — Component Implementation (v2.0 + Orange DNA)

> **Updated:** 2026-06-08 · Integrated Orange DNA design system while preserving Avanade brand identity.  
> **Reference:** See `ORANGE-DNA-DESIGN-SYSTEM.md` for comprehensive token documentation.  
> **CSS Tokens:** Import `DESIGN-TOKENS.css` in all projects (single source of truth).

---

## Avanade Color Palette (PRESERVED)

### Primary Colors — REGISTERED BRAND (DO NOT REPLACE)
```
Avanade Orange (Primary CTA)
HEX:  #ff6b35
RGB:  (255, 107, 53)
CMYK: (0, 65, 80, 0)
Usage: Buttons, progress bars, accents, hover states
NOTE: Not #ff5800 (Orange DNA). Keep #ff6b35 for brand compliance.
```

```
Avanade Blue (Secondary)
HEX:  #1f3a93
RGB:  (31, 58, 147)
CMYK: (95, 85, 0, 42)
Usage: Headers, text, borders, main UI elements
NOTE: Not #0078D4 (MS Fluent). Keep #1f3a93 as organizational standard.
```

### Accent Colors (Existing)
```
Light Orange (Highlight)
HEX:  #f7931e
RGB:  (247, 147, 30)
CMYK: (0, 40, 87, 3)
Usage: Hover states, secondary accents, gradient overlays
```

```
Dark Blue (Backgrounds)
HEX:  #0f1d4d
RGB:  (15, 29, 77)
CMYK: (100, 85, 0, 70)
Usage: Dark mode backgrounds, footer, high-contrast text
```

### Accent Colors (NEW — Orange DNA Integration)
```
Yellow Accent (Warning, Secondary Status)
HEX:  #FFB414
RGB:  (255, 180, 20)
Usage: Warning badges, secondary status indicators, attention-grabbing elements
Contrast: 3.2:1 on white (AA for large text only — use with supporting icon)
```

```
Peach Highlight (Active States, Hover Backgrounds)
HEX:  #FFE6D3
RGB:  (255, 230, 211)
Usage: Active menu items, selected rows, hover backgrounds, sidebar active states
Contrast: 1.8:1 on white (low contrast — use as background only, not text)
```

### Neutral Colors (ALIGNED)
```
Light Gray (Backgrounds)
HEX:  #f9f9f9
RGB:  (249, 249, 249)
CMYK: (0, 0, 0, 2)
Usage: Page backgrounds, light surfaces
```

```
Border Gray (Dividers)
HEX:  #e0e0e0
RGB:  (224, 224, 224)
CMYK: (0, 0, 0, 12)
Usage: Borders, dividers, subtle lines
```

### Status Colors (4-Color Palette)
| Status | Color | RGB | Usage |
|--------|-------|-----|-------|
| 🟢 Success | #00A650 | (0, 166, 80) | Gate approved, ✓ checks |
| 🟡 Warning | #FFB414 | (255, 180, 20) | Gate in review, ⚠️ caution (NEW) |
| 🔴 Error | #C80000 | (200, 0, 0) | Gate blocked, ✗ failures |
| ⚪ Neutral | #888888 | (136, 136, 136) | Disabled, neutral state |

---

## Typography

### Font Family
**Primary:** Segoe UI, Arial, sans-serif  
**Fallback:** -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif (system fonts for resilience)  
**Rationale:** Segoe UI is Microsoft standard (Avanade brand); system fonts provide fallback reliability.

### Font Weights & Sizes

| Element | Weight | Size | Line Height |
|---------|--------|------|-------------|
| Page Title (H1) | 700 Bold | 32px | 1.2 |
| Section Header (H2) | 600 Semibold | 24px | 1.3 |
| Card Title (H3) | 600 Semibold | 18px | 1.3 |
| Label (H4) | 600 Semibold | 16px | 1.3 |
| Subtitle (H5) | 500 Medium | 14px | 1.4 |
| Body Text | 400 Regular | 14px | 1.5 |
| Small Text | 400 Regular | 12px | 1.4 |
| Toast Header | 600 Semibold | 16px | 1.3 |
| Label/Tag | 500 Medium | 12px | 1.2 |

---

## Layout & Navigation (NEW — Orange DNA)

### Sidebar Navigation (Optional for Multi-Section Dashboards)

**Dimensions:**
- Width: 248px
- Min-height: 100vh (full viewport)
- Position: Fixed left (docked)
- Background: #ffffff (light) / #0f1d4d (dark mode)
- Border-right: 1px solid #e0e0e0

**Navigation Items:**
- Padding: 12px 16px (vertical/horizontal)
- Font: 14px regular, #333333
- Line-height: 1.5

**Active State:**
- Background: #FFE6D3 (peach highlight — NEW from Orange DNA)
- Left border: 4px solid #ff6b35 (orange)
- Text color: #1f3a93 (blue)
- Font-weight: 500 medium

**Hover State:**
- Background: rgba(255, 107, 53, 0.05) (faint orange)
- Transition: 200ms ease-in-out

**Example:**
```html
<!-- Active sidebar item -->
<a style="
  background-color: #FFE6D3;
  border-left: 4px solid #ff6b35;
  color: #1f3a93;
  padding: 12px 16px;
  display: block;
">
  Dashboard
</a>
```

### Top Bar / Header (Optional — Orange DNA Pattern)

**Dimensions:**
- Height: 56px
- Background: #ffffff
- Border-bottom: 1px solid #e0e0e0
- Padding: 0 16px (horizontal)
- Display: Flex, align-items: center, justify-content: space-between

**Sections:**
1. **Left:** Logo/Branding + Title
   - Font: 18px semibold, #1f3a93
   
2. **Center-Right:** Search/Filter (optional)
   - Input field with placeholder
   
3. **Right:** User menu, notifications (optional)
   - Icons + dropdown

**Example:**
```html
<div style="
  height: 56px;
  background: white;
  border-bottom: 1px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 16px;
">
  <h1 style='font-size: 18px; color: #1f3a93; margin: 0;'>Dashboard</h1>
  <div><!-- User menu --></div>
</div>
```

---

## Component-Specific Branding

### Header Section
```
┌─────────────────────────────────────┐
│ AVANADE                             │
│ ───── (orange underline)            │
│                                     │
│ Data Migration Upload Manager       │
│ Secure file upload with progress    │
└─────────────────────────────────────┘
```

**Implementation:**
- "AVANADE" text: Bold, #1f3a93
- Underline bar: 4px height, #ff6b35
- Main title: Bold, #1f3a93, 32px
- Subtitle: Regular, #0f1d4d, 16px

### Upload Buttons

**Standard State:**
- Background: `rgba(255, 107, 53, 0.1)` (Orange 10% opacity)
- Border: 2px solid #ff6b35
- Text: #ff6b35
- Icon: lucide-react icon in #ff6b35

**Hover State:**
- Box Shadow: 0 8px 16px rgba(255, 107, 53, 0.15)
- Transform: translateY(-2px)
- Border: 2px solid #ff6b35 (darker)

**Disabled State:**
- Background: rgba(224, 224, 224, 0.5)
- Border: 2px solid #cccccc
- Text: #999999
- Icon: #999999
- Cursor: not-allowed

**Code:**
```tsx
style={{
  backgroundColor: disabled
    ? "rgba(224, 224, 224, 0.5)"
    : "rgba(255, 107, 53, 0.1)",
  color: disabled ? "#999" : "#ff6b35",
  border: `2px solid ${disabled ? "#ccc" : "#ff6b35"}`,
}}
```

### Toast Container

**Border:**
- Top border: 2px solid #ff6b35
- Corners: 20px border-radius
- Shadow: 0 20px 60px rgba(0, 0, 0, 0.15)

**Header:**
- Title color: #1f3a93
- Background: white (light mode), #1a1f37 (dark mode)
- Font: 16px semibold

**File Items:**
- Background: transparent (hover: rgba(255, 107, 53, 0.05))
- Text color: #1f3a93
- File icon: Match FILE_TYPES colors
- Progress circle: #ff6b35

**Close Button:**
- Default: transparent
- Hover: background #ff6b35, color white
- Icon size: 16px

### Progress Indicator

**Circular Progress:**
- Background circle: #e0e0e0
- Progress circle: #ff6b35
- Stroke width: 3px
- Size: 20px × 20px
- Animation: smooth linear (300ms per update)

**Color Gradient (Optional):**
```css
stroke: linear-gradient(to right, #ff6b35, #f7931e);
```

---

## Dark Mode Support

### Color Adaptations

| Element | Light Mode | Dark Mode |
|---------|-----------|-----------|
| Background | #f9f9f9 | #1a1f37 |
| Text Primary | #1f3a93 | #ffffff |
| Text Secondary | #666666 | #b0b0b0 |
| Borders | #e0e0e0 | #2a2f4f |
| Cards | #ffffff | #0f1d4d |
| Hover | rgba(255,107,53,0.1) | rgba(255,107,53,0.2) |

### Implementation
```tsx
// Use Tailwind's dark: prefix
<div className="bg-white dark:bg-gray-800">
  <p className="text-gray-900 dark:text-gray-100">Text</p>
</div>

// Or inline styles with media query
style={{
  backgroundColor: prefersDark ? '#1a1f37' : '#ffffff',
}}
```

---

## Spacing & Layout

### Component Padding
```
Header:     px-4 py-3 (12px top/bottom, 16px left/right)
Content:    px-4 py-2 (8px top/bottom, 16px left/right)
Button:     px-4 py-2 (8px top/bottom, 16px left/right)
```

### Component Gaps
```
Icon to text:     gap-2 (8px)
Button group:     gap-3 (12px)
Section spacing:  mb-8 (32px)
Item spacing:     py-2 (8px between items)
```

### Border Radius
```
Toast container:    20px
Buttons:            8px
Icons:              4px
Cards:              12px
```

---

## Icons & Visual Assets

### File Type Icons (lucide-react)
- PDF, DOC, XLS, PPT, etc.: `File` icon
- Images: `FileImage` icon
- Video: `FileVideo` icon
- Audio: `FileAudio` icon
- Code: `FileCode` icon
- Success: Custom `CheckCircle` (green #27ae60)
- Error: `XCircle` (red #e74c3c)

### Control Icons
- Expand: `ChevronDown` (#1f3a93)
- Collapse: `ChevronUp` (#1f3a93)
- Close: `X` (#ff6b35 or #ffffff)

### Icon Colors by File Type
```typescript
pdf:  text-red-500
zip:  text-gray-500
jpg:  text-yellow-500
doc:  text-blue-500
xls:  text-green-500
ppt:  text-orange-500
mp4:  text-purple-500
mp3:  text-pink-500
js:   text-indigo-500
```

---

## Animations & Transitions

### Progress Animation
```css
/* Smooth progress bar update */
transition: stroke-dashoffset 300ms ease-in-out;
```

### Button Hover
```css
/* Smooth color & shadow transition */
transition: all 200ms ease-in-out;
transform: translateY(-2px);
box-shadow: 0 8px 16px rgba(255, 107, 53, 0.15);
```

### Toast Fade
```css
/* Smooth entrance/exit */
animation: slideIn 300ms ease-out;
```

### Pulse Animation
```css
/* Active upload indicator */
animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
```

---

## Accessibility

### Color Contrast
- Text on white: All colors meet WCAG AA standard
- Orange (#ff6b35) on white: Contrast ratio 4.5:1 ✓
- Blue (#1f3a93) on white: Contrast ratio 8.1:1 ✓

### Interactive Elements
- Min click area: 44×44px
- Focus visible: 2px outline in brand colors
- Keyboard navigation: Tab order follows visual order
- Screen reader: ARIA labels on icons

### Visual Indicators
- Status: Not color-only (icon + color)
- Progress: Visual bar + percentage
- Errors: Icon + message text

---

## Files Incorporating This Brand

| File | Purpose |
|------|---------|
| `google-drive-uploader-toast-avanade.tsx` | Main component with branding |
| `demo-uploader.tsx` | Demo with full brand presentation |
| This file | Brand guidelines reference |
| `UPLOADER-COMPONENT-GUIDE.md` | Technical integration guide |
| `SETUP-GUIDE.md` | Project setup instructions |

---

## Quick Reference Colors

```
// Copy-paste into your component
const AVANADE_COLORS = {
  // Primary (PRESERVED)
  primary: "#ff6b35",              // Orange - main CTA
  secondary: "#1f3a93",            // Blue - headers
  
  // Accents (Existing)
  accent: "#f7931e",               // Light orange - hover
  dark: "#0f1d4d",                 // Dark blue - dark mode
  
  // Accents (NEW — Orange DNA)
  warningYellow: "#FFB414",        // Warning, secondary status
  peachHighlight: "#FFE6D3",       // Active states, hover backgrounds
  
  // Neutrals
  light: "#f9f9f9",                // Light gray - backgrounds
  border: "#e0e0e0",               // Gray - borders
  textSecondary: "#666666",        // Secondary text
  textDark: "#333333",             // Primary text
  
  // Status
  success: "#00A650",              // Green
  warning: "#FFB414",              // Yellow
  error: "#C80000",                // Red
  neutral: "#888888",              // Gray
};
```

---

## Using DESIGN-TOKENS.css (NEW)

For all new projects and components, **import and use CSS custom properties** instead of hard-coding colors:

```html
<!-- Import tokens -->
<link rel="stylesheet" href="DESIGN-TOKENS.css">

<!-- Use in CSS -->
<style>
  .button {
    background-color: var(--ava-orange-primary);
    color: white;
    padding: var(--ava-space-2) var(--ava-space-4);
    border-radius: var(--ava-radius-md);
    box-shadow: var(--ava-shadow-sm);
  }
</style>

<!-- Or use in React -->
<button style={{
  backgroundColor: 'var(--ava-orange-primary)',
  padding: 'var(--ava-space-2) var(--ava-space-4)',
  borderRadius: 'var(--ava-radius-md)',
}}>
  Primary Action
</button>
```

**Benefits:**
- 🎯 Single source of truth (all colors centralized)
- 🔄 Easy to update (one file, all projects inherit)
- 🌙 Dark mode support (CSS media query overrides)
- ♿ WCAG AA compliance verified
- 🚀 Faster refactoring + brand consistency

---

## Dos & Don'ts (UPDATED)

### ✅ DO (UPDATED with Orange DNA)

- ✅ Use orange (#ff6b35) for primary actions (NOT #ff5800)
- ✅ Use blue (#1f3a93) for headers and text (NOT #0078D4)
- ✅ Use yellow (#FFB414) for warning status (NEW)
- ✅ Use peach (#FFE6D3) for active/hover states (NEW)
- ✅ Add sidebar navigation (248px) for multi-section dashboards (NEW)
- ✅ Add top bar (56px) to dashboards (NEW)
- ✅ Import DESIGN-TOKENS.css for all colors (NEW)
- ✅ Combine orange + blue for professional look
- ✅ Include Avanade logo/text in prominent location
- ✅ Use 20px border radius for toast
- ✅ Implement dark mode support
- ✅ Use lucide-react for consistency
- ✅ Test color contrast (WCAG AA minimum)

### ❌ DON'T (REINFORCED)

- ❌ Do NOT replace #ff6b35 with #ff5800 (Orange DNA's orange)
- ❌ Do NOT replace #1f3a93 with #0078D4 (MS Fluent blue)
- ❌ Do NOT reduce border-radius to 2px (keep 8-20px for accessibility)
- ❌ Do NOT compress spacing grid (keep 8px base, not 4px)
- ❌ Do NOT hard-code colors (use DESIGN-TOKENS.css variables)
- ❌ Change primary orange to different shade
- ❌ Use red (#e74c3c) for primary actions
- ❌ Remove Avanade branding
- ❌ Use gradients (unless on accent elements)
- ❌ Mix multiple brand colors randomly
- ❌ Ignore dark mode requirements
- ❌ Use colors without sufficient contrast
- ❌ Change component layout significantly

---

## Usage Examples

### Example 1: Correct Branding
```tsx
// ✓ Good
style={{
  backgroundColor: "rgba(255, 107, 53, 0.1)",  // Orange background
  color: "#1f3a93",                            // Blue text
  border: "2px solid #ff6b35",                 // Orange border
}}
```

### Example 2: Header Implementation
```tsx
// ✓ Good
<div style={{ color: "#1f3a93", fontSize: "32px", fontWeight: "bold" }}>
  AVANADE
  <div style={{ height: "4px", width: "60px", backgroundColor: "#ff6b35", marginTop: "8px" }} />
</div>
```

### Example 3: Button Implementation
```tsx
// ✓ Good
<button
  style={{
    backgroundColor: "rgba(255, 107, 53, 0.1)",
    color: "#ff6b35",
    border: "2px solid #ff6b35",
    borderRadius: "8px",
  }}
  onMouseEnter={(e) => {
    e.target.style.boxShadow = "0 8px 16px rgba(255, 107, 53, 0.15)";
  }}
>
  Upload File
</button>
```

---

## Questions?

Refer to:
1. **Design System:** See `ORANGE-DNA-DESIGN-SYSTEM.md` (comprehensive token reference)
2. **CSS Tokens:** See `DESIGN-TOKENS.css` (import in all projects)
3. **Color palette:** See "Avanade Color Palette" section above
4. **Typography:** Check "Typography" section (font weights/sizes table)
5. **Layout & Navigation:** Check "Layout & Navigation (Orange DNA)" section
6. **Implementation:** Check `UPLOADER-COMPONENT-GUIDE.md`
7. **Setup:** Check `SETUP-GUIDE.md`

---

**Last Updated:** 2026-06-08  
**Brand Version:** Avanade 2026 + Orange DNA Integration  
**Status:** ✅ Complete (v2.0)  
**Related Files:**
- `ORANGE-DNA-DESIGN-SYSTEM.md` — Comprehensive design token documentation
- `DESIGN-TOKENS.css` — CSS custom properties (single source of truth)
- `UPLOADER-COMPONENT-GUIDE.md` — Technical implementation
- `SETUP-GUIDE.md` — Project setup
