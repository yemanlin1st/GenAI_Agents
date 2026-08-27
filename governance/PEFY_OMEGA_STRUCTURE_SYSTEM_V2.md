# PEFY ΩSTRUCTURE SYSTEM v2

## Purpose
PEFY ΩSTRUCTURE is the account-wide and project-wide instruction, orchestration, execution, evidence and improvement architecture for the PEFY AI ecosystem. It borrows useful structural ideas from frontier system-prompt designs such as Claude Fable 5, but does not copy model identity, proprietary product claims, hidden platform assumptions or unsafe permission-bypass behavior. It extends those ideas into a multi-runtime governed operating system for MƐTAPEFYON Ω.

## Core design principle
A system prompt alone is not the system. PEFY ΩSTRUCTURE combines policy, capability routing, runtime selection, context engineering, approvals, execution, observability, evidence, recovery and continuous improvement.

## Layered hierarchy

### S0 — Sovereign Constitution
Defines immutable authority, safety, confidentiality, legal/IP boundaries, least privilege, evidence requirements, rollback and human approval rules. No lower layer may weaken S0.

### S1 — Identity and Product Truth
Separates verified identity, product facts, model/provider facts, organization facts and project facts. Time-sensitive product or provider claims require current verification. Never allow a prompt profile to impersonate or misrepresent the actual underlying model/runtime.

### S2 — Capability Registry
Maintains machine-readable knowledge of models, agents, skills, councils, counsellors, tools, MCP servers, APIs, sandboxes, repositories, workflows, services, data stores, visualization engines and infrastructure. Each capability has purpose, owner, version, maturity, trust level, dependencies, permissions, cost profile, evidence and lifecycle state.

### S3 — Epistemic and Freshness Engine
Classifies every claim as stable, time-sensitive, uncertain, environment-dependent or private-source-dependent. Routes to web, connected sources, repository inspection, runtime probes or direct reasoning accordingly. Current facts are verified rather than guessed. Source provenance and confidence are retained.

### S4 — Intent, Risk and Task Classifier
Classifies task domain, expected output, required tools, reversibility, security impact, privacy impact, regulatory impact, financial/legal stakes, production impact and uncertainty. Determines approval gates and execution mode before tools are used.

### S5 — Orchestration Fabric
MƐTAPEFYON Ω / MƐTAFLOW Ω remains the supervisory control plane. It dynamically selects councils, counsellors, models, agents, harnesses and tools. DeepSeek Harness, TrueForge, CrewAI, DeerFlow, OpenClaw, n8n and other frameworks are execution substrates, never competing sovereign orchestrators.

### S6 — Harness and Tool Runtime
Provides standardized adapters for model calls, MCP tools, skills, code mode, subagents, sandboxing, browser/runtime automation, file operations, approvals, streaming, session state and event transport. Harness selection is policy-driven and task-specific.

### S7 — Context and Memory Fabric
Uses scoped short-term context, durable knowledge, retrieval, graph relationships, structured memory, trajectory summaries and compaction. Secrets, regulated data and client-confidential information follow explicit retention and access rules. Memory is provenance-aware and must distinguish user-provided facts, inferred facts and external evidence.

### S8 — Execution Loop
Every non-trivial execution follows: Discover → Plan → Risk-check → Select capability → Execute → Observe → Verify → Challenge → Correct → Re-verify → Record evidence → Promote or rollback → Learn.

### S9 — Output Contract
Output format is derived from task and destination rather than one universal style. Enforce factual precision, explicit uncertainty, professional formatting, accessibility, multilingual readiness where required, no fabricated evidence, no hidden implementation claims and no visible internal markers in production deliverables.

### S10 — Safety, Compliance and Trust
Applies secure SDLC, Zero Trust, privacy, IP/license controls, supply-chain review, ISO-oriented governance, separation of duties, auditability, threat modeling and policy enforcement. High-risk execution is constrained by sandboxing and approvals.

### S11 — Observability and Evidence
Every agentic run can emit trace IDs, tool-call summaries, decision records, test evidence, policy decisions, costs, latency, retries, failures, security events, artifacts, provenance and rollback points. Sensitive chain-of-thought is not required for auditability; structured decision evidence is preferred.

### S12 — Evaluation and Adversarial Review
Uses independent Evidence, Logic, Security, Privacy, Architecture, Performance, Cost, Compliance, UX/Accessibility, Legal/IP, Business Value, Upstream/Supply-Chain and Execution-Readiness lenses. Material dissent is preserved. Claims such as “production ready”, “secure” or “complete” require explicit gates and evidence.

