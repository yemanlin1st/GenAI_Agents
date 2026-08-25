# DeepSeek Harness Integration

This directory adds DeepSeek Harness as an optional skill/execution layer for the agent stack.

## What is included

- `SKILL.md` — activation rules, architecture, security policy, quality gates, and interoperability guidance.
- `install.sh` — isolated installer for the official `deepseek-harness-sdk` Python package.

## Intended role

DeepSeek Harness is an execution substrate, not a replacement for the existing orchestration, governance, security, or model-routing layers.

Use it when plugin-based tool composition, sandboxed coding, session replay/fork/resume, subagent scheduling, or trajectory analysis materially improves execution.

## Deployment policy

DeepSeek Harness is currently an upstream developer preview. Before production-like use:

1. Set `DSH_PY_VERSION` to a tested package version.
2. Run in an isolated workspace or sandbox.
3. Keep credentials in an approved secret manager.
4. Restrict filesystem/network/tool privileges.
5. Enable code, dependency, secret, and policy checks.
6. Review trajectory retention because sessions may contain sensitive operational context.
7. Maintain a rollback path for upgrades.

## Install

```bash
cd skills/deepseek-harness
chmod +x install.sh
DSH_PY_VERSION=<tested-version> ./install.sh
```

For a disposable developer environment where version pinning is not yet established:

```bash
./install.sh
```

## Official Web UI quick start

When Node.js is available:

```bash
npx @deepseek-ai/dsh web
```

## Credentials

Do not store secrets in this repository. Inject them at runtime:

```bash
export DEEPSEEK_BASE_URL="<approved-endpoint>"
export DEEPSEEK_API_KEY="<runtime-secret>"
```

## Promotion gate

Do not mark the integration production-qualified until the pinned harness version has passed functional, security, compatibility, rollback, and trace-retention tests in the target environment.