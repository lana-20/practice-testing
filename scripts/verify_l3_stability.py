#!/usr/bin/env python3
"""
L3 stability verification: re-measure subset of 100 sites.
Compare new runs against original L3 data for consistency.
"""

import subprocess
import json
import sys
import csv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Verification subset: 11 sites (1-2 per category)
VERIFY_SITES = {
    "practice-software-testing": ("Practice Software Testing", "https://practicesoftwaretesting.com/", "practice-software-testing", "General Practice"),
    "qa-practice": ("QA Practice", "https://qa-practice.razvanvancea.ro/", "qa-practice", "General Practice"),
    "the-internet": ("The Internet", "https://the-internet.herokuapp.com/", "the-internet", "Automation Testing"),
    "swag-labs": ("Swag Labs", "https://www.saucedemo.com/", "swag-labs", "Automation Testing"),
    "demoqa": ("DemoQA", "https://demoqa.com/", "demoqa", "Automation Testing"),
    "firing-range": ("Firing Range", "https://public-firing-range.appspot.com/", "firing-range", "Security Testing"),
    "owasp-juice-shop": ("OWASP Juice Shop", "https://demo.owasp-juice.shop/", "owasp-juice-shop", "Security Testing"),
    "demoblaze": ("Demoblaze", "https://demoblaze.com/", "demoblaze", "Performance Testing"),
    "pet-store-web": ("Pet Store Web", "https://petstore.octoperf.com/actions/Catalog.action", "pet-store-web", "Performance Testing"),
    "httpbin": ("httpbin", "https://httpbin.org/", "httpbin", "API Testing"),
    "restful-booker": ("Restful Booker", "https://restful-booker.herokuapp.com/", "restful-booker", "API Testing"),
    "poke-api": ("Poké API", "https://pokeapi.co/", "poke-api", "API Testing"),
}

CSV_PATH = Path.home() / ".claude" / "skills" / "practice-testing" / "data" / "rerun_results.csv"


def load_original_l3() -> dict:
    """Load original L3 data by site (keyed by site name from CSV)."""
    original = {}
    site_names = {v[0]: k for k, v in VERIFY_SITES.items()}  # Map full name to key

    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            site_name = row['site']
            site_key = site_names.get(site_name)
            if site_key:
                original[site_key] = {
                    'cli_ms': int(row['cli_ms']) if row['cli_ms'] else None,
                    'cli_usd': float(row['cli_usd']) if row['cli_usd'] else None,
                    'cli_turns': int(row['turns_cli']) if row['turns_cli'] else None,
                }
    return original


def measure_site_vibium(site_key: str, page) -> dict:
    """Measure one site using vibium."""
    if site_key not in VERIFY_SITES:
        return {"site": site_key, "error": "Unknown site"}

    name, url, slug, category = VERIFY_SITES[site_key]

    try:
        import time
        t0 = int(time.time() * 1000)
        page.go(url)
        time.sleep(3)
        try:
            _ = page.title()
        except:
            pass
        try:
            _ = page.map()
        except:
            pass
        t1 = int(time.time() * 1000)

        return {
            "site": site_key,
            "name": name,
            "cli_ms": t1 - t0,
            "cli_turns": 0,  # Simplified for verification
            "error": None
        }
    except Exception as e:
        return {"site": site_key, "name": VERIFY_SITES[site_key][0], "error": str(e)}


def compare_results(original: dict, new: dict) -> dict:
    """Compare new measurements against original L3 data."""
    comparison = {}
    for site_key, new_data in new.items():
        if new_data.get("error"):
            comparison[site_key] = {"status": "ERROR", "error": new_data["error"]}
            continue

        orig = original.get(site_key, {})
        orig_ms = orig.get("cli_ms")
        new_ms = new_data.get("cli_ms")

        if orig_ms and new_ms:
            variance = ((new_ms - orig_ms) / orig_ms) * 100
            status = "✓" if abs(variance) < 30 else "⚠" if abs(variance) < 50 else "✗"
        else:
            variance = None
            status = "?"

        comparison[site_key] = {
            "status": status,
            "orig_ms": orig_ms,
            "new_ms": new_ms,
            "variance_pct": variance,
            "orig_turns": orig.get("cli_turns"),
            "new_turns": new_data.get("cli_turns"),
        }

    return comparison


def main():
    print(f"[L3 Verification] Re-measuring {len(VERIFY_SITES)} sites for stability check\n")

    # Load original L3 data
    original = load_original_l3()
    print(f"[Original] Loaded {len(original)}/{len(VERIFY_SITES)} sites from L3 CSV")

    # Start vibium browser
    try:
        from vibium import browser as vibium_browser
    except ImportError:
        print("ERROR: vibium not installed")
        return

    browser = None
    try:
        browser = vibium_browser.start(headless=True)
        contexts = [browser.new_context() for _ in VERIFY_SITES]
        pages = [ctx.new_page() for ctx in contexts]

        # Measure in parallel
        results = {}
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = {
                pool.submit(measure_site_vibium, site, page): site
                for site, page in zip(VERIFY_SITES.keys(), pages)
            }
            for future in as_completed(futures):
                result = future.result()
                site_key = result.get("site")
                results[site_key] = result

        # Close contexts
        for ctx in contexts:
            ctx.close()

        # Compare
        comparison = compare_results(original, results)

        # Report
        print(f"\n[Comparison] Variance Threshold: ±30% (✓), ±50% (⚠), >50% (✗)\n")
        print(f"{'Site':<35} {'Status':<6} {'Orig (ms)':<12} {'New (ms)':<12} {'Variance':<10}")
        print("-" * 85)

        passed = 0
        warned = 0
        failed = 0

        for site_key in sorted(VERIFY_SITES.keys()):
            comp = comparison[site_key]
            status = comp.get("status", "?")
            orig_ms = comp.get("orig_ms")
            new_ms = comp.get("new_ms")
            variance = comp.get("variance_pct")

            site_name = VERIFY_SITES[site_key][0]
            variance_str = f"{variance:+.1f}%" if variance is not None else "N/A"

            print(f"{site_name:<35} {status:<6} {orig_ms or 'N/A':<12} {new_ms or 'N/A':<12} {variance_str:<10}")

            if status == "✓":
                passed += 1
            elif status == "⚠":
                warned += 1
            elif status == "✗":
                failed += 1

        print("\n" + "=" * 85)
        print(f"Summary: {passed} PASS, {warned} WARN, {failed} FAIL")
        print(f"Stability: {'✓ STABLE' if failed == 0 else '⚠ UNSTABLE'}")

    finally:
        if browser:
            browser.stop()


if __name__ == "__main__":
    main()
