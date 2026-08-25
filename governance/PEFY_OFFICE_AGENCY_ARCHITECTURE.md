# PEFY Office Agency Ω™ — Reference Architecture

## 1. Mission

PEFY Office Agency Ω™ (ΩOFFICE) is a reusable enterprise delivery office for all PEFY projects. It creates a project-scoped virtual organization from approved human and agentic capabilities, coordinates work, records evidence, and hands changes to established engineering/release systems.

It does not replace MƐTAPEFYON Ω, PEA, project owners, repositories, CI/CD systems or human accountability.

## 2. Authority model

Principal / Authorized Human
→ PEA / MƐTAPEFYON Ω
→ Agent Manager Review Gate
→ ΩOFFICE Director and Staffing Router
→ Project Cell
→ Domain Teams
→ Scoped Tools/Runtimes
→ Independent Verification
→ Change/Release Gate

Rules:
- policy authority and execution authority are separated;
- execution runtimes are replaceable adapters;
- secrets are brokered, never owned by office agents;
- no framework may become a second sovereign orchestrator;
- high-impact promotion requires independent evidence and authorized approval.

## 3. Control-plane services

### Project Registry
Creates a tenant/namespace per project and points to repositories, environments, owners, classifications and lifecycle state.

### Capability Registry
Maps every skill, agent, tool, MCP server, model adapter, harness and workflow to canonical source, version, authority, permissions, lifecycle state, owner and qualification evidence.

### Agent Manager Gate
Admits, reviews, quarantines, promotes, deprecates and retires subordinate capabilities.

### Staffing Router
Selects the smallest competent team from the role registry based on project profile, task type, risk and resource budget.

### Work Graph
Represents objectives, deliverables, dependencies, blockers, reviews, evidence and approvals as an auditable DAG. Cycles are detected before execution.

### Mailbox and Handoff Bus
Provides typed point-to-point and group messages for agent-to-agent and human-to-agent coordination. Handoffs include context hash, inputs, expected output, acceptance criteria, security label and owner.

### Project Memory
Project-scoped working memory with retention, access policy, provenance and data classification. Cross-project memory is denied unless explicitly authorized.

### Evidence Ledger
Stores source SHA, build/test identifiers, security scan status, benchmarks, approvals, waivers, artifacts, rollback reference and final promotion state.

### Policy and Approval Queue
Routes operations that change production, identity, secrets, infrastructure, legal/IP state or destructive data to authorized approval.

### Observability Plane
Captures task state, latency, retries, resource consumption, tool calls, failures, handoffs, queue depth and evidence completeness. It must support OpenTelemetry-compatible export and privacy-aware redaction.

### Resource Governor
Controls concurrency, model/API budget, token use, CPU/GPU/memory, storage, network egress, retry budgets and timeouts. Backpressure is mandatory when downstream capacity is saturated.

## 4. Execution adapters

ΩOFFICE may route work to approved adapters such as Codex, OpenCode, Claude Code distributions, DeepSeek Harness, CrewAI, DeerFlow, OpenClaw/NemoClaw, n8n, MCP services, CI runners and project-specific automation.

Adapters expose a common envelope:
- capability ID and lifecycle state;
- task and acceptance criteria;
- project namespace;
- allowed tools/data/network;
- budget/time limits;
- output/evidence contract;
- cancellation and rollback hooks.

Provider policy, identity, secrets and global orchestration remain outside the adapter.

## 5. Dynamic project cells

A Project Cell contains only roles needed for the current objective. Typical cells:

### Product discovery cell
Product Manager + Business Analyst + UX Research + Product Designer + Solution Architect + Security/Privacy reviewer.

### Build cell
Product Architect + Software Architect + Developers + DevSecOps + QA + SRE + AppSec + Documentation.

### AI/Agentic cell
AI/Agentic Architect + LLM/Agent Engineers + RAG/Data + Model Evaluation + Security + Platform/SRE + Product.

### Cyber/critical cell
Cybersecurity Architect + DevSecOps + IAM/Zero Trust + AppSec + Detection/Red Team + SRE + Risk/Compliance + independent verifier.

### Production-release cell
Production Manager + Release Engineer + SRE + QA + Security + Change Manager + Service Owner + rollback owner.

## 6. Lifecycle

INTAKE → CLASSIFY → STAFF → PLAN → EXECUTE → VERIFY → RED-TEAM/REVIEW → APPROVE → RELEASE → OBSERVE → LEARN.

Every transition has entry/exit criteria. A failed gate returns work to the appropriate stage with a typed failure classification rather than bypassing the control.

## 7. Failure taxonomy

- PRODUCT: source/product behavior is incorrect.
- PLATFORM: CI runner, OS, hosted service or external platform prevented valid execution.
- HARNESS: qualification/test harness is wrong or mismatched to the candidate.
- GOVERNANCE: policy, provenance, permissions or approval gate failed.
- UPSTREAM: source dependency or canonical upstream causes/contains the issue.
- TRANSIENT: non-reproducible contention/network/runner flake supported by rerun evidence.
- HUMAN_ATTESTATION: a legitimate human/legal approval is required.

A red check cannot be converted to green merely by relabelling. Evidence is required.

## 8. Production-readiness contract

Production promotion requires:
- deterministic or acceptably reproducible build;
- unit/integration/E2E evidence appropriate to risk;
- SAST/secret/dependency/supply-chain checks;
- target-host or equivalent runtime qualification;
- identity/secrets/data-boundary validation;
- availability, capacity, latency and failure-recovery evidence;
- backup/restore or rollback proof;
- observability/alerting/runbook ownership;
- license/provenance/notices;
- change approval and accountable owner;
- documented residual risks.

Source-level CI alone is never sufficient for production qualification.

## 9. Multi-project adaptation

ΩOFFICE is project-agnostic. A Project Adapter maps a project's actual repository and operational reality into the common control plane. Adapters must be thin and declarative. Project-specific business logic stays in the project.

Supported dimensions include web/SaaS, mobile, desktop, AI, data, FinTech, cybersecurity, infrastructure, WordPress, media/video, QSE/HSE, document-generation, research and other PEFY verticals.

## 10. Security baseline

- Zero Trust and least privilege;
- short-lived scoped credentials through an approved broker;
- no secret in prompts, logs or repository files;
- sandbox by default for untrusted/experimental tools;
- egress allowlisting where feasible;
- provenance/SBOM for releasable software;
- signed or attestable artifacts where supported;
- immutable evidence references;
- two-person control for break-glass/high-consequence actions when configured;
- explicit data retention and deletion policies.

## 11. Efficiency baseline

Only the minimum team and minimum context necessary are activated. Work is parallelized only where dependencies allow it. Expensive models/runtimes are selected by task value and evidence need. Cached/reusable evidence is accepted only when candidate SHA, environment and policy scope still match.

## 12. Ownership

The PEFY Office Agency architecture, PEFY-specific policies, role composition, adapters, governance contracts and proprietary implementations are PEFY-owned assets subject to applicable corporate IP governance. Third-party components retain their own licenses and attribution requirements.
