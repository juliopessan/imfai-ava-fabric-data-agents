/**
 * Orange DNA + Consultoria Hybrid Components
 * Reference implementation for React components using DESIGN-TOKENS.css
 * 
 * Components:
 * - Sidebar Navigation (248px fixed)
 * - Top Bar (56px fixed)
 * - Status Badge (4-color palette)
 * - KPI Card (with peach highlight on hover)
 */

import React, { useState } from 'react';

// Design Tokens (from DESIGN-TOKENS.css)
const COLORS = {
  primary_orange: '#ff6b35',
  secondary_blue: '#1f3a93',
  peach_highlight: '#FFE6D3',
  yellow_warning: '#FFB414',
  white: '#ffffff',
  light_bg: '#f9f9f9',
  border: '#e0e0e0',
  text_primary: '#333333',
};

const SPACING = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px',
  '2xl': '48px',
};

// ============================================================================
// COMPONENT 1: Sidebar Navigation
// ============================================================================
interface SidebarNavItem {
  icon: string;
  label: string;
  active?: boolean;
}

interface SidebarProps {
  items: SidebarNavItem[];
  onItemClick?: (label: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ items, onItemClick }) => {
  return (
    <nav
      style={{
        position: 'fixed',
        left: 0,
        top: '56px',
        width: '248px',
        height: 'calc(100vh - 56px)',
        background: COLORS.white,
        borderRight: `1px solid ${COLORS.border}`,
        padding: `${SPACING.lg} 0`,
        overflowY: 'auto',
        zIndex: 999,
      }}
    >
      <ul style={{ listStyle: 'none', margin: 0, padding: 0 }}>
        {items.map((item) => (
          <li
            key={item.label}
            onClick={() => onItemClick?.(item.label)}
            style={{
              padding: `${SPACING.md} ${SPACING.lg}`,
              color: item.active ? COLORS.primary_orange : COLORS.text_primary,
              cursor: 'pointer',
              borderLeft: `3px solid ${item.active ? COLORS.primary_orange : 'transparent'}`,
              background: item.active ? COLORS.peach_highlight : 'transparent',
              fontWeight: item.active ? 600 : 400,
              transition: 'all 0.2s ease',
              fontSize: '0.95em',
            }}
            onMouseEnter={(e) => {
              if (!item.active) {
                e.currentTarget.style.background = COLORS.light_bg;
              }
            }}
            onMouseLeave={(e) => {
              if (!item.active) {
                e.currentTarget.style.background = 'transparent';
              }
            }}
          >
            {item.icon} {item.label}
          </li>
        ))}
      </ul>
    </nav>
  );
};

// ============================================================================
// COMPONENT 2: Top Bar
// ============================================================================
interface TopBarProps {
  logo?: string;
  onSearch?: (query: string) => void;
  userInitials?: string;
}

export const TopBar: React.FC<TopBarProps> = ({
  logo = '📊 Dashboard',
  onSearch,
  userInitials = 'RC',
}) => {
  const [searchInput, setSearchInput] = useState('');

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        height: '56px',
        background: COLORS.white,
        borderBottom: `1px solid ${COLORS.border}`,
        zIndex: 1000,
        display: 'flex',
        alignItems: 'center',
        padding: `0 ${SPACING.lg}`,
        gap: SPACING.md,
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
      }}
    >
      <div
        style={{
          fontWeight: 700,
          fontSize: '1.2em',
          color: COLORS.primary_orange,
          textDecoration: 'none',
          minWidth: '200px',
        }}
      >
        {logo}
      </div>

      <input
        type="text"
        placeholder="🔍 Buscar..."
        value={searchInput}
        onChange={(e) => {
          setSearchInput(e.target.value);
          onSearch?.(e.target.value);
        }}
        style={{
          flex: 1,
          maxWidth: '400px',
          padding: `${SPACING.sm} ${SPACING.md}`,
          border: `1px solid ${COLORS.border}`,
          borderRadius: '8px',
          fontFamily: 'inherit',
          fontSize: '0.95em',
        }}
      />

      <div
        style={{
          display: 'flex',
          gap: SPACING.md,
          marginLeft: 'auto',
          alignItems: 'center',
        }}
      >
        <div
          style={{
            width: '40px',
            height: '40px',
            borderRadius: '50%',
            background: COLORS.primary_orange,
            color: COLORS.white,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontWeight: 600,
            fontSize: '0.9em',
          }}
        >
          {userInitials}
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// COMPONENT 3: Status Badge (4-color palette)
// ============================================================================
type StatusType = 'success' | 'warning' | 'error' | 'info';

interface StatusBadgeProps {
  status: StatusType;
  label: string;
  icon?: string;
}

