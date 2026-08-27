#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
RUNTIME_DIR="$ROOT/integrations/pefy-extension-runtime"

command -v node >/dev/null 2>&1 || { echo "Node.js is required" >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is required" >&2; exit 1; }

node - <<'NODE'
const [major, minor] = process.versions.node.split('.').map(Number);
if (major < 22 || (major === 22 && minor < 13)) {
  console.error(`Node >=22.13.0 required; found ${process.versions.node}`);
  process.exit(1);
}
NODE

cd "$RUNTIME_DIR"

# Exact versions are declared in package.json. npm will create/update package-lock.json
# on the target host so the resolved transitive dependency graph becomes reproducible.
npm install --save-exact
npm run verify:deps
npm run verify:three

cat <<'EOF'
PEFY extension runtime dependencies are provisioned.

Security note:
- TrueForge local mode must remain localhost-only unless a hardened shared/hosted deployment is configured.
- Do not use blanket permission bypasses.
- Configure models, MCP servers, sandboxes and secrets outside committed source.
- Promote to production only after PEFY security, interoperability, performance and rollback gates pass.
EOF
