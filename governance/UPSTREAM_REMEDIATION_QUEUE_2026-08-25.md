# PEFY Upstream Remediation Queue — 2026-08-25

Status: ACTIVE / CONTROLLED. No production branch promotion is authorized by this record alone.

## P1 — CrewAI
- Local: `yemanlin1st/crewAI`
- Verified upstream: `crewAIInc/crewAI`
- State at assessment: U1 BEHIND-ONLY
- Ahead: 0
- Behind: 543
- Previous local main head / rollback reference: `fc6792d0678fb6c80a81b13289b09ae01a29a3fd`
- Upstream candidate head: `4e0b2e2b157ab509fc0221826a09661dc87aa2bf`
- Staging branch created: `upstream-sync/2026-08-25`
- Draft sync PR: #1
- Current gate: HOLD FOR VALIDATION
- Evidence gap: no CI status surfaced for the staged commit in the fork.
- Required next gates: install/build, unit/integration tests, security/dependency/secret checks, API/plugin compatibility, MƐTAPEFYON adapter regression, memory/latency baseline, rollback proof.

## P1 — DeerFlow
- Local: `yemanlin1st/deer-flow`
- Verified upstream: `bytedance/deer-flow`
- State at assessment: U1 BEHIND-ONLY
- Ahead: 0
- Behind: 1,353
- Upstream candidate head: `431892e16abff5f11c50be37eeb0699af958896f`
- Staging branch created: `upstream-sync/2026-08-25`
- Classification: MIGRATION-SCALE SYNC
- Current gate: HOLD FOR MIGRATION VALIDATION
- Required next gates: architecture delta review, Python/Node runtime requirements, dependency and lockfile migration, sandbox/memory/tool/skill API compatibility, state/memory/session migration, security scans, full regression, performance baseline, rollback.

## P1 — n8n
- Local: `yemanlin1st/n8n`
- Verified upstream: `n8n-io/n8n`
- State at assessment: U1 BEHIND-ONLY
- Ahead: 0
- Behind: 7,640
- Upstream candidate head: `c09da09d3884fa3a8e634d32411893395d406dd7`
- Upstream head included release tag merge `n8n@2.37.0` at assessment time.
- Staging branch created: `upstream-sync/2026-08-25`
- Classification: MIGRATION-SCALE SYNC
- Current gate: HOLD FOR MIGRATION VALIDATION
- Required next gates: fair-code/license review, Node/runtime requirements, database migrations, credential encryption compatibility, workflow schema compatibility, community node compatibility, queues/workers/webhooks, environment variables, backup/restore, integration tests, security scans, performance and rollback.

## P1 — GenAI_Agents control-plane placement
- Local: `yemanlin1st/GenAI_Agents`
- Verified upstream: `NirDiamant/GenAI_Agents`
- Repository is a public fork.
- Current PEFY governance, upstream-control and DeepSeek Harness integration artifacts have been added into this fork.
- Risk: mixing proprietary/internal control-plane material with an externally-derived public reference repository creates IP, visibility, lifecycle and upstream-convergence complexity.
- Current gate: PRESERVE, DO NOT DELETE.
- Required correction: migrate governance/control-plane artifacts to a dedicated PEFY-owned private repository when an appropriate connected destination is available, verify copied content and history, then remove or reduce public-fork overlays only through controlled cleanup.
- GitHub Actions evidence: no workflow runs were visible at assessment time; treat the scheduled workflow as configured but not yet runtime-proven.

## P1 — DeepSeek Harness
- Upstream: `deepseek-ai/deepseek-harness`
- Local integration: `yemanlin1st/GenAI_Agents/skills/deepseek-harness`
- Upstream is active, MIT licensed, default branch `master` at assessment time.
- Treatment: direct-upstream watch rather than fork sync.
- Current gate: version pin + sandbox qualification required before production-like use.

## Promotion rule
A staging branch may replace the default branch only after its project-specific validation matrix passes and a rollback point is confirmed. Large behind-only deltas are not considered low-risk merely because `ahead_by` is zero.
