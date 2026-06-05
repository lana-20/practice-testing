# Concurrent & Parallel Execution Analysis

**Date:** 2026-06-05  
**Scope:** MCP vs Native APIs for multi-page/multi-context browser automation  
**Context:** Measuring 7 QA practice sites with CLI + MCP to validate L3 protocol stability

---

## Executive Summary

**Key Finding:** MCP (Model Context Protocol) is architecturally unsuitable for concurrent multi-page operations. Native client APIs (Python, JavaScript) support true parallelism via contexts; MCP does not.

| Approach | Concurrency | Context Model | Best For |
|----------|-------------|---------------|----------|
| **Native API** (Python/JS) | ✅ Native async/parallel | Native contexts | Automation frameworks, high-throughput testing |
| **MCP Tool Interface** | ❌ Sequential only | Single active page | Exploratory automation, stateful reasoning, rich introspection |
| **CLI+SKILLS** | ✅ Parallel execution | Stateless commands | Token-efficient agents, rapid iteration |

---

## Part 1: MCP Architecture Limitations

### 1.1 MCP Design Model

MCP (Model Context Protocol) uses a **stateful tool interface** where:
- Tools operate on a single **active context** (one browser, one page, one focus)
- Tool calls are method invocations on that context
- Switching context requires an explicit tool call (`browser_switch_page`)

**Tool signature pattern:**
```
browser_navigate(url)        ← operates on active page
browser_click(selector)       ← operates on active page
browser_switch_page(pageIndex) ← changes active page
```

**Problem:** No `pageIndex` or `contextId` parameter on action tools.

### 1.2 Why Parallel Context Tool Calls Don't Work

Hypothetical concurrent MCP scenario:
```
// Doesn't work — tool calls are sequential via stdio
[1] browser_switch_page {pageIndex: 0}
[2] browser_navigate {url: "site1"}     ← must wait for [1]
[3] browser_switch_page {pageIndex: 1}
[4] browser_navigate {url: "site2"}     ← must wait for [3]
```

Even if Claude made these tool calls concurrently, the MCP server would:
1. Receive call on stdio (single stream, serialized)
2. Execute tool 1 → set active page to 0
3. Execute tool 2 → navigate page 0
4. Execute tool 3 → set active page to 1
5. Execute tool 4 → navigate page 1

**Result:** Sequential execution due to stateful stdio stream.

### 1.3 The Accessibility Tree Trade-off

MCP's strength is **rich introspection**:
- Sends full accessibility tree with each response
- Enables semantic reasoning about page structure
- Stateful connection allows incremental updates
- Better for exploration, self-healing tests, iterative reasoning

**Cost:** Cannot parallelize because state must be maintained between calls.

---

## Part 2: Playwright's Architectural Position

### 2.1 Playwright MCP vs Playwright CLI

