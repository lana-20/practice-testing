# Level N Rerun Protocol

> **Skill loader note:** SKILL.md is the file the skill loader reads automatically. This file (PROTOCOL.md) must be explicitly loaded by agents or the orchestrating session — it is not auto-injected. When spawning rerun agents, include the relevant sections from this file directly in the agent prompt (as done in the active rerun sessions).

Measures per-site CLI ($), CLI turns, MCP ($), MCP turns for all sites.
Run when methodology changes (e.g. new bracket placement, updated token_bracket.py).
Appends results to `rerun_results.csv`; last `clean-two-phase` row per site wins.

---

## Infrastructure

- `token_bracket.py` — `~/.claude/skills/practice-testing/token_bracket.py`
- `rerun_results.csv` — `~/.claude/skills/practice-testing/rerun_results.csv`
- `populate_readme.py` — regenerates README per-site rows from CSV (L3 > L2, last wins); run with `--force` to overwrite filled cells
- `update_timing.py` — updates per-site ms/speed columns in README from CSV
- CSV columns: `site,category,cli_ms,cli_usd,turns_cli,mcp_ms,mcp_usd,turns_mcp,notes`
- Repo: github.com/lana-20/practice-testing

## Orchestration

MCP shares a single browser daemon — parallel MCP agents cause session conflicts.
CLI agents run in parallel. Each agent runs `vibium stop/start` in Bash A; if two agents overlap on that call they can collide, but in practice Agent 2's stop fires after Agent 1 has already moved into Bash B, so the risk is low and accepted.
**Two-phase approach: parallel CLI → sequential MCP.**

1. Read CSV to find already-done sites:
   `cat ~/.claude/skills/practice-testing/rerun_results.csv`
2. Cross-reference against the Site List below. Find next N unfinished sites in order.
   Sites marked `↺` need a redo even if they appear in the CSV.
3. **Phase 1 — CLI (parallel):** Spawn all N CLI-only agents IN A SINGLE MESSAGE.
   Use `subagent_type: "general-purpose"`. Each saves results to `/tmp/rerun_{SLUG}_cli.json`.
   Wait for all to complete.
4. **Phase 2 — MCP (sequential):** Spawn MCP agents ONE AT A TIME — send one Agent call,
   wait for it to return, then send the next.
5. After all MCP agents complete, print results table and offer to continue.

**BiDi dead-frame fix:** If a site opens new tabs (e.g. UI5 Demo Kit), the MCP daemon
gets stuck on stale frame IDs for subsequent sites. Fix: use `browser_new_page {url}`
instead of `browser_navigate`, then immediately `browser_close_page {index:0}`.

**Unstable CLI timing:** If a CLI run returns an implausibly high ms value (e.g. >60s for a simple login flow), rerun that site — the `vibium wait load` timeout can occasionally block on ad reloads. Triple-running and taking the median is safer for sites with ad overlays.

---

## CLI-Only Agent Prompt Template

Fill in NAME, URL, SLUG (lowercase-hyphenated, e.g. `evil-tester`), CLI_TEST_STEPS.

