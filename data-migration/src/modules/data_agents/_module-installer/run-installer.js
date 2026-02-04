const path = require('node:path');
const { install } = require('./installer');

/**
 * Runner local (CLI) para testar o installer do módulo sem depender do runtime BMAD.
 *
 * Uso:
 *   node src\modules\data_agents\_module-installer\run-installer.js
 */

async function main() {
  const projectRoot = path.resolve(__dirname, '..', '..', '..', '..');

  const config = {
    artifacts_root: '{project-root}/_bmad-output',
    project_code: 'trip-data-poc',
  };

  const ok = await install({ projectRoot, config, logger: console });
  process.exitCode = ok ? 0 : 1;
}

main().catch((err) => {
  // eslint-disable-next-line no-console
  console.error('Installer runner failed:', err);
  process.exitCode = 1;
});
