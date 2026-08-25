#!/usr/bin/env python3
"""PEFY upstream drift auditor.

Read-only by design. Enumerates accessible repositories owned by GITHUB_OWNER,
identifies GitHub forks, verifies their parent repositories, computes default-
branch ahead/behind state, detects basic license/default-branch drift, and emits
JSON + Markdown reports.

Environment:
  GITHUB_OWNER              account owner to audit (default: yemanlin1st)
  GH_TOKEN / GITHUB_TOKEN   optional GitHub token; never printed
  OUTPUT_DIR                report destination (default: artifacts/upstream)
  MAX_REPOS                 optional positive integer limit for controlled tests

The script performs no repository mutation.
"""

from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

API = "https://api.github.com"
OWNER = os.getenv("GITHUB_OWNER", "yemanlin1st")
TOKEN = os.getenv("GH_TOKEN") or os.getenv("GITHUB_TOKEN") or ""
OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", "artifacts/upstream"))
MAX_REPOS = int(os.getenv("MAX_REPOS", "0") or 0)
USER_AGENT = "PEFY-Upstream-Audit/1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _headers() -> dict[str, str]:
    h = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    if TOKEN:
        h["Authorization"] = f"Bearer {TOKEN}"
    return h


def gh_get(path_or_url: str, *, allow_404: bool = False, retries: int = 3) -> Any:
    url = path_or_url if path_or_url.startswith("http") else f"{API}{path_or_url}"
    last_error: Exception | None = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers=_headers(), method="GET")
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else None
        except urllib.error.HTTPError as exc:
            if exc.code == 404 and allow_404:
                return None
            if exc.code in (403, 429) and attempt + 1 < retries:
                retry_after = exc.headers.get("Retry-After")
                time.sleep(int(retry_after) if retry_after and retry_after.isdigit() else 2 ** attempt)
                last_error = exc
                continue
            raise
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < retries:
                time.sleep(2 ** attempt)
                continue
            raise
    if last_error:
        raise last_error
    raise RuntimeError(f"GitHub request failed without exception: {url}")


def paged(path: str) -> Iterable[dict[str, Any]]:
    page = 1
    while True:
        sep = "&" if "?" in path else "?"
        items = gh_get(f"{path}{sep}per_page=100&page={page}")
        if not items:
            return
        for item in items:
            yield item
        if len(items) < 100:
            return
        page += 1


def enumerate_owned_repos() -> list[dict[str, Any]]:
    # Public path is reliable with both anonymous and installation tokens.
    repos = list(paged(f"/users/{urllib.parse.quote(OWNER)}/repos?type=owner&sort=full_name"))

    # If a user-scoped token is supplied, attempt to augment with private repos.
    if TOKEN:
        try:
            private_visible = list(paged("/user/repos?affiliation=owner&visibility=all&sort=full_name"))
            by_id = {r["id"]: r for r in repos}
            for repo in private_visible:
                if repo.get("owner", {}).get("login", "").lower() == OWNER.lower():
                    by_id[repo["id"]] = repo
            repos = list(by_id.values())
        except urllib.error.HTTPError:
            # A repository-scoped GITHUB_TOKEN may not support /user/repos.
            pass

    repos.sort(key=lambda r: r.get("full_name", "").lower())
    if MAX_REPOS > 0:
        repos = repos[:MAX_REPOS]
    return repos


def spdx(license_obj: dict[str, Any] | None) -> str | None:
    if not license_obj:
        return None
    return license_obj.get("spdx_id") or license_obj.get("key")


def divergence_class(ahead: int | None, behind: int | None, parent_archived: bool) -> str:
    if parent_archived:
        return "U4_ORPHANED_OR_ARCHIVED"
    if ahead is None or behind is None:
        return "UNKNOWN"
    if ahead == 0 and behind == 0:
        return "U0_CLEAN"
    if ahead == 0 and behind > 0:
        return "U1_BEHIND_ONLY"
    if ahead > 0 and behind == 0:
        return "U2_AHEAD_ONLY"
    if ahead > 0 and behind > 0:
        return "U3_DIVERGED"
    return "UNKNOWN"


