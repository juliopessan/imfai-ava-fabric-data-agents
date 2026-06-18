#!/usr/bin/env python3
"""
Repository Structure Validator
Ensures repository conforms to expected organization
"""

import os
import sys
from pathlib import Path
from datetime import datetime

BASE = Path(".")

class StructureValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = []
        
    def check_project(self, project_path, project_name):
        """Validate a project's structure"""
        
        # Check for orphaned Python files in root
        root_files = [f for f in os.listdir(project_path) if os.path.isfile(os.path.join(project_path, f))]
        python_in_root = [f for f in root_files if f.endswith('.py')]
        
        if python_in_root:
            self.errors.append(f"[{project_name}] Python scripts in root: {python_in_root}")
        else:
            self.passed.append(f"[{project_name}] No Python scripts in root ✅")
        
        # Check for orphaned documentation files in root
        docs_in_root = [f for f in root_files if f.endswith('.md') and f not in ['README.md']]
        if docs_in_root:
            self.warnings.append(f"[{project_name}] Doc files in root: {docs_in_root}")
        else:
            self.passed.append(f"[{project_name}] Docs organized (except README) ✅")
        
        # Check for required folders
        required_dirs = ['outputs', 'scripts']
        for dir_name in required_dirs:
            dir_path = os.path.join(project_path, dir_name)
            if not os.path.isdir(dir_path):
                self.errors.append(f"[{project_name}] Missing {dir_name}/ folder")
            else:
                self.passed.append(f"[{project_name}] {dir_name}/ exists ✅")
        
        # Check for wave-config.yaml
        if not os.path.exists(os.path.join(project_path, 'wave-config.yaml')):
            self.warnings.append(f"[{project_name}] Missing wave-config.yaml")
        else:
            self.passed.append(f"[{project_name}] wave-config.yaml present ✅")
    
    def validate(self):
        """Run full validation"""
        print("\n" + "="*80)
        print("REPOSITORY STRUCTURE VALIDATION")
        print("="*80 + "\n")
        
        # Check projects
        projects_path = BASE / "projects"
        projects = [d for d in os.listdir(projects_path) 
                   if os.path.isdir(os.path.join(projects_path, d))]
        
        for project in projects:
            project_full_path = os.path.join(projects_path, project)
            self.check_project(project_full_path, project)
        
        # Print results
        if self.passed:
            print("✅ PASSED:")
            for msg in self.passed:
                print(f"  {msg}")
        
        if self.warnings:
            print("\n⚠️  WARNINGS:")
            for msg in self.warnings:
                print(f"  {msg}")
        
        if self.errors:
            print("\n❌ ERRORS:")
            for msg in self.errors:
                print(f"  {msg}")
            return False
        else:
            print("\n" + "="*80)
            print("✅ ALL CHECKS PASSED")
            print("="*80 + "\n")
            return True
    
    def summary(self):
        """Print summary"""
        total = len(self.passed) + len(self.warnings) + len(self.errors)
        print(f"\nSummary:")
        print(f"  Passed:  {len(self.passed)}")
        print(f"  Warnings: {len(self.warnings)}")
        print(f"  Errors:  {len(self.errors)}")
        print(f"  Total:   {total}")
        
        if self.errors:
            print(f"\n❌ Status: FAILED ({len(self.errors)} errors)")
            return 1
        elif self.warnings:
            print(f"\n⚠️  Status: PASSED WITH WARNINGS ({len(self.warnings)} warnings)")
            return 0
        else:
            print(f"\n✅ Status: PASSED")
            return 0

if __name__ == "__main__":
    validator = StructureValidator()
    success = validator.validate()
    exit_code = validator.summary()
    sys.exit(exit_code)
