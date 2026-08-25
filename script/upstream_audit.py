#!/usr/bin/env python3
"""Read-only upstream drift and release intelligence auditor for PEFY repositories.

The auditor is intentionally non-mutating. It inventories repository lineage,
release/tag signals, branch heads, effective license evidence and fork drift so that
a separate governed change process can decide whether to synchronize, migrate,
backport, preserve a PEFY delta, or take no action.

Token precedence:
1. PEFY_PORTFOLIO_TOKEN - explicitly authorized portfolio/private access.
2. GITHUB_TOKEN - GitHub Actions token; usually current repo + public data.
3. no token - public GitHub API with lower rate limits.
"""

from __future__ import annotations

import argparse
import base64
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
USER_AGENT = "PEFY-Upstream-Audit/1.2"
_CACHE: dict[str, Any] = {}
LICENSE_CANDIDATES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING", "COPYING.md")


def token() -> str | None:
    return os.getenv("PEFY_PORTFOLIO_TOKEN") or os.getenv("GITHUB_TOKEN") or None


def request_json(path_or_url: str, *, allow_404: bool = False) -> Any:
    url = path_or_url if path_or_url.startswith("https://") else f"{API}{path_or_url}"
    if url in _CACHE:
        return _CACHE[url]

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
            data = json.loads(response.read().decode("utf-8"))
            _CACHE[url] = data
            return data
    except urllib.error.HTTPError as exc:
        if allow_404 and exc.code == 404:
            _CACHE[url] = None
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


def metadata_license(meta: dict[str, Any] | None) -> str | None:
    if not meta:
        return None
    lic = meta.get("license") or {}
    return lic.get("spdx_id") or lic.get("key")


def detect_license_text(text: str) -> str | None:
    normalized = " ".join(text.replace("\r", "\n").split())
    upper = normalized.upper()

    if "MIT LICENSE" in upper and "PERMISSION IS HEREBY GRANTED" in upper:
        return "MIT"
    if "APACHE LICENSE" in upper and "VERSION 2.0" in upper:
        return "Apache-2.0"
    if "GNU AFFERO GENERAL PUBLIC LICENSE" in upper and "VERSION 3" in upper:
        return "AGPL-3.0"
    if "GNU GENERAL PUBLIC LICENSE" in upper and "VERSION 3" in upper:
        return "GPL-3.0"
    if "GNU GENERAL PUBLIC LICENSE" in upper and "VERSION 2" in upper:
        return "GPL-2.0"
    if "GNU LESSER GENERAL PUBLIC LICENSE" in upper and "VERSION 3" in upper:
        return "LGPL-3.0"
    if "MOZILLA PUBLIC LICENSE" in upper and "VERSION 2.0" in upper:
        return "MPL-2.0"
    if "BOOST SOFTWARE LICENSE" in upper and "VERSION 1.0" in upper:
        return "BSL-1.0"
    if "BSD 3-CLAUSE" in upper:
        return "BSD-3-Clause"
    if "BSD 2-CLAUSE" in upper:
        return "BSD-2-Clause"
    return None


def effective_license(repo: str, meta: dict[str, Any]) -> tuple[str, str]:
    detected = metadata_license(meta)
    if detected and str(detected).upper() not in {"NOASSERTION", "OTHER", "UNKNOWN"}:
        return str(detected), "github_metadata"

    for candidate in LICENSE_CANDIDATES:
        path = urllib.parse.quote(candidate, safe="")
        content = request_json(f"/repos/{repo}/contents/{path}", allow_404=True)
        if not isinstance(content, dict) or content.get("type") != "file":
            continue
        encoded = content.get("content")
        if not encoded or content.get("encoding") != "base64":
            continue
        try:
            raw = base64.b64decode(encoded.replace("\n", ""), validate=False)
            text = raw.decode("utf-8", errors="replace")
        except Exception:
            continue
        recognized = detect_license_text(text)
        if recognized:
            return recognized, f"file:{candidate}"

    unresolved = str(detected) if detected else "UNKNOWN"
    return unresolved, "unresolved"


