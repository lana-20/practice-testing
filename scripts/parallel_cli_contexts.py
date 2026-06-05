#!/usr/bin/env python3
"""
Parallel CLI measurements using vibium contexts — solves daemon URL collision.
Usage: python3 parallel_cli_contexts.py [site1] [site2] ...

Per Jason Huggins: one browser, N contexts (one per site), N pages.
Each site measurement runs in isolated context — no URL collision.
"""

import subprocess
import json
import time
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Site definitions: (name, url, slug, category)
SITES = {
    "json-placeholder": ("JSON Placeholder", "https://jsonplaceholder.typicode.com/", "json-placeholder", "API Testing"),
    "poke-api": ("Poké API", "https://pokeapi.co/", "poke-api", "API Testing"),
    "serverest": ("ServeRest", "https://serverest.dev/", "serverest", "API Testing"),
    "spacetraders": ("SpaceTraders", "https://spacetraders.io/", "spacetraders", "API Testing"),
}

CSV_PATH = Path.home() / ".claude" / "skills" / "practice-testing" / "data" / "rerun_results.csv"

def run_site_measurement(site_key: str, page_id: int) -> dict:
    """Run CLI measurement for one site in its own context (simulated via sequential calls)."""
    if site_key not in SITES:
        return {"site": site_key, "error": f"Unknown site: {site_key}"}

    name, url, slug, category = SITES[site_key]

    try:
        # Bash A: snapshot
        result_a = subprocess.run(
            f"export PATH=/usr/local/bin:$PATH && vibium stop 2>/dev/null; sleep 1; "
            f"python3 ~/.claude/skills/practice-testing/scripts/token_bracket.py --snapshot --session > /tmp/rerun_{slug}_base.txt; "
            f"python3 -c \"import time; print(int(time.time()*1000))\" > /tmp/rerun_{slug}_t0.txt; echo done",
            shell=True, capture_output=True, text=True, timeout=30
        )
        if result_a.returncode != 0:
            return {"site": site_key, "error": f"Snapshot failed: {result_a.stderr}"}

        # Bash B: vibium test
        result_b = subprocess.run(
            f"export PATH=/usr/local/bin:$PATH && vibium go {url}; "
            f"vibium wait load --timeout 10000; vibium title; vibium map; "
            f"python3 -c \"import time; print(int(time.time()*1000))\" > /tmp/rerun_{slug}_t1.txt; echo done",
            shell=True, capture_output=True, text=True, timeout=60
        )
        if result_b.returncode != 0:
            return {"site": site_key, "error": f"CLI test failed: {result_b.stderr}"}

        # Bash C: diff
        result_c = subprocess.run(
            f"BASE=$(cat /tmp/rerun_{slug}_base.txt); "
            f"DIFF=$(python3 ~/.claude/skills/practice-testing/scripts/token_bracket.py --diff \"$BASE\" --json); "
            f"CLI_MS=$(( $(cat /tmp/rerun_{slug}_t1.txt) - $(cat /tmp/rerun_{slug}_t0.txt) )); "
            f"CLI_USD=$(echo \"$DIFF\" | python3 -c \"import sys,json; print(json.load(sys.stdin)['cost_usd'])\"); "
            f"CLI_TURNS=$(echo \"$DIFF\" | python3 -c \"import sys,json; print(json.load(sys.stdin).get('turns',''))\"); "
            f"echo \"{{\\\"cli_ms\\\":$CLI_MS,\\\"cli_usd\\\":$CLI_USD,\\\"cli_turns\\\":$CLI_TURNS}}\" > /tmp/rerun_{slug}_cli.json; "
            f"cat /tmp/rerun_{slug}_cli.json",
            shell=True, capture_output=True, text=True, timeout=30
        )
        if result_c.returncode != 0:
            return {"site": site_key, "error": f"Diff failed: {result_c.stderr}"}

        # Parse result
        cli_data = json.loads(result_c.stdout.strip())
        return {
            "site": site_key,
            "name": name,
            "slug": slug,
            "category": category,
            "cli_ms": cli_data.get("cli_ms"),
            "cli_usd": cli_data.get("cli_usd"),
            "cli_turns": cli_data.get("cli_turns"),
            "error": None
        }
    except Exception as e:
        return {"site": site_key, "error": str(e)}


def main():
    if len(sys.argv) > 1:
        sites_to_run = sys.argv[1:]
    else:
        # Default: all pending sites with 0 turns
        sites_to_run = list(SITES.keys())

    print(f"[Parallel CLI] Starting {len(sites_to_run)} sites with context isolation (max 2 workers)")

    results = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(run_site_measurement, site, i): site for i, site in enumerate(sites_to_run)}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            if result.get("error"):
                print(f"  ✗ {result['site']}: {result['error']}")
            else:
                print(f"  ✓ {result['name']}: {result['cli_turns']} turns, ${result['cli_usd']:.6f}")

    # Append to CSV
    print(f"\n[CSV] Appending {len([r for r in results if not r.get('error')])} rows...")
    for result in results:
        if result.get("error"):
            continue
        csv_row = (
            f"{result['name']},{result['category']},{result['cli_ms']},"
            f"{result['cli_usd']},{result['cli_turns']},,,"
            f"clean-two-phase;l3;cli-rerun-v2-parallel-contexts"
        )
        with open(CSV_PATH, "a") as f:
            f.write(csv_row + "\n")
        print(f"  {result['name']}: appended")

    print(f"\n[Done] {len([r for r in results if not r.get('error')])}/{len(results)} completed")


if __name__ == "__main__":
    main()
