# CLI vs MCP — Behavioral Comparison

Compiled from practice-testing exercise across 99 sites (2026-04-22 → 2026-05-19). Updated for v26.5.31 (2026-06-01).
Organized by command/tool pair. Confirmed differences come from observed cross-site behavior, not docs.

---

## Paired Commands — Diffs and Samesies

### navigate — `vibium go` / `browser_navigate`

| | CLI | MCP |
|---|---|---|
| HTTP-only URLs | BiDi error, page not loaded | Loads silently, no error |
| Subdomain pages | Deadlocks (B3) — must use `eval 'location.href="..."'` | Works without deadlock |
| Same-origin navigation | Same | Same |

**Verdict:** MCP wins on HTTP and subdomain navigation. CLI requires eval workaround for both.

---

### map — `vibium map` / `browser_map`

| | CLI | MCP |
|---|---|---|
| Standard DOM | Returns interactive refs | Returns interactive refs |
| React/Angular SPAs (JS-heavy) | May return nothing on first map | Same |
| Some SPAs (Angular Material, SAP UI5, Black Box Puzzles) | Returns nothing or subset | Returns more elements — up to 128+ vs 0 |
| Shadow DOM pages (Polymer Shop) | Returns nothing | Returns nothing |
| Async-loaded content | Misses elements not yet rendered | Same |

**Verdict:** Same behavior in most cases. MCP `browser_map` finds more elements on a subset of pages where CLI returns nothing or a subset — not consistently across all frameworks.

---

### get_text / text — `vibium text` / `browser_get_text`

| | CLI | MCP |
|---|---|---|
| Normal pages | Returns visible text | Same |
| Empty/blank/invisible pages | Works (returns empty string) | Works (returns empty string) — MB9 fixed in v26.5.31 |
| Very large text bodies (e.g. 5000 API results) | Crashes BiDi session | Returns oversized-output error (no crash) |

**Verdict:** Same on normal and empty pages. Different failure modes only on very large text — CLI crashes, MCP returns oversized error.

---

### evaluate / eval — `vibium eval 'expr'` / `browser_evaluate {expression}`

| | CLI | MCP |
|---|---|---|
| Multi-statement with semicolons | Fails due to shell quoting — split into separate calls | No shell quoting issue; all in one call |
| Expression returning `""` | Works | Works — MB6 fixed in v26.5.31 |
| Expression returning `null` | Works | Works |
| Parallel/async (`Promise.all`) | Limited | Works cleanly |

**Verdict:** CLI has shell quoting constraint only. Empty-string return now works in both.

---

### fill — `vibium fill selector value` / `browser_fill {selector, value}`

| | CLI | MCP |
|---|---|---|
| Text inputs | Works | Same |
| `<textarea>` | Works — B7 fixed in v26.5.31 | Works — MB7 fixed in v26.5.31 |
| Fill with empty string to clear | Rejects `""` — use eval to clear (B20 open) | Throws "value is required" — use eval to clear |
| Framework-driven inputs (React, Angular) | May not trigger state update | Same; use `browser_type` for key-event-driven components |

**Verdict:** Same on standard inputs and textarea (both fixed). Neither can clear a field with empty string — use eval.

---

### type — `vibium type selector value` / `browser_type {selector, value}`

| | CLI | MCP |
|---|---|---|
| Text inputs | Works | Same |
| `<textarea>` | Works | Works |
| Framework-driven textareas (React/Angular) | Works — fires events | Works — fires key events that update component state |
| Date inputs (`input[type=date]`) | Needs eval `.value =` (fill/type both fail) | Same — use eval |

**Verdict:** Same behavior across the board.

---

### select — `vibium select selector value` / `browser_select {selector, value}`

| | CLI | MCP |
|---|---|---|
| Matching | Matches by visible label OR value attribute (B5 fixed v26.5.31) | Same (shared engine fix) |
| Non-existent value | Errors: `no <option> matches "..."` exit 1 (B5 fixed) | Same |
| Angular ng-model select | Fails — model not updated | Same failure — use `eval .value= + dispatchEvent(change)` |

