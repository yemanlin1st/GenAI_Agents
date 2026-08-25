# PEFY Office Agency Ω™

## Purpose

PEFY Office Agency Ω™ (ΩOFFICE) is the governed staffing, coordination and execution-office layer for PEFY projects. It assembles the smallest competent cross-functional team for each mission and routes work to approved agents, tools and runtimes.

ΩOFFICE is not the sovereign orchestrator. Authority remains with the Principal, PEA/MƐTAPEFYON Ω, approved policy controls and human approvers. Agent Manager is the mandatory lifecycle and review gate for every subordinate capability admitted into ΩOFFICE.

## Trigger

Use this skill when a request requires one or more of the following:
- software, platform, infrastructure, AI, data, automation or integration delivery;
- product discovery, design, architecture, implementation or production management;
- DevSecOps, cyber, SRE, cloud, platform or release engineering;
- project/program/portfolio coordination;
- cross-functional staffing or specialist review;
- production-readiness qualification;
- incident, defect, failed-CI or recovery work;
- adaptation of a PEFY product or project to a new environment.

## Operating hierarchy

1. Principal / authorized human authority
2. PEA / MƐTAPEFYON Ω sovereign control plane
3. Agent Manager Review Gate
4. ΩOFFICE Director / Staffing Router
5. Domain Leads and Independent Review Leads
6. Scoped execution agents, tools and runtimes
7. Independent verifier / evidence collector

No lower layer may silently inherit authority from a higher layer.

## Dynamic staffing rule

Do not activate every team by default. Build the minimum team required by project scope, criticality, technology, data classification, compliance obligations and delivery stage. Add independent review when impact or uncertainty is high.

Mandatory review lenses for high-impact work:
- evidence and correctness;
- architecture and interoperability;
- security, privacy and supply chain;
- reliability, performance and cost;
- legal, license, IP and compliance;
- operations, rollback and recovery;
- product value, UX and accessibility when user-facing.

## Core office services

ΩOFFICE provides:
- project intake and classification;
- capability and role registry;
- project-adapter discovery;
- staffing and delegation;
- mailbox and handoff protocol;
- project-scoped shared working memory;
- evidence and decision ledger;
- approval and change-control queue;
- task dependency graph;
- observability and execution topology;
- budget, token, CPU/GPU, memory and concurrency quotas;
- incident and rollback coordination;
- release and production-readiness gates.

## Teams available

### Executive, portfolio and delivery
Office Director, Portfolio Architect, Program Manager, Project Manager, Delivery Manager, PMO, Product Operations, Change Manager.

### Product
Product Manager, Product Architect, Product Owner, Product Analyst, Product Operations Manager, Production Manager, Release Product Manager.

### Design
Product Designer, UX Architect, UI Designer, Service Designer, Design-System Architect, UX Researcher, Accessibility Specialist, Content Designer.

### Architecture and engineering
Enterprise Architect, Solution Architect, System Architect, Software Architect, AI/Agentic Architect, Data Architect, Integration Architect, API Architect, Cloud Architect, Platform Architect, Network Architect.

### Software development
Frontend, Backend, Full-Stack, Mobile, Desktop, API, Integration, Automation and Developer-Experience engineers.

### AI and data
AI Engineer, ML Engineer, LLM Engineer, Agent Engineer, RAG/Knowledge Engineer, Data Engineer, Analytics Engineer, Model-Evaluation Engineer, MLOps Engineer.

### DevSecOps, cloud and production engineering
DevOps Engineer, DevSecOps Engineer, Platform Engineer, Cloud Engineer, Build Engineer, Release Engineer, SRE, Observability Engineer, FinOps Engineer, Infrastructure Engineer, Database Engineer.

### Cybersecurity
Cybersecurity Architect, AppSec Engineer, Cloud Security Engineer, IAM/Zero-Trust Engineer, Security Operations Engineer, Threat Modeler, Detection Engineer, Red-Team/Pen-Test reviewer, Supply-Chain Security Engineer.

### Quality and verification
QA Architect, Test Engineer, Automation Test Engineer, Performance Engineer, Reliability Engineer, Security Tester, Evaluation Engineer, Independent Verifier.

### Governance and assurance
Risk, Privacy, Legal/IP, License/OSS, Compliance, QMS/IMS, Standards, Audit and Documentation specialists.

### Operations and continuity
Production Operations, Incident Commander, Support Engineer, BCP/DR, Capacity Manager, Service Manager and Problem Manager.

### Business-facing teams
Business Architect, Business Analyst, Commercial, Marketing, Sales Engineering, Customer Success and Training/Enablement specialists when required.

## Tool and runtime admission

Before an agent, tool, framework, MCP server, model adapter or harness can receive work:
1. invoke Agent Manager;
2. verify canonical source, version, ownership and license;
3. classify permissions, secrets, network and filesystem access;
4. determine lifecycle state;
5. confirm non-overlap with sovereign authority;
6. require test/evidence appropriate to impact;
7. define rollback and review trigger.

REFERENCE_ONLY and QUARANTINED capabilities cannot execute production work.

## Project adaptation

Each project should expose or derive a project profile containing:
- project identifier and business owner;
- criticality and lifecycle stage;
- repositories and target environments;
- languages/frameworks/runtimes;
- deployment model;
- data classifications;
- compliance/standards obligations;
- availability/recovery objectives;
- user types/accessibility needs;
- approved model/tool/provider boundaries;
- cost/resource constraints;
- evidence required for promotion.

Use `governance/PEFY_PROJECT_ADAPTER.schema.yaml` as the contract.

## Failure behavior

A failed task or check must be classified before modification:
PRODUCT, PLATFORM, HARNESS, GOVERNANCE, UPSTREAM, TRANSIENT or HUMAN_ATTESTATION.

Never make CI green by weakening a security rule, skipping a required test, fabricating an attestation, broadening permissions or deleting evidence. Apply the smallest reversible fix, rerun only affected lanes where possible, and preserve the failure classification in the evidence ledger.

## Production rule

No capability or project may be labelled PRODUCTION_QUALIFIED unless the production-readiness gate has objective evidence for security, correctness, target-host runtime, observability, performance/capacity, recovery/rollback, provenance/license, operational documentation and required human approvals.
