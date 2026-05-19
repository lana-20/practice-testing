---
name: practice-testing
description: Explore and test QA practice sites. Pass a site name or URL to navigate, map, interact, and report bugs/observations. Use when asked to test practice sites or QA playgrounds.
---

# practice-testing

Run exploratory tests on QA practice sites using vibium browser automation.

## How to run

`/practice-testing [site-name-or-url] [--cli|--mcp]`

- `/practice-testing AcademyBugs` — test by name (default: CLI mode)
- `/practice-testing Parabank --mcp` — test using vibium MCP tools
- `/practice-testing https://example.com` — test any URL directly
- `/practice-testing` — list all available practice sites

### Mode selection

**CLI mode** (default): Uses vibium CLI commands via Bash tool.
- Invoked as shell commands: `vibium go`, `vibium map`, `vibium click @eN`, etc.
- Requires `export PATH="/usr/local/bin:$PATH"` prefix to avoid Python vibium binary
- Daemon can deadlock on native dialogs — pre-stub with `eval 'window.alert=function(){}'`
- `vibium select` matches by option value attribute, not display text

**MCP mode**: Uses `mcp__vibium__browser_*` tool calls directly.
- Dialog handling via `browser_dialog_accept` / `browser_dialog_dismiss`
- **MB3 applies to MCP too**: direct `browser_click` on a native `alert()` trigger deadlocks — use `browser_evaluate { setTimeout(..., 300) }` + `browser_sleep {ms: 350}` + `browser_dialog_accept {}` pattern
- `browser_select` matches by option value (same as CLI)
- `browser_find` with `role=link` times out on `<button>` elements — use `browser_map` refs or CSS selectors
- `browser_get_text` throws `invalid_union` on empty/blank page content (MB9) — use `browser_evaluate { expression: "document.body.innerText || null" }` instead
- `browser_evaluate` returning `""` throws `invalid_union` (MB6) — use `|| null`, never `|| ''`
- MCP runs a separate browser session from the CLI daemon; stop/start MCP browser via `browser_stop` + `browser_start`

## Site Directory

### General Practice