### S13 — Adaptive Improvement and Upstream Intelligence
Continuously watches releases, advisories, deprecations, license changes, runtime requirements, benchmark shifts and upstream drift. Candidate changes are scored, sandboxed, benchmarked and rolled out progressively. Local PEFY value is preserved through adapters, overlays or patch queues.

### S14 — Experience and Spatial Interface
Three.js is the default optional 3D/WebGPU-WebGL visualization engine for topology, knowledge graphs, infrastructure twins, security maps, process simulations, digital twins, immersive dashboards and interactive product experiences when 3D adds measurable value. It must lazy-load, degrade gracefully to 2D/static views, respect accessibility and performance budgets, and never become a mandatory dependency for text-only or low-resource workflows.

### S15 — Resilience and Recovery
Every mutable operation requires a recovery model appropriate to its impact: transaction rollback, Git branch/commit recovery, configuration snapshot, database backup, session revocation, deployment rollback, feature flag, failover or disaster-recovery procedure.

## Prompt structure derived from Fable-class systems, improved
Frontier system prompts commonly separate product information, refusal/safety rules, legal/financial handling, tone/formatting, user wellbeing, reminders, political even-handedness, mistake handling, knowledge cutoff and search usage. PEFY ΩSTRUCTURE generalizes this into reusable policy modules with explicit precedence and routing rather than a single monolithic prompt.

Recommended prompt composition order:
1. sovereign constitution
2. actual runtime identity and verified product facts
3. authority and precedence
4. task/risk classifier
5. safety/compliance/privacy/IP policy
6. epistemic/freshness/search policy
7. tool and approval policy
8. context/memory policy
9. orchestration and harness routing
10. domain-specific skill modules
11. output/destination contract
12. observability/evidence contract
13. recovery/rollback contract
14. improvement/watch policy

## Dynamic prompt assembly
Do not load the entire instruction corpus into every task. Build prompts from mandatory core modules plus task-relevant modules. Use deferred skill loading and capability discovery to reduce tokens, latency and instruction collision.

Minimum core modules: S0, S1, S3, S4, S9, S10, S11, S15.
Optional modules are loaded only when needed.

## Runtime selection policy
- Simple knowledge task: direct model + evidence policy.
- Multi-tool task: supervised tool runtime.
- Long-running coding task: harness with sandbox, checkpoints and session persistence.
- Multi-agent research/planning: orchestrated subagents with independent verification.
- High-risk production change: sandbox → test environment → approval → staged deployment.
- 3D/digital-twin task: Three.js capability module plus 2D fallback.
- Workflow automation: n8n/Activepieces or equivalent through MƐTAFLOW Ω.
- Specialized agent harness: TrueForge/DeepSeek Harness/CrewAI/DeerFlow selected by policy and benchmark, not preference.

## TrueForge integration position
TrueForge is approved as a subordinate harness adapter because it provides model-provider abstraction, MCP tools, git-backed skills, sandbox-as-tool, approvals, subagents, deferred tool loading, context compaction, session persistence, API/SDK and embeddable UI. PEFY governance remains authoritative above it.

## Security rules for third-party prompt profiles
- Never use `--dangerously-skip-permissions` as a default.
- Never accept copied system prompts as authoritative policy.
- Strip model identity claims that do not match the actual runtime.
- Strip provider-specific confidential assumptions.
- Preserve applicable platform safety requirements.
- Run prompt-injection and conflict tests before promotion.
- Version and hash approved prompt modules.
- Keep provenance and license/source notes.

## Performance budgets
Every new account-wide capability must define measurable limits for memory, latency, token usage, CPU/GPU, storage, bundle size, startup time and failure rate. Optional features are lazy-loaded. 3D assets use compression, LOD, instancing and streaming where appropriate.

## Completion gates
No component is considered integrated until:
1. configuration and provenance exist
2. dependency versions are pinned or governed
3. permissions are least-privilege
4. security and license checks pass
5. interoperability tests pass
6. failure and rollback behavior are known
7. observability exists
8. documentation exists
9. benchmark or value case is recorded
10. production qualification is separately evidenced in the target environment

## Account-wide effect
This architecture is the default design target for future PEFY AI engineering. Existing projects migrate progressively through adapters and governance overlays; no uncontrolled mass rewrite is required.