```
You are a QA cost-measurement agent — CLI phase only.
Run the CLI test across THREE separate bash calls (never combine them), then stop.
Do NOT use any MCP browser tools.

Site: {NAME}
URL: {URL}
Slug: {SLUG}

## Protocol

### Bash call A — snapshot only (preliminary — must be its own call)
  export PATH="/usr/local/bin:$PATH"
  vibium stop 2>/dev/null; sleep 1
  python3 ~/.claude/skills/practice-testing/token_bracket.py --snapshot --session > /tmp/rerun_{SLUG}_base.txt
  python3 -c "import time; print(int(time.time()*1000))" > /tmp/rerun_{SLUG}_t0.txt
  echo "snapshot done"

### Bash call B — CLI test (Claude generates this script here; cost falls inside bracket)
  export PATH="/usr/local/bin:$PATH"
  vibium go {URL}
  vibium wait load --timeout 10000
  vibium title
  vibium map
  {CLI_TEST_STEPS}
  python3 -c "import time; print(int(time.time()*1000))" > /tmp/rerun_{SLUG}_t1.txt

### Bash call C — diff + save
  BASE=$(cat /tmp/rerun_{SLUG}_base.txt)
  DIFF=$(python3 ~/.claude/skills/practice-testing/token_bracket.py --diff "$BASE" --json)
  CLI_MS=$(( $(cat /tmp/rerun_{SLUG}_t1.txt) - $(cat /tmp/rerun_{SLUG}_t0.txt) ))
  CLI_USD=$(echo "$DIFF" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['cost_usd'])")
  CLI_TURNS=$(echo "$DIFF" | python3 -c "import sys,json; print(json.load(sys.stdin).get('turns',''))")
  echo "{\"cli_ms\":$CLI_MS,\"cli_usd\":$CLI_USD,\"cli_turns\":$CLI_TURNS}" > /tmp/rerun_{SLUG}_cli.json
  cat /tmp/rerun_{SLUG}_cli.json

Output the JSON content, then stop.
```

---

## MCP-Only Agent Prompt Template

Fill in NAME, URL, SLUG, CATEGORY, MCP_TEST_STEPS.

```
You are a QA cost-measurement agent — MCP phase only.
Read saved CLI data, run the MCP test, append the CSV row, then stop.
Do NOT use vibium CLI commands. Do NOT run parallel work.

Site: {NAME}
URL: {URL}
Slug: {SLUG}
Category: {CATEGORY}

## Protocol

### Step 1 — Read CLI results
Run via Bash:
  cat /tmp/rerun_{SLUG}_cli.json

Parse cli_ms, cli_usd, cli_turns from the JSON.

### Step 2 — MCP snapshot (own bash call — MCP tool calls follow in the next turn)
Run via Bash:
  python3 ~/.claude/skills/practice-testing/token_bracket.py --snapshot --session > /tmp/rerun_{SLUG}_mcp_base.txt
  python3 -c "import time; print(int(time.time()*1000))" > /tmp/rerun_{SLUG}_mcp_t0.txt
  echo "MCP snapshot done"

### Step 3 — MCP test
Call these MCP tools in sequence:
  browser_stop   (ignore errors — clears any leftover session)
  browser_start
  browser_navigate url="{URL}"
  browser_wait_for_load timeout=10000
  browser_map
  {MCP_TEST_STEPS}

### Step 4 — Diff + record
Run via Bash:
  python3 -c "import time; print(int(time.time()*1000))" > /tmp/rerun_{SLUG}_mcp_t1.txt
  BASE_MCP=$(cat /tmp/rerun_{SLUG}_mcp_base.txt)
  DIFF=$(python3 ~/.claude/skills/practice-testing/token_bracket.py --diff "$BASE_MCP" --json)
  MCP_MS=$(( $(cat /tmp/rerun_{SLUG}_mcp_t1.txt) - $(cat /tmp/rerun_{SLUG}_mcp_t0.txt) ))
  MCP_USD=$(echo "$DIFF" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['cost_usd'])")
  MCP_TURNS=$(echo "$DIFF" | python3 -c "import sys,json; print(json.load(sys.stdin).get('turns',''))")
  CLI_DATA=$(cat /tmp/rerun_{SLUG}_cli.json)
  CLI_MS=$(echo "$CLI_DATA" | python3 -c "import sys,json; print(json.load(sys.stdin)['cli_ms'])")
  CLI_USD=$(echo "$CLI_DATA" | python3 -c "import sys,json; print(json.load(sys.stdin)['cli_usd'])")
  CLI_TURNS=$(echo "$CLI_DATA" | python3 -c "import sys,json; print(json.load(sys.stdin).get('cli_turns',''))")
  echo "{NAME},{CATEGORY},$CLI_MS,$CLI_USD,$CLI_TURNS,$MCP_MS,$MCP_USD,$MCP_TURNS,clean-two-phase;l3" \
    >> ~/.claude/skills/practice-testing/rerun_results.csv
  tail -1 ~/.claude/skills/practice-testing/rerun_results.csv

Output the appended CSV row, then stop.
```