**Verdict:** Identical behavior. Both now match by visible label OR value attribute; both error on no match. Angular ng-model limitation applies to both.

---

### click — `vibium click selector` / `browser_click {selector}`

| | CLI | MCP |
|---|---|---|
| Standard interactive elements | Works | Same |
| `input[type=submit]` | Sometimes needs `eval .click()` | Works directly — no eval needed |
| Zero-size elements | Fails | Same failure |
| Elements obscured by overlay | Fails | Same; try `eval element.click()` |

**Verdict:** MCP `browser_click` succeeds on some elements (e.g. `input[type=submit]`) that CLI needs eval for.

---

### dblclick — `vibium dblclick` / `browser_dblclick`

| | CLI | MCP |
|---|---|---|
| Standard double-click | Works | Same |
| Entering edit mode (e.g. ToDo List) | Works | Works — follow with `browser_fill` + Enter |

**Verdict:** Same.

---

### check / uncheck — `vibium check` / `browser_check`, `vibium uncheck` / `browser_uncheck`

| | CLI | MCP |
|---|---|---|
| Visible checkboxes | Works | Same |
| Obscured checkboxes (e.g. ToDo List, React Shopping Cart) | Fails — use `vibium mouse click x y` | Fails — use `browser_mouse_click {x, y}` at computed coords |

**Verdict:** Same — both fail on obscured checkboxes; both need coordinate click workaround.

---

### hover — `vibium hover` / `browser_hover`

| | CLI | MCP |
|---|---|---|
| Interactive elements | Works | Same |
| Non-interactive `<div>` elements | Works — B30 partial fix v26.5.31 | Same |
| Non-interactive `<img>` with external src | Fails: `visible check failed — zero size` (B30 still open) | Use `browser_mouse_move` to computed coords |
| Other non-interactive elements | Use `vibium mouse move x y` | Use `browser_mouse_move` to computed coords |

**Verdict:** CLI partial improvement — hover on `<div>` now works. Both still need coordinate mouse_move for `<img>` with external src (zero-size race) and other non-interactive elements.

---

### find — `vibium find {role, text}` / `browser_find {role, text}`

| | CLI | MCP |
|---|---|---|
| Finding by text | Works; returns outermost matching element | Same |
| `role="link"` on `<a>` | Works | Same |
| `role="link"` on `<button>` | Works | Times out — use `browser_map` ref or CSS selector instead |
| `role="button"` on `<button>` | Works | Works |

**Verdict:** MCP `browser_find {role: "link"}` times out on `<button>` elements. CLI handles it correctly.

---

### press — `vibium press key` / `browser_press {key}`

| | CLI | MCP |
|---|---|---|
| Standard keys (Enter, Tab, Escape) | Works | Same |

**Verdict:** Same.

---

### keys — `vibium keys` / `browser_keys`

**Verdict:** Same. No behavioral differences observed.

---

### drag — `vibium drag` / `browser_drag`

| | CLI | MCP |
|---|---|---|
| Standard HTML drag-and-drop | Works | Same |
| jQuery UI droppable | Fires events but framework ignores them | Same limitation |
| Shadow DOM drag targets | Use coordinate fallback | Same |
| `vibium drag @ref` / `browser_drag` on some sites | Fails — use mouse coords | Works when content is top-level |
| Polymer events | Not fired by standard drag | Not fired — must use `browser_mouse_click` at bounding-box coords |

**Verdict:** Same limitations across frameworks. Coordinate-based mouse events are the common fallback for both.

---

### scroll — `vibium scroll` / `browser_scroll`

**Verdict:** Same. No behavioral differences observed.

---

### focus — `vibium focus` / `browser_focus`

**Verdict:** Same. No behavioral differences observed.

---

### upload — `vibium upload` / `browser_upload`

**Verdict:** Same. Confirmed working on both.

---

### mouse_move / mouse_click / mouse_down / mouse_up

