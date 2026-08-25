# PEFY Sovereign Control-Plane Migration Plan

## Problem
PEFY-specific governance, council logic, skills, release intelligence and account-control material currently coexist inside repositories that are forks of external projects. This increases upstream conflict, accidental disclosure, maintenance burden and ownership ambiguity.

## Target state
Create a dedicated private PEFY-owned control-plane repository. It becomes the authoritative source for:
- MƐTAPEFYON Ω / MƐTAFLOW Ω orchestration policy
- PEA operating rules
- council/counsellor routing and review policies
- capability registry and authority map
- skill manifests and internal adapters
- upstream delta ledger and release intelligence
- security, approval and change-control policy
- qualification matrices and performance baselines
- evidence schemas, audit reports and rollback records
- proprietary integration contracts

External/forked repositories remain implementation substrates, references or vendor/upstream mirrors.

## Repository boundaries
### Private control plane
Must contain only PEFY-owned or properly licensed reusable governance/configuration/code. Client secrets, credentials and regulated data remain in approved secret/data stores, not Git.

### Upstream mirrors/forks
Contain upstream code plus the smallest necessary PEFY adapter delta. Avoid account governance documents inside application forks.

### Product repositories
Contain product-specific code and public-safe documentation. Import control-plane behavior through versioned adapters/policies rather than copy/paste.

## Migration sequence
1. Create a private repository under the intended PEFY ownership namespace.
2. Enable branch protection, required review, secret scanning, dependency/security checks and signed/provenance-aware release practices where supported.
3. Copy governance and skill assets with provenance and history references.
4. Classify every copied item public/internal/confidential/restricted.
5. Remove or redact anything inappropriate for a control repository.
6. Create versioned policy bundles and adapter interfaces.
7. Point Codex, CrewAI, DeerFlow, DeepSeek Harness, OpenClaw, OpenCode, n8n and other runtimes to the control plane through thin adapters.
8. Validate behavior in sandbox.
9. Freeze new PEFY governance additions to external forks.
10. After validation, replace duplicated governance copies with pointers/adapters where practical.
11. Retain migration evidence and rollback refs.

## Codex special migration
The current `yemanlin1st/codex` fork has a U3 divergent state with a PEFY documentation/MCP delta. Preserve `pefy-delta/2026-06-16`, use `upstream-sync/2026-08-25` as clean code baseline, extract PEFY-owned governance to the private control plane, then reapply only code-level integrations still needed against current upstream.

## Acceptance gates
- private authoritative destination exists
- ownership and access model approved
- no secrets or restricted client data committed
- provenance and licenses documented
- all PEFY governance assets inventoried
- adapters tested against at least one current runtime
- rollback path verified
- old fork locations marked non-authoritative
- monitoring/watchlists point to the new source of truth

## Stop rule
Do not delete the existing PEFY governance content from forks until the private destination is created, validated, backed up and accepted.