---

## Post-batch steps

After all MCP agents in a batch complete:

1. Append corrected rows to CSV if any CLI reruns were needed (last-wins logic handles it)
2. Regenerate README:
   ```sh
   cd ~/.claude/skills/practice-testing
   python3 populate_readme.py --force && python3 update_timing.py
   ```
3. Update aggregate tables in README manually (populate_readme.py updates per-site rows only; aggregates require manual recalculation from CSV — see METHODOLOGY.md)
4. Update Site List below
5. Commit: `git add rerun_results.csv README.md && git commit -m "batch N: L3 AT N/42 (...)"`

---

## Site List for Rerun

Level 2 complete (2026-06-03). Level 3 in progress (2026-06-04+).
- **Measured:** 90/100 sites (74 GP+AT+API(4) cli-rerun-v2 + 7 Security + 3 Performance + 6 API fresh in session 2026-06-04)
- **Still pending:** 10 sites (4 API with 0 CLI turns + 6 API/Security remaining)

**Session 2026-06-04 findings — parallel agent collisions:**
Both CLI parallel batches (C1–C6) and foreground MCP agents running simultaneously caused data loss:

1. **Vibium daemon URL collision** (C1–C6 parallel CLI batches + shared daemon):
   - Parallel `vibium go` calls all target same daemon session; last agent's URL "wins"
   - Previous agents measure wrong page (e.g., Gin & Juice Shop saw Try Hack Me, Blaze Demo saw Swagger UI)
   - Affected: corrupted CLI cost/turns for 5 sites (Gin & Juice Shop, Blaze Demo, Demoblaze, Restful Booker, OWASP Juice Shop) + MCP measurement still valid (reads from correct URL)
   - **Fix:** Use vibium's **parallel context support** (like Playwright's `browser.newContext()`); see agent-test-automation skill for pattern

2. **Token bracket birthtime race** (background CLI batch during foreground MCP):
   - MCP agents create newer JSONL files; background CLI batch's `--snapshot --session` picked those up instead of own file
   - Result: 0 CLI turns for 4 API sites (json-placeholder, poke-api, serverest, spacetraders)
   - **Fix:** Session registration at agent start — `python3 token_bracket.py --register-session > /tmp/my_session.txt` once per agent, then use `--snapshot --session-file "$(cat /tmp/my_session.txt)"` for all snapshots

**Known data quality issues:**
- 4 sites need solo CLI reruns (0 turns): json-placeholder, poke-api, serverest, spacetraders
- Some URLs may have changed: DemoQA, Global SQA Demo, GreenKart, Hands-On Selenium WebDriver — verify CLI ms data before analysis

L3 ✓✓ = both L2 and L3 measured. L3 ✓ = L3 only. L2 ✓ = L2 only (pending L3).

**General Practice (28/28 L3, all cli-rerun-v2):**
AcademyBugs L3✓✓, A11y Coffee L3✓✓, Basic Calculator L3✓✓, BearQ L3✓,
Bill Payment API L3✓, Black Box Puzzles L3✓✓, BookCart L3✓✓, Candy Mapper L3✓✓,
Cnarios L3✓✓, Evil Tester L3✓✓, Gefälscht CompuTech L3✓✓, Parabank L3✓✓,
Parking Cost Calculator L3✓✓, PHP Travels L3✓✓, Polymer Shop L3✓✓, Potion Shop L3✓✓,
Practice Software Testing L3✓✓, PrestaShop L3✓✓, PromptQA Playground L3✓,
QA Practice L3✓✓, QA Training Simulator L3✓✓, Real World Example Apps L3✓✓,
testers.ai L3✓✓, Test Track L3✓✓, The Boozang Test Lab L3✓✓,
The iframe Search Engine L3✓✓,
ToDo List L3✓✓, UI5 Demo Kit L3✓✓