| Name | URL | CLI Notes | MCP Notes |
|------|-----|-----------|-----------|
| AcademyBugs | https://academybugs.com/ | 25 bugs planted; dismiss tutorial modal + cookie banner; sort dropdown non-functional with text-based select — select uses numeric values ("0"–"4"); view filter (10/25/50) broken; cart total bug: $152.99 for $45 item + $7.99 shipping (expected $52.99); Russian text bug at /account/ | `browser_select` by value works — sort IS functional; map refs for dismiss; same bugs |
| Basic Calculator | https://testsheepnz.github.io/BasicCalculator.html | Prototype + builds 1–9; select operation by value ("0"–"4"), not text | same as CLI |
| Black Box Puzzles | https://blackboxpuzzles.workroomprds.com/ | Only 22, 24, 26b, 29, 31, 33, 34 work (Flash); `vibium map` returns nothing on index; coordinate clicks inside puzzle custom elements | `browser_map` finds all puzzle nav links; coordinate clicks still required inside custom elements |
| BookCart | https://bookcart.azurewebsites.net/ | Azure-hosted; backend frequently hibernated; Angular Material inputs fill by `#mat-input-N` | `browser_find {role:"link", text:"Login"}` times out — Login is a button, use map ref; same hibernated backend |
| Cnarios | https://www.cnarios.com/ | Challenges work; /concepts/* pages render blank (React routing bug) | `browser_get_text` throws `invalid_union` on blank pages (MB9) — use `browser_evaluate { expression: "document.body.innerText \|\| null" }` |
| Evil Tester | https://testpages.eviltester.com/styled/index.html | Stub alert/confirm/prompt via `eval` BEFORE clicking alert buttons | `browser_click` on alert button deadlocks (MB3); use `browser_evaluate {setTimeout(...,300)}` + `browser_sleep {ms:350}` + `browser_dialog_accept {}` |
| Gefälscht CompuTech | https://webtestingcourse.dequecloud.com/ | Intentionally inaccessible; contact form fields need `input[name=x]` selectors; contact URL is `/contact.php` (not `/contact/` — 404) | `browser_map` refs work for form fields without name selectors; same `/contact.php` URL |
| Magento | https://magento.softwaretestingboard.com/ | DOWN — Cloudflare 526 SSL error as of 2026-04-22 | same — still down |
| Parabank | https://parabank.parasoft.com/parabank/admin.htm | Run DB Initialize first; after init any username/password logs in (intentional); use for form/validation testing only | same as CLI |
| Parking Cost Calculator | https://www.shino.de/parkcalc/ | Option values not text for lot dropdown; input names PascalCase (`StartingDate`, `LeavingTime`); invalid dates → inline error (not blank page); Valet: $12 ≤5h / $18/day >5h (boundary inclusive at exactly 5h); Economy: $9/day max | same as CLI — all rates and selectors confirmed |
| PHP Travels | http://phptravels.com/demo/ | Landing page only — credentials sent by email; Login nav broken (redirects to same page); Submit button deadlocks daemon — pre-stub dialogs before clicking | No deadlock on Submit; Submit obscured to `browser_click` — use `eval document.getElementById('demo').click()`; math captcha: read `#numb1 + #numb2` from DOM dynamically |
| Polymer Shop | https://shop.polymer-project.org/ | All UI in Web Components shadow DOM — `vibium map` returns nothing; traverse via `eval shadowRoot`; coordinate clicks for buttons; cart server-side | Same shadow DOM constraints; `shadowRoot.querySelector('button').click()` does NOT fire Polymer events — must use `browser_mouse_click` at computed bounding-box coordinates |
| Practice Software Testing | https://practicesoftwaretesting.com/ | Angular app; add to cart works without login; credentials: `customer@practicesoftwaretesting.com` / `welcome01`; Login is `input[type=submit]` — use `eval.click()` | `browser_click` on `input[type=submit]` works directly — no eval needed; `browser_map` finds all 71 elements cleanly |
| Presta Shop | https://demo.prestashop.com/ | Store in iframe — get inner URL via `eval 'document.querySelector("#framelive")?.src'` after 5s wait; subdomains expire ~2 min; `vibium go` to subdomain pages deadlocks (B3) — use `eval 'location.href="..."'`; add-to-cart AJAX fails silently (cart stays 0) | `browser_navigate` to subdomain pages works without deadlock; same AJAX failure; same subdomain expiry; `browser_map` finds 106 elements |
| QA Practice | https://qa-practice.razvanvancea.ro/ | Login: `admin@admin.com` / `admin123`; ADD TO CART uppercase — use map refs; pre-stub alert/confirm before clicking alert buttons; checkout: Shipping Details form (phone, street, city, country) | MB3 deadlock on direct Alert button click — use setTimeout+sleep+dialog_accept; full e-commerce flow works; country select value = display text exactly (e.g. "United States of America") |
| QA Training Simulator | https://bugeater.web.app/ | **BugEater 2.0** (as of 04.2026): challenges renumbered (#1.1–#7.6); `vibium fill` works on React inputs; dismiss react-joyride tutorial; two cookie banners (homepage + `/app/list`); old note "scripted/functional crash with TypeError" is outdated | Direct URL to all route types works — no TypeError; `browser_fill` works on React inputs; dismiss tutorial with Skip; two cookie banners; challenge list at `/app/list` |
| Random User Generator | https://randomuser.me/ | API testing site; API at `/api/`; `?results=0/abc/-1/5001` all silently return 1 result; `?format=csv` triggers download — crashes BiDi session; `vibium text` crashes on `?results=5000` — use `vibium eval 'JSON.parse(document.body.innerText)'`; `?inc=name,email` and `?seed=abc` work | `browser_get_text` on `?results=5000` → oversized output error (not crash, but unusable); use `browser_evaluate {JSON.parse(document.body.innerText)}` instead; skip `?format=csv` (download may crash session) |
| Real World Example Apps | https://codebase.show/projects/realworld | Requires GitHub OAuth; SvelteKit SPA needs ~3s after `wait load`; Frontend/Backend/Fullstack tabs and language filters work via `vibium click`; after `vibium back` from GitHub sleep 3s again | Same as CLI — 3s sleep required; tabs/language filters work via `browser_click`; Sign in → GitHub OAuth confirmed |
| The Boozang Test Lab | https://thelab.boozang.com/ | React SPA; `vibium fill` works for inputs; Form Fill saves to shared DB — use unique test data; navigate to challenge pages via direct URL | Homepage `browser_map` returns only 10 elements — challenge section not visible; use direct URLs (e.g. `/formFill`, `/sortedList`); `browser_fill` and `browser_click` work cleanly |
| The iframe Search Engine | https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html | Use `vibium fill` (not type) for search input; `vibium select` with non-existent value silently sets `selectedIndex=-1` (B5); use full URL as option value; "Go search" opens in new tab; Bing embeds; Google/DuckDuckGo block iframe | `browser_fill` works; `browser_select` by full URL value works; B5 confirmed — non-existent value returns success but `selectedIndex=-1`; always verify select state |
| The Internet | http://the-internet.herokuapp.com/ | 44 examples; `vibium hover` fails on non-interactive elements — use `vibium mouse move x y`; `vibium frame` doesn't persist between CLI calls — use `eval contentDocument.body`; `vibium fill` fails on `input[type=range]` — use `eval .value + dispatchEvent`; `vibium check` fails on obscured checkboxes — use `vibium mouse click x y`; `vibium drag`/`upload`/`press` work; shadow_dom page 404 | `browser_map` returns all 44 links; `browser_drag` works; `browser_upload` works; `browser_press` works; `browser_fill` fails on range — use eval; `browser_check` fails obscured — use `browser_mouse_click` at coords; hover via `browser_mouse_move` to computed coords + `getComputedStyle()`; MB1 on `browser_count`; MB3 on direct alert click; MB6 on `.style.display` (use `getComputedStyle`) |
| The Random Number Service | https://www.random.org/ | Cookie banner on load — dismiss "Allow All"; generator forms not in `vibium map` — use URL params or `eval form.submit()`; inline `eval` with semicolons fails (shell quoting) — use direct URL params; validation: min>max/num>10000 → error; negative accepted; `?format=plain` returns raw text | same as CLI — cookie banner via `browser_click "Allow All"`; `browser_map` finds all nav links (81 refs); URL params work for all generator types; skip `?format=csv` (download may crash session) |
| Testing Challenges | http://testingchallenges.thetestingmap.org/ | HTTP-only; Chrome BiDi blocks navigation entirely; cannot be tested with vibium | same — `browser_navigate` fails with BiDi "unknown error"; SKIP |
| ToDo List | https://todolist.james.am/#/ | AngularJS app; `vibium check` fails on checkboxes (obscured) — use `vibium mouse click x y`; `vibium dblclick` enters edit mode; BUG: item counter off by 1; BUG: delete button title "TODO:REMOVE THIS EVENTUALLY"; no localStorage persistence | same bugs confirmed; `browser_check` fails (obscured) — use `browser_mouse_click` at computed coords; `browser_dblclick` + `browser_fill` + Enter for edit; whitespace input silently rejected |
| UI5 Demo Kit | https://ui5.sap.com/#/demoapps | SAP UI5 SPA; main page `vibium map` returns nothing — use `vibium find text` for nav; demo app links via `eval querySelector.click()`; individual apps have normal DOM; Shopping Cart demo fully interactive | `browser_map` returns 128 refs on main page (unlike CLI); top nav works via `browser_click`; Shopping Cart demo: add-to-cart → cart panel → proceed to checkout all work; demo app URLs extractable via `browser_evaluate` |

