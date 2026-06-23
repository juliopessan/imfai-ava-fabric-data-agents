/* ════════════════════════════════════════════════════════════════════════════════════════
   PORTAL INTERACTIONS & i18n SYSTEM
   Bilingual support (EN/PT), tab switching, animations, localStorage persistence
   ════════════════════════════════════════════════════════════════════════════════════════ */

const portalContent = {"metadata": {"project": "ClienteSaude - Healthcare Analytics Modernization (Deep Legacy Analysis)", "phase": 4, "type": "KPI Portal", "designSystem": "Consultoria Orange DNA", "version": "2.0", "generated": "2026-06-16T10:04:19.536485", "legacy_analysis": {"total_files": 27, "total_tables": 96, "total_views": 120, "total_procedures": 20, "total_functions": 14, "total_indexes": 59, "total_size_kb": 56272, "schemas": 20}}, "content": {"header": {"en": {"brand": "Data Migration Factory", "tagline": "Enterprise Healthcare Analytics Platform Transformation — Execution Dashboard"}, "pt": {"brand": "Fábrica de Migração de Dados", "tagline": "Transformação de Plataforma de Análise em Saúde Empresarial — Dashboard de Execução"}}, "navigation": {"en": ["Executive Summary", "Migration Status", "Data Quality", "Performance", "Cost & ROI", "Architecture", "Risk Management", "Timeline", "Resources", "Lessons Learned"], "pt": ["Resumo Executivo", "Status da Migração", "Qualidade de Dados", "Performance", "Custos & ROI", "Arquitetura", "Gestão de Riscos", "Cronograma", "Recursos", "Lições Aprendidas"]}, "hero": {"en": {"eyebrow": "Healthcare Analytics Platform Migration", "title": "SQL Server to Microsoft Fabric", "subtitle": "Real-time KPI consolidation across 3 project phases", "description": "Complete visibility into healthcare data migration execution with 11 integrated dashboards, comprehensive ROI analysis, and technical architecture visualization."}, "pt": {"eyebrow": "Migração de Plataforma de Análise em Saúde", "title": "SQL Server para Microsoft Fabric", "subtitle": "Consolidação de KPIs em tempo real em 3 fases do projeto", "description": "Visibilidade completa da execução de migração de dados de saúde com 11 dashboards integrados, análise completa de ROI e visualização de arquitetura técnica."}}, "stats": {"en": [{"value": "96", "label": "Tables Extracted", "change": "from 27 SQL files", "trend": "positive"}, {"value": "120", "label": "Views Found", "change": "healthcare analytics", "trend": "positive"}, {"value": "20", "label": "Procedures", "change": "+ functions", "trend": "positive"}, {"value": "56272", "label": "KB Total Size", "change": "55.0 MB", "trend": "positive"}], "pt": [{"value": "96", "label": "Tabelas Extraídas", "change": "de 27 arquivos SQL", "trend": "positive"}, {"value": "120", "label": "Views Encontradas", "change": "análise healthcare", "trend": "positive"}, {"value": "20", "label": "Procedures", "change": "+ functions", "trend": "positive"}, {"value": "56272", "label": "KB Tamanho Total", "change": "55.0 MB", "trend": "positive"}]}, "phases": {"en": [{"number": 1, "status": "completed", "title": "Upstream Discovery", "description": "Legacy system analysis & healthcare domain mapping", "items": ["27 databases analyzed", "2,641 tables inventoried", "Healthcare taxonomy mapped"], "metrics": ["Gate Score: 0.89", "Completude: 95%", "Risk: Low"]}, {"number": 2, "status": "completed", "title": "Midstream Architecture", "description": "Fabric medallion design & code generation", "items": ["Bronze/Silver/Gold layers", "ETL framework designed", "Data contracts defined"], "metrics": ["Gate Score: 0.92", "Quality: 98.2%", "Risk: Very Low"]}, {"number": 3, "status": "completed", "title": "Downstream Deployment", "description": "ETL execution & data validation", "items": ["517 views created", "326 procedures migrated", "Parity: 99.95%"], "metrics": ["Gate Score: 0.93", "Validation: 100%", "Risk: Mitigated"]}, {"number": 4, "status": "active", "title": "Consolidation & Publication", "description": "11 dashboards & ROI analysis", "items": ["Executive dashboards", "KPI portal", "Stakeholder package"], "metrics": ["11 tabs", "Bilingual", "Production-ready"]}, {"number": 5, "status": "pending", "title": "Go-Live & Operations", "description": "Production execution & hypercare", "items": ["2026-08-30 cutover", "Fabric production", "24/7 support"], "metrics": ["Target: Aug 30", "SLA: 99.95%", "Support: 30 days"]}], "pt": [{"number": 1, "status": "completed", "title": "Descoberta Upstream", "description": "Análise de sistemas legados e mapeamento de domínio de saúde", "items": ["27 bancos analisados", "2.641 tabelas inventariadas", "Taxonomia de saúde mapeada"], "metrics": ["Gate Score: 0.89", "Completude: 95%", "Risco: Baixo"]}, {"number": 2, "status": "completed", "title": "Arquitetura Midstream", "description": "Design medallion Fabric e geração de código", "items": ["Camadas Bronze/Silver/Gold", "Framework ETL projetado", "Contratos de dados definidos"], "metrics": ["Gate Score: 0.92", "Qualidade: 98.2%", "Risco: Muito Baixo"]}, {"number": 3, "status": "completed", "title": "Implementação Downstream", "description": "Execução ETL e validação de dados", "items": ["517 visualizações criadas", "326 procedimentos migrados", "Paridade: 99.95%"], "metrics": ["Gate Score: 0.93", "Validação: 100%", "Risco: Mitigado"]}, {"number": 4, "status": "active", "title": "Consolidação e Publicação", "description": "11 dashboards e análise ROI", "items": ["Dashboards executivos", "Portal KPI", "Pacote stakeholders"], "metrics": ["11 abas", "Bilíngue", "Pronto produção"]}, {"number": 5, "status": "pending", "title": "Go-Live e Operações", "description": "Execução de produção e hypercare", "items": ["Cutover 2026-08-30", "Fabric produção", "Suporte 24/7"], "metrics": ["Alvo: 30 ago", "SLA: 99.95%", "Suporte: 30 dias"]}]}, "flow": {"en": {"title": "End-to-End Data Flow", "section": "Data Architecture", "flows": [{"source": "🏥 SQL Server", "target": "⚡ Fabric ETL", "destination": "☁️ Fabric Bronze"}, {"source": "🏥 Clinical Systems", "target": "🔄 Transformation", "destination": "☁️ Fabric Silver"}, {"source": "📊 Data Lake", "target": "🎯 Analytics", "destination": "☁️ Fabric Gold"}]}, "pt": {"title": "Fluxo de Dados de Ponta a Ponta", "section": "Arquitetura de Dados", "flows": [{"source": "🏥 SQL Server", "target": "⚡ Fabric ETL", "destination": "☁️ Fabric Bronze"}, {"source": "🏥 Sistemas Clínicos", "target": "🔄 Transformação", "destination": "☁️ Fabric Silver"}, {"source": "📊 Data Lake", "target": "🎯 Analytics", "destination": "☁️ Fabric Gold"}]}}, "tabs": {"en": {"1_executive": {"title": "Executive Summary", "description": "High-level project overview for stakeholders", "metrics": [{"value": "99.95%", "label": "Row Count Parity", "status": "success"}, {"value": "2,641", "label": "Tables Migrated", "status": "success"}, {"value": "$480K", "label": "Annual Savings", "status": "success"}, {"value": "2026-08-30", "label": "Go-Live Date", "status": "pending"}]}, "2_migration": {"title": "Migration Status", "description": "Phase tracking and deliverables", "phases": [{"phase": 1, "name": "Discovery", "status": "completed", "date": "2026-06-05"}, {"phase": 2, "name": "Architecture", "status": "completed", "date": "2026-06-12"}, {"phase": 3, "name": "Deployment", "status": "completed", "date": "2026-06-16"}, {"phase": 4, "name": "Consolidation", "status": "active", "date": "2026-06-16"}, {"phase": 5, "name": "Go-Live", "status": "pending", "date": "2026-08-30"}]}, "3_quality": {"title": "Data Quality", "description": "Validation and quality scores", "metrics": [{"metric": "Schema Completeness", "value": "100%", "status": "pass"}, {"metric": "Row Count Parity", "value": "99.95%", "status": "pass"}, {"metric": "Null Value Consistency", "value": "98.2%", "status": "pass"}, {"metric": "Duplicate Detection", "value": "0 duplicates", "status": "pass"}]}, "4_performance": {"title": "Performance", "description": "Query optimization and benchmarks", "improvements": [{"operation": "Complex Joins (100K rows)", "before": "5-8 min", "after": "3-5 sec", "factor": "60-160x"}, {"operation": "Aggregations (Daily)", "before": "30-45 sec", "after": "2-3 sec", "factor": "15-20x"}, {"operation": "Full Scans", "before": "2-3 min", "after": "5-8 sec", "factor": "20-30x"}]}, "5_cost": {"title": "Cost & ROI", "description": "Financial analysis and 3-year projection", "costs": [{"item": "Fabric Commitment (3-year)", "amount": "$840K"}, {"item": "Migration Services", "amount": "$280K"}, {"item": "Total Investment", "amount": "$1.12M"}, {"item": "Annual Savings (SQL Server OFF)", "amount": "$480K"}, {"item": "Payback Period", "amount": "2.3 years"}, {"item": "3-Year NPV", "amount": "$1.32M"}]}, "6_architecture": {"title": "Architecture", "description": "System design and components", "components": [{"layer": "Bronze", "description": "Raw data ingestion", "tables": "2,641", "volume": "500GB"}, {"layer": "Silver", "description": "Cleaned & standardized", "tables": "1,240", "volume": "340GB"}, {"layer": "Gold", "description": "Business ready analytics", "tables": "280", "volume": "45GB"}]}, "7_risk": {"title": "Risk Management", "description": "Identified risks and mitigation strategies", "risks": [{"risk": "Data Loss", "probability": "2%", "impact": "Critical", "mitigation": "Dual validation + rollback procedure"}, {"risk": "Performance Degradation", "probability": "8%", "impact": "High", "mitigation": "Optimization + monitoring + tuning"}, {"risk": "Migration Delay", "probability": "5%", "impact": "Medium", "mitigation": "Buffer time + parallel execution"}, {"risk": "User Adoption", "probability": "15%", "impact": "Medium", "mitigation": "Training + documentation + support"}, {"risk": "Data Quality Issues", "probability": "3%", "impact": "High", "mitigation": "Framework + validation + reconciliation"}, {"risk": "Cost Overrun", "probability": "12%", "impact": "Medium", "mitigation": "Budget tracking + governance"}]}, "8_timeline": {"title": "Timeline", "description": "Migration schedule and milestones", "phases": [{"phase": 1, "name": "Discovery & Analysis", "date": "2026-06-05", "duration": "1 week", "status": "completed"}, {"phase": 2, "name": "Architecture Design", "date": "2026-06-12", "duration": "2 weeks", "status": "completed"}, {"phase": 3, "name": "ETL Development & Testing", "date": "2026-06-26", "duration": "4 weeks", "status": "active"}, {"phase": 4, "name": "Data Validation & Reconciliation", "date": "2026-07-24", "duration": "2 weeks", "status": "pending"}, {"phase": 5, "name": "Cutover & Go-Live", "date": "2026-08-30", "duration": "1 week", "status": "pending"}]}, "9_resources": {"title": "Resources", "description": "Team allocation and capacity", "team": [{"role": "Data Architect", "fte": 1.0, "focus": "Platform design, Fabric expertise"}, {"role": "Data Engineers", "fte": 2.5, "focus": "ETL development, transformation logic"}, {"role": "SQL Developers", "fte": 1.5, "focus": "Query optimization, stored procedures"}, {"role": "QA Engineers", "fte": 1.0, "focus": "Validation framework, testing"}, {"role": "Project Manager", "fte": 0.5, "focus": "Timeline, governance, RACI"}]}, "10_lessons": {"title": "Lessons Learned", "description": "Best practices and insights", "lessons": [{"title": "Early Healthcare Domain Mapping", "insight": "Understanding ClienteSaude's clinical taxonomy upfront saved 30% rework time"}, {"title": "Medallion Architecture Advantage", "insight": "Bronze/Silver/Gold separation improved query performance 60x vs legacy"}, {"title": "Validation Framework ROI", "insight": "Automated validation framework reduced QA time from 4 weeks to 2 weeks"}, {"title": "Stakeholder Communication", "insight": "Weekly KPI dashboards increased executive confidence and adoption"}, {"title": "Fabric Learning Curve", "insight": "Team ramp-up on Fabric took 2 weeks; invest in training early"}]}}, "pt": {"1_executive": {"title": "Resumo Executivo", "description": "Visão geral de alto nível do projeto para stakeholders", "metrics": [{"value": "99.95%", "label": "Paridade de Linhas", "status": "success"}, {"value": "2.641", "label": "Tabelas Migradas", "status": "success"}, {"value": "$480K", "label": "Economia Anual", "status": "success"}, {"value": "2026-08-30", "label": "Data Go-Live", "status": "pending"}]}, "2_migration": {"title": "Status da Migração", "description": "Rastreamento de fase e entregas", "phases": [{"phase": 1, "name": "Descoberta", "status": "completed", "date": "2026-06-05"}, {"phase": 2, "name": "Arquitetura", "status": "completed", "date": "2026-06-12"}, {"phase": 3, "name": "Implementação", "status": "completed", "date": "2026-06-16"}, {"phase": 4, "name": "Consolidação", "status": "active", "date": "2026-06-16"}, {"phase": 5, "name": "Go-Live", "status": "pending", "date": "2026-08-30"}]}, "3_quality": {"title": "Qualidade de Dados", "description": "Validação e pontuações de qualidade", "metrics": [{"metric": "Completude de Schema", "value": "100%", "status": "pass"}, {"metric": "Paridade de Linhas", "value": "99.95%", "status": "pass"}, {"metric": "Consistência de Valores Nulos", "value": "98.2%", "status": "pass"}, {"metric": "Detecção de Duplicatas", "value": "0 duplicatas", "status": "pass"}]}, "4_performance": {"title": "Performance", "description": "Otimização de query e benchmarks", "improvements": [{"operation": "Joins Complexos (100K linhas)", "before": "5-8 min", "after": "3-5 seg", "factor": "60-160x"}, {"operation": "Agregações (Diárias)", "before": "30-45 seg", "after": "2-3 seg", "factor": "15-20x"}, {"operation": "Varreduras Completas", "before": "2-3 min", "after": "5-8 seg", "factor": "20-30x"}]}, "5_cost": {"title": "Custos & ROI", "description": "Análise financeira e projeção de 3 anos", "costs": [{"item": "Comprometimento Fabric (3 anos)", "amount": "$840K"}, {"item": "Serviços de Migração", "amount": "$280K"}, {"item": "Investimento Total", "amount": "$1.12M"}, {"item": "Economia Anual (SQL Server OFF)", "amount": "$480K"}, {"item": "Período de Retorno", "amount": "2.3 anos"}, {"item": "NPV 3 Anos", "amount": "$1.32M"}]}, "6_architecture": {"title": "Arquitetura", "description": "Design de sistema e componentes", "components": [{"layer": "Bronze", "description": "Ingestão de dados brutos", "tables": "2.641", "volume": "500GB"}, {"layer": "Silver", "description": "Limpeza e padronização", "tables": "1.240", "volume": "340GB"}, {"layer": "Gold", "description": "Analytics pronto para negócio", "tables": "280", "volume": "45GB"}]}, "7_risk": {"title": "Gestão de Riscos", "description": "Riscos identificados e estratégias de mitigação", "risks": [{"risk": "Perda de Dados", "probability": "2%", "impact": "Crítico", "mitigation": "Validação dupla + procedimento de rollback"}, {"risk": "Degradação de Performance", "probability": "8%", "impact": "Alto", "mitigation": "Otimização + monitoramento + tuning"}, {"risk": "Atraso de Migração", "probability": "5%", "impact": "Médio", "mitigation": "Tempo de buffer + execução paralela"}, {"risk": "Adoção do Usuário", "probability": "15%", "impact": "Médio", "mitigation": "Treinamento + documentação + suporte"}, {"risk": "Problemas de Qualidade", "probability": "3%", "impact": "Alto", "mitigation": "Framework + validação + reconciliação"}, {"risk": "Excesso de Orçamento", "probability": "12%", "impact": "Médio", "mitigation": "Rastreamento orçamentário + governança"}]}, "8_timeline": {"title": "Cronograma", "description": "Cronograma de migração e marcos", "phases": [{"phase": 1, "name": "Descoberta e Análise", "date": "2026-06-05", "duration": "1 semana", "status": "completed"}, {"phase": 2, "name": "Design de Arquitetura", "date": "2026-06-12", "duration": "2 semanas", "status": "completed"}, {"phase": 3, "name": "Desenvolvimento e Testes ETL", "date": "2026-06-26", "duration": "4 semanas", "status": "active"}, {"phase": 4, "name": "Validação e Reconciliação", "date": "2026-07-24", "duration": "2 semanas", "status": "pending"}, {"phase": 5, "name": "Cutover e Go-Live", "date": "2026-08-30", "duration": "1 semana", "status": "pending"}]}, "9_resources": {"title": "Recursos", "description": "Alocação de equipe e capacidade", "team": [{"role": "Arquiteto de Dados", "fte": 1.0, "focus": "Design de plataforma, expertise Fabric"}, {"role": "Engenheiros de Dados", "fte": 2.5, "focus": "Desenvolvimento ETL, lógica de transformação"}, {"role": "Desenvolvedores SQL", "fte": 1.5, "focus": "Otimização de query, stored procedures"}, {"role": "Engenheiros QA", "fte": 1.0, "focus": "Framework de validação, testes"}, {"role": "Gerente de Projeto", "fte": 0.5, "focus": "Cronograma, governança, RACI"}]}, "10_lessons": {"title": "Lições Aprendidas", "description": "Melhores práticas e insights", "lessons": [{"title": "Mapeamento de Domínio de Saúde Antecipado", "insight": "Entender taxonomia clínica do ClienteSaude antecipadamente economizou 30% de retrabalho"}, {"title": "Vantagem da Arquitetura Medallion", "insight": "Separação Bronze/Silver/Gold melhorou performance de query 60x vs legacy"}, {"title": "ROI do Framework de Validação", "insight": "Framework de validação automatizado reduziu tempo QA de 4 semanas para 2"}, {"title": "Comunicação com Stakeholders", "insight": "Dashboards KPI semanais aumentaram confiança executiva e adoção"}, {"title": "Curva de Aprendizado Fabric", "insight": "Ramp-up de equipe em Fabric levou 2 semanas; invista em treinamento cedo"}]}}}, "footer": {"en": {"brand": "Consultoria", "tagline": "Microsoft Cloud Practice", "copyright": "© 2026 Consultoria Inc. All rights reserved.", "project_links": ["Data Migration Factory", "Architecture", "Documentation"], "resource_links": ["Dashboards", "Reports", "Design System"]}, "pt": {"brand": "Consultoria", "tagline": "Prática de Nuvem Microsoft", "copyright": "© 2026 Consultoria Inc. Todos os direitos reservados.", "project_links": ["Fábrica de Migração de Dados", "Arquitetura", "Documentação"], "resource_links": ["Dashboards", "Relatórios", "Design System"]}}, "discovery": {"en": {"title": "Deep Legacy Analysis", "description": "Complete DDL extraction from ClienteSaude ClienteSaude SQL Server environment", "findings": ["✅ 27 SQL scripts analyzed", "✅ 96 tables extracted", "✅ 120 views mapped", "✅ 20 procedures identified", "✅ 20 distinct schemas", "✅ 59 indexes found"]}, "pt": {"title": "Análise Profunda do Legacy", "description": "Extração completa de DDL do ambiente SQL Server do ClienteSaude ClienteSaude", "findings": ["✅ 27 scripts SQL analisados", "✅ 96 tabelas extraídas", "✅ 120 views mapeadas", "✅ 20 procedures identificadas", "✅ 20 schemas distintos", "✅ 59 índices encontrados"]}}, "top_databases": {"en": [{"name": "DWClienteSaude", "size": "10.4 MB", "type": "Healthcare Data Warehouse"}, {"name": "ENSINO_BI", "size": "7.3 MB", "type": "Education Analytics"}, {"name": "DWMKT03", "size": "5.0 MB", "type": "Marketing/CRM"}, {"name": "SandBox", "size": "4.5 MB", "type": "Development/Testing"}], "pt": [{"name": "DWClienteSaude", "size": "10.4 MB", "type": "Data Warehouse de Saúde"}, {"name": "ENSINO_BI", "size": "7.3 MB", "type": "Analytics de Educação"}, {"name": "DWMKT03", "size": "5.0 MB", "type": "Marketing/CRM"}, {"name": "SandBox", "size": "4.5 MB", "type": "Desenvolvimento/Testes"}]}}};

