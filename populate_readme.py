#!/usr/bin/env python3
"""
populate_readme.py — Fill CLI ($), MCP ($), Cost× columns in README.md
from clean-two-phase rows in rerun_results.csv.

Usage:
  python3 populate_readme.py            # update README.md in place
  python3 populate_readme.py --dry-run  # preview only
"""

import csv
import sys
from pathlib import Path

BASE = Path(__file__).parent

# Sites where MCP cost is N/A (submit crashes session or site gone)
MCP_NA = {"PHP Travels", "Black Box Puzzles", "BookCart"}

def load_clean_results(csv_path):
    """Return dict of site → latest clean-two-phase row."""
    results = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "clean-two-phase" in row.get("notes", ""):
                results[row["site"]] = row  # last occurrence wins
    return results

def fmt_cost(usd_str):
    if not usd_str or usd_str in ("N/A", ""):
        return "N/A"
    try:
        return f"${float(usd_str):.3f}"
    except ValueError:
        return "N/A"

def fmt_ratio(cli_str, mcp_str):
    if not cli_str or not mcp_str or "N/A" in (cli_str, mcp_str):
        return "N/A"
    try:
        cli, mcp = float(cli_str), float(mcp_str)
        if cli == 0:
            return "N/A"
        return f"{mcp / cli:.1f}×"
    except ValueError:
        return "N/A"

def update_readme(readme_path, results, dry_run=False):
    lines = readme_path.read_text().splitlines(keepends=True)
    updated = 0
    new_lines = []

    for line in lines:
        if not line.startswith("| "):
            new_lines.append(line)
            continue

        parts = line.split("|")
        # Expect at least: | site | url | cli_ms | cli_usd | mcp_ms | mcp_usd | speed | cost_ratio | finding |
        if len(parts) < 10:
            new_lines.append(line)
            continue

        site_name = parts[1].strip()
        row = results.get(site_name)

        if not row:
            new_lines.append(line)
            continue

        # Only update if placeholders are still present
        if parts[4].strip() not in ("—", "") and parts[6].strip() not in ("—", ""):
            new_lines.append(line)
            continue

        cli_usd_val = row["cli_usd"]
        mcp_usd_val = "N/A" if site_name in MCP_NA else row["mcp_usd"]

        parts[4] = f" {fmt_cost(cli_usd_val)} "
        parts[6] = f" {fmt_cost(mcp_usd_val)} "
        parts[8] = f" {fmt_ratio(cli_usd_val, mcp_usd_val)} "

        line = "|".join(parts)
        updated += 1
        new_lines.append(line)

    print(f"Updated {updated} / {len(results)} sites")
    if not dry_run:
        readme_path.write_text("".join(new_lines))
    else:
        print("(dry run — README not modified)")

    return updated

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    results = load_clean_results(BASE / "rerun_results.csv")
    print(f"Loaded {len(results)} clean-two-phase sites from CSV")
    update_readme(BASE / "README.md", results, dry_run=dry_run)
