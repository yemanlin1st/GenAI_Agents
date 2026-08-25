# DeepSeek Harness Skill

## Purpose

Use DeepSeek Harness (`dsh`) as an additional agent-execution harness for coding, repository operations, tool orchestration, sandboxed experimentation, multi-step workflows, and reproducible agent trajectories.

This skill augments existing agents and skills. It must not replace the primary orchestration layer, security controls, governance rules, or model-routing policy.

## Upstream

- Project: DeepSeek Harness
- Publisher: DeepSeek AI
- Repository: https://github.com/deepseek-ai/deepseek-harness
- License: MIT
- Status: Developer Preview

## Trigger conditions

Invoke this skill when a task benefits from one or more of the following:

- agentic software engineering
- repository-wide code changes
- repeatable tool-use workflows
- subagent orchestration
- sandboxed execution
- session replay, fork, resume, or trajectory analysis
- custom agent presets
- plugin-based agent composition
- Python-driven harness execution
- benchmark or evaluation runs in minimal or controlled environments

Do not invoke it for simple requests that do not need a harness.

## Core architecture

DeepSeek Harness is based on Cordis and treats capabilities as plugins. Models, tools, skills, sessions, sandboxes, storage, loops, scheduling, and UI components can be mounted or recomposed.

Supported operating patterns include:

- Standard mode: full coding-agent toolset
- Code mode: TypeScript-based multi-step tool orchestration
- Minimal mode: constrained shell and editor environment for benchmark-style runs
- Creator mode: runtime inspection, plugin experimentation, and preset authoring
- Python SDK: programmatic JSON-RPC control of the harness runtime

## Integration policy

1. Preserve the existing orchestration hierarchy.
2. Treat DeepSeek Harness as a pluggable execution substrate, not as the sole decision authority.
3. Keep model selection externalized so the harness can be routed through approved DeepSeek-compatible endpoints or approved local/proxy endpoints.
4. Route privileged actions through existing approval, policy, and audit controls.
5. Keep all workspaces isolated and disposable by default.
6. Never provide production credentials to an unconstrained agent workspace.
7. Use least privilege for filesystem, shell, network, repository, cloud, and deployment permissions.
8. Require explicit approval before destructive operations, production deployment, infrastructure mutation, credential rotation, or irreversible data changes.

## Security and privacy controls

DeepSeek Harness records detailed append-only session trajectories. Treat those records as sensitive operational data.

Required controls:

- redact secrets before prompts or tool outputs are persisted
- prohibit storage of API keys, private keys, passwords, tokens, customer secrets, or regulated personal data in trajectories
- use secret references or environment injection instead of embedding secrets in prompts/configuration
- define retention and deletion rules for trajectories
- restrict trajectory access by role
- encrypt trajectory/session storage at rest when persisted outside a disposable developer environment
- isolate shell execution from host-critical paths
- restrict outbound network access where practical
- scan generated code and dependencies before promotion
- require SAST, dependency/SBOM, secret scanning, and test gates before merge or deployment

## Compatibility policy

DeepSeek Harness is in developer preview and may introduce compatibility-breaking changes.

Therefore:

- pin tested versions in production-like environments
- validate upgrades in a disposable branch or sandbox first
- keep integration adapters thin
- avoid coupling business logic directly to unstable harness internals
- maintain a rollback path
- record the tested harness version with each release

## Official quick start

Web UI:

```bash
npx @deepseek-ai/dsh web
```

Source build:

```bash
git clone https://github.com/deepseek-ai/deepseek-harness.git
cd deepseek-harness
pnpm install
pnpm run build
pnpm dsh web
```

Python SDK:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install deepseek-harness-sdk
```

Environment variables commonly used by the Python runtime:

```bash
export DEEPSEEK_BASE_URL="<approved-endpoint>"
export DEEPSEEK_API_KEY="<secret-reference-or-runtime-injection>"
```

Never commit real credentials.

## Recommended execution flow

1. Classify the task and required privilege level.
2. Select the smallest viable harness mode.
3. Mount only required tools/plugins.
4. Create an isolated workspace.
5. Inject only approved context and secrets.
6. Execute with traceability enabled.
7. Run tests and security checks.
8. Review the trajectory for anomalous or over-privileged behavior.
9. Require human approval for high-impact changes.
10. Promote only validated artifacts.

## Relationship to the broader agent stack

Use DeepSeek Harness as an additional execution and composition layer alongside existing coding agents, agent frameworks, workflow engines, local-model runtimes, and orchestration systems. Prefer adapter-based interoperability over duplicated orchestration logic.

Where another harness is better suited to a task, route to that harness instead of forcing DeepSeek Harness.

## Quality gates

A DeepSeek Harness task is considered complete only when:

- requested output exists and is reproducible
- tests pass
- no secrets are exposed
- destructive changes were authorized
- dependency/security checks are acceptable
- trajectory/audit evidence is retained according to policy
- rollback or recovery is understood for production-impacting changes

## Maintenance

Review this skill whenever the upstream harness publishes a new tagged release, changes its plugin API, modifies session formats, or changes security/runtime behavior.