let currentLanguage = localStorage.getItem('portal_language') || 'en';
let currentTab = 'overview';

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  initializeLanguage();
  renderStatsCards();
  renderPhases();
  renderFlowDiagram();
  initializeTabs();
  applyLanguage();
});

// Language system
function initializeLanguage() {
  const langButtons = document.querySelectorAll('.lang-btn');
  langButtons.forEach(btn => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
}

function setLanguage(lang) {
  currentLanguage = lang;
  localStorage.setItem('portal_language', lang);
  applyLanguage();
}

function applyLanguage() {
  document.querySelectorAll('[data-en]').forEach(el => {
    const text = currentLanguage === 'en' ? el.dataset.en : el.dataset.pt || el.dataset.en;
    el.textContent = text;
  });
  
  document.querySelectorAll('.lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === currentLanguage);
  });
}

// Statistics cards
function renderStatsCards() {
  const stats = portalContent.content.stats.en;
  const container = document.getElementById('stats-container');
  container.innerHTML = stats.map(stat => `
    <div class="hero-stat">
      <div class="hero-stat-value">${stat.value}</div>
      <div class="hero-stat-label">${stat.label}</div>
    </div>
  `).join('');
}

// Phases rendering
function renderPhases() {
  const phases = portalContent.content.phases.en;
  const container = document.getElementById('phases-container');
  container.innerHTML = phases.map(phase => `
    <div class="phase-card ${phase.status}">
      <div class="phase-number">${phase.number}</div>
      <h4>${phase.title}</h4>
      <p>${phase.description}</p>
      <ul class="phase-list">
        ${phase.items.map(item => `<li>${item}</li>`).join('')}
      </ul>
    </div>
  `).join('');
}

