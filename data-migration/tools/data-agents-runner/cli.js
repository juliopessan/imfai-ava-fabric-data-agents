#!/usr/bin/env node

const path = require('node:path');

const { resolveProjectRoot, resolveArtifactsRoot, getProjectPaths } = require('./lib/paths');
const { install } = require('../../src/modules/data_agents/_module-installer/installer');
const { runWorkflowStatus } = require('./workflows/workflowStatus');
const { validateGate1, validateGate2, validateGate3 } = require('./workflows/gates');

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--project-root') args.projectRoot = argv[++i];
    else if (a === '--artifacts-root') args.artifactsRoot = argv[++i];
    else if (a === '--project-code') args.projectCode = argv[++i];
    else args._.push(a);
  }
  return args;
}

function printHelp() {
  console.log('data-agents-runner');
  console.log('');
  console.log('Usage:');
  console.log('  node tools\\data-agents-runner\\cli.js <command> [--project-code X] [--artifacts-root PATH]');
  console.log('');
  console.log('Commands:');
  console.log('  selftest          Run installer + workflow-status + gates on default project');
  console.log('  workflow-status   Generate planning-artifacts/status.md');
  console.log('  gate-1            Generate planning-artifacts/gate-1-report.md');
  console.log('  gate-2            Generate planning-artifacts/gate-2-report.md');
  console.log('  gate-3            Generate implementation-artifacts/gate-3-report.md');
  console.log('  orchestrate       Run workflow-status then suggest next workflow');
}

async function main() {
  const args = parseArgs(process.argv);
  const cmd = args._[0];
  if (!cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') {
    printHelp();
    process.exitCode = cmd ? 0 : 1;
    return;
  }

  const projectRoot = resolveProjectRoot(args.projectRoot);
  const projectCode = args.projectCode || 'trip-data-poc';
  const artifactsRoot = resolveArtifactsRoot(projectRoot, args.artifactsRoot);

  const ctx = {
    projectRoot,
    artifactsRoot,
    projectCode,
    paths: getProjectPaths({ projectRoot, artifactsRoot, projectCode }),
  };

  // Ensure folder structure exists using the module's installer logic
  await install({
    projectRoot,
    config: { artifacts_root: artifactsRoot, project_code: projectCode },
    logger: console,
  });

  if (cmd === 'workflow-status') {
    const res = await runWorkflowStatus(ctx);
    console.log(`OK: wrote ${path.relative(projectRoot, res.output)}`);
    return;
  }

  if (cmd === 'gate-1') {
    const res = await validateGate1(ctx);
    console.log(`${res.ok ? 'PASS' : 'FAIL'}: wrote ${path.relative(projectRoot, res.output)}`);
    return;
  }

  if (cmd === 'gate-2') {
    const res = await validateGate2(ctx);
    console.log(`${res.ok ? 'PASS' : 'FAIL'}: wrote ${path.relative(projectRoot, res.output)}`);
    return;
  }

  if (cmd === 'gate-3') {
    const res = await validateGate3(ctx);
    console.log(`${res.ok ? 'PASS' : 'FAIL'}: wrote ${path.relative(projectRoot, res.output)}`);
    return;
  }

  if (cmd === 'orchestrate') {
    const res = await runWorkflowStatus(ctx);
    console.log(`OK: wrote ${path.relative(projectRoot, res.output)}`);
    console.log(`Next: ${res.next.workflow} (agent: ${res.next.agent})`);
    console.log(`Reason: ${res.next.reason}`);
    return;
  }

  if (cmd === 'selftest') {
    const st = await runWorkflowStatus(ctx);
    const g1 = await validateGate1(ctx);
    const g2 = await validateGate2(ctx);
    const g3 = await validateGate3(ctx);

    console.log(`Status: wrote ${path.relative(projectRoot, st.output)}`);
    console.log(`Gate1: ${g1.ok ? 'PASS' : 'FAIL'} (${path.relative(projectRoot, g1.output)})`);
    console.log(`Gate2: ${g2.ok ? 'PASS' : 'FAIL'} (${path.relative(projectRoot, g2.output)})`);
    console.log(`Gate3: ${g3.ok ? 'PASS' : 'FAIL'} (${path.relative(projectRoot, g3.output)})`);
    return;
  }

  console.error(`Unknown command: ${cmd}`);
  printHelp();
  process.exitCode = 1;
}

main().catch((err) => {
  console.error(err);
  process.exitCode = 1;
});