def embedded_full_name(value: Any) -> str | None:
    return value.get("full_name") if isinstance(value, dict) else None


def branch_head(repo: str, branch: str) -> str | None:
    commit = request_json(
        f"/repos/{repo}/commits/{urllib.parse.quote(branch, safe='')}",
        allow_404=True,
    )
    return commit.get("sha") if isinstance(commit, dict) else None


def latest_signal(repo: str) -> dict[str, Any]:
    release = request_json(f"/repos/{repo}/releases/latest", allow_404=True)
    tags = request_json(f"/repos/{repo}/tags?per_page=1", allow_404=True) or []
    return {
        "latest_release": release.get("tag_name") if release else None,
        "latest_release_published_at": release.get("published_at") if release else None,
        "latest_tag": tags[0].get("name") if tags else None,
    }


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


def compare_fork(local_meta: dict[str, Any], upstream_meta: dict[str, Any]) -> dict[str, Any] | None:
    local_full = local_meta["full_name"]
    local_owner = local_meta["owner"]["login"]
    local_branch = local_meta["default_branch"]
    upstream_full = upstream_meta["full_name"]
    upstream_branch = upstream_meta["default_branch"]

    if local_full == upstream_full:
        return None

    spec = (
        f"{urllib.parse.quote(upstream_branch, safe='')}"
        f"...{urllib.parse.quote(local_owner, safe='')}:"
        f"{urllib.parse.quote(local_branch, safe='')}"
    )
    return request_json(f"/repos/{upstream_full}/compare/{spec}", allow_404=True)


def known_license(value: str | None) -> bool:
    return bool(value and str(value).upper() not in {"UNKNOWN", "NOASSERTION", "OTHER"})


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
        local_branch = local.get("default_branch")
        parent = embedded_full_name(local.get("parent"))
        canonical_source = embedded_full_name(local.get("source"))
        local_license, local_license_source = effective_license(repo, local)

        result.update(
            {
                "visibility": local.get("visibility"),
                "default_branch": local_branch,
                "local_head": branch_head(repo, local_branch) if local_branch else None,
                "local_pushed_at": local.get("pushed_at"),
                "local_license": local_license,
                "local_license_source": local_license_source,
                "local_license_metadata": metadata_license(local),
                "local_archived": bool(local.get("archived")),
                "fork_parent": parent,
                "canonical_source": canonical_source,
                "intermediate_fork": bool(parent and canonical_source and parent != canonical_source),
            }
        )
        result.update(latest_signal(repo))

        if entry.get("upstream_only"):
            result.update(
                {
                    "upstream": repo,
                    "state": "UPSTREAM_ONLY",
                    "upstream_head": result.get("local_head"),
                    "upstream_pushed_at": local.get("pushed_at"),
                    "upstream_dormancy_days": iso_age_days(local.get("pushed_at")),
                    "upstream_license": local_license,
                    "upstream_license_source": local_license_source,
                    "license_delta": False,
                }
            )
            return result

        upstream_ref = entry.get("upstream") or parent or canonical_source
        if not upstream_ref:
            result.update({"state": "NO_UPSTREAM", "upstream": None})
            return result

        upstream = request_json(f"/repos/{upstream_ref}")
        upstream_branch = upstream.get("default_branch")
        upstream_license, upstream_license_source = effective_license(upstream_ref, upstream)
        result.update(
            {
                "upstream": upstream_ref,
                "upstream_default_branch": upstream_branch,
                "upstream_head": branch_head(upstream_ref, upstream_branch) if upstream_branch else None,
                "upstream_pushed_at": upstream.get("pushed_at"),
                "upstream_dormancy_days": iso_age_days(upstream.get("pushed_at")),
                "upstream_license": upstream_license,
                "upstream_license_source": upstream_license_source,
                "upstream_license_metadata": metadata_license(upstream),
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
                }
            )
        else:
            result["state"] = "UNKNOWN"

        result["license_delta"] = bool(
            known_license(local_license)
            and known_license(upstream_license)
            and local_license != upstream_license
        )
        return result

    except Exception as exc:  # evidence collection must continue across the portfolio
        result["state"] = "ERROR"
        result["error"] = str(exc)
        return result


