#!/usr/bin/env python3
"""Read-only repository portfolio inventory for PEFY governance.

Discovers repositories under configured GitHub owners, classifies likely capability
roles, records fork lineage and surfaces hygiene/risk flags. The script never mutates
repositories.

Privacy safeguard: authenticated private-repository enumeration is disabled when the
control repository is public unless PEFY_ALLOW_PRIVATE_INVENTORY=1 is explicitly set.
That override should only be used in an approved private evidence environment.
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Iterable

API = "https://api.github.com"
USER_AGENT = "PEFY-Portfolio-Inventory/1.0"
_CACHE: dict[str, Any] = {}


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


def paged(path: str, *, max_pages: int = 50) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    separator = "&" if "?" in path else "?"
    for page in range(1, max_pages + 1):
        url = f"{path}{separator}per_page=100&page={page}"
        batch = request_json(url)
        if not isinstance(batch, list):
            raise RuntimeError(f"Expected list from {url}")
        rows.extend(batch)
        if len(batch) < 100:
            break
    return rows


def authenticated_login() -> str | None:
    if not token():
        return None
    try:
        data = request_json("/user")
        return data.get("login") if isinstance(data, dict) else None
    except Exception:
        return None


def control_repo_is_private() -> bool:
    override = os.getenv("PEFY_ALLOW_PRIVATE_INVENTORY", "").strip().lower()
    if override in {"1", "true", "yes"}:
        return True

    control_repo = os.getenv("GITHUB_REPOSITORY")
    if not control_repo:
        return False
    meta = request_json(f"/repos/{control_repo}", allow_404=True)
    return bool(meta and meta.get("private"))


def list_owner_repositories(owner: dict[str, Any], *, include_private: bool) -> list[dict[str, Any]]:
    name = owner["name"]
    kind = owner["type"]
    login = authenticated_login()

    if kind == "user":
        if include_private and login and login.lower() == name.lower():
            return paged("/user/repos?affiliation=owner&visibility=all&sort=full_name")
        return paged(f"/users/{urllib.parse.quote(name, safe='')}/repos?type=owner&sort=full_name")

    if kind == "org":
        repo_type = "all" if include_private else "public"
        return paged(
            f"/orgs/{urllib.parse.quote(name, safe='')}/repos?type={repo_type}&sort=full_name"
        )

    raise ValueError(f"Unsupported owner type: {kind}")


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def age_days(value: str | None) -> int | None:
    timestamp = parse_time(value)
    if not timestamp:
        return None
    return max(0, (dt.datetime.now(dt.timezone.utc) - timestamp).days)


def license_id(repo: dict[str, Any]) -> str | None:
    lic = repo.get("license") or {}
    return lic.get("spdx_id") or lic.get("key")


def markers_match(text: str, markers: Iterable[str]) -> bool:
    return any(marker.lower() in text for marker in markers)


def classify(repo: dict[str, Any], rules: dict[str, Any]) -> tuple[str, str]:
    text = f"{repo.get('name', '')} {repo.get('description') or ''}".lower()

    # Discovery/reference wins first so "awesome-openclaw" is not treated as a runtime.
    if markers_match(text, rules.get("discovery_markers", [])):
        return "discovery_reference", "A5"
    if markers_match(text, rules.get("secure_sandbox_markers", [])):
        return "secure_sandbox_runtime", "A3"
    if markers_match(text, rules.get("coding_runtime_markers", [])):
        return "coding_runtime", "A3"
    if markers_match(text, rules.get("multi_agent_markers", [])):
        return "multi_agent_runtime", "A3"
    if markers_match(text, rules.get("workflow_markers", [])):
        return "workflow_automation", "A3"
    if markers_match(text, rules.get("gateway_markers", [])):
        return "agent_gateway", "A3"
    if markers_match(text, rules.get("security_markers", [])):
        return "security_product_or_tool", "REVIEW"
    if markers_match(text, rules.get("skills_markers", [])):
        return "skill_or_adapter", "A4"
    return "unclassified", "REVIEW"


def fork_lineage(repo: dict[str, Any]) -> tuple[str | None, str | None]:
    if not repo.get("fork"):
        return None, None
    full_name = repo["full_name"]
    detail = request_json(f"/repos/{full_name}")
    parent = detail.get("parent") or {}
    source = detail.get("source") or {}
    return parent.get("full_name"), source.get("full_name")


def family_tags(repo: dict[str, Any]) -> list[str]:
    text = f"{repo.get('name', '')} {repo.get('description') or ''}".lower()
    families = {
        "claude": ["claude"],
        "openclaw": ["openclaw", "clawteam", "nemoclaw"],
        "codex": ["codex"],
        "opencode": ["opencode"],
        "crew": ["crewai"],
        "deerflow": ["deer-flow", "deerflow"],
        "metagpt": ["metagpt"],
        "n8n": ["n8n"],
        "mcp": ["mcp"],
        "skills": ["skill", "skills"],
        "video": ["video", "openvid", "flick", "dramaclaw"],
        "wordpress": ["wordpress"],
        "security": ["security", "cyber", "firewall", "garkael", "siem", "soc"],
    }
    return sorted(name for name, terms in families.items() if any(term in text for term in terms))


def inventory_repo(
    repo: dict[str, Any],
    *,
    rules: dict[str, Any],
    dormant_days: int,
    large_repository_kb: int,
) -> dict[str, Any]:
    capability_class, authority_tier = classify(repo, rules)
    parent, source = fork_lineage(repo)
    pushed_age = age_days(repo.get("pushed_at"))
    size_kb = int(repo.get("size") or 0)
    lic = license_id(repo)

    flags: list[str] = []
    if repo.get("archived"):
        flags.append("ARCHIVED")
    if repo.get("disabled"):
        flags.append("DISABLED")
    if pushed_age is not None and pushed_age >= dormant_days:
        flags.append("DORMANT")
    if size_kb >= large_repository_kb:
        flags.append("LARGE_REPOSITORY")
    if not lic or str(lic).upper() in {"NOASSERTION", "OTHER"}:
        flags.append("LICENSE_REVIEW")
    if repo.get("fork") and repo.get("visibility") == "public":
        flags.append("PUBLIC_FORK")
    if parent and source and parent != source:
        flags.append("MULTI_HOP_FORK")
    if capability_class == "unclassified":
        flags.append("AUTHORITY_CLASSIFICATION_REQUIRED")
    if repo.get("default_branch") not in {"main", "master", "dev"}:
        flags.append("NONSTANDARD_DEFAULT_BRANCH")

    return {
        "repository": repo.get("full_name"),
        "owner": (repo.get("owner") or {}).get("login"),
        "name": repo.get("name"),
        "description": repo.get("description"),
        "visibility": repo.get("visibility") or ("private" if repo.get("private") else "public"),
        "fork": bool(repo.get("fork")),
        "fork_parent": parent,
        "canonical_source": source,
        "multi_hop_fork": bool(parent and source and parent != source),
        "default_branch": repo.get("default_branch"),
        "archived": bool(repo.get("archived")),
        "disabled": bool(repo.get("disabled")),
        "created_at": repo.get("created_at"),
        "updated_at": repo.get("updated_at"),
        "pushed_at": repo.get("pushed_at"),
        "pushed_age_days": pushed_age,
        "size_kb": size_kb,
        "license_metadata": lic,
        "capability_class": capability_class,
        "authority_tier": authority_tier,
        "families": family_tags(repo),
        "flags": flags,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_owner = collections.Counter(row.get("owner") for row in rows)
    by_class = collections.Counter(row.get("capability_class") for row in rows)
    by_visibility = collections.Counter(row.get("visibility") for row in rows)
    flag_counts = collections.Counter(flag for row in rows for flag in row.get("flags", []))
    family_counts = collections.Counter(family for row in rows for family in row.get("families", []))

    return {
        "repositories": len(rows),
        "by_owner": dict(sorted(by_owner.items())),
        "by_capability_class": dict(sorted(by_class.items())),
        "by_visibility": dict(sorted(by_visibility.items())),
        "flags": dict(sorted(flag_counts.items())),
        "overlap_families": {
            family: count
            for family, count in sorted(family_counts.items(), key=lambda item: (-item[1], item[0]))
            if count >= 2
        },
    }


def render_markdown(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    rows = payload["repositories"]
    lines = [
        "# PEFY Repository Portfolio Inventory",
        "",
        f"Generated: {payload['generated_at']}",
        f"Private inventory enabled: {payload['private_inventory_enabled']}",
        f"Repositories inventoried: {summary['repositories']}",
        "",
        "## Capability classes",
        "",
    ]
    for key, value in summary["by_capability_class"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Portfolio flags", ""])
    for key, value in summary["flags"].items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## Overlap families", ""])
    for key, value in summary["overlap_families"].items():
        lines.append(f"- {key}: {value}")

    priority_rows = [row for row in rows if row.get("flags")]
    priority_rows.sort(key=lambda row: (-len(row.get("flags", [])), row.get("repository", "")))
    lines.extend(
        [
            "",
            "## Flagged repositories",
            "",
            "| Repository | Class | Authority | Age days | Size KB | Flags |",
            "|---|---|---|---:|---:|---|",
        ]
    )
    for row in priority_rows[:150]:
        lines.append(
            "| {repository} | {capability_class} | {authority_tier} | {age} | {size} | {flags} |".format(
                repository=row.get("repository", ""),
                capability_class=row.get("capability_class", ""),
                authority_tier=row.get("authority_tier", ""),
                age=row.get("pushed_age_days", ""),
                size=row.get("size_kb", 0),
                flags=", ".join(row.get("flags", [])).replace("|", "/"),
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation rules",
            "",
            "- Discovery/reference repositories are not runtime dependencies.",
            "- Public forks containing PEFY-specific governance require ownership/placement review.",
            "- Multi-hop forks must be remediated at the authoritative upstream layer first.",
            "- Dormancy is a review signal, not automatic deprecation.",
            "- Unclassified repositories require capability/authority assignment before broad integration.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scope", default="governance/PORTFOLIO_SCOPE.json")
    parser.add_argument("--out-dir", default="artifacts/portfolio-inventory")
    args = parser.parse_args()

    scope = json.loads(pathlib.Path(args.scope).read_text(encoding="utf-8"))
    inventory_cfg = scope.get("inventory", {})
    include_private = bool(inventory_cfg.get("include_private_when_authorized")) and control_repo_is_private()

    repositories: dict[str, dict[str, Any]] = {}
    errors: list[dict[str, str]] = []
    for owner in scope.get("owners", []):
        try:
            for repo in list_owner_repositories(owner, include_private=include_private):
                full_name = repo.get("full_name")
                if full_name:
                    repositories[full_name.lower()] = repo
        except Exception as exc:  # continue partial inventory with explicit error evidence
            errors.append({"owner": owner.get("name", ""), "error": str(exc)})

    rows = [
        inventory_repo(
            repo,
            rules=scope.get("classification", {}),
            dormant_days=int(inventory_cfg.get("dormant_days", 365)),
            large_repository_kb=int(inventory_cfg.get("large_repository_kb", 500000)),
        )
        for repo in repositories.values()
        if inventory_cfg.get("include_archived", True) or not repo.get("archived")
        if inventory_cfg.get("include_forks", True) or not repo.get("fork")
    ]
    rows.sort(key=lambda row: row.get("repository", "").lower())

    payload = {
        "schema_version": "1.0",
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "private_inventory_enabled": include_private,
        "errors": errors,
        "summary": summarize(rows),
        "repositories": rows,
    }

    out_dir = pathlib.Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "portfolio-inventory.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (out_dir / "portfolio-inventory.md").write_text(render_markdown(payload), encoding="utf-8")
    print(render_markdown(payload))

    if errors:
        print(f"Inventory completed with {len(errors)} owner/API errors.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
