# PEFY Agent Manager Review Gate

Status: GOVERNANCE CONTROL
Scope: agents, agentic frameworks, skills, tools, harnesses, MCP servers, workflow engines, model adapters and reviewer agents.

## Authority

The Agent Manager is a management and review layer. It is not the sovereign orchestrator.

Authority order:
1. Principal authority / approved human governance
2. PEA and MƐTAPEFYON Ω policy/control plane
3. Relevant Council Fabric and independent review lenses
4. Agent Manager Review Gate
5. Agents, tools, skills, harnesses and execution substrates
6. Independent verifiers

The Agent Manager may block, quarantine, downgrade or recommend retirement. It may not bypass human approvals, security policy, legal/IP constraints, evidence gates or rollback requirements.

## Mandatory review lifecycle

Every material agent/tool passes:

AM0 DISCOVER
- identity, source, owner, license, visibility and upstream
- role and intended authority
- dependency/runtime requirements
- overlap with existing capabilities

AM1 TRUST
- provenance and release integrity
- secrets and credential model
- network/egress and filesystem permissions
- sandbox and privilege boundary
- supply-chain/SBOM/scanning evidence when applicable

AM2 FIT
- architecture fit and interoperability
- duplicate-orchestrator detection
- authority collision detection
- data classification and privacy fit
- offline/self-hosted constraints when required

AM3 PROVE
- unit/integration/E2E evidence appropriate to risk
- security tests
- performance/resource baseline
- failure/retry/recovery behavior
- rollback evidence

AM4 ADMIT
Classify one of:
- REFERENCE_ONLY
- EXPERIMENTAL
- SANDBOX_QUALIFIED
- CONTROLLED_PILOT
- PRODUCTION_QUALIFIED
- QUARANTINED
- DEPRECATED
- RETIRED

AM5 OPERATE
- health and failure-rate review
- latency, memory, CPU/GPU and cost observation
- drift, release and vulnerability monitoring
- permission drift review
- output quality and policy-compliance sampling

AM6 CHANGE
- assess upstream release or local patch
- preserve local capability and IP
- stage migration
- re-run relevant proof gates
- approve, reject or backport narrowly

AM7 REVIEW OUTPUT
For high-impact work, the Agent Manager verifies that the producing agent:
- used the correct authority and data scope
- did not invent evidence
- respected tool permissions
- exposed uncertainty and blockers
- retained source/provenance links
- produced rollback/recovery information when changes were made
- was independently verified where required

AM8 RETIRE
- remove execution authority before removal
- preserve evidence and dependency map
- migrate consumers
- revoke credentials/tokens
- archive or delete only through approved change control

## Tool Review Gate

Before a new tool is treated as active capability, the Agent Manager records:
- tool identity and purpose
- canonical source and current version
- license and IP treatment
- required credentials
- minimum permissions
- network/data access
- installation/runtime location
- overlap with current tools
- security evidence
- compatibility evidence
- performance/resource evidence
- update policy
- rollback/uninstall path
- admission state

A tool discovered on GitHub, in a catalog or by another agent is not automatically trusted or installed.

## Conflict rules

- PEA/MƐTAPEFYON Ω retains routing and policy authority.
- Councils provide domain challenge and decision support.
- Agent Manager controls lifecycle, capability admission and agent/tool review.
- Verifiers test claims independently.
- Harnesses such as CrewAI, DeepSeek Harness, OpenClaw/NemoClaw, DeerFlow, n8n, OpenCode or MetaGPT remain subordinate execution/reference substrates unless separately promoted by evidence.

## Stop conditions

Immediately block or quarantine when any of the following is detected:
- secret exposure or uncontrolled credential persistence
- unbounded network/filesystem/command authority
- license/IP incompatibility
- unsigned or unexplained binary/source provenance at a sensitive boundary
- unreviewed breaking upstream change
- evidence fabrication or production-ready claim without proof
- authority collision with the sovereign control plane
- destructive migration without rollback
- repeated high-severity security findings without accepted treatment

## Review result format

Each review returns:
- capability
- current state
- risk tier
- evidence passed
- evidence missing
- blockers
- retained local capabilities/IP
- recommended action
- required approver
- rollback path
- next review trigger

This gate is mandatory for future material additions and major upgrades in the PEFY agentic portfolio.