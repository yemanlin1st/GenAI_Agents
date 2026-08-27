# TrueForge Harness Adapter

## Status
Approved subordinate execution harness for PEFY/MƐTAPEFYON Ω. It does not replace the sovereign orchestration, security, governance, model-routing or approval layers.

## Verified upstream capabilities
TrueForge provides an agent execution loop with multi-provider model connectivity, MCP tools, git-backed skills, sandbox-as-tool, approvals, subagents, deferred tool loading, context compaction, session persistence, HTTP API/TypeScript SDK and embeddable chat UI.

## Version policy
Initial validated integration target:
- `@truefoundry/trueforge`: `0.1.4`
- `@truefoundry/trueforge-sdk`: `0.1.4`
- `@truefoundry/trueforge-ui`: `0.2.4`

Re-verify versions before every upgrade. Major/minor changes are not auto-promoted.

## Runtime placement
MƐTAPEFYON Ω → policy/router → TrueForge adapter → agent loop → model/MCP/skills/sandbox → evidence/telemetry → PEFY verifier.

## Local evaluation mode
Use only on localhost. Local mode is for development/evaluation and should not be exposed to the internet without the shared/hosted security model.

## Hosted/production-like mode
Require:
- authenticated access, preferably OIDC where supported
- Postgres-backed persistence where appropriate
- Redis only when required by the selected deployment architecture
- TLS termination
- network segmentation and egress policy
- secrets outside repository and prompt content
- sandbox isolation
- explicit tool approvals for privileged/destructive actions
- audit/event export into PEFY observability
- backup, restore and rollback procedure

## PEFY routing rules
Choose TrueForge when at least one applies:
- persistent multi-turn agent sessions are valuable
- MCP resource catalogs are needed
- sandbox-as-tool is needed
- deferred tool loading or subagents materially reduce context cost
- an embeddable agent UI/API is required
- reproducible harness benchmarking is required

Do not choose TrueForge solely because it exists. Compare against DeepSeek Harness, CrewAI, DeerFlow, OpenClaw, native provider agents or direct tool execution using cost, latency, memory, reliability, security, maintainability and task success rate.

## Security constraints
- least privilege by default
- no blanket tool authorization
- no permission-bypass flags as standard configuration
- secrets remain externalized
- sandbox network access is deny-by-default when practical
- high-risk tools require human approval
- logs/trajectories are reviewed for sensitive data
- third-party skills are treated as untrusted until reviewed
- MCP servers require provenance and authentication review

## Evidence contract
Each qualifying run should capture: runtime version, agent profile version, selected model, tool/MCP set, approval events, sandbox identity, task outcome, errors/retries, latency, token/cost metrics where available, verifier result and rollback reference.

## Upgrade gate
Verify source authenticity → changelog/release delta → dependency/license/security impact → sandbox test → interoperability regression → benchmark → approval → staged promotion → rollback retained.
