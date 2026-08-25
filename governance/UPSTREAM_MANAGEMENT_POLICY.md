# PEFY Upstream Management & Adaptive Synchronization Policy

## Objective
Keep externally-derived repositories, runtimes, frameworks, skills, tools and dependency trees synchronized with verified upstreams without destroying local value, importing avoidable risk, or creating update noise.

This policy extends L5 WATCH and L7 PROVE of the PEFY AI Continuous Improvement architecture.

## Core rule
Upstream maintenance is not "always merge latest". Every repository is classified by divergence state and then handled with the least-risk strategy.

## Divergence classes

### U0 — CLEAN
`ahead_by = 0`, `behind_by = 0`

Action:
- no synchronization required
- continue release/security monitoring

### U1 — BEHIND-ONLY
`ahead_by = 0`, `behind_by > 0`

Preferred action:
- preserve current head as rollback reference
- inspect release notes, breaking changes, license/runtime changes and security advisories
- if small delta: reviewable integration PR is acceptable
- if large delta: prefer native fork synchronization / fast-forward instead of a giant review PR
- run dependency install, tests, security gates and benchmark after synchronization
- promote only when gates pass

### U2 — AHEAD-ONLY
`ahead_by > 0`, `behind_by = 0`

Action:
- preserve local commits
- identify whether they are intentional PEFY adaptations, temporary patches or obsolete changes
- consider contributing generally useful fixes upstream
- do not reset or overwrite local commits

### U3 — DIVERGED
`ahead_by > 0`, `behind_by > 0`

Action:
1. create preservation branch/tag/reference
2. inventory local-only commits
3. classify each local delta: keep, upstreamed, obsolete, security patch, branding/IP, adapter, configuration, experimental
4. update a clean integration branch from upstream
5. replay only approved local deltas using rebase/cherry-pick/patch/adapter strategy
6. resolve conflicts deliberately
7. run full regression/interoperability/security/performance gates
8. compare behavior with pre-update baseline
9. promote through PR/change control
10. retain rollback point

### U4 — ORPHANED / UPSTREAM MOVED
Upstream archived, renamed, deleted, relicensed, abandoned or replaced.

Action:
- verify authoritative successor
- perform license and provenance review
- evaluate migration vs maintained internal fork
- freeze upgrades until ownership decision is recorded

## Adaptive thresholds
The system must not treat all behind-only forks the same.

Suggested defaults:
- 1–20 commits behind: normal review PR or fast-forward candidate
- 21–200 commits: integration branch + focused compatibility review
- 201–1000 commits: native sync/fast-forward preferred, then full regression
- >1000 commits or major-version jump: migration event, not routine update

These thresholds are guidance, not hard rules. Security urgency, semantic-version jumps, runtime requirements and local modifications override commit-count heuristics.

## Required pre-sync checks
- verified parent/source repository
- branch mapping is correct
- local branch head recorded
- ahead/behind state measured
- latest upstream release/tag/version identified when applicable
- changelog/release notes reviewed
- security advisories/CVEs checked
- license changes checked
- language/runtime requirements checked
- dependency lockfile changes assessed
- database/schema migrations assessed
- API/plugin/protocol breaking changes assessed
- required secrets and infrastructure changes assessed without exposing secrets

## Required post-sync gates
- clean checkout/install/build
- unit tests
- integration tests
- E2E tests where applicable
- SAST
- dependency/vulnerability scan
- secret scan
- SBOM refresh for production-relevant components
- container/IaC scan where applicable
- interoperability tests with MƐTAPEFYON Ω / MƐTAFLOW Ω and dependent adapters
- performance baseline comparison
- memory/resource comparison
- migration/rollback verification
- documentation/version registry update

## Security patch prioritization
A fork may remain on an older feature baseline only if required security fixes are not missed. When full upstream synchronization is temporarily blocked:
- identify security-relevant upstream commits/releases
- backport the minimal safe patch when feasible
- document deviation and residual risk
- schedule full convergence

## Local adaptation preservation
Local value must never be erased merely to become current. Preserve intentional PEFY differentiation through thin adapters, extension modules, configuration overlays, patch queues or clearly separated proprietary modules. Avoid deep invasive forks where an adapter can provide the same behavior.

## Upstream contribution rule
When a local fix is generic, non-proprietary and suitable for the source project, prefer contributing it upstream. This reduces long-term fork maintenance. Proprietary business logic, client data, internal governance, credentials and protected IP must not be upstreamed.

## Update decision score
Score each candidate synchronization 0–5 for:
- security urgency
- functional benefit
- performance benefit
- interoperability benefit
- upstream maturity
- breaking-change risk
- local-delta complexity
- test coverage confidence
- rollback confidence
- operational urgency

Prioritize high security/benefit and high rollback confidence. Defer low-value updates with high migration risk.

## Current verified examples — 2026-08-25
- yemanlin1st/crewAI -> crewAIInc/crewAI: behind-only by 543 commits, ahead 0. Draft synchronization PR created for controlled review.
- yemanlin1st/deer-flow -> bytedance/deer-flow: behind-only by 1,353 commits, ahead 0. Treat as migration-scale synchronization.
- yemanlin1st/n8n -> n8n-io/n8n: behind-only by 7,640 commits, ahead 0. Treat as migration-scale synchronization; check licensing/runtime/database migration changes before updating.

These counts are point-in-time evidence and must be recomputed before any actual synchronization.

## Prohibitions
- no `reset --hard` against unclassified local work
- no mass force-push
- no auto-merge of major upstream updates without tests
- no assumption that latest equals safest
- no license change acceptance without review
- no production upgrade without rollback
- no secret injection into CI logs or patch files
- no upstream contribution of protected PEFY/client IP