def severity_key(row: dict[str, Any]) -> tuple[int, int]:
    priority_order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    state_order = {
        "ERROR": 0,
        "U4": 1,
        "U3": 2,
        "U1": 3,
        "U2": 4,
        "UNKNOWN": 5,
        "NO_UPSTREAM": 6,
        "U0": 7,
        "UPSTREAM_ONLY": 8,
    }
    return priority_order.get(row.get("priority"), 9), state_order.get(row.get("state"), 9)


def recommendation(row: dict[str, Any]) -> str:
    if row.get("state") == "ERROR":
        return "restore audit visibility before change"
    if row.get("license_delta"):
        return "block promotion; reconcile effective license/provenance first"
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
        "| Priority | Repository | Upstream | State | Ahead | Behind | Scale | Effective licenses | Recommendation |",
        "|---|---|---|---:|---:|---:|---|---|---|",
    ]
    for row in sorted(rows, key=severity_key):
        licenses = f"{row.get('local_license', '')} -> {row.get('upstream_license', '')}"
        if row.get("license_delta"):
            licenses += " [DELTA]"
        lines.append(
            "| {priority} | {repository} | {upstream} | {state} | {ahead} | {behind} | {scale} | {licenses} | {recommendation} |".format(
                priority=row.get("priority", ""),
                repository=row.get("repository", ""),
                upstream=row.get("upstream", ""),
                state=row.get("state", ""),
                ahead=row.get("ahead_by", ""),
                behind=row.get("behind_by", ""),
                scale=row.get("drift_scale", ""),
                licenses=licenses.replace("|", "/"),
                recommendation=recommendation(row).replace("|", "/"),
            )
        )

    multi_hop = [row for row in rows if row.get("intermediate_fork")]
    if multi_hop:
        lines.extend(["", "## Multi-hop fork chains", ""])
        for row in multi_hop:
            lines.append(
                f"- {row['repository']}: parent={row.get('fork_parent')}, canonical_source={row.get('canonical_source')}, tracked_upstream={row.get('upstream')}"
            )

    unresolved_licenses = [
        row
        for row in rows
        if not known_license(row.get("local_license"))
        or (row.get("upstream") and not known_license(row.get("upstream_license")))
    ]
    if unresolved_licenses:
        lines.extend(["", "## License evidence still unresolved", ""])
        for row in unresolved_licenses:
            lines.append(
                f"- {row['repository']}: local={row.get('local_license')} ({row.get('local_license_source')}), upstream={row.get('upstream_license')} ({row.get('upstream_license_source')})"
            )

    lines.extend(
        [
            "",
            "## Rules",
            "",
            "- This report is read-only evidence. It is not approval to merge or upgrade.",
            "- U3 requires explicit local-delta preservation.",
            "- Effective license deltas block promotion until reconciled.",
            "- GitHub NOASSERTION metadata is rechecked against common license files before creating a license delta.",
            "- Multi-hop fork chains must be remediated at the authoritative layer first.",
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
        "schema_version": "1.2",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "token_mode": (
            "portfolio"
            if os.getenv("PEFY_PORTFOLIO_TOKEN")
            else ("github-actions" if os.getenv("GITHUB_TOKEN") else "anonymous-public")
        ),
        "results": sorted(rows, key=severity_key),
    }
    (out_dir / "upstream-audit.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "upstream-audit.md").write_text(render_markdown(rows), encoding="utf-8")

    errors = [row for row in rows if row.get("state") == "ERROR"]
    print(render_markdown(rows))
    if errors:
        print(f"Audit completed with {len(errors)} visibility/API errors.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