def sync_scale(behind: int | None) -> str:
    if behind is None or behind <= 0:
        return "none"
    if behind <= 20:
        return "small"
    if behind <= 200:
        return "medium"
    if behind <= 1000:
        return "large"
    return "migration_scale"


def recommendation(kind: str, behind: int | None) -> str:
    if kind == "U0_CLEAN":
        return "No sync required; continue release/security monitoring."
    if kind == "U1_BEHIND_ONLY":
        scale = sync_scale(behind)
        if scale == "small":
            return "Review changelog/security impact; use reviewable PR or fast-forward; run gates."
        if scale == "medium":
            return "Use integration branch or native fork sync; run compatibility/security regression."
        if scale == "large":
            return "Prefer native fork sync/fast-forward over giant PR; full regression and rollback proof."
        return "Treat as migration-scale synchronization: preserve head, assess breaking changes/license/runtime/migrations, sync in controlled environment, then full qualification."
    if kind == "U2_AHEAD_ONLY":
        return "Preserve and classify local commits; upstream generic fixes where appropriate; do not reset."
    if kind == "U3_DIVERGED":
        return "Create preservation ref, classify local-only commits, integrate current upstream on clean branch, replay approved deltas, resolve conflicts, run full gates."
    if kind == "U4_ORPHANED_OR_ARCHIVED":
        return "Freeze automatic update; verify successor, license, ownership and migration strategy."
    return "Manual upstream relationship review required."


@dataclass
class ForkAudit:
    repository: str
    visibility: str
    default_branch: str
    fork_head_sha: str | None
    fork_pushed_at: str | None
    parent: str | None
    parent_default_branch: str | None
    parent_head_sha: str | None
    parent_pushed_at: str | None
    parent_archived: bool
    ahead_by: int | None
    behind_by: int | None
    divergence: str
    sync_scale: str
    fork_license: str | None
    parent_license: str | None
    license_drift: bool
    branch_name_mismatch: bool
    recommendation: str
    error: str | None = None


def audit_fork(repo_summary: dict[str, Any]) -> ForkAudit:
    full_name = repo_summary["full_name"]
    try:
        repo = gh_get(f"/repos/{full_name}")
        parent = repo.get("parent") or repo.get("source")
        if not parent:
            raise RuntimeError("fork=true but GitHub returned no parent/source")

        parent_name = parent["full_name"]
        fork_branch = repo["default_branch"]
        parent_branch = parent["default_branch"]

        # GitHub compare accepts cross-fork head syntax owner:branch.
        head_owner = repo["owner"]["login"]
        compare_spec = f"{urllib.parse.quote(parent_branch, safe='')}...{urllib.parse.quote(head_owner, safe='')}:{urllib.parse.quote(fork_branch, safe='')}"
        comparison = gh_get(f"/repos/{parent_name}/compare/{compare_spec}")

        ahead = comparison.get("ahead_by")
        behind = comparison.get("behind_by")
        kind = divergence_class(ahead, behind, bool(parent.get("archived")))

        return ForkAudit(
            repository=full_name,
            visibility=repo.get("visibility", "unknown"),
            default_branch=fork_branch,
            fork_head_sha=(comparison.get("head_commit") or {}).get("sha"),
            fork_pushed_at=repo.get("pushed_at"),
            parent=parent_name,
            parent_default_branch=parent_branch,
            parent_head_sha=(comparison.get("base_commit") or {}).get("sha"),
            parent_pushed_at=parent.get("pushed_at"),
            parent_archived=bool(parent.get("archived")),
            ahead_by=ahead,
            behind_by=behind,
            divergence=kind,
            sync_scale=sync_scale(behind),
            fork_license=spdx(repo.get("license")),
            parent_license=spdx(parent.get("license")),
            license_drift=spdx(repo.get("license")) != spdx(parent.get("license")),
            branch_name_mismatch=fork_branch != parent_branch,
            recommendation=recommendation(kind, behind),
        )
    except Exception as exc:  # report failures without aborting whole portfolio
        return ForkAudit(
            repository=full_name,
            visibility=repo_summary.get("visibility", "unknown"),
            default_branch=repo_summary.get("default_branch", "unknown"),
            fork_head_sha=None,
            fork_pushed_at=repo_summary.get("pushed_at"),
            parent=None,
            parent_default_branch=None,
            parent_head_sha=None,
            parent_pushed_at=None,
            parent_archived=False,
            ahead_by=None,
            behind_by=None,
            divergence="UNKNOWN",
            sync_scale="unknown",
            fork_license=spdx(repo_summary.get("license")),
            parent_license=None,
            license_drift=False,
            branch_name_mismatch=False,
            recommendation="Manual review required because automated audit failed.",
            error=f"{type(exc).__name__}: {exc}",
        )


