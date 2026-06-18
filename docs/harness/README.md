# 🔄 Harness — CI/CD & Deployment

**Owner:** DevOps Team  
**Theme:** CI/CD pipelines, deployment automation, build management  
**Status:** ✅ Ready for Reference

---

## 📋 Contents

This folder contains **Harness CI/CD configuration and deployment guides**.

### **Files in This Folder**

| File | Purpose | Audience | Focus |
|------|---------|----------|-------|
| **HARNESS-CHANGELOG.md** | Pipeline changelog & updates | DevOps, Developers | Version history, changes |
| **HARNESS-MANIFEST.md** | Deployment manifest & config | DevOps, Release Mgmt | Pipeline definition, deployment |

---

## 🎯 Quick Start

### **For DevOps / Release Management**
```
1. Read: HARNESS-MANIFEST.md (configuration)
2. Review: HARNESS-CHANGELOG.md (recent changes)
3. Deploy: Using pipeline definition
```

### **For Developers (CI/CD Integration)**
```
1. Read: HARNESS-MANIFEST.md (relevant sections)
2. Understand: Your service's deployment pipeline
3. Trigger: Builds via Harness
```

---

## 🔑 Key Topics

### **Pipeline Configuration**
- Build stages
- Deployment strategies
- Environment configuration
- Approval gates

### **Deployment Management**
- Blue-green deployment
- Canary releases
- Rollback procedures
- Health checks

### **CI/CD Automation**
- Automated builds
- Testing integration
- Artifact management
- Release orchestration

---

## 🔗 Related Documents

### **In This Folder**
- Both files listed above

### **In Other Folders**
- `../governance/AUDIT-REPORT-2026-06-16.md` — Deployment audits
- `../observability/OBSERVABILITY-AND-TRACES.md` — Pipeline monitoring

---

## 📖 File Descriptions

### **HARNESS-MANIFEST.md**
```
📋 Harness Pipeline Configuration

Covers:
  • Pipeline structure & stages
  • Build definition
  • Deployment configuration
  • Environment setup
  • Artifact management
  • Approval workflows

Audience: DevOps, release managers
Use for: Pipeline setup, deployment configuration
Prerequisite: Basic Harness familiarity
```

### **HARNESS-CHANGELOG.md**
```
📝 Pipeline Changes & Version History

Covers:
  • Recent pipeline updates
  • Configuration changes
  • Stage modifications
  • Deployment strategy updates
  • Known issues

Audience: DevOps, developers
Use for: Understanding recent changes, troubleshooting
Prerequisite: Access to Harness platform
```

---

## 🔄 How to Use These Files

### **Scenario 1: "I need to deploy a service"**
```
Read:
1. HARNESS-MANIFEST.md (pipeline definition)

Follow:
1. Locate your service in manifest
2. Trigger build stage
3. Monitor deployment
4. Verify health checks

Result: ✅ Service deployed
```

### **Scenario 2: "I need to update the pipeline"**
```
Read:
1. HARNESS-MANIFEST.md (full)
2. HARNESS-CHANGELOG.md (recent changes)

Update:
1. Modify pipeline definition
2. Document changes in CHANGELOG
3. Test in staging
4. Deploy to production

Result: ✅ Pipeline updated
```

### **Scenario 3: "I need to troubleshoot a failed build"**
```
Check:
1. HARNESS-CHANGELOG.md (recent changes)
2. Pipeline logs in Harness
3. Deployment status

Debug:
1. Review build logs
2. Check artifact creation
3. Verify environment variables

Result: ✅ Issue identified & fixed
```

---

## 📚 Key Concepts

### **Build Pipeline**
- Code compilation
- Testing execution
- Artifact creation
- Registry push

### **Deployment Strategy**
- Blue-green (zero downtime)
- Canary (gradual rollout)
- Rolling (staged replacement)
- Feature flags (progressive)

### **Approval Gates**
- Manual approvals
- Automated checks
- Compliance validation
- Sign-off workflows

### **Rollback Procedures**
- Automatic rollback triggers
- Manual rollback execution
- Health verification
- Notification alerts

---

## 🔄 Workflow: Adding Harness Docs

### **When Adding a File**
1. **Decide**: Is it CI/CD related? (pipelines, deployment, build)
2. **Place it here** in `docs/harness/`
3. **Update this README.md** (add to "Contents" table)
4. **Update HARNESS-CHANGELOG.md** (if configuration changed)

### **Naming Convention**
- Use: `HARNESS-<TOPIC>.md`
- Examples:
  - ✅ `HARNESS-MANIFEST.md`
  - ✅ `HARNESS-DEPLOYMENT-STRATEGY.md`
  - ✅ `HARNESS-TROUBLESHOOTING.md`
  - ❌ `deployment.md` (too generic)

### **Changelog Updates**
- Always update HARNESS-CHANGELOG.md when modifying pipelines
- Include: date, change description, author, impact
- Keep most recent entries at top

---

## ✅ Checklist: Before Deployment

- [ ] Read HARNESS-MANIFEST.md
- [ ] Understand pipeline stages
- [ ] Know deployment strategy
- [ ] Reviewed HARNESS-CHANGELOG.md
- [ ] Approval gates cleared
- [ ] Staging tests passed
- [ ] Rollback plan confirmed

**All checked? Ready to deploy! 🚀**

---

## 📞 Support

### **"How do I deploy a service?"**
→ HARNESS-MANIFEST.md (pipeline section)

### **"What changed recently?"**
→ HARNESS-CHANGELOG.md

### **"How do I roll back?"**
→ HARNESS-MANIFEST.md (rollback section)

### **"I need monitoring for deployments"**
→ ../observability/OBSERVABILITY-AND-TRACES.md

---

**Status:** ✅ Ready for Deployment | 🔄 CI/CD  
**Created:** 2026-06-18 | **Owner:** DevOps Team

Let's ship it! 🚀