const STATUS_COLORS: Record<StatusType, string> = {
  success: '#22c55e', // green
  warning: COLORS.yellow_warning,
  error: '#ef4444', // red
  info: COLORS.secondary_blue,
};

export const StatusBadge: React.FC<StatusBadgeProps> = ({
  status,
  label,
  icon = '',
}) => {
  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: SPACING.sm,
        padding: `${SPACING.sm} ${SPACING.md}`,
        borderRadius: '20px',
        backgroundColor: `${STATUS_COLORS[status]}20`, // 20% opacity
        color: STATUS_COLORS[status],
        fontWeight: 600,
        fontSize: '0.9em',
        border: `1px solid ${STATUS_COLORS[status]}`,
      }}
    >
      {icon && <span>{icon}</span>}
      <span>{label}</span>
    </span>
  );
};

// ============================================================================
// COMPONENT 4: KPI Card (with Orange DNA peach highlight)
// ============================================================================
interface KPICardProps {
  value: string | number;
  label: string;
  sublabel?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
}

export const KPICard: React.FC<KPICardProps> = ({
  value,
  label,
  sublabel,
  trend = 'neutral',
  trendValue,
}) => {
  const [isHovered, setIsHovered] = useState(false);

  const trendIcons = {
    up: '📈',
    down: '📉',
    neutral: '→',
  };

  return (
    <div
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      style={{
        background: COLORS.white,
        border: `1px solid ${COLORS.border}`,
        borderRadius: '8px',
        padding: SPACING.lg,
        textAlign: 'center',
        transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
        boxShadow: isHovered
          ? '0 12px 32px rgba(0, 0, 0, 0.15)'
          : '0 2px 8px rgba(0, 0, 0, 0.08)',
        backgroundColor: isHovered ? COLORS.peach_highlight : COLORS.white,
        cursor: 'pointer',
        transform: isHovered ? 'translateY(-4px)' : 'none',
      }}
    >
      <div
        style={{
          fontSize: '2.2em',
          fontWeight: 700,
          color: COLORS.primary_orange,
          marginBottom: SPACING.sm,
        }}
      >
        {value}
      </div>
      <div
        style={{
          fontSize: '0.95em',
          fontWeight: 600,
          color: COLORS.text_primary,
          marginBottom: SPACING.xs,
        }}
      >
        {label}
      </div>
      {sublabel && (
        <div
          style={{
            fontSize: '0.85em',
            color: COLORS.text_primary,
            opacity: 0.7,
          }}
        >
          {sublabel}
        </div>
      )}
      {trendValue && (
        <div
          style={{
            fontSize: '0.85em',
            marginTop: SPACING.md,
            color: STATUS_COLORS[trend === 'up' ? 'success' : trend === 'down' ? 'error' : 'info'],
          }}
        >
          {trendIcons[trend]} {trendValue}
        </div>
      )}
    </div>
  );
};

// ============================================================================
// EXAMPLE USAGE / DEMO
// ============================================================================
export const OrangeDNAComponentsDemo: React.FC = () => {
  const sidebarItems = [
    { icon: '📊', label: 'Dashboard', active: true },
    { icon: '📈', label: 'Analytics' },
    { icon: '👥', label: 'Team' },
    { icon: '⚙️', label: 'Settings' },
  ];

  return (
    <div style={{ background: COLORS.light_bg, minHeight: '100vh' }}>
      <TopBar userInitials="RC" />
      <Sidebar items={sidebarItems} />

      <div
        style={{
          marginLeft: '248px',
          marginTop: '56px',
          padding: SPACING.lg,
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
          gap: SPACING.lg,
        }}
      >
        <KPICard value={24} label="Projetos Ativos" sublabel="Multi-domain specialists" trend="up" trendValue="+12%" />
        <KPICard value="$2.5M" label="Faturamento" sublabel="YTD" trend="up" trendValue="+8%" />
        <KPICard value="92%" label="Taxa de Sucesso" sublabel="Execuções" trend="neutral" trendValue="0%" />
        <KPICard value="15" label="Equipe" sublabel="Engenheiros" trend="down" trendValue="-2" />
      </div>

      <div
        style={{
          marginLeft: '248px',
          marginTop: '56px',
          padding: SPACING.lg,
          display: 'flex',
          gap: SPACING.md,
          flexWrap: 'wrap',
        }}
      >
        <StatusBadge status="success" label="Ativo" icon="🟢" />
        <StatusBadge status="warning" label="Atenção" icon="🟡" />
        <StatusBadge status="error" label="Bloqueado" icon="🔴" />
        <StatusBadge status="info" label="Informação" icon="ℹ️" />
      </div>
    </div>
  );
};