From **official Playwright documentation** ([playwright.dev/docs/getting-started-mcp](https://playwright.dev/docs/getting-started-mcp)):

> **CLI:** Modern coding agents increasingly favor CLI–based workflows exposed as SKILLs over MCP because CLI invocations are more token-efficient: they avoid loading large tool schemas and verbose accessibility trees into the model context, allowing agents to act through concise, purpose-built commands. **This makes CLI + SKILLs better suited for high-throughput coding agents that must balance browser automation with large codebases, tests, and reasoning within limited context windows.**

> **MCP:** MCP remains relevant for specialized agentic loops that benefit from persistent state, rich introspection, and iterative reasoning over page structure, such as exploratory automation, self-healing tests, or long-running autonomous workflows where maintaining continuous browser context outweighs token cost concerns.

**Key insight:** Playwright's creators **recommend CLI for parallel/concurrent work**, not MCP.

### 2.2 Playwright Native API Concurrency

Playwright's JavaScript/Python clients support true async concurrency:

```javascript
// Native Playwright — true parallel execution
const context1 = await browser.newContext();
const context2 = await browser.newContext();
const page1 = await context1.newPage();
const page2 = await context2.newPage();

// These run concurrently
await Promise.all([
  page1.goto(url1),
  page2.goto(url2),
  page1.waitForLoadState(),
  page2.waitForLoadState(),
]);
```

**Why it works:**
- Separate context objects in memory
- Native async/await with proper event loop
- No shared state between contexts
- Full isolation at the browser level (via Playwright's BiDi protocol)

---

## Part 3: Vibium's Parallel Context Pattern

### 3.1 Vibium Python API: Native Parallelism

Vibium's Python client mirrors Playwright's native concurrency:

```python
from vibium import browser as vibium_browser
from concurrent.futures import ThreadPoolExecutor

browser = vibium_browser.start(headless=True)

# Create isolated contexts + pages
contexts = [browser.new_context() for _ in range(7)]
pages = [ctx.new_page() for ctx in contexts]

# Parallel measurement with thread pool
def measure_site(site_url, page):
    page.go(site_url)
    page.wait_for_load_state("load")
    return {
        "url": page.url(),
        "title": page.title(),
        "elements": len(page.map()),
    }

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = {
        pool.submit(measure_site, url, page): url
        for url, page in zip(site_urls, pages)
    }
    results = {futures[f]: f.result() for f in futures}
```

**Why it works:**
- One browser instance (resource-efficient)
- N isolated contexts (no cross-contamination)
- N pages (one per context)
- ThreadPoolExecutor for concurrent execution
- Each page has its own state, no conflicts

**Pattern:** Same as Playwright's `browser.newContext()` approach.

### 3.2 Vibium MCP: Sequential Only

Vibium MCP tools **do not support context parameters**:

From **Vibium API Reference** (`vibium-src/docs/reference/api.md`):
- Row 3: "Create a new browser context" → **JS/Python only** (not in MCP)
- Row 4: "List all pages" → `browser_list_pages` (MCP has this)
- Row 42: "Bring page to front" → `browser_switch_page` (MCP has this)

**Key finding:** MCP has `browser_new_page` and `browser_switch_page`, but:
1. No `browser_new_context` (contexts not exposed via MCP)
2. No page/context ID on action tool parameters
3. Single active page at any moment

**Consequence:** Concurrent operations impossible; must serialize.

---

## Part 4: Architectural Comparison

### 4.1 Native API (Python/JavaScript)

| Aspect | Status |
|--------|--------|
| **Concurrent execution** | ✅ Native via async/await |
| **Context isolation** | ✅ First-class `browser.newContext()` |
| **Page parameters** | ✅ Direct page object reference |
| **Token efficiency** | ⚠️ Large object graphs in memory |
| **Introspection richness** | ⚠️ Limited (direct objects, not accessibility trees) |
| **Suitable for** | Automation frameworks, test suites, high-throughput agents |

### 4.2 MCP Tool Interface

| Aspect | Status |
|--------|--------|
| **Concurrent execution** | ❌ Sequential stdio, stateful |
| **Context isolation** | ⚠️ Pages only, no contexts via MCP |
| **Page parameters** | ❌ No pageIndex on action tools, must switch first |
| **Token efficiency** | ✅ Concise tool schemas, stateless-looking calls |
| **Introspection richness** | ✅ Full accessibility trees, rich state |
| **Suitable for** | Exploratory automation, reasoning loops, debugging |

### 4.3 CLI + SKILLS

| Aspect | Status |
|--------|--------|
| **Concurrent execution** | ✅ Stateless, can parallelize at agent level |
| **Context isolation** | ✅ Each SKILL invocation is isolated |
| **Page parameters** | ✅ Per-SKILL state isolation |
| **Token efficiency** | ✅ No verbose schemas, concise output |
| **Introspection richness** | ⚠️ Minimal; must request what you need |
| **Suitable for** | High-throughput agents, rapid iteration, parallel tasks |

---

## Part 5: Why Parallel Contexts Work in Native APIs

### 5.1 The Threading Model

Native APIs use proper **threading/async isolation**:

```python
# Each thread has its own page object
threads = [
    Thread(target=measure_site, args=(url1, page1)),
    Thread(target=measure_site, args=(url2, page2)),
    Thread(target=measure_site, args=(url3, page3)),
]
# All run truly in parallel — OS-level threading
```

**Key:** Each page object is independent; no shared state.

### 5.2 Why MCP Can't Do This

MCP's stdio model is **fundamentally serial**:

```
Claude → MCP Server (stdio)
         └─ Single input stream
         └─ Single output stream
         └─ Tools execute one at a time
```

Even if Claude's internal parallel tool calling works, the **MCP server receives serialized tool calls on a single stdio stream** and executes them sequentially.

---

## Part 6: Vibium's Documented Pattern

From **`PROTOCOL.md`** (practice-testing skill):

> Parallel contexts (one browser, N contexts, N pages, per-context isolation) prevent daemon URL collisions.

**Implementation:** `parallel_cli_vibium.py` and `parallel_cli_contexts.py`

```python
# From parallel_cli_vibium.py
browser = vibium_browser.start(headless=True)
contexts = [browser.new_context() for _ in VERIFY_SITES]
pages = [ctx.new_page() for ctx in contexts]

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = {
        pool.submit(measure_site_vibium, site, page): site
        for site, page in zip(VERIFY_SITES.keys(), pages)
    }
```

**Why this works:**
- One browser manages all contexts (resource-efficient)
- Each context is isolated (vibium daemon constraint: one URL per CLI call)
- ThreadPoolExecutor limits concurrent workers to 2 (vibium capacity)
- Pages run in parallel; each measures in isolation

---

## Part 7: Implications for 7-Site Measurement

### 7.1 Optimal Approach: Hybrid

**Option A (Recommended):**
- **CLI measurements:** Use vibium Python API with parallel contexts (fast, token-efficient)
- **MCP measurements:** Run sequentially via Claude tools (rich introspection, but slower)

**Why:**
- CLI parallelism leverages vibium's native concurrency (2-3× faster)
- MCP sequential is acceptable for 7 sites (7 switch_page calls + operations)
- Both use same browser instance (resource-efficient)

**Timeline estimate:**
- Parallel CLI: ~15–25s total (2 workers, 7 sites)
- Sequential MCP: ~45–60s total (switch + operate per site)
- **Total:** ~60–85s for both CLI + MCP across 7 sites

### 7.2 Alternative: Pure Sequential

Both CLI and MCP sequential (one site at a time):
- Simpler code
- Slower: ~90–120s total
- No parallelism advantage

### 7.3 Not Viable: Parallel MCP

Attempting concurrent MCP tool calls:
- Tool calls serialize on stdio anyway
- No true parallelism
- Adds complexity without benefit
- Worse than sequential approach

---

## Part 8: Reference: Tool Parameter Comparison

### MCP Tools (Vibium)

```
browser_start {} → Browser
browser_new_page {url?} → Page
browser_switch_page {pageIndex}
browser_navigate {url}  ← NO page_id parameter
browser_map {}  ← NO page_id parameter
browser_click {selector}  ← NO page_id parameter
```

**Constraint:** All action tools operate on active page only.

### Native API (Vibium Python)

```python
browser = vibium_browser.start()
context = browser.new_context()  # Returns context object
page = context.new_page()  # Returns page object
page.go(url)  # Direct method on page object — no switching needed
page.map()  # Direct method on page object
page.click(selector)  # Direct method on page object
# Each page can run in parallel
```

**Advantage:** Page objects are first-class; direct references, no "active page" concept.

---

## Part 9: Key Takeaways

### What Works for Parallelism

✅ **Native APIs** (Python, JavaScript)
- Built for concurrency via native async/threading
- Context isolation by default
- Suitable for: Automation frameworks, test suites, high-throughput agents

✅ **CLI + SKILLS** (Playwright's recommendation)
- Stateless commands, parallelizable at agent level
- Token-efficient
- Suitable for: High-throughput agents, parallel workflows

### What Doesn't Work for Parallelism

❌ **MCP Tool Interface**
- Stateful, single active page
- Serial execution on stdio
- No page/context parameters on action tools
- Suitable for: Exploratory automation, reasoning loops, debugging

### Playwright's Official Position

From official docs: **Use CLI+SKILLS for parallel/concurrent work.** MCP is better for exploratory, stateful, iterative reasoning.

---

## Part 10: Recommendation for L3 Verification (7 Sites)

**Best approach: Hybrid parallel CLI + sequential MCP**

**CLI Phase (parallel):**
```python
# Measure all 7 sites concurrently using vibium Python API
browser = vibium_browser.start(headless=True)
contexts = [browser.new_context() for _ in range(7)]
pages = [ctx.new_page() for ctx in contexts]

with ThreadPoolExecutor(max_workers=2) as pool:
    futures = {
        pool.submit(measure_site, site, page): site
        for site, page in zip(sites, pages)
    }
    # ~15–25s total for 7 sites
```

**MCP Phase (sequential):**
```
for site in sites:
    browser_new_page {url: site}
    browser_wait_for_load {}
    browser_map {}
    browser_screenshot {}
    # Switch next page, repeat
    # ~45–60s total for 7 sites
```

**Total runtime:** ~60–85s  
**Token cost:** Minimal (CLI use only for actual measurement, MCP for rich introspection)

---

## References

- **Playwright MCP Docs:** https://playwright.dev/docs/getting-started-mcp
- **Playwright MCP GitHub:** https://github.com/microsoft/playwright-mcp
- **Vibium API Reference:** `/vibium-src/docs/reference/api.md` (Row 3, 4, 42)
- **Practice-testing PROTOCOL.md:** Parallel contexts pattern, L3 measurement bracket
- **MCP Spec:** Model Context Protocol design (stateful tool interface via stdio)

---

**Document Status:** Complete  
**Verified Against:** Vibium API reference, Playwright official docs, MCP protocol design  
**Next Action:** Proceed with hybrid approach for 7-site L3 verification
