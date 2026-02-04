const path = require('node:path');
const { isoNow } = require('../lib/markdown');
const { ensureDir, listFiles, listDirs, fileExists, writeFileAtomic } = require('../lib/fsutil');

const UPSTREAM_FILES = [
  'problem-statement.md',
  'kpis.md',
  'analytical-questions.md',
  'sttm.md',
  'dq-initial.md',
];

const MIDSTREAM_FILES = ['architecture.md', 'data-model.md', 'agent-blueprint.md', 'agent-execution-contracts.md'];

const GOVERNANCE_FILES = ['dq-rules.md', 'monitoring-spec.md'];

function decideStream(presentSet) {
  const hasUpstream = UPSTREAM_FILES.every((f) => presentSet.has(f));
  const hasMidstream = MIDSTREAM_FILES.every((f) => presentSet.has(f));

  if (!hasUpstream) return { stream: 'UPSTREAM', evidence: UPSTREAM_FILES.filter((f) => presentSet.has(f)) };
  if (!hasMidstream) return { stream: 'MIDSTREAM', evidence: MIDSTREAM_FILES.filter((f) => presentSet.has(f)) };
  return { stream: 'DOWNSTREAM', evidence: [...UPSTREAM_FILES, ...MIDSTREAM_FILES].filter((f) => presentSet.has(f)) };
}

async function runWorkflowStatus(ctx) {
  const statusPath = path.join(ctx.paths.planning, 'status.md');

  await ensureDir(ctx.paths.planning);
  await ensureDir(ctx.paths.implementation);
  await ensureDir(ctx.paths.logs);

  const planningFiles = await listFiles(ctx.paths.planning);
  const implFiles = await listFiles(ctx.paths.implementation);
  const implDirs = await listDirs(ctx.paths.implementation);
  const logFiles = await listFiles(ctx.paths.logs);

  const presentPlanning = new Set(planningFiles);
  const { stream, evidence } = decideStream(presentPlanning);

  const gates = {
    gate1: UPSTREAM_FILES,
    gate2: [...MIDSTREAM_FILES, ...GOVERNANCE_FILES],
    gate3: ['sql/', 'pyspark/', 'tests/', 'README.md', 'gate-3-report.md'],
  };

  const gate1 = gates.gate1.map((f) => ({
    item: f,
    ok: presentPlanning.has(f),
    kind: 'planning',
  }));

  const gate2 = gates.gate2.map((f) => ({
    item: f,
    ok: presentPlanning.has(f),
    kind: 'planning',
  }));

  const implSetFiles = new Set(implFiles);
  const implSetDirs = new Set(implDirs.map((d) => `${d}/`));

  const gate3 = gates.gate3.map((f) => {
    const ok = f.endsWith('/') ? implSetDirs.has(f) : implSetFiles.has(f);
    return { item: f, ok, kind: 'implementation' };
  });

  // Next suggestion
  const gate1Ok = gate1.every((x) => x.ok);
  const gate2Ok = gate2.every((x) => x.ok);
  const gate3Ok = gate3.some((x) => x.ok); // gate3 is more subjective; treat as "some evidence"

  let next;
  if (!gate1Ok) {
    next = {
      agent: 'data-strategist / business-analyst',
      workflow: 'data-strategy / business-analysis',
      reason: 'Gate 1 pendente (artefatos UPSTREAM incompletos)',
    };
  } else if (!gate2Ok) {
    next = {
      agent: 'data-solution-architect / data-modeler / agent-designer',
      workflow: 'architecture / data-model / agent-blueprint + agent-contracts',
      reason: 'Gate 2 pendente (artefatos MIDSTREAM/Governance incompletos)',
    };
  } else if (!gate3Ok) {
    next = {
      agent: 'data-engineer-exec',
      workflow: 'delivery + unit-tests',
      reason: 'Sem evidência suficiente de outputs DOWNSTREAM (sql/pyspark/tests)',
    };
  } else {
    next = {
      agent: 'orchestrator',
      workflow: 'gate-3-down-prod + governance',
      reason: 'Há evidência de outputs; seguir para validação final e governança',
    };
  }

  const lines = [];
  lines.push(`# Project Status — ${ctx.projectCode}`);
  lines.push('');
  lines.push(`Generated: ${isoNow()}`);
  lines.push('');

  lines.push('## Artefatos encontrados');
  lines.push('');
  lines.push('### planning-artifacts');
  lines.push(...planningFiles.map((f) => `- ${f}`));
  if (planningFiles.length === 0) lines.push('- (none)');
  lines.push('');

  lines.push('### implementation-artifacts');
  if (implDirs.length) lines.push(...implDirs.map((d) => `- ${d}/`));
  if (implFiles.length) lines.push(...implFiles.map((f) => `- ${f}`));
  if (implDirs.length === 0 && implFiles.length === 0) lines.push('- (none)');
  lines.push('');

  lines.push('### logs');
  lines.push(...logFiles.map((f) => `- ${f}`));
  if (logFiles.length === 0) lines.push('- (none)');
  lines.push('');

  lines.push('## Estado atual');
  lines.push(`- Stream: **${stream}**`);
  lines.push(`- Evidências: ${evidence.length ? evidence.map((e) => `\`${e}\``).join(', ') : '(nenhuma)'}`);
  lines.push('');

  function renderGate(title, items) {
    lines.push(`### ${title}`);
    for (const it of items) {
      lines.push(`${it.ok ? '✅' : '⏳'} ${it.kind === 'planning' ? 'planning' : 'impl'}: ${it.item}`);
    }
    lines.push('');
  }

  lines.push('## Gates');
  lines.push('');
  renderGate('Gate 1 (UP→MID)', gate1);
  renderGate('Gate 2 (MID→DOWN)', gate2);
  renderGate('Gate 3 (DOWN→PROD)', gate3);

  lines.push('## Próximo passo sugerido');
  lines.push('');
  lines.push(`- Principal: **${next.workflow}** (agente: **${next.agent}**)`);
  lines.push(`- Motivo: ${next.reason}`);
  lines.push('');

  lines.push('## Histórico');
  lines.push(`- ${isoNow()} — stream=${stream} — sugestão=${next.workflow}`);
  lines.push('');

  await writeFileAtomic(statusPath, lines.join('\n'));

  return {
    ok: true,
    output: statusPath,
    stream,
    next,
  };
}

module.exports = { runWorkflowStatus };
