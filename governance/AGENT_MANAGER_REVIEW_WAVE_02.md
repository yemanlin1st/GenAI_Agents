# Agent Manager Review — Wave 02

Date: 2026-08-25
Decision authority: Human governance + PEA / MƐTAPEFYON Ω
Review layer: PEFY Agent Manager
Promotion policy: evidence-gated, non-destructive, rollback-required

## 1. PEFY-TECH/NemoClaw

Capability role: hardened OpenClaw/OpenShell execution, sandbox and managed-inference substrate.
Canonical source: NVIDIA/NemoClaw.
Candidate: `fa4eea8cfc89096fe562c3624cb7ec38496ecfda`.
Risk tier: HIGH.
Agent Manager state: SANDBOX_QUALIFIED.

Evidence passed:
- reviewed production dependency audit at HIGH threshold
- build/typecheck
- installer integration, 606 tests passed / 1 skipped
- WeChat locked-runtime audit
- 909 plugin tests and high coverage
- ShellCheck SARIF
- CodeQL Python and JavaScript/TypeScript
- CLI shards 1,2,4,5,6,7,8,9,11
- former shard-3 timeout disproved by five consecutive focused passes

Blockers:
- fork provenance portability in shard 10
- canonical historical tag portability in shard 12
- explicit authorized DCO `Signed-off-by`
- target-host OpenShell isolation/policy, credential injection, live-provider routing, performance, recovery and rollback proof

Recommended action: retain candidate in controlled qualification branch. Do not merge to production/default branch.
Required approvers: security + architecture + legal/provenance + change control + authorized DCO signatory.
Rollback: preserve current PEFY baseline and candidate SHA independently; no destructive ref movement.
Next review trigger: provenance/history remediation or target-host qualification evidence.

## 2. OpenClaw

Capability role: subordinate agent/runtime platform beneath PEA / MƐTAPEFYON Ω.
Canonical source: openclaw/openclaw.
Candidate: `b9d522738d5e087c1783e38eb1401eebcabc40de`, version 2026.8.1.
Risk tier: HIGH.
Agent Manager state: SANDBOX_QUALIFIED, pending terminal static lane and target-host migration proof.

Evidence passed at review:
- frozen dependency installation
- exact version and schema checks: state 9, agent 17
- dependency vulnerability gate
- base configuration schema
- SQLite session schema
- plugin SDK surface
- plugin contracts
- authentication compatibility
- strict build smoke
- CLI smoke
- no conflict markers
- workflow checks
- runtime sidecars
- plugin inventory and version synchronization

Pending at review capture:
- global core lint lane still executing

Blockers:
- real state/schema migration against representative data
- live provider integration under PEFY model-routing policy
- memory/session compatibility
- target-host performance, recovery and rollback

Recommended action: keep exact upstream candidate isolated. No production promotion yet.
Required approvers: architecture + security + operations/change control.
Rollback: current local baseline retained separately; qualification PR never merged.
Next review trigger: static lane terminal result or target-host migration proof.

## 3. OpenCode

Capability role: coding/execution agent substrate, subordinate to PEFY orchestration and policy.
Canonical source: anomalyco/opencode.
Candidate: `69aaa22793bcbe0b016ad9cfad22616906766df0`.
Risk tier: HIGH.
Agent Manager state: QUARANTINED_FOR_WINDOWS_PRODUCTION, SANDBOX_QUALIFIED_FOR_LINUX_E2E.

Evidence passed:
- GitHub-hosted qualification successfully bypassed unavailable third-party Blacksmith runners without altering upstream product code
- Linux E2E passed
- Linux unit suite produced 3315 pass, 22 skip, 1 todo and one timing-bound failure
- Bun 1.3.14/toolchain successfully installed on Linux and Windows

Open findings:
- Linux one assertion measured 15.212s against a strict <15s requirement. Reproducibility not established.
- Windows unit tests expose repeated first-use ripgrep 15.1.0 download/PowerShell extraction timeouts and SIGTERM. This is a real Windows portability blocker.
- Windows E2E still executing at review capture.
- patched MCP/provider dependency provenance and AI SDK 6 behavioral compatibility still require focused review.

Recommended action: Linux controlled sandbox only. Do not promote Windows. Do not weaken timeouts to manufacture green CI.
Required approvers: coding-platform architecture + security/supply-chain + Windows compatibility owner.
Rollback: keep current OpenCode baseline and exact candidate/ref; no default-branch migration.
Next review trigger: focused Linux timing rerun, Windows ripgrep remediation evidence, or terminal Windows E2E.

## 4. MetaGPT-x / MetaGPT 1.0.0

Capability role: multi-agent reference/execution framework, subordinate to PEFY authority.
Canonical source: FoundationAgents/MetaGPT.
Canonical candidate: `11cdf466d042aece04fc6cfd13b28e1a70341b1f`.
PEFY compatibility patch candidate: `click<8.2` for Typer 0.9.0 compatibility.
Risk tier: MEDIUM-HIGH.
Agent Manager state: SANDBOX_QUALIFIED_WITH_EXPLICIT_DOWNSTREAM_PATCH.

Evidence passed:
- canonical installation, pip dependency check and import across Python 3.9/3.10/3.11
- canonical CLI exposed a reproducible Click 8.4.2 / Typer 0.9.0 incompatibility on Python 3.10/3.11
- explicit `click<8.2` patch restores install + pip check + import + CLI on Python 3.9/3.10/3.11
- canonical unit suite on Python 3.10 passes with patch
- hardened pre-commit portability remediation passes after replacing SSH hook sources with HTTPS and moving to Actions v4/minimum permissions

Blockers:
- OCR capability retention decision because canonical 1.0.0 no longer activates the local OCR extra
- broader PEFY integration testing
- performance and rollback evidence
- license/provenance review of retained and patched capabilities

Recommended action: retain the compatibility patch as an explicit PEFY delta. Do not hide it inside the canonical identity. Keep OCR as a carve-out decision, not silent feature loss.
Required approvers: architecture + capability owner + legal/provenance + change control.
Rollback: canonical SHA and downstream patch remain separate; reverting the patch restores exact upstream candidate.
Next review trigger: OCR retention decision or broader integration proof.

## Portfolio decision

No component in this wave is admitted as `PRODUCTION_QUALIFIED`.

Current admissions:
- NemoClaw: SANDBOX_QUALIFIED
- OpenClaw: SANDBOX_QUALIFIED
- OpenCode: Linux sandbox qualification only; Windows QUARANTINED_FOR_PRODUCTION
- MetaGPT 1.0.0 + explicit Click compatibility patch: SANDBOX_QUALIFIED

The Agent Manager therefore blocks any automatic production promotion or default-branch convergence until component-specific remaining gates are satisfied.

This review does not replace human approval, legal attestations, relevant councils, independent verification or target-host qualification.