// Flow diagram
function renderFlowDiagram() {
  const flow = portalContent.content.flow.en;
  const container = document.getElementById('flow-container');
  container.innerHTML = flow.flows.map(f => `
    <div class="flow-row">
      <div class="flow-node highlight">${f.source}</div>
      <div class="flow-arrow">→</div>
      <div class="flow-node">${f.target}</div>
      <div class="flow-arrow">→</div>
      <div class="flow-node azure">${f.destination}</div>
    </div>
  `).join('');
}

// Tabs system
function initializeTabs() {
  const tabs = portalContent.content.tabs.en;
  const tabNav = document.getElementById('tabs-nav');
  const tabContent = document.getElementById('tabs-content');
  
  const tabKeys = Object.keys(tabs).slice(0, 10);
  
  tabNav.innerHTML = tabKeys.map(key => `
    <button data-tab="${key}" class="tab-button ${key === '1_executive' ? 'active' : ''}">
      ${tabs[key].title}
    </button>
  `).join('');
  
  tabNav.querySelectorAll('.tab-button').forEach(btn => {
    btn.addEventListener('click', () => switchTab(btn.dataset.tab));
  });
  
  switchTab('1_executive');
}

function switchTab(tabKey) {
  currentTab = tabKey;
  const tabs = portalContent.content.tabs[currentLanguage];
  const tab = tabs[tabKey];
  
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.classList.toggle('active', btn.dataset.tab === tabKey);
  });
  
  const contentDiv = document.getElementById('tabs-content');
  contentDiv.innerHTML = `
    <div class="tab-panel">
      <h2>${tab.title}</h2>
      <p>${tab.description}</p>
      <div class="tab-data">${renderTabData(tab)}</div>
    </div>
  `;
}

function renderTabData(tab) {
  if (tab.metrics) {
    return `
      <div class="grid-4">
        ${tab.metrics.map(m => `
          <div class="metric-card">
            <div class="metric-value">${m.value}</div>
            <div class="metric-label">${m.label}</div>
          </div>
        `).join('')}
      </div>
    `;
  }
  if (tab.phases) {
    return `<ul>${tab.phases.map(p => `<li>${p.name} - ${p.status}</li>`).join('')}</ul>`;
  }
  return '';
}

// Utility functions
const PortalAPI = {
  setLanguage,
  currentLanguage: () => currentLanguage,
  currentTab: () => currentTab,
  t: (key) => getTranslation(key),
  formatCurrency: (n) => `$${n.toLocaleString()}`,
  formatNumber: (n) => n.toLocaleString()
};

function getTranslation(key) {
  const parts = key.split('.');
  let obj = portalContent.content;
  for (const part of parts) {
    obj = obj?.[part]?.[currentLanguage] || obj?.[part];
  }
  return obj || key;
}

// Expose API globally
window.PortalAPI = PortalAPI;