### Automation Testing

| Name | URL | CLI Notes | MCP Notes |
|------|-----|-----------|-----------|
| Automation Bookstore | https://automationbookstore.dev/ | Filter-only SPA; all 8 book links `href="#"` (no detail page); case-insensitive real-time filter works; no "no results" message on empty filter | same as CLI; filter hides via CSS class not `style.display` — DOM style checks mislead; use screenshot to verify filter state |
| Automation Camp | https://play2.automationcamp.ir/ | Alert button + invalid login deadlock daemon — `eval` override does not prevent it; valid login: `test`/`test`; `input[type=date]` — use `eval .value =`; form submits as GET | same as CLI; `browser_fill` fails on textarea (MB7) — `eval .value= + dispatchEvent(input)` works; skip alert button (MB3); date/range via eval |
| Applitools Demo | https://demo.applitools.com/ | Intentional visual bugs; login accepts any credentials; dashboard shows `$350%7` (corrupted — intentional); timestamps malformed; all action links dead (`href="#"`) | same as CLI — empty credentials login works; intentional bugs present; action links `href="#"` |
| Automation Exercise | https://www.automationexercise.com/ | Ad overlay intercepts nav clicks — use direct URLs; dismiss ad "Close" SVG before interacting; full e-commerce flow works; test cases at `/test_cases` | navigate to `/product_details/N` directly (clicking "View Product" div lands on wrapper, not link); ad is small bottom banner (not blocking); full search → add-to-cart → view cart flow confirmed |
| Automation in Testing | https://automationintesting.online/#/ | Check Availability obscured after date entry — use `eval '#booking button'.click()`; full booking flow works; admin at `/admin` (`admin`/`password`); `#description` textarea not fillable via `vibium fill` — use `eval + dispatchEvent(new Event("input",{bubbles:true}))` | `browser_fill` fails on textarea (MB7); use `browser_type` (not eval) for framework-driven textareas — fires key events that update component state; Submit button obscured — `eval '#contact form button'.click()`; full booking confirmed end-to-end |
| Automation Testing Practice | https://testautomationpractice.blogspot.com/ | `input[type=date]` not fillable — use `eval .value =`; datepicker `readonly` — calendar only; alert buttons deadlock — pre-stub; Colors dropdown has duplicate option values; broken links go to HTTP-only domain (Chrome blocks) | — |
| Automation Test Store | https://automationteststore.com/ | Full flow: search → detail → Add to Cart → Checkout; guest checkout via `accountFrm_accountguest` radio; search by URL params; `vibium select` for product variants | — |
| Automate Now Sandbox | https://automatenow.io/sandbox-automation-testing-practice-website/ | Sub-pages at `practice-automation.com/*`; homepage links obscured by ads — use `eval querySelectorAll("a")[N]?.click()`; Form Fields Submit fires `window.alert()` — pre-stub; `input[type=range]` needs `eval + dispatchEvent`; name input needs `vibium click` before `vibium fill` | — |
| Expand Testing | https://practice.expandtesting.com/ | Homepage links obscured by ads — navigate by direct URL; Login button obscured — `eval 'document.querySelector("button[type=submit]").click()'`; credentials: `practice` / `SuperSecretPassword!`; valid login → `/secure` | — |
| Coffee Cart | https://coffee-cart.app/ | Product cards not in `vibium map` — use `vibium find "[data-test='Espresso']"`; in-memory cart — use UI link, never `vibium go /cart`; checkout modal: name + email required; full flow works | — |
| Commit Quality | https://commitquality.com/ | `input[type=date]` — use `vibium type` not `fill`; date filter rejects today — use past dates; Login credentials not public | — |
| Contact List App | https://thinking-tester-contact-list.herokuapp.com/ | Full CRUD; edit form fill by index via eval; delete triggers `window.confirm` — pre-stub; registration creates persistent account | — |
| Demo SaaS | https://demo-saas.bugbug.io/ | Email verification required — dashboard inaccessible without real email; landing page and validation flows testable | — |
| GreenKart | https://rahulshettyacademy.com/seleniumPractise/#/ | Ticker banner intercepts nav clicks — use `eval location.href=`; search: `vibium press Enter`; ADD TO CART: scroll into view first; drag: `mouse move/down/up` coords; Bugs: "Quantiry" typo, silent promo failure, Rice price inversion | — |
| Global SQA Demo | http://www.globalsqa.com/demo-site/ | Component links redirect to ad — navigate sub-pages directly; widgets in iframes — navigate to iframe URL directly; `vibium drag @ref` fails — use mouse coords | — |
| Hands-On Selenium WebDriver | https://bonigarcia.dev/selenium-webdriver-java/ | 30 sub-pages; `vibium fill` fails on `<textarea>` — use `vibium type`; calculator buttons are `span.btn` — use eval; login page slow — add `sleep 3` after submit | — |
| Lambdatest Playground | https://ecommerce-playground.lambdatest.io/ | Nav obscured by sticky header — use direct URLs; Add to Cart fails for guests; "Size required!" blocks add to cart (no actual options); `window.cart.add(id,qty)` is the AJAX function | — |
| Let Code | https://letcode.in/test | Hub links redirect to ad — use direct URLs; `/alert` page deadlocks on load (native confirm fires immediately) — avoid or use MCP `browser_dialog_accept` | `/alert` page: use `browser_dialog_accept` immediately after navigate to handle auto-firing confirm |
| Locator Game | https://testsmith-io.github.io/locator-game/ | 13 levels; `vibium fill @e3 "selector"` + `vibium click @e5` to answer; CSS and XPath modes | — |
| Practice Test Automation | https://practicetestautomation.com/practice/ | Login: `student`/`Password123`; `sleep 5` before `vibium url` after login (BiDi timing); exceptions page: Row 2 added dynamically after Add click (`sleep 2`) | — |
| QA Playground | https://qaplayground.dev/ | 24 mini-apps; OTP needs `vibium type` not `fill`; shadow DOM, range slider, sortable list all need eval; no `vibium switch` — navigate directly | — |
| React Shopping Cart | https://react-shopping-cart-67954.firebaseapp.com/ | Size filter checkboxes obscured — use `eval .click()`; cart drawer opened by last elem in `vibium map`; no real checkout | — |
| Selectors Hub | https://selectorshub.com/xpath-practice-page/ | Email input `readonly` — `eval .removeAttribute("readonly")`; open shadow DOM on `#userName`, closed on `#userPass`; nested and iframe shadow DOM scenarios | — |
| Selenium Playground | https://www.lambdatest.com/selenium-playground/ | Demo links redirect to testmuai.com — blocked by Cloudflare bot protection; not accessible as of 2026-05-18 | — |
| Swag Labs | https://www.saucedemo.com/ | Credentials: `standard_user`/`secret_sauce`; cart icon not in `vibium map` — use `eval .click()`; sort values: "az"/"za"/"lohi"/"hilo"; problem_user has intentional image/sort bugs | — |
| Sweet Shop | https://sweetshop.netlify.app/ | "Add to Basket" not in `vibium map` — use `eval .click()`; two inputs with same `id="name"` — fill second via `eval querySelectorAll[1]`; delivery radio obscured — use `eval .click()` | — |
| Tricentis Obstacle Course | https://obstaclecourse.tricentis.com/Obstacles | Obstacles randomized; success modal obscured — use `eval btn-success.click()`; drag-and-drop unresponsive to mouse events | — |
| UI Test Automation Playground | http://uitestingplayground.com/ | HTTP-only — Chrome BiDi blocks completely; cannot be tested with vibium | — |
| Weather Shopper | https://weathershopper.pythonanywhere.com/ | Temperature-based product selection; Stripe iframe cross-origin — not fillable via eval; test card: 4242 4242 4242 4242 / 12/26 / 123 | — |
| XYZ Bank | https://www.globalsqa.com/angularJs-protractor/BankingProject/ | `vibium select` doesn't trigger ng-model — use `eval .value= + dispatchEvent(change)`; Add Customer fires `window.alert()` — pre-stub | — |

