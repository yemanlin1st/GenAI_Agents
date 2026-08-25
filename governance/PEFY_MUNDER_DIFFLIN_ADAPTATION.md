# PEFY adaptation of Munder Difflin patterns

## Decision

PEFY will not make Munder Difflin a sovereign runtime and will not copy its product identity, visual assets or central-orchestrator model. PEFY Office Agency Ω™ adopts selected architectural patterns through clean PEFY-owned contracts and replaceable adapters.

The resulting PEFY capability is ΩOFFICE, governed by MƐTAPEFYON Ω/PEA and Agent Manager.

## Useful patterns retained conceptually

- real CLI/runtime sessions rather than simulated workers;
- optional PTY-backed interactive execution;
- isolated worktree/workspace per worker when parallel code modification is required;
- typed mailbox and handoff mechanism;
- durable task/decision/evidence ledger;
- project-scoped long-term working memory;
- observable office/topology view;
- task dependencies and scheduled work;
- budget accounting and circuit breakers;
- human approval for spend, scope, destructive or high-impact operations;
- multi-provider and local-model adapters;
- OpenTelemetry-compatible execution traces;
- guarded filesystem/Git operations.

## Patterns deliberately changed

### Sovereign authority
A tool-specific central or “GOD” orchestrator is not used. MƐTAPEFYON Ω/PEA remains sovereign; Agent Manager controls capability lifecycle; ΩOFFICE staffs and coordinates scoped execution.

### Multi-project isolation
Every project receives a namespace, data classification, repository scope, environment scope, memory boundary, budgets and evidence ledger. Cross-project access is denied unless explicitly approved.

### Agent lifecycle governance
Every external agent/runtime passes canonical-source, version, license, permission, sandbox, security, compatibility and evidence review before execution authority is granted.

### Enterprise security
The PEFY design adds policy-as-code, least privilege, secret brokering, egress controls, provenance, SBOM expectations, artifact identity, supply-chain checks, independent review, target-host qualification and rollback proof.

### Production operations
The office includes SRE, incident management, production management, capacity, recovery, BCP/DR, runbooks and service ownership. A successful source build alone is insufficient for production.

### Resource efficiency
Agents are not permanently spawned. The Staffing Router selects the minimum competent cell, enforces concurrency/backpressure and terminates idle/ephemeral workers according to policy.

### Memory governance
Memory is project-scoped, classified, access-controlled, provenance-aware and subject to retention/deletion rules. Semantic indexes are adapters and may be replaced without changing authority.

### Visual layer
An office/cockpit visualization is optional. PEFY-owned visual assets and design-system components must be used. No third-party art asset is incorporated unless its license and attribution are explicitly approved.

### Failure management
Failures are typed as PRODUCT, PLATFORM, HARNESS, GOVERNANCE, UPSTREAM, TRANSIENT or HUMAN_ATTESTATION. A gate cannot be bypassed merely to obtain a green CI state.

## Adapter targets

ΩOFFICE can expose reviewed adapters for:
- OpenAI Codex;
- OpenCode;
- approved Claude Code distribution;
- DeepSeek Harness;
- CrewAI;
- DeerFlow;
- OpenClaw/NemoClaw;
- n8n where licensing/use case permits;
- approved MCP services;
- Ollama/local engines and approved remote model routes;
- GitHub/CI/CD and project automation.

Each adapter maps a common task envelope to the native runtime and returns evidence in a common result envelope.

## Common task envelope

Required fields:
- task_id;
- project_id;
- objective;
- acceptance_criteria;
- role/capability requested;
- allowed repositories/paths;
- allowed tools/network/data;
- data classification;
- timeout and resource budget;
- required evidence;
- approval class;
- cancellation/rollback policy.

## Common result envelope

Required fields:
- task_id and candidate SHA/artifact identity when applicable;
- execution adapter/version;
- outcome;
- changed assets;
- tests/checks/evidence;
- failure classification when not successful;
- residual risks;
- rollback reference;
- reviewer/gate decision.

## All-project adaptation

The Project Adapter schema allows ΩOFFICE to operate across PEFY software, cybersecurity, FinTech, AI, WordPress/web, mobile, infrastructure, media/video, data, QSE/HSE, documents/research and future product lines without hard-coding a single project's stack into the office core.

## IP and licensing boundary

PEFY-specific governance, project adapters, role registry, policies, workflow contracts, UI/design assets and implementation extensions are maintained as PEFY-owned assets. Third-party code remains governed by its original license. Upstream generic fixes can be contributed only when they contain no PEFY-confidential or proprietary material.
