# PEFY AI Portfolio Convergence — Execution Wave 02

Date: 2026-08-25
Status: CONTROLLED / NO AUTO-MERGE
Authority: MƐTAPEFYON Ω / MƐTAFLOW Ω / PEA

## Objective

Move the highest-risk agent/runtime forks from generic upstream-drift awareness to evidence-based migration dossiers while preserving PEFY-owned governance, configuration, data, security boundaries and rollback.

## Dependency order

1. Sovereign control-plane extraction
   - Mandatory before removing PEFY governance artifacts from externally-derived repositories.
   - Codex is the immediate extraction candidate because its 16 local commits modify no Codex core source.

2. OpenClaw qualification
   - Must precede production-like NemoClaw qualification because NemoClaw executes/hosts OpenClaw-related workloads.
   - Local package baseline: 2026.4.3.
   - Current upstream package baseline: 2026.8.1.
   - Current upstream schema contracts explicitly include state schema 9 and agent schema 17.
   - Current supported Node release floors: 22.22.3+, 24.15.0+, 25.9.0+; Node 23 unsupported.
   - Migration must validate state/session/config/plugin/provider/memory/approval contracts and preserve THIRD_PARTY_NOTICES.

3. PEFY-TECH/NemoClaw qualification
   - Organization-level fork is authoritative for convergence; downstream personal fork waits.
   - Local package remains 0.1.0 but is a thin historical implementation requiring Node >=20 and directly depending on OpenClaw 2026.3.11.
   - Current NVIDIA upstream remains package 0.1.0 but requires Node >=22.19 and has evolved into a broader OpenShell-based secure-agent distribution with OpenClaw, Hermes and LangChain Deep Agents, managed inference, policy-boundary compilation, policy schemas, state-lock plans and significantly larger test/benchmark surfaces.
   - Never propagate to yemanlin1st/NemoClaw until the exact organization-level commit is qualified.

4. OpenCode qualification — parallel after common MCP/model-router contracts are frozen
   - Local Bun 1.3.10 -> upstream Bun 1.3.14.
   - AI SDK 5.0.124 -> 6.0.168.
   - Node type baseline 22.x -> 24.x.
   - SST 3.18.10 -> 4.13.1.
   - Turbo 2.8.13 -> 2.10.2.
   - Playwright 1.51.0 -> 1.59.1.
   - Current upstream patches MCP SDK and several AI/provider dependencies; effective runtime behavior therefore includes upstream patchsets and requires provenance/compatibility review.

5. MetaGPT qualification — parallel after common model-router/knowledge contracts are frozen
   - Local 0.8.1 -> canonical 1.0.0.
   - Python remains >=3.9,<3.12.
   - Local test stack protobuf 3.19.6 -> upstream ~=4.25.5.
   - Local OCR extra is active while canonical upstream comments it out; preserve OCR as a separately qualified PEFY capability if operationally required.
   - RAG/vector stores remain subordinate to the PEFY sovereign knowledge fabric.

## P0/P1 migration gates

Every migration requires all applicable gates below before promotion:

- provenance/license/notice validation
- configuration and state backup/restore
- schema/API migration
- auth/identity/secret handling
- sandbox/filesystem/network/exec policy
- MCP and tool-permission compatibility
- provider/model-router compatibility
- memory/knowledge authority boundaries
- dependency integrity and patched-dependency review
- SAST, secret scan, SBOM and container/image checks where applicable
- representative integration/E2E tasks
- latency, memory, startup, task-success, retry and cost baseline
- rollback test
- explicit approval

## Capability authority rules

- MƐTAPEFYON Ω / MƐTAFLOW Ω / PEA owns sovereign orchestration, policy, approval, model-routing governance and authoritative memory/knowledge policy.
- OpenClaw is a gateway/execution runtime.
- NemoClaw/OpenShell is a hardened sandbox/inference execution layer.
- OpenCode is a coding execution/client surface.
- MetaGPT, DeerFlow and CrewAI are selectable subordinate multi-agent frameworks.
- n8n is an internal workflow engine subject to its license constraints.
- Discovery/catalog repositories never become automatic runtime dependencies.

## Promotion rule

No draft qualification PR is merge approval. A PR may only leave DRAFT/BLOCKED after evidence demonstrates that required gates pass on the intended deployment profile and that the rollback path is operational.