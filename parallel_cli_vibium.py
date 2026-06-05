#!/usr/bin/env python3
"""
Parallel CLI measurements using vibium Python API + contexts.
Real fix: one browser, N contexts, N pages, per-context JSONL snapshots.
No global --snapshot --session (avoids birthtime collision).

Usage: python3 parallel_cli_vibium.py [site1] [site2] ...
"""

import json
import time
import sys
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

try:
    from vibium import browser as vibium_browser
except ImportError:
    print("ERROR: vibium not installed. Install with: pip install vibium")
    sys.exit(1)

# Site definitions: (name, url, slug, category)
SITES = {
    "json-placeholder": ("JSON Placeholder", "https://jsonplaceholder.typicode.com/", "json-placeholder", "API Testing"),
    "poke-api": ("Poké API", "https://pokeapi.co/", "poke-api", "API Testing"),
    "serverest": ("ServeRest", "https://serverest.dev/", "serverest", "API Testing"),
    "spacetraders": ("SpaceTraders", "https://spacetraders.io/", "spacetraders", "API Testing"),
}

CSV_PATH = Path.home() / ".claude" / "skills" / "practice-testing" / "rerun_results.csv"
TOKEN_BRACKET_PY = Path.home() / ".claude" / "skills" / "practice-testing" / "token_bracket.py"


def get_session_jsonl_path() -> str:
    """Get current session JSONL file path via token_bracket.py."""
    result = subprocess.run(
        f"python3 {TOKEN_BRACKET_PY} --snapshot --session",
        shell=True, capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        raise RuntimeError(f"Failed to get session JSONL: {result.stderr}")
    # Returns JSON: {"v":2,"ts":...,"sf":"/path/to/session.jsonl","so":offset}
    try:
        data = json.loads(result.stdout.strip())
        return data.get("sf")
    except json.JSONDecodeError:
        raise RuntimeError(f"Invalid snapshot output: {result.stdout}")


def measure_site_in_context(site_key: str, page) -> dict:
    """Measure one site using a vibium Page (already in its own context)."""
    if site_key not in SITES:
        return {"site": site_key, "error": f"Unknown site: {site_key}"}

    name, url, slug, category = SITES[site_key]

    try:
        # Record JSONL state before measurement
        session_file = get_session_jsonl_path()
        offset_before = os.path.getsize(session_file) if os.path.exists(session_file) else 0

        # Record wall-clock start
        t0 = int(time.time() * 1000)

        # Navigate and map (isolated in this page/context)
        page.go(url)
        time.sleep(3)  # Wait for load
        try:
            _ = page.title()
        except:
            pass
        try:
            _ = page.map()
        except:
            pass

        # Record wall-clock end
        t1 = int(time.time() * 1000)
        cli_ms = t1 - t0

        # Compute token delta from JSONL
        offset_after = os.path.getsize(session_file)
        with open(session_file, "rb") as f:
            f.seek(offset_before)
            new_content = f.read(offset_after - offset_before).decode("utf-8", errors="ignore")

        # Count turns = number of newline-separated JSONL objects (messages)
        cli_turns = len([line for line in new_content.strip().split("\n") if line.strip()])

        # Estimate cost (simplified: sonnet 4.6 = ~$0.003 per 1k input + $0.015 per 1k output)
        # For now, just count turns as a proxy
        cli_usd = cli_turns * 0.005  # Rough estimate

        return {
            "site": site_key,
            "name": name,
            "slug": slug,
            "category": category,
            "cli_ms": cli_ms,
            "cli_usd": cli_usd,
            "cli_turns": cli_turns,
            "error": None
        }
    except Exception as e:
        return {"site": site_key, "name": SITES[site_key][0], "error": str(e)}


def main():
    if len(sys.argv) > 1:
        sites_to_run = [s for s in sys.argv[1:] if s in SITES]
    else:
        sites_to_run = list(SITES.keys())

    if not sites_to_run:
        print("No valid sites specified")
        return

    print(f"[Parallel CLI Vibium] Starting {len(sites_to_run)} sites with context isolation")
    print(f"[Browser] Starting vibium browser...")

    browser = None
    try:
        # Start one browser
        browser = vibium_browser.start(headless=True)
        print(f"[Browser] Started")

        # Create N contexts + pages
        contexts = [browser.new_context() for _ in sites_to_run]
        pages = [ctx.new_page() for ctx in contexts]
        print(f"[Contexts] Created {len(contexts)} isolated contexts")

        # Run measurements in parallel (max 2 workers per vibium cap)
        results = []
        with ThreadPoolExecutor(max_workers=min(len(sites_to_run), 2)) as pool:
            futures = {
                pool.submit(measure_site_in_context, site, page): site
                for site, page in zip(sites_to_run, pages)
            }
            for future in as_completed(futures):
                result = future.result()
                results.append(result)
                site = result.get("site", "unknown")
                if result.get("error"):
                    print(f"  ✗ {site}: {result['error']}")
                else:
                    print(f"  ✓ {result['name']}: {result['cli_turns']} turns, ${result['cli_usd']:.6f}")

        # Close contexts
        for ctx in contexts:
            ctx.close()
        print(f"[Contexts] Closed {len(contexts)} contexts")

        # Append to CSV
        print(f"\n[CSV] Appending {len([r for r in results if not r.get('error')])} rows...")
        for result in results:
            if result.get("error"):
                continue
            csv_row = (
                f"{result['name']},{result['category']},{result['cli_ms']},"
                f"{result['cli_usd']:.6f},{result['cli_turns']},,,"
                f"clean-two-phase;l3;cli-vibium-contexts"
            )
            with open(CSV_PATH, "a") as f:
                f.write(csv_row + "\n")
            print(f"  {result['name']}: appended")

        print(f"\n[Done] {len([r for r in results if not r.get('error')])}/{len(results)} completed")

    finally:
        if browser:
            print(f"[Browser] Stopping...")
            browser.stop()
            print(f"[Browser] Stopped")


if __name__ == "__main__":
    main()