### API Testing

| Name | URL |
|------|-----|
| JSON Placeholder | https://jsonplaceholder.typicode.com/ |
| Restful Booker | https://restful-booker.herokuapp.com/ |
| ReqRes | https://reqres.in/ |
| httpbin | https://httpbin.org/ |
| Swagger Petstore | https://petstore.swagger.io/ |
| Poké API | https://pokeapi.co/ |
| Rick and Morty API | https://rickandmortyapi.com/graphql |
| Airport Gap | https://airportgap.com/ |
| Automation Exercise API | https://www.automationexercise.com/api_list |

### Performance Testing

| Name | URL |
|------|-----|
| Blaze Demo | http://blazedemo.com/index.php |
| Computer Database | https://computer-database.gatling.io/computers |
| Demoblaze | https://demoblaze.com/ |
| Pet Store Web | https://petstore.octoperf.com/actions/Catalog.action |

---

## Exploratory Test Protocol

When given a site to test, run this structured protocol. Skip steps that are not applicable (e.g. login for sites without auth).

### Step 1 — Reachability

**CLI:**
```sh
vibium go <url>
vibium wait load --timeout 10000
vibium title
vibium screenshot -o step1-load.png
```

**MCP:**
```
browser_navigate {url}
browser_wait_for_load {timeout: 10000}
browser_get_title
browser_screenshot {filename: "step1-load.png"}
```
Record: loaded / timed out / error page.

