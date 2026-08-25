# PEFY Failure Remediation

## Purpose

Use this skill to diagnose and remediate failed CI/CD checks, tests, builds, deployments, agent tasks, migrations, integrations and production-readiness gates across PEFY projects.

The objective is not cosmetic green status. The objective is a verified, minimal, reversible correction that preserves or strengthens assurance.

## Required loop

1. INVENTORY
   - identify failed, cancelled, skipped, queued and missing checks;
   - bind each observation to repository/project, SHA, workflow/job/test and environment.
2. CLASSIFY
   - PRODUCT;
   - PLATFORM;
   - HARNESS;
   - GOVERNANCE;
   - UPSTREAM;
   - TRANSIENT;
   - HUMAN_ATTESTATION.
3. REPRODUCE OR DISPROVE
   - inspect logs/source/config;
   - rerun the smallest affected lane when transient failure is plausible;
   - use focused qualification probes for expensive matrices.
4. ROOT CAUSE
   - distinguish symptom from initiating cause;
   - identify whether local changes, upstream drift, environment, permissions, toolchain, dependency or policy caused the failure.
5. DESIGN FIX
   - smallest reversible change;
   - no permission broadening unless explicitly justified and approved;
   - no deletion/skip/timeout inflation used as a first-line fix;
   - preserve upstream compatibility where practical.
6. APPLY IN ISOLATION
   - qualification/remediation branch;
   - preserve rollback SHA;
   - separate product patches from CI/platform patches.
7. VERIFY
   - rerun affected test plus adjacent regression surface;
   - record PASS/FAIL/SKIP/CANCEL separately;
   - validate security, performance and compatibility impact.
8. REVIEW
   - Agent Manager for capability/tool implications;
   - relevant council/reviewer lenses;
   - human approval where legally or operationally required.
9. PROMOTE
   - only after required evidence is complete;
   - never merge qualification-only trigger branches.
10. LEARN
   - update reusable test/harness/policy when the root cause reveals a systemic weakness.

## Anti-patterns prohibited

- disabling security checks to obtain green CI;
- blanket `continue-on-error` for required gates;
- fabricating DCO/sign-off/identity/approval;
- force-resetting a branch to upstream without preserving local work;
- `npm audit fix --force` or analogous breaking mass-upgrade without qualification;
- blindly raising all timeouts;
- classifying a missing/skipped test as pass;
- using a qualification trigger PR as a production patch;
- merging a test harness into runtime code without review;
- claiming the entire portfolio is failure-free without portfolio-wide current evidence.

## Optimization

Prefer targeted reruns, focused probes and cached evidence tied to immutable candidate SHA. Parallelize independent investigations. Do not repeatedly execute expensive lanes whose known blocker is unchanged.

## Production escalation

Any failed production deployment, security gate, data migration, recovery test, identity control or integrity/provenance control is P0 until classified. Production promotion remains blocked until resolution or an authorized, documented risk acceptance exists.