CLI: `vibium mouse move x y` / `vibium mouse click x y` / `vibium mouse down x y` / `vibium mouse up x y`
MCP: `browser_mouse_move {x,y}` / `browser_mouse_click {x,y}` / `browser_mouse_down {x,y}` / `browser_mouse_up {x,y}`

**Verdict:** Same. Low-level coordinate actions behave identically.

---

### back / forward — `vibium back` / `browser_back`, `vibium forward` / `browser_forward`

**Verdict:** Same. No behavioral differences observed.

---

### frames / frame — `vibium frames` / `browser_frames`, `vibium frame` / `browser_frame`

| | CLI | MCP |
|---|---|---|
| Listing frames | `vibium frames` lists available frames | `browser_frames` same |
| Entering frame context | `vibium frame "<name>"` — does NOT persist between calls; subsequent commands run in main frame | `browser_frame` — returns metadata only, does NOT switch context |
| Workaround | `eval contentDocument.body` from within frame | `eval contentDocument.body` or navigate directly to iframe src URL |

**Verdict:** Same limitation. Neither properly switches frame context for subsequent commands. Both require eval workarounds.

---

### get_url / url — `vibium url` / `browser_get_url`

| | CLI | MCP |
|---|---|---|
| Normal read | Works | Same |
| Immediately after navigation (post-login) | BiDi timing issue — need `sleep 5` | No timing issue observed |

**Verdict:** CLI has post-navigation timing sensitivity. MCP doesn't.

---

### screenshot — `vibium screenshot -o file.png [--full-page]` / `browser_screenshot {filename, fullPage}`

**Verdict:** Same. Identical behavior.

---

### get_title / title — `vibium title` / `browser_get_title`

**Verdict:** Same.

---

### diff_map — `vibium diff map` / `browser_diff_map`

**Verdict:** Same concept. No behavioral differences observed in practice.

---

### stop / start — `vibium stop` / `browser_stop`, `vibium start` / `browser_start`

| | CLI | MCP |
|---|---|---|
| Scope | Restarts the CLI daemon | Restarts the MCP browser session |
| Cross-interface | CLI stop/start has NO effect on MCP session | MCP stop/start has NO effect on CLI daemon |

**Verdict:** Completely isolated sessions. Restarting one does not affect the other.

---

### Dialog handling — no CLI tool / `browser_dialog_accept` + `browser_dialog_dismiss`

| | CLI | MCP |
|---|---|---|
| Native alert/confirm/prompt | Pre-stub BEFORE clicking: `eval 'window.alert=function(){}'` — clicking first deadlocks daemon permanently | Has native `browser_dialog_accept` / `browser_dialog_dismiss` tools |
| Direct click on alert trigger | Deadlocks daemon (B3 open) — requires `pkill -f vibium && sleep 2 && vibium daemon start` | Also deadlocks (MB3 open, deferred) — `browser_click` hangs until i/o timeout |
| Safe pattern | `eval 'window.alert=function(){}'` → then click | `browser_evaluate {setTimeout(..., 300)}` + `browser_sleep {ms: 350}` + `browser_dialog_accept {}` |
| Recovery from deadlock | `pkill -f vibium && sleep 2 && vibium daemon start && sleep 2` | `browser_stop` + `browser_start` |

