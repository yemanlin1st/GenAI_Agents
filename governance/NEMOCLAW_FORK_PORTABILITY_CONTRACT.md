# PEFY NemoClaw Fork Portability Contract

Date: 2026-08-25
Status: REQUIRED BEFORE PEFY-TECH/NemoClaw PROMOTION
Scope: NVIDIA/NemoClaw -> PEFY-TECH/NemoClaw -> approved downstream forks

## Purpose

Preserve NVIDIA's strong artifact, workflow, provenance and historical-upgrade controls while making them valid in a governed PEFY fork. Portability must never be achieved by weakening identity verification, disabling historical-upgrade tests, bypassing signed provenance, or treating a PEFY fork as if it were the canonical NVIDIA repository.

## Verified portability blockers

### 1. Canonical repository identity is embedded in artifact-boundary tests

Current canonical tests construct provenance with `candidateRepository: "NVIDIA/NemoClaw"` and current production validation binds:

- candidate repository
- candidate commit SHA
- workflow SHA
- run ID and run attempt
- artifact ID and digest
- payload SHA-256
- build source revision
- remote repository identity

This is a desirable security boundary. It must remain strict.

PEFY implication: a qualification or runtime artifact produced inside `PEFY-TECH/NemoClaw` requires a two-level provenance statement rather than a simple repository-name substitution.

### 2. Historical upgrade fixtures depend on canonical tags not present in the PEFY fork

The exact-upstream qualification run proved that historical installer/upgrade tests require at least:

- `v0.0.36`
- `v0.0.55`
- `v0.0.74`
- `v0.0.89`

These refs exist in `NVIDIA/NemoClaw` but are absent from `PEFY-TECH/NemoClaw`. The resulting failures are lineage/history portability failures, not evidence that the current NVIDIA runtime is functionally broken.

## Required provenance model

Every promoted PEFY NemoClaw build must record all of the following identities separately:

1. `canonicalRepository`: `NVIDIA/NemoClaw`
2. `canonicalSourceSha`: exact NVIDIA commit qualified by PEFY
3. `pefyRepository`: `PEFY-TECH/NemoClaw`
4. `pefySourceSha`: exact PEFY commit containing only approved PEFY adaptations on top of the canonical source
5. `pefyPatchSetDigest`: deterministic digest of the approved PEFY delta, or an explicit EMPTY value when none exists
6. `workflowRepository` and `workflowSha`
7. `artifactId`, `artifactDigest`, `payloadSha256`
8. `build.sourceRevision`
9. `qualificationEvidenceId`

No field may silently substitute for another.

## Historical-reference policy

Canonical historical tags are evidence, not PEFY-owned releases.

PEFY MUST NOT:

- recreate NVIDIA tags with different objects
- retag PEFY-modified commits using canonical NVIDIA tag names
- silently import tags without verifying their canonical object identity
- use missing tags as justification to skip historical-upgrade tests

Approved approaches, in order of preference:

1. Historical test fixtures fetch or reference the canonical NVIDIA repository explicitly and verify the expected tag/object SHA before use.
2. If local mirroring is operationally required, canonical tag refs are mirrored read-only only after exact ref/object verification and are marked as vendor-origin evidence, never PEFY release tags.
3. PEFY release tags use an independent PEFY namespace/versioning convention.

## Fork-aware artifact validation

A future PEFY portability adapter may extend the provenance schema, but it MUST preserve these invariants:

- canonical source identity cannot be changed by the fork
- the PEFY patch set is explicit and digestible
- artifact payload identity is content-addressed
- artifact restore rejects repository/SHA/workflow mismatches
- no arbitrary caller may claim NVIDIA canonical identity
- downstream forks consume only an exact PEFY-qualified commit and its evidence bundle
- rollback identifies both canonical source and PEFY patch set

## Qualification treatment of current failures

- Artifact identity tests failing solely because they expect `NVIDIA/NemoClaw` in a PEFY fork are classified as `FORK_PROVENANCE_PORTABILITY_BLOCKER`, not runtime failure.
- Historical upgrade tests failing because canonical tags are absent from PEFY-TECH are classified as `CANONICAL_HISTORY_PORTABILITY_BLOCKER`, not runtime failure.
- Neither classification permits promotion until the portability controls above are implemented and re-tested.

## Security non-regression rules

PEFY adaptations MUST NOT:

- replace strict equality checks with wildcard repository acceptance
- trust repository names supplied only by untrusted input
- disable SHA/digest checks
- disable workflow/run-attempt binding
- bypass artifact content-addressing
- lower dependency/security audit thresholds
- skip historical upgrade compatibility purely because the fork lacks canonical history

## Promotion gate

PEFY-TECH/NemoClaw remains blocked until:

- current NVIDIA source baseline passes applicable product/security tests
- fork provenance portability is implemented and tested
- canonical historical upgrade fixtures run successfully through a verified NVIDIA reference source or verified mirror
- DCO/legal attestation is provided by an authorized human where required
- OpenClaw dependency compatibility is qualified separately
- target-host OpenShell policy, runtime, performance and recovery tests pass
- rollback from the PEFY candidate is demonstrated