### Step 2 — Page structure

**CLI:**
```sh
vibium text
vibium map
```

**MCP:**
```
browser_get_text
browser_map
```
Note: main navigation links, prominent headings, form count, interactive element count.
MCP `browser_get_text` throws a schema error on blank pages — if the page has no content, use `browser_evaluate` with `document.body.innerText + ''` instead.

### Step 3 — Navigation smoke test
Click 2–3 main nav links. After each:

**CLI:**
```sh
vibium click @eN
vibium diff map
vibium url
```

**MCP:**
```
browser_click {selector: "@eN"}
browser_map
browser_get_url
```
Record: destination URL, any errors, broken links.

### Step 4 — Core functionality (site-specific)
Adapt based on site type:

**E-commerce** (BookCart, Magento, Swag Labs, etc.)
- Browse product listing
- Open a product detail page
- Add to cart
- View cart, verify item appears

**Form-heavy** (Parabank, PHP Travels, etc.)
- Find the primary form
- Submit empty — check for validation errors
- Fill with valid data — check for success or expected flow

**Bug-hunting sites** (AcademyBugs, ToDo List, QA Practice, etc.)
- Interact with all visible controls
- Try edge cases: empty inputs, special characters, large numbers, rapid clicks
- Note any unexpected behavior, error messages, or visual glitches

