/**
 * ═══════════════════════════════════════════════════════════════════════════
 * CONSULTORIA KPI PORTAL — INTERACTION LOGIC
 * ═══════════════════════════════════════════════════════════════════════════
 */

// Global state
let currentLanguage = 'en';
let currentTab = '1_executive';
let portalContent = null;

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * INITIALIZATION
 * ═══════════════════════════════════════════════════════════════════════════
 */

document.addEventListener('DOMContentLoaded', async () => {
  console.log('🚀 Initializing Consultoria KPI Portal...');

  // Load content
  await loadPortalContent();

  // Initialize UI
  initializeLanguage();
  initializeTabs();
  initializeInteractions();

  console.log('✅ Portal initialized successfully');
});

/**
 * LOAD PORTAL CONTENT FROM JSON
 */
async function loadPortalContent() {
  try {
    const response = await fetch('./PORTAL_CONTENT.json');
    portalContent = await response.json();
    console.log('✅ Content loaded:', portalContent);
  } catch (error) {
    console.error('❌ Failed to load portal content:', error);
    // Fallback to English
    currentLanguage = 'en';
  }
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * LANGUAGE MANAGEMENT (i18n)
 * ═══════════════════════════════════════════════════════════════════════════
 */

function initializeLanguage() {
  // Set initial language from localStorage or default to 'en'
  currentLanguage = localStorage.getItem('portal_language') || 'en';

  // Update UI
  updateLanguageUI();
  applyLanguage();
}

function setLanguage(lang) {
  if (lang !== currentLanguage) {
    currentLanguage = lang;
    localStorage.setItem('portal_language', lang);
    updateLanguageUI();
    applyLanguage();
  }
}

function updateLanguageUI() {
  const langButtons = document.querySelectorAll('.lang-btn');
  langButtons.forEach(btn => {
    btn.classList.toggle('active', btn.dataset.lang === currentLanguage);
  });
}

function applyLanguage() {
  // Update all data-en / data-pt elements
  document.querySelectorAll('[data-en][data-pt]').forEach(el => {
    const content =
      currentLanguage === 'en'
        ? el.dataset.en
        : currentLanguage === 'pt'
          ? el.dataset.pt
          : el.dataset.en;
    el.textContent = content;
  });

  // Update innerHTML elements with translations
  applyDynamicTranslations();
}

function applyDynamicTranslations() {
  if (!portalContent) return;

  // Update header
  const headerBrand = document.querySelector('.header-brand');
  if (headerBrand) {
    const brandText = portalContent.content.header[currentLanguage].brand;
    if (headerBrand.textContent.includes('ClienteBanco')) {
      headerBrand.textContent = brandText;
    }
  }

  // Update hero section
  updateHeroTranslations();

  // Update tabs navigation
  updateTabsNavigation();
}

function updateHeroTranslations() {
  const hero = portalContent.content.hero[currentLanguage];

  const eyebrow = document.querySelector('.hero-eyebrow');
  if (eyebrow) eyebrow.textContent = hero.eyebrow;

  const title = document.querySelector('.hero-title');
  if (title) title.textContent = hero.title;

  const subtitle = document.querySelector('.hero-subtitle');
  if (subtitle) subtitle.textContent = hero.subtitle;

  const description = document.querySelector('.hero-description');
  if (description) description.textContent = hero.description;
}

function updateTabsNavigation() {
  const navItems = document.querySelectorAll('.tabs-nav-item');
  const tabs = portalContent.content.navigation[currentLanguage];

  navItems.forEach((item, index) => {
    if (tabs[index]) {
      item.textContent = tabs[index];
    }
  });
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * TABS MANAGEMENT
 * ═══════════════════════════════════════════════════════════════════════════
 */

function initializeTabs() {
  const tabItems = document.querySelectorAll('.tabs-nav-item');
  tabItems.forEach((item, index) => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const tabKey = ['1_executive', '2_migration', '3_quality', '4_performance', '5_cost', '6_architecture', '7_risk', '8_timeline', '9_resources', '10_lessons'][index];
      switchTab(tabKey);
    });
  });

  // Initialize first tab
  switchTab('1_executive');
}

