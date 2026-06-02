# Practice Testing Rerun — Scope & Estimate

Last updated: June 1, 2026 · vibium v26.5.31

---

## Raw browser automation time (from README timing data)

| Mode | Sites | Time |
|---|---|---|
| CLI | 99 | ~450s (~7.5 min) |
| MCP | 99 | ~2,263s (~38 min) |
| Combined | — | ~45 min |

## Full rerun estimate (both modes, all 99 sites)

LLM overhead dominates — previous run logged ~844 total turns (111 CLI + 733 MCP). At ~10–20s per response that's 2–4 hours of pure inference time. Context limits cap each session at ~5–8 sites.

| | Estimate |
|---|---|
| Sessions needed | ~18–22 |
| Time per session | ~30–45 min |
| **Total wall-clock** | **~10–15 hours across 3–5 days** |

Matches the original run cadence: 2026-04-22 → 2026-05-19.

---

## Targeted rerun — sites that actually need re-verification (v26.5.31)

The comparison doc is already updated from confirmed test results. Only sites with behavior changes need spot-checks.

### Select behavior (B5 fixed — label+value now works)

~15 sites that previously had "select by value only" workarounds:

- AcademyBugs
- Basic Calculator
- Parking Cost Calculator
- The iframe Search Engine
- Swag Labs
- Automation Test Store
- Lambdatest Playground
- Let Code
- DemoQA (select-menu sub-page)
- XYZ Bank (ng-model separate issue — still needs eval)
- QA Practice (country select)
- Blaze Demo
- Automation Camp
- Automation Testing Practice (Colors dropdown)
- Pet Store Web

### ~~Dialog handling~~ — MB3 still open (deferred in v26.5.31, #151)

Dialog deadlock confirmed on The Internet and Evil Tester. setTimeout+sleep+dialog_accept pattern remains required for MCP. No dialog sites need retesting — behavior unchanged.

### Textarea fill (B7/MB7 fixed — browser_fill now works)

~8 sites where fill on textarea previously required type or eval:

- Evil Tester (basic HTML form)
- Automation in Testing (#description — framework-driven, may still need type)
- Automation Testing Practice
- Hands-On Selenium WebDriver
- Automate Now Sandbox
- Practice Automation
- DemoQA (text-box sub-page)
- Potion Shop

---

## Targeted rerun estimate

~23 spot-checks across select and textarea categories (dialog dropped — MB3 unchanged).

| | Estimate |
|---|---|
| Sessions needed | ~3–4 |
| Time per session | ~30–40 min |
| **Total wall-clock** | **~1.5–2.5 hours** |
