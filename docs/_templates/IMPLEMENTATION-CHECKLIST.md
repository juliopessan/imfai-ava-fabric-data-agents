# Executive Dashboard — Implementation Checklist

**Status:** ✅ Production Ready  
**Compliance:** Avanade Style Guide 100%  
**Date:** 2026-06-05

---

## Phase 1: Review & Validation ✅

- [x] Dashboard HTML created (executive-dashboard.html)
- [x] All Avanade colors applied (#FF5800, Greys, status colors)
- [x] Segoe UI typography + proper weight hierarchy
- [x] Cards with border-top orange + hover effects
- [x] 8px base spacing throughout
- [x] Master gradient hero + tagline "Do what matters"
- [x] 3-gate flow visualization with status badges
- [x] 21-agent portfolio table (by phase)
- [x] 26-skill inventory cards
- [x] Governance framework documented
- [x] Responsive design (mobile → desktop)
- [x] Semantic HTML (headers, main, footer, tables)
- [x] Accessibility (WCAG 2.1 AA)
- [x] Validator passed: 100% compliant

---

## Phase 2: Setup & Configuration

### **For First-Time Users**
```bash
# 1. Open in browser
open reports/executive-dashboard.html

# 2. Review all sections (should take 5 minutes)

# 3. Generate sample dashboard to test automation
python reports/generate-dashboard.py --sample

# 4. Check generated file
open reports/executive-dashboard-WAVE-001.html
```

### **For Automation Integration**
```bash
# 1. Create wave config JSON
cat > projects/my-wave/wave-config.json << 'EOF'
{
  "wave_name": "WAVE-001",
  "discovery_owner": "discovery-scout",
  "entities": [
    {"name": "customer_dim", "rows": 1500000},
    {"name": "orders_fact", "rows": 25000000}
  ]
}
EOF

# 2. Create gate scores JSON
cat > projects/my-wave/gate-scores.json << 'EOF'
{
  "gate1": {"score": 0.92, "status": "approved"},
  "gate2": {"score": 0.78, "status": "in_review"},
  "gate3": {"score": null, "status": "pending"}
}
EOF

# 3. Generate dashboard with live data
python reports/generate-dashboard.py \
  --wave-config projects/my-wave/wave-config.json \
  --gate-scores projects/my-wave/gate-scores.json \
  --output reports/WAVE-001-executive-dashboard.html

# 4. Validate compliance
python reports/validate-compliance.py reports/WAVE-001-executive-dashboard.html
```

---

## Phase 3: Distribution

### **Option A: Email Distribution**
```bash
# Manual: Attach HTML or PDF to weekly report email
# Recipients: Steering committee, PMO leads, project sponsors

Subject: "Data Migration Factory — Week 22 Status Dashboard"
Body: "See attached dashboard for executive overview of wave progress."
Attachment: WAVE-001-executive-dashboard.html (or PDF)
```

### **Option B: Teams Integration**
```bash
# Pinned Message in Teams Channel:
# [Link to executive-dashboard.html on intranet]
# Updated: Every Monday 09:00 UTC
# [Screenshot of 3-gate flow status]
```

### **Option C: Intranet Portal**
```bash
# 1. Copy HTML to web server
cp reports/WAVE-001-executive-dashboard.html /var/www/dashboards/

# 2. Set up auto-refresh
# Apache: Add cache headers + CORS
# URL: https://intranet.acme.com/dashboards/WAVE-001.html

# 3. Share link in exec comms
```

### **Option D: PDF for Presentations**
```bash
# 1. Generate HTML
python reports/generate-dashboard.py --sample --output temp.html

# 2. Export to PDF (Chrome/Edge)
# File → Print → "Save as PDF"

# 3. Embed in PowerPoint
# Insert → Picture → temp.pdf
# OR Print to PDF, then use PDF-to-image converter

# 4. Share in deck
```

---

## Phase 4: Ongoing Maintenance

### **Weekly Status Updates**
- [ ] Day: Every Monday 09:00 UTC
- [ ] Task: Run generator with latest gate scores
- [ ] Command: `python reports/generate-dashboard.py --wave-config ... --gate-scores ...`
- [ ] Output: Send HTML to steering committee
- [ ] Archive: Save as `reports/WAVE-001-week-22.html`

### **Gate Approvals**
- [ ] When Gate 1 approved:
  - Update gate-scores.json with score + status
  - Regenerate dashboard
  - Email snapshot to stakeholders
  - Commit to Git (`git add reports/WAVE-001-gate1-approved.html`)

- [ ] When Gate 2 approved:
  - Update gate-scores.json
  - Regenerate dashboard
  - Publish to intranet
  - Update Teams pinned message

- [ ] When Gate 3 approved:
  - Update gate-scores.json (completed)
  - Regenerate dashboard (final state)
  - Archive snapshot
  - Publish post-migration report

### **Quarterly Brand Audit**
- [ ] Verify colors still match #FF5800 (no drift)
- [ ] Check Segoe UI font still loads
- [ ] Validate responsive breakpoints on new devices
- [ ] Run compliance validator: `python validate-compliance.py`

---

## Customization Checklist

### **If Adding New Sections**
- [ ] Create new `<div class="ava-section">`
- [ ] Add `<div class="ava-accent-bar"></div>` before heading
- [ ] Use `<h2>` for section titles (Light 32pt)
- [ ] Apply `ava-card` class to cards (border-top orange)
- [ ] Use `ava-grid ava-grid--3col` for multi-column layouts
- [ ] Test responsive (open DevTools, toggle mobile)
- [ ] Run validator: `python validate-compliance.py`

### **If Updating Metrics**
- [ ] Locate metric card (search for `ava-metric__value`)
- [ ] Update number (keep same HTML structure)
- [ ] Update label (keep same style)
- [ ] No other changes needed
- [ ] Optional: regenerate with Python if data sources change

### **If Creating Variants**
- [ ] Copy executive-dashboard.html → new-variant.html
- [ ] Edit HTML (keep CSS unchanged)
- [ ] Test on mobile + desktop
- [ ] Run validator
- [ ] Document changes in EXECUTIVE-DASHBOARD-GUIDE.md

---

## Troubleshooting

### **Dashboard looks different in my browser**
- ✅ Expected — system fonts vary by OS
- ✅ Segoe UI fallback to system-ui, sans-serif — design valid
- ✅ Colors should match (use HEX #FF5800 exactly)

### **PDF export has broken layout**
- ✅ Solution: Use Chrome/Edge (Firefox may have issues)
- ✅ Settings: Print background graphics, landscape mode
- ✅ Alternative: `wkhtmltopdf` CLI tool

### **Can't see Segoe UI font**
- ✅ Not required — fallback works
- ✅ Dashboard is still 100% Avanade compliant
- ✅ Install Segoe UI from Windows font manager if desired

### **Gate status not updating**
- ✅ Check gate-scores.json format (valid JSON?)
- ✅ Run generator with `--wave-config` and `--gate-scores` flags
- ✅ Test with sample: `python generate-dashboard.py --sample`

### **Validator reports compliance issues**
- ✅ Run: `python validate-compliance.py reports/executive-dashboard.html`
- ✅ If PASSED: ✅ You're compliant — deploy
- ✅ If FAILED: Fix issues before distribution

---

## Key Files at a Glance

| File | Size | Purpose | Update |
|------|------|---------|--------|
| `executive-dashboard.html` | 40KB | Template (static) | Rarely |
| `generate-dashboard.py` | 5KB | Data generator | Maintenance |
| `validate-compliance.py` | 8KB | Compliance check | Never |
| `EXECUTIVE-DASHBOARD-GUIDE.md` | 10KB | User guide | As needed |
| `README.md` | 8KB | Quick start | As needed |

---

## Success Criteria

✅ **All Met:**
- [x] Dashboard created in 100% Avanade Style
- [x] Compliance validator passes
- [x] Responsive on all devices
- [x] Accessible (WCAG 2.1 AA)
- [x] Python generator works with live data
- [x] Documentation complete
- [x] Ready for production deployment

---

## Go-Live Readiness

### **Day 1: Launch**
- [ ] Open executive-dashboard.html in browser
- [ ] Share link with steering committee
- [ ] Explain sections (3 minutes)
- [ ] Demo gate status colors
- [ ] Show next steps

### **Day 2–7: Weekly Cadence**
- [ ] Generate fresh dashboard each Monday
- [ ] Email to stakeholders
- [ ] Update Teams pinned message
- [ ] Monitor for feedback

### **Ongoing: Maintenance**
- [ ] Update gate-scores.json weekly
- [ ] Regenerate before steering meetings
- [ ] Archive approved gates
- [ ] Validate compliance quarterly

---

## Quick Reference: Commands

```bash
# View dashboard
open reports/executive-dashboard.html

# Generate with live data
python reports/generate-dashboard.py \
  --wave-config projects/WAVE-001/wave-config.json \
  --gate-scores projects/WAVE-001/gate-scores.json \
  --output reports/WAVE-001-dashboard.html

# Generate sample (for testing)
python reports/generate-dashboard.py --sample

# Validate compliance
python reports/validate-compliance.py reports/executive-dashboard.html

# Export to PDF (via CLI)
wkhtmltopdf reports/executive-dashboard.html report.pdf
```

---

## Notes

- 📌 All files in `/reports/` — no external dependencies
- 📌 Single HTML file: no CSS/JS links needed
- 📌 100% self-contained — can email or share offline
- 📌 Fully responsive — works on phone, tablet, desktop, print
- 📌 No Microsoft login required — plain browser + PDF export

---

**Status:** ✅ Ready for Production  
**Next:** Open dashboard in browser and review!  
**Support:** See EXECUTIVE-DASHBOARD-GUIDE.md for detailed help