**Verdict:** MCP has dedicated dialog tools; CLI must pre-stub via eval. Both deadlock if the click fires before the dialog handler is in place — same root constraint, different mitigation syntax. (#146, #151, #128 deferred to follow-up release.)

---

## MCP-Only Tools (no CLI equivalent confirmed)

| MCP Tool | Purpose | Notes |
|---|---|---|
| `browser_a11y_tree` | Accessibility tree dump | No CLI equivalent |
| `browser_count {selector}` | Count matching elements | No CLI equivalent — MB1 fixed in v26.5.31 |
| `browser_delete_cookies` | Delete cookies | No CLI equivalent |
| `browser_dialog_accept` / `browser_dialog_dismiss` | Native dialog interception | CLI must pre-stub via eval |
| `browser_download_set_dir` | Set download directory | No CLI equivalent |
| `browser_emulate_media` | Media type emulation (print/screen) | No CLI equivalent |
| `browser_find_all {selector}` | Find all matching elements | CLI `vibium find` returns first match only |
| `browser_get_attribute {selector, name}` | Get element attribute value | CLI needs `eval getAttribute(...)` |
| `browser_get_cookies` / `browser_set_cookie` | Cookie read/write | No CLI equivalent |
| `browser_get_html {selector}` | Get innerHTML/outerHTML | No CLI equivalent |
| `browser_get_value {selector}` | Get input current value | No CLI equivalent |
| `browser_get_viewport` / `browser_set_viewport` | Viewport dimensions | No CLI equivalent |
| `browser_get_window` / `browser_set_window` | Window position/size | No CLI equivalent |
| `browser_highlight {selector}` | Visual highlight in browser | No CLI equivalent |
| `browser_is_checked` / `browser_is_enabled` / `browser_is_visible` | Boolean state queries | CLI needs eval or `vibium find` pattern |
| `browser_list_pages` / `browser_new_page` / `browser_close_page` / `browser_switch_page` | Multi-tab management | CLI has no tab management |
| `browser_pdf` | Export page as PDF | No CLI equivalent |
| `browser_record_start` / `browser_record_stop` (+ chunk/group variants) | Session recording | No CLI equivalent |
| `browser_reload` | Reload current page | CLI uses `eval 'location.reload()'` |
| `browser_restore_storage` / `browser_storage_state` | localStorage/sessionStorage snapshot/restore | No CLI equivalent |
| `browser_scroll_into_view {selector}` | Scroll element into viewport | CLI uses `eval scrollIntoView()` |
| `browser_set_content {html}` | Replace page content with raw HTML | No CLI equivalent |
| `browser_set_geolocation` | Spoof browser geolocation | No CLI equivalent |
| `browser_sleep {ms}` | Wait in milliseconds | CLI uses shell `sleep N` (seconds only) |
| `browser_wait_for_fn {fn}` | Wait until JS expression is truthy | No CLI equivalent |
| `browser_wait_for_text {text}` | Wait until text appears on page | No CLI equivalent |
| `browser_wait_for_url {url}` | Wait until URL matches | No CLI equivalent |
| `page_clock_install` / `page_clock_set_fixed_time` / `page_clock_set_system_time` / `page_clock_set_timezone` / `page_clock_pause_at` / `page_clock_resume` / `page_clock_fast_forward` / `page_clock_run_for` | Mock/control page clock | No CLI equivalent |

---

## CLI-Only Behaviors (observed, no MCP equivalent)

| CLI Behavior | Notes |
|---|---|
| PATH prefix required | Must `export PATH="/usr/local/bin:$PATH"` to avoid Python vibium binary | 
| Shell sleep (seconds) | `sleep N` — integer seconds only; MCP `browser_sleep {ms}` is milliseconds |
| Daemon persistence across Bash tool calls | CLI daemon stays alive between shell invocations; MCP tools are stateless calls |
| Pre-stub required before any alert-triggering click | No MCP equivalent — MCP uses dialog tools instead |

---

## Cross-Cutting Behavioral Samesies

These behave identically across both interfaces:

- **select**: both match by visible label OR value attribute (B5/engine fixed v26.5.31); both error on non-existent option
- **textarea fill**: both work with `fill` (B7/MB7 fixed v26.5.31); `type` still works as alternative
- **obscured checkbox**: both fail with `check`; both need coordinate click
- **shadow DOM**: both return nothing from map; both need `eval shadowRoot`
- **Angular ng-model select**: both fail to trigger model update; both need eval + dispatchEvent
- **canvas/custom-painted elements**: both return nothing from map; both need coordinate click from getBoundingClientRect
- **Azure/Heroku hibernated backends**: same 3s wait + reload needed
- **CSS text-transform**: both find by DOM text, not rendered text
- **frame context**: neither properly persists frame switch; both need eval workaround
- **jQuery UI droppable**: drag fires but framework ignores — eval workaround for both
- **BiDi session recovery**: both need stop + start after broken pipe