def write_reports(repos: list[dict[str, Any]], audits: list[ForkAudit]) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    generated = utc_now()

    counts: dict[str, int] = {}
    for a in audits:
        counts[a.divergence] = counts.get(a.divergence, 0) + 1

    payload = {
        "schema_version": "1.0",
        "generated_at": generated,
        "owner": OWNER,
        "scope_note": "Private repositories are included only if the supplied token can enumerate them.",
        "repositories_seen": len(repos),
        "forks_audited": len(audits),
        "counts": counts,
        "audits": [asdict(a) for a in audits],
    }
    json_path = OUTPUT_DIR / "upstream-audit.json"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    md: list[str] = [
        "# PEFY Upstream Drift Audit",
        "",
        f"Generated: {generated}",
        f"Owner: `{OWNER}`",
        f"Repositories seen: **{len(repos)}**",
        f"Forks audited: **{len(audits)}**",
        "",
        "> Private repositories are included only when the supplied token can enumerate them. This report is read-only evidence, not a production qualification.",
        "",
        "## Summary",
        "",
    ]
    for key in sorted(counts):
        md.append(f"- {key}: **{counts[key]}**")

    md.extend([
        "",
        "## Fork status",
        "",
        "| Repository | Upstream | State | Ahead | Behind | Scale | License drift | Recommendation |",
        "|---|---|---:|---:|---:|---|---|---|",
    ])
    for a in sorted(audits, key=lambda x: ((x.behind_by or 0), (x.ahead_by or 0)), reverse=True):
        err = f" ERROR: {a.error}" if a.error else ""
        md.append(
            f"| `{a.repository}` | `{a.parent or 'unknown'}` | {a.divergence} | "
            f"{a.ahead_by if a.ahead_by is not None else '?'} | "
            f"{a.behind_by if a.behind_by is not None else '?'} | {a.sync_scale} | "
            f"{'yes' if a.license_drift else 'no'} | {a.recommendation}{err} |"
        )

    md.extend([
        "",
        "## Interpretation",
        "",
        "- U0 CLEAN: no synchronization required.",
        "- U1 BEHIND-ONLY: upstream can usually be integrated without preserving local-only commits, but all change gates still apply.",
        "- U2 AHEAD-ONLY: preserve and classify local value before any reset or upstream contribution.",
        "- U3 DIVERGED: preservation + controlled replay/rebase/cherry-pick strategy required.",
        "- U4 ORPHANED/ARCHIVED: ownership/successor decision required before updates.",
        "",
        "Never perform force-push, destructive reset, production upgrade, or license acceptance from this report alone.",
    ])

    md_path = OUTPUT_DIR / "upstream-audit.md"
    md_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return json_path, md_path


def main() -> int:
    repos = enumerate_owned_repos()
    forks = [r for r in repos if r.get("fork")]
    audits = [audit_fork(r) for r in forks]
    json_path, md_path = write_reports(repos, audits)

    print(f"PEFY upstream audit complete: repos={len(repos)} forks={len(audits)}")
    print(f"JSON: {json_path}")
    print(f"Markdown: {md_path}")

    unknown = sum(1 for a in audits if a.divergence == "UNKNOWN")
    if unknown:
        print(f"WARNING: {unknown} fork(s) require manual upstream review.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
