#!/usr/bin/env python3
"""Update CLI ms, MCP ms, Speed columns in README.md from clean-two-phase CSV rows."""

import csv
import sys
from pathlib import Path

BASE = Path(__file__).parent

def load_clean_results(csv_path):
    results = {}
    with open(csv_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "clean-two-phase" in row.get("notes", ""):
                results[row["site"]] = row
    return results

def fmt_ms(ms_str):
    try:
        return f"{int(ms_str):,}"
    except (ValueError, TypeError):
        return str(ms_str)

def fmt_speed(cli_ms, mcp_ms):
    try:
        c, m = int(cli_ms), int(mcp_ms)
        if c == 0:
            return "N/A"
        return f"{m/c:.1f}×"
    except (ValueError, TypeError):
        return "N/A"

def update(readme_path, results, dry_run=False):
    lines = readme_path.read_text().splitlines(keepends=True)
    updated = 0
    new_lines = []
    for line in lines:
        if not line.startswith("| "):
            new_lines.append(line)
            continue
        parts = line.split("|")
        if len(parts) < 10:
            new_lines.append(line)
            continue
        site = parts[1].strip()
        row = results.get(site)
        if not row:
            new_lines.append(line)
            continue
        cli_ms = row["cli_ms"]
        mcp_ms = row["mcp_ms"]
        # Always update CLI ms
        parts[3] = f" {fmt_ms(cli_ms)} "
        # Update MCP ms and Speed only when measured
        if mcp_ms not in ("N/A", ""):
            parts[5] = f" {fmt_ms(mcp_ms)} "
            parts[7] = f" {fmt_speed(cli_ms, mcp_ms)} "
        line = "|".join(parts)
        updated += 1
        new_lines.append(line)
    print(f"Updated timing for {updated} / {len(results)} sites")
    if not dry_run:
        readme_path.write_text("".join(new_lines))
    else:
        print("(dry run — README not modified)")

if __name__ == "__main__":
    dry_run = "--dry-run" in sys.argv
    results = load_clean_results(BASE / "rerun_results.csv")
    print(f"Loaded {len(results)} clean-two-phase sites from CSV")
    update(BASE / "README.md", results, dry_run)
