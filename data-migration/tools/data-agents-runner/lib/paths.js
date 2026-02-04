const path = require('node:path');

function resolveProjectRoot(projectRootArg) {
  return projectRootArg ? path.resolve(projectRootArg) : path.resolve(__dirname, '..', '..', '..');
}

function resolveArtifactsRoot(projectRoot, artifactsRootArg) {
  if (!artifactsRootArg) return path.join(projectRoot, '_bmad-output');
  // Support {project-root}/ prefix convention used by installer runner
  const normalized = artifactsRootArg.replace('{project-root}/', '');
  return path.isAbsolute(normalized) ? normalized : path.join(projectRoot, normalized);
}

function getProjectPaths({ projectRoot, artifactsRoot, projectCode }) {
  const projectArtifactsRoot = path.join(artifactsRoot, projectCode);
  return {
    projectRoot,
    artifactsRoot,
    projectCode,
    projectArtifactsRoot,
    planning: path.join(projectArtifactsRoot, 'planning-artifacts'),
    implementation: path.join(projectArtifactsRoot, 'implementation-artifacts'),
    logs: path.join(projectArtifactsRoot, 'logs'),
  };
}

module.exports = {
  resolveProjectRoot,
  resolveArtifactsRoot,
  getProjectPaths,
};
