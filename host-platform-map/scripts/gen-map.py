#!/usr/bin/env python3
"""Walk host platform module descriptors and emit a markdown table.

Usage: python3 gen-map.py <host-source-dir> [--ecosystem odoo|npm|pyproject|wp]

Detects the ecosystem automatically unless --ecosystem is given.
Prints a markdown table to stdout; parse errors are logged to stderr.
"""

import argparse
import ast
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib  # type: ignore
    except ImportError:
        tomllib = None  # type: ignore


def truncate_list(items: list, limit: int = 5) -> str:
    if len(items) <= limit:
        return ", ".join(items)
    return ", ".join(items[:limit]) + ", …"


# --- Odoo ---

def parse_odoo(root: Path) -> list[dict]:
    rows = []
    for manifest in root.rglob("__manifest__.py"):
        try:
            data = ast.literal_eval(manifest.read_text())
        except Exception as e:
            print(f"skip {manifest}: {e}", file=sys.stderr)
            continue
        rows.append({
            "name": data.get("name", manifest.parent.name),
            "category": data.get("category", ""),
            "summary": data.get("summary", data.get("description", ""))[:80],
            "depends": truncate_list(data.get("depends", [])),
        })
    return rows


def emit_odoo(rows: list[dict]) -> str:
    lines = ["| Module | Category | Summary | Key dependencies |",
             "|--------|----------|---------|-----------------|"]
    for r in sorted(rows, key=lambda r: r["name"].lower()):
        lines.append(f"| {r['name']} | {r['category']} | {r['summary']} | {r['depends']} |")
    return "\n".join(lines)


# --- npm / VS Code ---

def parse_npm(root: Path) -> list[dict]:
    rows = []
    for pkg in root.rglob("package.json"):
        if "node_modules" in pkg.parts:
            continue
        try:
            data = json.loads(pkg.read_text())
        except Exception as e:
            print(f"skip {pkg}: {e}", file=sys.stderr)
            continue
        if "name" not in data:
            continue
        deps = list(data.get("dependencies", {}).keys()) + list(data.get("peerDependencies", {}).keys())
        rows.append({
            "name": data["name"],
            "description": data.get("description", "")[:80],
            "keywords": ", ".join(data.get("keywords", [])[:5]),
            "deps": truncate_list(deps),
        })
    return rows


def emit_npm(rows: list[dict]) -> str:
    lines = ["| Package | Description | Keywords | Key dependencies |",
             "|---------|-------------|----------|-----------------|"]
    for r in sorted(rows, key=lambda r: r["name"].lower()):
        lines.append(f"| {r['name']} | {r['description']} | {r['keywords']} | {r['deps']} |")
    return "\n".join(lines)


# --- Python (pyproject.toml) ---

def parse_pyproject(root: Path) -> list[dict]:
    if tomllib is None:
        print("tomllib/tomli not available — install tomli for Python <3.11", file=sys.stderr)
        return []
    rows = []
    for toml in root.rglob("pyproject.toml"):
        try:
            data = tomllib.loads(toml.read_text())
        except Exception as e:
            print(f"skip {toml}: {e}", file=sys.stderr)
            continue
        proj = data.get("project", {})
        if not proj.get("name"):
            continue
        eps = list(data.get("project", {}).get("entry-points", {}).keys())
        rows.append({
            "name": proj["name"],
            "description": proj.get("description", "")[:80],
            "keywords": ", ".join(proj.get("keywords", [])[:5]),
            "entry_points": ", ".join(eps[:5]) or "—",
        })
    return rows


def emit_pyproject(rows: list[dict]) -> str:
    lines = ["| Package | Description | Keywords | Entry-point groups |",
             "|---------|-------------|----------|--------------------|"]
    for r in sorted(rows, key=lambda r: r["name"].lower()):
        lines.append(f"| {r['name']} | {r['description']} | {r['keywords']} | {r['entry_points']} |")
    return "\n".join(lines)


# --- WordPress plugins ---

_WP_FIELDS = {
    "Plugin Name": re.compile(r"Plugin Name:\s*(.+)"),
    "Description": re.compile(r"Description:\s*(.+)"),
    "Requires": re.compile(r"Requires(?: at least)?:\s*(.+)"),
    "Requires PHP": re.compile(r"Requires PHP:\s*(.+)"),
}


def parse_wp(root: Path) -> list[dict]:
    rows = []
    for php in root.glob("**/*.php"):
        if php.stat().st_size > 64_000:
            continue
        try:
            text = php.read_text(errors="replace")
        except Exception:
            continue
        if "Plugin Name:" not in text:
            continue
        fields: dict[str, str] = {}
        for key, pat in _WP_FIELDS.items():
            m = pat.search(text)
            if m:
                fields[key] = m.group(1).strip()
        if "Plugin Name" not in fields:
            continue
        rows.append({
            "name": fields.get("Plugin Name", ""),
            "description": fields.get("Description", "")[:80],
            "requires": fields.get("Requires", ""),
            "requires_php": fields.get("Requires PHP", ""),
        })
    return rows


def emit_wp(rows: list[dict]) -> str:
    lines = ["| Plugin | Description | Requires WP | Requires PHP |",
             "|--------|-------------|-------------|--------------|"]
    for r in sorted(rows, key=lambda r: r["name"].lower()):
        lines.append(f"| {r['name']} | {r['description']} | {r['requires']} | {r['requires_php']} |")
    return "\n".join(lines)


# --- Detection ---

def detect_ecosystem(root: Path) -> str:
    if any(root.rglob("__manifest__.py")):
        return "odoo"
    if any(p for p in root.rglob("package.json") if "node_modules" not in p.parts):
        return "npm"
    if any(root.rglob("pyproject.toml")):
        return "pyproject"
    for php in root.glob("**/*.php"):
        try:
            if "Plugin Name:" in php.read_text(errors="replace"):
                return "wp"
        except Exception:
            continue
    return ""


# --- Main ---

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Host source directory to scan")
    parser.add_argument("--ecosystem", choices=["odoo", "npm", "pyproject", "wp"],
                        help="Force ecosystem detection")
    args = parser.parse_args()

    root = args.root.resolve()
    if not root.is_dir():
        sys.exit(f"error: {root} is not a directory")

    ecosystem = args.ecosystem or detect_ecosystem(root)
    if not ecosystem:
        sys.exit(
            "error: could not detect ecosystem. Expected one of:\n"
            "  odoo       — __manifest__.py files\n"
            "  npm        — package.json files (outside node_modules)\n"
            "  pyproject  — pyproject.toml files\n"
            "  wp         — PHP files with 'Plugin Name:' header\n"
            "Pass --ecosystem to specify manually."
        )

    parsers = {"odoo": (parse_odoo, emit_odoo),
               "npm": (parse_npm, emit_npm),
               "pyproject": (parse_pyproject, emit_pyproject),
               "wp": (parse_wp, emit_wp)}

    parse_fn, emit_fn = parsers[ecosystem]
    rows = parse_fn(root)

    if not rows:
        sys.exit(f"error: no {ecosystem} descriptors found under {root}")

    print(emit_fn(rows))
    print(f"\n<!-- generated by gen-map.py from {root} on {date.today()} — host version: unknown (add manually) -->")


if __name__ == "__main__":
    main()
