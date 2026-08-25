# PEFY Upstream Remediation Policy

## Objective
Keep externally-derived PEFY components current, secure, performant and maintainable without erasing intentional local adaptations or allowing uncontrolled upstream changes to enter production.

## Upstream state model
- U0 CLEAN: local branch is synchronized with verified upstream.
- U1 BEHIND-ONLY: local has no unique commits and can normally fast-forward after qualification.
- U2 AHEAD-ONLY: local adaptations exist; preserve them as owned PEFY delta.
- U3 DIVERGED: both local and upstream changed; treat as controlled merge/rebase/migration work.
- U4 ORPHANED/MOVED/ARCHIVED: upstream ownership, viability or migration target must be re-established.

## Remediation algorithm
1. Verify upstream identity, ownership and license.
2. Record current local commit, branch, release and rollback point.
3. Quantify ahead/behind state and branch mismatch.
4. Read upstream release notes, manifests and breaking changes.
5. Assess security, runtime, schema, data migration, API, plugin and license effects.
6. Protect intentional local PEFY changes as explicit delta patches or adapters.
7. Build a disposable qualification branch or sandbox.
8. Run relevant tests, security checks and benchmarks.
9. For U1: prefer fast-forward only when evidence is green.
10. For U2: do not overwrite. Track local delta and upstream equivalence.
11. For U3: use three-way analysis. Separate trivial, mechanical and semantic conflicts. Resolve semantic conflicts only with domain-aware review.
12. For U4: freeze automatic update assumptions, identify successor/fork/vendor path, and perform migration review.
13. For critical vulnerabilities where full convergence is unsafe, backport the smallest verified security fix.
14. Promote through review/approval. Never force-push production branches.
15. Retain rollback commit/tag, migration notes and evidence.

## Conflict handling
Conflicts are classified as:
- C0 formatting/generated artifacts: regenerate from authoritative source.
- C1 dependency/lockfile: reconcile from manifests, then regenerate lockfile and test.
- C2 configuration: merge by environment ownership and least privilege.
- C3 API/schema: requires compatibility and migration testing.
- C4 security/auth/identity: requires Security Council and independent verification.
- C5 business logic/IP: preserve PEFY-owned intent unless explicitly superseded.

## Upgrade decision gates
Approve only when:
- upstream is authentic and supportable
- license remains acceptable
- no unresolved critical security finding exists
- migrations are reversible or recoverable
- required regression tests pass
- dependent integrations remain compatible
- performance/cost regression is within accepted threshold
- local PEFY delta is preserved and documented
- rollback is viable

## Efficiency rules
- Never clone or rebuild everything when a compare/diff is sufficient.
- Prefer thin adapters to invasive forks.
- Keep a local delta ledger for long-lived forks.
- Collapse duplicate capabilities before adding another framework.
- Benchmark only metrics relevant to the changed execution path.
- Backport critical fixes when full migration cost is disproportionate.

## Upstream contribution policy
Generic, non-proprietary bug fixes may be proposed upstream when doing so reduces future maintenance burden. PEFY-specific business logic, security policy, confidential architecture, client data and proprietary orchestration remain private.

## Evidence required per remediation
- source/upstream identity
- local rollback commit
- compare result
- release/changelog assessment
- migration/compatibility assessment
- security scan results
- test results
- benchmark delta where relevant
- local-delta preservation record
- approval decision
- final promoted commit/release