function switchTab(tabKey) {
  currentTab = tabKey;

  // Update nav items
  const navItems = document.querySelectorAll('.tabs-nav-item');
  const tabs = Object.keys(portalContent.content.tabs);
  const tabIndex = tabs.indexOf(tabKey);

  navItems.forEach((item, index) => {
    item.classList.toggle('active', index === tabIndex);
  });

  // Update content
  const contents = document.querySelectorAll('.tabs-content');
  contents.forEach((content, index) => {
    content.classList.toggle('active', index === tabIndex);
  });

  // Render tab content
  renderTabContent(tabKey);
}

function renderTabContent(tabKey) {
  if (!portalContent) return;

  const tabData = portalContent.content.tabs[tabKey];
  if (!tabData) return;

  const tabContent = document.querySelector('.tabs-content.active');
  if (!tabContent) return;

  // Clear existing content
  tabContent.innerHTML = '';

  const langData = tabData[currentLanguage];

  // Add title and description
  const header = document.createElement('div');
  header.className = 'section-header';
  header.innerHTML = `
    <div class="eyebrow">${langData.title}</div>
    <h2>${langData.title}</h2>
    <p>${langData.description}</p>
  `;
  tabContent.appendChild(header);

  // Add metrics/content based on tab type
  if (langData.metrics) {
    const metricsGrid = document.createElement('div');
    metricsGrid.className = 'grid grid-4';
    langData.metrics.forEach(metric => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <div class="stat">
          <div class="stat-value">${metric.value}</div>
          <div class="stat-label">${metric.label}</div>
          ${metric.change ? `<div class="stat-change ${metric.trend}">${metric.change}</div>` : ''}
        </div>
      `;
      metricsGrid.appendChild(card);
    });
    tabContent.appendChild(metricsGrid);
  }

  // Add improvements table for performance tab
  if (langData.improvements) {
    const table = document.createElement('table');
    table.innerHTML = `
      <tr>
        <th>${currentLanguage === 'en' ? 'Query' : 'Consulta'}</th>
        <th>${currentLanguage === 'en' ? 'Before' : 'Antes'}</th>
        <th>${currentLanguage === 'en' ? 'After' : 'Depois'}</th>
        <th>${currentLanguage === 'en' ? 'Improvement' : 'Melhoria'}</th>
      </tr>
      ${langData.improvements
        .map(
          imp => `
        <tr>
          <td>${imp.query}</td>
          <td>${imp.before}</td>
          <td>${imp.after}</td>
          <td class="text-bold" style="color: var(--ava-success);">${imp.gain}</td>
        </tr>
      `
        )
        .join('')}
    `;
    tabContent.appendChild(table);
  }

  // Add cost summary
  if (langData.summary) {
    const summaryGrid = document.createElement('div');
    summaryGrid.className = 'grid grid-3 mt-lg';
    Object.entries(langData.summary).forEach(([key, value]) => {
      const card = document.createElement('div');
      card.className = 'card';
      const label =
        key === 'investment'
          ? currentLanguage === 'en'
            ? 'Total Investment'
            : 'Investimento Total'
          : key === 'monthly_savings'
            ? currentLanguage === 'en'
              ? 'Monthly Savings'
              : 'Economia Mensal'
            : key === 'annual_savings'
              ? currentLanguage === 'en'
                ? 'Annual Savings'
                : 'Economia Anual'
              : key === 'payback'
                ? currentLanguage === 'en'
                  ? 'Payback Period'
                  : 'Período de Retorno'
                : '3-Year NPV';
      card.innerHTML = `
        <h4>${label}</h4>
        <div class="stat-value">${value}</div>
      `;
      summaryGrid.appendChild(card);
    });
    tabContent.appendChild(summaryGrid);
  }

  // Add components table for architecture tab
  if (langData.components) {
    const table = document.createElement('table');
    table.innerHTML = `
      <tr>
        <th>${currentLanguage === 'en' ? 'Layer' : 'Camada'}</th>
        <th>${currentLanguage === 'en' ? 'Systems' : 'Sistemas'}</th>
        <th>${currentLanguage === 'en' ? 'Volume' : 'Volume'}</th>
      </tr>
      ${langData.components
        .map(
          comp => `
        <tr>
          <td><strong>${comp.layer}</strong></td>
          <td>${comp.systems.join(', ')}</td>
          <td>${comp.volume}</td>
        </tr>
      `
        )
        .join('')}
    `;
    tabContent.appendChild(table);
  }

  // Add risks table
  if (langData.risks) {
    const table = document.createElement('table');
    table.innerHTML = `
      <tr>
        <th>${currentLanguage === 'en' ? 'Risk' : 'Risco'}</th>
        <th>${currentLanguage === 'en' ? 'Impact' : 'Impacto'}</th>
        <th>${currentLanguage === 'en' ? 'Probability' : 'Probabilidade'}</th>
        <th>${currentLanguage === 'en' ? 'Mitigation' : 'Mitigação'}</th>
      </tr>
      ${langData.risks
        .map(
          risk => `
        <tr>
          <td><strong>${risk.risk}</strong></td>
          <td>${risk.impact}</td>
          <td>${risk.probability}</td>
          <td>${risk.mitigation}</td>
        </tr>
      `
        )
        .join('')}
    `;
    tabContent.appendChild(table);
  }

  // Add schedule/timeline
  if (langData.schedule) {
    const steps = document.createElement('ol');
    steps.className = 'steps';
    langData.schedule.forEach((item, index) => {
      const li = document.createElement('li');
      li.className = 'steps-item';
      li.innerHTML = `
        <div class="steps-number">${index + 1}</div>
        <div class="steps-content">
          <h4>${item.phase}</h4>
          <div class="steps-date">${item.date} • ${item.duration}</div>
        </div>
      `;
      steps.appendChild(li);
    });
    tabContent.appendChild(steps);
  }

  // Add team table
  if (langData.team) {
    const table = document.createElement('table');
    table.innerHTML = `
      <tr>
        <th>${currentLanguage === 'en' ? 'Role' : 'Papel'}</th>
        <th>${currentLanguage === 'en' ? 'FTE' : 'FTE'}</th>
        <th>${currentLanguage === 'en' ? 'Focus' : 'Foco'}</th>
      </tr>
      ${langData.team
        .map(
          member => `
        <tr>
          <td><strong>${member.role}</strong></td>
          <td>${member.fte}</td>
          <td>${member.focus}</td>
        </tr>
      `
        )
        .join('')}
    `;
    tabContent.appendChild(table);
  }

  // Add lessons learned
  if (langData.lessons) {
    const lessonsDiv = document.createElement('div');
    lessonsDiv.className = 'grid grid-2 gap-lg';
    langData.lessons.forEach(lesson => {
      const card = document.createElement('div');
      card.className = 'card';
      card.innerHTML = `
        <h4>${lesson.title}</h4>
        <p>${lesson.insight}</p>
      `;
      lessonsDiv.appendChild(card);
    });
    tabContent.appendChild(lessonsDiv);
  }
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * INTERACTIONS
 * ═══════════════════════════════════════════════════════════════════════════
 */

function initializeInteractions() {
  // Language switch
  const langButtons = document.querySelectorAll('.lang-btn');
  langButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      setLanguage(btn.dataset.lang);
    });
  });

  // Smooth scroll
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Add animation to cards on scroll
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  });

  document.querySelectorAll('.card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'all var(--ava-transition-normal)';
    observer.observe(card);
  });
}

/**
 * ═══════════════════════════════════════════════════════════════════════════
 * UTILITY FUNCTIONS
 * ═══════════════════════════════════════════════════════════════════════════
 */

/**
 * Format a number as currency
 */
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: 0,
  }).format(value);
}

/**
 * Format a number with thousands separator
 */
function formatNumber(value) {
  return new Intl.NumberFormat('en-US').format(value);
}

/**
 * Get translation for a key
 */
function t(key) {
  if (!portalContent) return key;

  const keys = key.split('.');
  let value = portalContent.content;

  for (const k of keys) {
    value = value[k];
    if (!value) return key;
  }

  return typeof value === 'object' ? value[currentLanguage] || value.en : value;
}

/**
 * Log portal analytics (placeholder)
 */
function logAnalytics(event, data) {
  console.log(`📊 Analytics: ${event}`, data);
  // In production, send to analytics service
}

// Export for console access
window.PortalAPI = {
  setLanguage,
  switchTab,
  currentLanguage: () => currentLanguage,
  currentTab: () => currentTab,
  t,
  formatCurrency,
  formatNumber,
  logAnalytics,
};

console.log('✅ PortalAPI available. Usage: PortalAPI.setLanguage("pt"), PortalAPI.switchTab("2_migration")');
