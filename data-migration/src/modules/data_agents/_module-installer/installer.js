const fs = require('node:fs/promises');
const path = require('node:path');

async function ensureDir(dirPath) {
  await fs.mkdir(dirPath, { recursive: true });
}

/**
 * Data & Agentic AI — BMAD-Data Module Installer
 *
 * Creates a minimal folder structure for generated artifacts based on module config.
 *
 * Expected config variables (from module.yaml):
 * - artifacts_root
 * - project_code
 */
async function install(options) {
  const { projectRoot, config, logger } = options;

  const log = logger?.log ? logger : console;

  try {
    log.log('Installing Data & Agentic AI — BMAD-Data...');

    const artifactsRoot = (config?.artifacts_root || '{output_folder}').toString();
    const projectCode = (config?.project_code || 'trip-data-poc').toString();

    // If user passed {project-root}/..., normalize to a path under the project
    const normalizedArtifactsRoot = artifactsRoot.replace('{project-root}/', '');

    // If user passed an absolute path, keep it. Otherwise, resolve relative to projectRoot.
    const basePath = path.isAbsolute(normalizedArtifactsRoot)
      ? normalizedArtifactsRoot
      : path.join(projectRoot, normalizedArtifactsRoot);

    const target = path.join(basePath, projectCode);

    const folders = [
      target,
      path.join(target, 'planning-artifacts'),
      path.join(target, 'implementation-artifacts'),
      path.join(target, 'logs'),
    ];

    for (const folder of folders) {
      await ensureDir(folder);
      log.log(`Ensured directory: ${path.relative(projectRoot, folder) || folder}`);
    }

    log.log('✓ Data & Agentic AI — BMAD-Data installation complete');
    return true;
  } catch (error) {
    log.error(`Error installing module: ${error?.message || error}`);
    return false;
  }
}

module.exports = { install };
