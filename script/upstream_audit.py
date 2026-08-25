#!/usr/bin/env python3
"""Read-only upstream drift and release intelligence auditor for PEFY repositories.

Uses only the Python standard library. It never mutates repositories.

Token precedence:
1. PEFY_PORTFOLIO_TOKEN - recommended for explicitly authorized portfolio/private access.
2. GITHUB_TOKEN - useful in GitHub Actions for the current repository and public data.
3. no token - public GitHub API with lower rate limits.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

API = "https://api.github.com"
USER_AGENT = "PEFY-Upstream-Audit/1.0"


def token() -> str | None:
    return os.getenv("PEFY_PORTFOLIO_TOKEN") or os.getenv("GITHUB_TOKEN") or None


def request_json(path_or_url: str, *, allow_404: bool = False) -> Any:
    url = path_or_url if path_or_url.startswith("https://") else f"{API}{path_or_url}"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": USER_AGENT,
    }
    tok = token()
    if tok:
        headers["Authorization"] = f"Bearer {tok}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        if allow_404 and exc.code == 404:
            return None
        body = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"GitHub API {exc.code} for {url}: {body}") from exc


def iso_age_days(value: str | None) -> int | None:
    if not value:
        return None
    try:
        when = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
        now = dt.datetime.now(dt.timezone.utc)
        return max(0, (now - when).days)
    except ValueError:
        return None


def license_id(meta: dict[str, Any] | None) -> str | None:
    if not meta:
        return None
    lic = meta.get("license") or {}
    return lic.get("spdx_id") or lic.get("key")


def state_from_compare(compare: dict[str, Any] | None, upstream_meta: dict[str, Any] | None) -> str:
    if upstream_meta and (upstream_meta.get("archived") or upstream_meta.get("disabled")):
        return "U4"
    if not compare:
        return "UNKNOWN"
    ahead = int(compare.get("ahead_by") or 0)
    behind = int(compare.get("behind_by") or 0)
    if ahead == 0 and behind == 0:
        return "U0"
    if ahead == 0 and behind > 0:
        return "U1"
    if ahead > 0 and behind == 0:
        return "U2"
    if ahead > 0 and behind > 0:
        return "U3"
    return "UNKNOWN"


def drift_scale(behind: int) -> str:
    if behind == 0:
        return "none"
    if behind < 50:
        return "small"
    if behind < 500:
        return "medium"
    if behind < 2000:
        return "large"
    if behind < 10000:
        return "migration-scale"
    return "extreme-migration-scale"


def latest_signal(repo: str) -> dict[str, Any]:
    release = request_json(f"/repos/{repo}/releases/latest", allow_404=True)
    tags = request_json(f"/repos/{repo}/tags?per_page=1", allow_404=True) or []
    return {
        "latest_release": release.get("tag_name") if release else None,
        "latest_release_published_at": release.get("published_at") if release else None,
        "latest_tag": tags[0].get("name") if tags else None,
    }


def compare_fork(local_meta: dict[str, Any], upstream_meta: dict[str, Any]) -> dict[str, Any] | None:
    local_full = local_meta["full_name"]
    local_owner = local_meta["owner"]["login"]
    local_branch = local_meta["default_branch"]
    upstream_full = upstream_meta["full_name"]
    upstream_branch = upstream_meta["default_branch"]

    if local_full == upstream_full:
        return None

    spec = f"{urllib.parse.quote(upstream_branch, safe='')}...{urllib.parse.quote(local_owner, safe='')}:{urllib.parse.quote(local_branch, safe='')}"
    return request_json(f"/repos/{upstream_full}/compare/{spec}", allow_404=True)


def audit_entry(entry: dict[str, Any]) -> dict[str, Any]:
    repo = entry["repository"]
    result: dict[str, Any] = {
        "repository": repo,
        "priority": entry.get("priority", "P2"),
        "checked_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "upstream_only": bool(entry.get("upstream_only")),
    }
    try:
        local = request_json(f"/repos/{repo}")
        result.update(
            {
                "visibility": local.get("visibility"),
                "default_branch": local.get("default_branch"),
                "local_pushed_at": local.get("pushed_at"),
                "local_license": license_id(local),
                "local_archived": bool(local.get("archived")),
            }
        )
        result.update(latest_signal(repo))

        if entry.get("upstream_only"):
            result.update(
                {
                    "upstream": repo,
                    "state": "UPSTREAM_ONLY",
                    "upstream_pushed_at": local.get("pushed_at"),
                    "upstream_dormancy_days": iso_age_days(local.get("pushed_at")),
                    "upstream_license": license_id(local),
                }
            )
            return result

        upstream_ref = entry.get("upstream")
        if not upstream_ref and local.get("fork"):
            parent = local.get("parent") or local.get("source")
            upstream_ref = parent.get("full_name") if parent else None

        if not upstream_ref:
            result.update({"state": "NO_UPSTREAM", "upstream": None})
            return result

        upstream = request_json(f"/repos/{upstream_ref}")
        result.update(
            {
                "upstream": upstream_ref,
                "upstream_default_branch": upstream.get("default_branch"),
                "upstream_pushed_at": upstream.get("pushed_at"),
                "upstream_dormancy_days": iso_age_days(upstream.get("pushed_at")),
                "upstream_license": license_id(upstream),
                "upstream_archived": bool(upstream.get("archived")),
                "upstream_disabled": bool(upstream.get("disabled")),
            }
        )
        upstream_signal = latest_signal(upstream_ref)
        result.update({f"upstream_{key}": value for key, value in upstream_signal.items()})

        compare = compare_fork(local, upstream)
        if compare:
            ahead = int(compare.get("ahead_by") or 0)
            behind = int(compare.get("behind_by") or 0)
            result.update(
                {
                    "state": state_from_compare(compare, upstream),
                    "ahead_by": ahead,
                    "behind_by": behind,
                    "drift_scale": drift_scale(behind),
                    "merge_base": (compare.get("merge_base_commit") or {}).get("sha"),
                    "local_head": (compare.get("head_commit") or {}).get("sha"),
                    "upstream_head": (compare.get("base_commit") or {}).get("sha"),
                }
            )
        else:
            result["state"] = "UNKNOWN"

        local_lic = result.get("local_license")
        upstream_lic = result.get("upstream_license")
        result["license_delta"] = bool(local_lic and upstream_lic and local_lic != upstream_lic)
        return result
    except Exception as exc:  # noqa: BLE001 - evidence collector must continue portfolio run
        result["state"] = "ERROR"
        result["error"] = str(exc)
        return result


def severity_key(row: dict[str, Any]) -> tuple[int, int]:
    p = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}.get(row.get("priority"), 9)
    state = {"ERROR": 0, "U4": 1, "U3": 2, "U1": 3, "U2": 4, "UNKNOWN": 5, "NO_UPSTREAM": 6, "U0": 7, "UPSTREAM_ONLY": 8}.get(row.get("state"), 9)
    return p, state


def recommendation(row: dict[str, Any]) -> str:
    if row.get("state") == "ERROR":
        return "restore audit visibility before change"
    if row.get("license_delta"):
        return "block promotion; reconcile license/provenance first"
    state = row.get("state")
    if state == "U3":
        return "preserve local delta; perform controlled three-way migration"
    if state == "U1":
        return "create qualification branch; test before fast-forward/migration"
    if state == "U2":
        return "preserve local overlay; monitor upstream equivalence"
    if state == "U4":
        return "freeze upgrades; identify supported successor or migration path"
    if state == "U0":
        return "no sync required; continue release/security watch"
    if state == "UPSTREAM_ONLY":
        return "track releases/tags/security; pin before production use"
    if state == "NO_UPSTREAM":
        return "classify as PEFY-owned, vendor mirror, or untracked external source"
    return "review manually"


def render_markdown(rows: list[dict[str, Any]]) -> str:
    lines = [
        "# PEFY Upstream Audit",
        "",
        f"Generated: {dt.datetime.now(dt.timezone.utc).isoformat()}",
        "",
        "| Priority | Repository | State | Ahead | Behind | Scale | License delta | Recommendation |",
        "|---|---|---:|---:|---:|---|---|---|",
    ]
    for row in sorted(rows, key=severity_key):
        lines.append(
            "| {priority} | {repository} | {state} | {ahead} | {behind} | {scale} | {license_delta} | {recommendation} |".format(
                priority=row.get("priority", ""),
                repository=row.get("repository", ""),
                state=row.get("state", ""),
                ahead=row.get("ahead_by", ""),
                behind=row.get("behind_by", ""),
                scale=row.get("drift_scale", ""),
                license_delta="YES" if row.get("license_delta") else "no",
                recommendation=recommendation(row).replace("|", "/"),
            )
        )
    lines.extend(
        [
            "",
            "## Rules",
            "",
            "- This report is read-only evidence. It is not approval to merge or upgrade.",
            "- U3 requires explicit local-delta preservation.",
            "- License deltas block promotion until reconciled.",
            "- Developer-preview/upstream-only components remain unqualified until pinned and tested.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watchlist", default="governance/UPSTREAM_WATCHLIST.json")
    parser.add_argument("--out-dir", default="artifacts/upstream-audit")
    args = parser.parse_args()

    watchlist_path = pathlib.Path(args.watchlist)
    data = json.loads(watchlist_path.read_text(encoding="utf-8"))
    rows = [audit_entry(entry) for entry in data.get("repositories", [])]

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_version": "1.0",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "token_mode": "portfolio" if os.getenv("PEFY_PORTFOLIO_TOKEN") else ("github-actions" if os.getenv("GITHUB_TOKEN") else "anonymous-public"),
        "results": sorted(rows, key=severity_key),
    }
    (out_dir / "upstream-audit.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out_dir / "upstream-audit.md").write_text(render_markdown(rows), encoding="utf-8")

    errors = [row for row in rows if row.get("state") == "ERROR"]
    print(render_markdown(rows))
    if errors:
        print(f"Audit completed with {len(errors)} visibility/API errors.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
