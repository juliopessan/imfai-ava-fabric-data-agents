# Gate Report Template
# Template ID: gate-report-tmpl
# Agent: Orchestrator
# Version: 1.0

template:
  name: "Gate Report Template"
  description: "Standard template for gate validation reports"
  output_format: "markdown"
  
sections:
  header:
    title: "🚦 Gate {gate_number} Validation Report"
    metadata:
      - field: "Gate"
        value: "{gate_name}"
      - field: "Date"
        value: "{validation_date}"
      - field: "Validated by"
        value: "Orchestrator"
      - field: "Project"
        value: "{project_name}"

  overall_result:
    title: "Overall Result"
    status_options:
      - value: "PASS"
        icon: "✅"
        color: "green"
        message: "All criteria met. Gate passed."
      - value: "PARTIAL"
        icon: "⚠️"
        color: "yellow"
        message: "Some conditions apply. See details."
      - value: "FAIL"
        icon: "❌"
        color: "red"
        message: "Criteria not met. Action required."

  artifact_checklist:
    title: "Artifact Checklist"
    columns:
      - name: "#"
        width: 5
      - name: "Artifact"
        width: 25
      - name: "Found"
        width: 10
      - name: "Location"
        width: 35
      - name: "Quality"
        width: 15
    icons:
      found: "✅"
      not_found: "❌"
      quality_good: "✅"
      quality_warning: "⚠️"
      quality_fail: "❌"

  detailed_findings:
    title: "Detailed Findings"
    per_artifact:
      - section: "Overview"
      - section: "Quality Assessment"
      - section: "Issues Found"
      - section: "Recommendations"

  gaps_identified:
    title: "Gaps Identified"
    format: "bullet_list"
    severity_levels:
      - level: "Critical"
        icon: "🔴"
      - level: "Major"
        icon: "🟠"
      - level: "Minor"
        icon: "🟡"

  recommendations:
    title: "Recommendations"
    on_pass:
      title: "Next Steps"
      content: |
        ✅ Gate {gate_number} PASSED. Project may proceed to {next_phase}.
        
        **Recommended Next Agent:** {next_agent}
        **Suggested Command:** `*{next_command}`
    on_fail:
      title: "Required Actions"
      content: |
        ❌ Gate {gate_number} FAILED. The following must be completed:
        
        {gap_list}
        
        **Recommended Agent:** {remediation_agent}
        **Suggested Command:** `*{remediation_command}`

  footer:
    content: "*Gate validation performed by Orchestrator Agent*"
    timestamp: true

variables:
  gate_number:
    type: "integer"
    required: true
    values: [1, 2, 3]
  
  gate_name:
    type: "string"
    required: true
    mapping:
      1: "UPSTREAM → MIDSTREAM"
      2: "MIDSTREAM → DOWNSTREAM"
      3: "DOWNSTREAM → PRODUCTION"
  
  validation_date:
    type: "date"
    format: "YYYY-MM-DD"
    default: "current"
  
  project_name:
    type: "string"
    required: false
    default: "Data Pipeline Project"
  
  next_phase:
    type: "string"
    mapping:
      1: "MIDSTREAM"
      2: "DOWNSTREAM"
      3: "PRODUCTION"
  
  next_agent:
    type: "string"
    mapping:
      1: "DataArchitect"
      2: "DataFlow"
      3: "DeliveryPro"
  
  next_command:
    type: "string"
    mapping:
      1: "create-architecture"
      2: "generate-ddl"
      3: "deployment-plan"

output_example: |
  # 🚦 Gate 1 Validation Report
  
  **Gate:** UPSTREAM → MIDSTREAM  
  **Date:** 2025-01-21  
  **Validated by:** Orchestrator  
  **Project:** NYC Taxi Analytics
  
  ---
  
  ## Overall Result
  
  **Status:** ✅ PASS
  
  All criteria met. Gate passed.
  
  ---
  
  ## Artifact Checklist
  
  | # | Artifact | Found | Location | Quality |
  |---|----------|-------|----------|---------|
  | 1 | Problem Statement | ✅ | docs/problem-statement.md | ✅ |
  | 2 | KPIs | ✅ | docs/kpis.md | ✅ |
  | 3 | Analytical Questions | ✅ | docs/analytical-questions.md | ✅ |
  | 4 | STTM | ✅ | docs/sttm.md | ⚠️ |
  | 5 | DQ Initial | ✅ | docs/dq-initial.md | ✅ |
  
  ---
  
  ## Recommendations
  
  ✅ Gate 1 PASSED. Project may proceed to MIDSTREAM.
  
  **Recommended Next Agent:** DataArchitect
  **Suggested Command:** `*create-architecture`
  
  ---
  
  *Gate validation performed by Orchestrator Agent*