**Todo / CRUD apps**
- Create an item
- Edit the item
- Delete the item
- Verify state after each action

**Calculators / tools**
- Test normal input and expected output
- Test boundary values: 0, negative, very large numbers
- Test invalid input types

### Step 5 — Screenshot and report

**CLI:**
```sh
vibium screenshot -o final.png --full-page
```

**MCP:**
```
browser_screenshot {filename: "final.png", fullPage: true}
```

---

## Reporting format

After testing, output a structured report:

```
## Practice Test Report: <Site Name>
URL: <url>
Date: <date>

### Reachability
[PASS/FAIL] Site loaded in ~Xs

### Structure
- Navigation: <items found>
- Forms: <count>
- Interactive elements: <count>

### Navigation
[PASS/FAIL] <link> → <destination> (<observation>)

### Core Functionality
[PASS/FAIL/BUG] <action> — <observation>

### Bugs Found
1. <description> — Steps: <steps> — Severity: Low/Medium/High
2. ...

### Notes
<anything unusual or interesting>
```

---

## Tips

### General (both modes)
- Always re-map after clicking navigation or submitting forms — refs expire on page change
- Sites marked "with bugs" are intentionally broken — report bugs as findings, not failures
- For sites requiring login, check the site's About/Demo page for credentials first
- Dismiss cookie banners and modals early — they obscure elements and block clicks
- Both `vibium select` (CLI) and `browser_select` (MCP) match by option `value` attribute, not display text; inspect option values first if unsure
- Elements styled with CSS `text-transform: uppercase` cannot be found by text — search for the actual DOM text (e.g. "Books" not "BOOKS")
- Canvas-rendered and custom-painted UIs won't appear in map — use `getBoundingClientRect()` eval to locate elements, then coordinate click
- Azure/Heroku-hosted demo sites may hibernate — if products or data don't load, wait 5s and reload once before reporting a bug
- For React SPAs, always test routes via in-app navigation first; direct URL navigation may fail if the server doesn't handle client-side routes

### CLI-specific
- Use `vibium find text` / `find role` instead of hardcoded refs for reliability
- iframes require `vibium frames` then `vibium frame "<name>"` before interacting inside them
- Pre-stub native dialogs before clicking: `vibium eval 'window.alert=function(){}'` — clicking first deadlocks the daemon
- Daemon broken pipe after idle or BiDi error: `vibium stop && sleep 2 && vibium start && sleep 2`
- Multi-statement evals with semicolons fail in shell quoting — split into separate `vibium eval` calls

### MCP-specific
- Use `browser_dialog_accept` / `browser_dialog_dismiss` for native dialogs — no deadlock risk
- `browser_find` with `role="link"` times out on `<button>` elements — use `browser_map` refs or CSS selectors instead
- `browser_get_text` throws `invalid_union` when page/element text is empty — vibium bug MB9; affects full-page form, selector on empty element, `about:blank`, whitespace-only body, and pages where all content is `display:none`; workaround: `browser_evaluate { expression: "document.body.innerText || null" }` (use `|| null`, NOT `|| ''` — empty string triggers MB6)
- `browser_evaluate` throws `invalid_union` when expression returns `""` — vibium bug MB6; ensure expressions never return empty string (use `|| null` fallback)
- MCP `browser_map` finds more elements on some pages than CLI `vibium map` (e.g. puzzle index links, Angular Material list items)
- Stop/restart MCP browser session with `browser_stop` + `browser_start` when BiDi errors occur — this does NOT affect the CLI daemon
