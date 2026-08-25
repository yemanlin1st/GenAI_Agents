# Initial PEFY AI Portfolio Baseline Audit — 2026-08-25

Status: METADATA-LEVEL BASELINE. This is not a code-complete or production qualification audit.

## Scope observed
GitHub inventory pagination confirms more than 200 accessible repositories in the connected account. The portfolio includes proprietary/project repositories, upstream/fork-like technology repositories, training/reference repositories, catalog/awesome lists, agent frameworks, skills, coding assistants, workflow engines, security tools, video systems, model-related repositories and business applications.

## Immediate architectural findings

### P1 — Capability overlap and orchestration ambiguity
Multiple repositories occupy overlapping capability domains. Examples include:
- Claude/Claude Code tooling, marketplaces, workflows, templates, skills, guides and alternate runtimes
- agent frameworks and multi-agent systems including CrewAI, AutoGPT, SuperAGI, MetaGPT, OpenAgents, AgentScope and others
- OpenClaw-related runtimes, skills, mission-control and collaboration variants
- AI/agent skills collections and multiple awesome/catalog repositories
- career/job application agent families
- video/montage/generation families
- LLM/model/resource collections

Risk: duplicated responsibilities, incompatible state/orchestration models, duplicated dependency trees, excessive update burden and unclear authority.

Control: MƐTAPEFYON Ω / MƐTAFLOW Ω remains the supervisory control plane. Other frameworks are classified as execution substrates, adapters, discovery sources or project-local tools. A capability registry must record which runtime is authoritative for each workstream.

### P1 — Upstream synchronization and supply-chain burden
A large portion of the portfolio appears to track external/open-source technologies or reference collections. Each such repository creates an upstream, licensing, vulnerability, dependency and compatibility monitoring obligation.

Control: every externally-derived repository must record verified upstream, current tracked commit/tag/version, license, update method, local modifications, security tier and rollback strategy.

### P1 — Public/private classification requires continuous review
The portfolio mixes public and private repositories. Proprietary PEFY assets, credentials, client-sensitive artifacts, internal prompts, private governance, deployment details and operational secrets require explicit repository classification and secret-scanning controls.

Control: apply a repository data-classification gate and verify that public visibility is intentional for each proprietary or operational project.

### P2 — Default-branch inconsistency
Observed default branches include main, master, dev, develop and project/release-specific branches. Some project repositories also use atypical default branches.

Risk: automation assumptions can target the wrong branch, upstream sync can diverge, and release processes become inconsistent.

Control: do not force a universal branch rename. Record the authoritative branch per repository, then standardize only where migration is low risk and evidence-backed.

### P2 — Repository footprint and duplicated local storage
Several repositories are large and multiple capability families appear replicated across related projects.

Risk: storage, cloning, indexing, CI and backup costs can become material.

Control: measure actual disk/index/CI impact before cleanup. Prefer shallow/sparse strategies, artifact storage, shared caches, dependency deduplication and reference-only catalog treatment where suitable.

### P2 — Discovery repositories must not become trusted runtime dependencies
The portfolio contains many awesome lists, collections, guides, tutorials and marketplaces.

Control: classify these as discovery/knowledge sources unless an item has passed provenance, license, security, quality and project-local qualification gates.

## Initial council ruling
APPROVED CONDITIONAL for the continuous-improvement control architecture.

Conditions:
1. Build the capability/dependency/upstream registry before broad cleanup.
2. Preserve existing working systems until replacement benefit is proven.
3. No silent mass install, mass deletion, mass upgrade or mass branch migration.
4. Security-critical findings take precedence over consolidation work.
5. Every production-impacting change requires isolated validation and rollback.
6. Preserve dissent and evidence in change records.

## First execution priorities
1. P0/P1 secret and repository-visibility review for proprietary/operational repositories.
2. Build machine-readable capability registry for the agentic/AI portfolio.
3. Identify authoritative vs reference-only repositories by capability family.
4. Resolve overlap at routing/governance level before physical deletion.
5. Map upstreams and versions for CrewAI, DeepSeek Harness, DeerFlow, DeepFlow, OpenCode, Claude-related tooling, n8n, OpenClaw and other active execution substrates.
6. Establish security/advisory/release watch for all verified upstreams.
7. Establish performance baselines for active runtimes before upgrades.
8. Schedule repository hygiene and lifecycle review.

## Evidence boundary
This baseline is derived from connected repository metadata and the current governance architecture. It does not claim that every repository has been source-audited, dependency-scanned, secret-scanned, benchmarked or runtime-tested. Those activities belong to subsequent controlled L0-L8 iterations.