**Automation Testing (42/42 L3, all cli-rerun-v2):**
Applitools Demo L3✓✓, ATM Practice App L3✓✓, Automate Now Sandbox L3✓✓,
Automation Bookstore L3✓✓, Automation Camp L3✓✓, Automation Exercise L3✓✓,
Automation in Testing L3✓✓, Automation Test Store L3✓✓, Automation Testing Practice L3✓✓,
Coffee Cart L3✓✓, Commit Quality L3✓✓, Contact List App L3✓✓, Demo SaaS L3✓✓,
DemoQA L3✓✓, Expand Testing L3✓✓,
GitHub Users Search L3✓✓, Global SQA Demo L3✓✓, GreenKart L3✓✓,
Hands-On Selenium WebDriver L3✓✓, Lambdatest Playground L3✓✓, Let Code L3✓✓,
Locator Game L3✓✓, NearForm Testing Playground L3✓✓, OrangeHRM L3✓✓,
Practice Automation L3✓✓, Practice Test Automation L3✓✓, QA Cloud L3✓✓,
QA Playground L3✓✓, QE Buggy Todo L3✓✓, React Shopping Cart L3✓✓,
SeleniumBase L3✓✓, Selenium Playground L3✓✓, Selectors Hub L3✓✓, Swag Labs L3✓✓,
Sweet Shop L3✓✓, TestDino L3✓✓, The Internet L3✓✓, Travel Agileway L3✓✓,
Tricentis Obstacle Course L3✓✓, var.parts L3✓✓, Weather Shopper L3✓✓, XYZ Bank L3✓✓

**Security Testing (7/7 L3, all fresh 2026-06-04):**
Firing Range L3✓, Gin & Juice Shop L3✓ (URL collision during batch C1, MCP valid), Google Gruyere L3✓,
OWASP Juice Shop L3✓ (URL collision during batch C1, MCP valid), OWASP VWAD L3✓, Try Hack Me L3✓, Zero Bank L3✓ (BiDi error expected, HTTP-only)
— bWAPP, DVGA, VAmPI, LabEx Cybersecurity: local Docker only — permanent —

**API Testing (20/20 L3 or L2 pending solo reruns):**
Random User Generator L3✓✓, The Random Number Service L3✓✓, API Challenges L3✓, QuickPizza L3✓ (prior),
Airport Gap L3✓, AP+ Developers L3✓, Automation Exercise API L3✓, Chuck Norris API L3✓, Countries GraphQL L3✓,
FakeRestAPI L3✓, Go REST L3✓, httpbin L3✓, Restful Booker L3✓, Rick and Morty API L3✓, Swagger Petstore L3✓, The Cat API L3✓,
JSON Placeholder L3 (0 turns — solo rerun pending), Poké API L3 (0 turns — solo rerun pending),
ServeRest L3 (0 turns — solo rerun pending), SpaceTraders L3 (0 turns — solo rerun pending)

**Performance Testing (3/3 L3, all fresh 2026-06-04):**
Blaze Demo L3✓ (URL collision during batch C2, MCP valid), Demoblaze L3✓ (URL collision during batch C2, MCP valid), Pet Store Web L3✓

Per-site test steps for each site are documented in the Site Directory in SKILL.md.

---

## Parallel context isolation pattern (vibium, 2026-06-04)

**Problem:** Parallel CLI agents all call `vibium go` on shared daemon → last agent's URL wins, earlier agents measure wrong pages.

**Solution (from agent-test-automation M05):** Use vibium's parallel contexts — one browser, N contexts, N pages. Each agent in its own context = isolated, no collision.

```python
from vibium import browser as vibium_browser
from concurrent.futures import ThreadPoolExecutor

browser = vibium_browser.start()
try:
    contexts = [browser.new_context() for _ in sites]
    pages = [ctx.new_page() for ctx in contexts]
    with ThreadPoolExecutor(max_workers=2) as pool:  # Vibium cap: 2 workers
        futures = {pool.submit(run_site, site, page): site for site, page in zip(sites, pages)}
        for future in as_completed(futures):
            results.append(future.result())
finally:
    for ctx in contexts:
        ctx.close()
    browser.stop()
```

Reference: agent-test-automation/05-multi-agent/vibium/run.py (lines 127–139 in SKILL.md).
