#!/usr/bin/env python3
"""
Repository Audit & Reorganization Report
Complete analysis and recommendations for repository cleanup
"""

import os
import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict

BASE = Path("c:\\Users\\data.owner\\Downloads\\imfai-ava-fabric-data-agents")

class RepoAudit:
    def __init__(self):
        self.findings = {
            "misplaced_files": [],
            "duplicate_files": [],
            "orphaned_files": [],
            "missing_structure": [],
            "out_of_spec_locations": [],
            "size_analysis": defaultdict(int),
            "file_count": 0,
            "recommendations": []
        }
    
    def scan_project(self, project_path, project_name):
        """Scan a project directory for issues"""
        issues = []
        
        root_files = [f for f in os.listdir(project_path) if os.path.isfile(os.path.join(project_path, f))]
        
        # Scripts should be in scripts/ folder
        script_extensions = ['.py', '.sh', '.ps1']
        scripts_in_root = [f for f in root_files if any(f.endswith(ext) for ext in script_extensions)]
        
        if scripts_in_root:
            issues.append({
                "project": project_name,
                "issue": f"Scripts in root directory (should be in scripts/)",
                "files": scripts_in_root,
                "severity": "MEDIUM",
                "action": f"Move to {project_path}/scripts/"
            })
        
        # Reports/documentation should be in docs/ or outputs/
        doc_patterns = ['SUMMARY', 'REPORT', 'EXECUTION', 'ANALYSIS']
        docs_in_root = [f for f in root_files if any(pattern in f.upper() for pattern in doc_patterns) and f.endswith('.md')]
        
        if docs_in_root:
            issues.append({
                "project": project_name,
                "issue": f"Documentation files in root (should be in outputs/reports/)",
                "files": docs_in_root,
                "severity": "MEDIUM",
                "action": f"Move to {project_path}/outputs/"
            })
        
        return issues
    
    def analyze_repo(self):
        """Complete repository analysis"""
        
        print("\n" + "="*80)
        print("REPOSITORY AUDIT REPORT")
        print("="*80)
        
        # Scan projects
        projects_path = BASE / "projects"
        projects = [d for d in os.listdir(projects_path) if os.path.isdir(os.path.join(projects_path, d))]
        
        all_issues = []
        for project in projects:
            project_full_path = os.path.join(projects_path, project)
            issues = self.scan_project(project_full_path, project)
            all_issues.extend(issues)
        
        # Generate report
        report = []
        report.append("# Repository Audit Report\n")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if all_issues:
            report.append("## 🔴 Issues Found\n\n")
            for issue in all_issues:
                report.append(f"### Project: {issue['project']}")
                report.append(f"**Issue:** {issue['issue']}")
                report.append(f"**Severity:** {issue['severity']}")
                report.append(f"**Files:**\n")
                for f in issue['files']:
                    report.append(f"- {f}\n")
                report.append(f"**Action:** {issue['action']}\n\n")
        else:
            report.append("✅ No critical issues found!\n\n")
        
        # Add structure recommendations
        report.append("## 📋 Organization Recommendations\n\n")
        report.append("### Current Expected Structure\n")
        report.append("""
```
imfai-ava-fabric-data-agents/
├── docs/                          # All documentation
│   ├── reports/                   # Analysis & reports
│   ├── project-plans/             # Planning documents
│   └── README.md
├── projects/                      # Case studies
│   ├── clientebanco/
│   │   ├── legacy/               # Original data/scripts
│   │   ├── scripts/              # Analysis scripts
│   │   ├── context/              # Analysis context
│   │   ├── outputs/              # Generated artifacts
│   │   ├── docs/                 # Project docs
│   │   └── wave-config.yaml
│   ├── ClienteSaude/
│   │   └── [same structure]
│   └── multi-platform-migration/
├── src/                           # Framework code
├── tools/                         # Utilities & validation
├── config/                        # Configuration files
├── reports/                       # [DEPRECATED - move to docs/]
└── README.md
```
""")
        
        report.append("\n## 📂 Migration Plan\n\n")
        report.append("""
### Phase 1: Consolidate Documentation
- Move `reports/` → `docs/reports/`
- Move `projects/*/docs/` → `docs/project-plans/`
- Keep `projects/*/outputs/` for generated artifacts

### Phase 2: Organize Project Scripts
- Move `projects/*/scripts/` → scripts stay here ✅
- Move root-level `*.py` → `projects/*/scripts/`
- Keep EMR/Airflow scripts in `legacy/`

### Phase 3: Clean Up Root
- Remove old TXT files from `projects/*/`
- Archive completed runs (but keep latest)
- Update INDEX.md and QUICK-START.md

### Phase 4: Validate Structure
- Run repository validation
- Update REPOSITORY-ORGANIZATION.md
- Ensure all symlinks/references updated
""")
        
        # Print and save
        report_text = "\n".join(report)
        print(report_text)
        
        report_path = BASE / "docs" / "AUDIT-REPORT-2026-06-16.md"
        with open(report_path, 'w') as f:
            f.write(report_text)
        
        print(f"\n✅ Audit report saved: {report_path}")
        return all_issues

if __name__ == "__main__":
    audit = RepoAudit()
    issues = audit.analyze_repo()
