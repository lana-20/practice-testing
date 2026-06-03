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
- Daemon can deadlock on native dialogs — pre-stub with `eval 'window.alert=function(){}'` (B3 still open)
- `vibium select` matches by visible label OR value attribute (B5 fixed v26.5.31); errors on non-existent option

**MCP mode**: Uses `mcp__vibium__browser_*` tool calls directly.
- Dialog handling via `browser_dialog_accept` / `browser_dialog_dismiss`
- **MB3 still open**: direct `browser_click` on a native `alert()` trigger deadlocks — use `browser_evaluate { setTimeout(..., 300) }` + `browser_sleep {ms: 350}` + `browser_dialog_accept {}` pattern (#151 deferred)
- `browser_select` matches by visible label OR value attribute (shared engine fix v26.5.31); errors on non-existent option
- `browser_find` with `role=link` times out on `<button>` elements — use `browser_map` refs or CSS selectors
- MCP runs a separate browser session from the CLI daemon; stop/start MCP browser via `browser_stop` + `browser_start`

## Site Directory

### General Practice

| Name | URL | CLI Notes | MCP Notes |
|------|-----|-----------|-----------|
| A11y Coffee | https://a11y.coffee/ | Static accessibility learning resource; 13 nav links; dark/light toggle; no mandatory waits | same as CLI |
| AcademyBugs | https://academybugs.com/ | 25 bugs planted; dismiss tutorial modal + cookie banner; sort dropdown non-functional (intentional app bug) — select by visible label ("Relevance", "Highest Price", etc.) or numeric value ("0"–"4"); view filter (10/25/50) broken; cart total bug: $152.99 for $45 item + $7.99 shipping (expected $52.99); Russian text bug at /account/ | sort IS functional in MCP; `browser_select` by label or value works; map refs for dismiss; same bugs |
| Basic Calculator | https://testsheepnz.github.io/BasicCalculator.html | Prototype + builds 1–9; select operation by visible label ("Add", "Subtract", etc.) or value ("0"–"4") | same as CLI |
| Black Box Puzzles | https://blackboxpuzzles.workroomprds.com/ | Only 22, 24, 26b, 29, 31, 33, 34 work (Flash); `vibium map` returns nothing on index; coordinate clicks inside puzzle custom elements | `browser_map` finds all puzzle nav links; coordinate clicks still required inside custom elements |
| BookCart | https://bookcart.azurewebsites.net/ | Azure-hosted; backend frequently hibernated; Angular Material inputs fill by `#mat-input-N` | `browser_find {role:"link", text:"Login"}` times out — Login is a button, use map ref; same hibernated backend |
| Candy Mapper | https://www.candymapper.net/ | UK testing sandbox; county selector, contact form, social links, reCAPTCHA challenge; 54 interactive elements; pre-stub alert before submitting forms (B3 still open) | `browser_fill` works on all form fields; `browser_select` for county picker; Submit → pre-stub `window.alert` then click (MB3 still open) |
| Cnarios | https://www.cnarios.com/ | Challenges work; /concepts/* pages render blank (React routing bug) | `browser_get_text` returns `""` on blank pages (MB9 fixed v26.5.31) |
| Evil Tester | https://testpages.eviltester.com/styled/index.html | Stub alert/confirm/prompt via `eval` BEFORE clicking alert buttons (B3 still open) | `browser_click` on alert button deadlocks (MB3 still open); use `browser_evaluate {setTimeout(...,300)}` + `browser_sleep {ms:350}` + `browser_dialog_accept {}` |
| Gefälscht CompuTech | https://webtestingcourse.dequecloud.com/ | Intentionally inaccessible; contact form fields need `input[name=x]` selectors; contact URL is `/contact.php` (not `/contact/` — 404) | `browser_map` refs work for form fields without name selectors; same `/contact.php` URL |
| Parabank | https://parabank.parasoft.com/parabank/admin.htm | Run DB Initialize first; after init any username/password logs in (intentional); use for form/validation testing only | same as CLI |
| Parking Cost Calculator | https://www.shino.de/parkcalc/ | Lot dropdown: select by visible label ("Valet Parking", "Short-Term Parking") or value ("Valet", "Short") — both work (B5 fixed v26.5.31); input names PascalCase (`StartingDate`, `LeavingTime`); invalid dates → inline error (not blank page); Valet: $12 ≤5h / $18/day >5h (boundary inclusive at exactly 5h); Economy: $9/day max | same as CLI — both label and value work |
| PHP Travels | http://phptravels.com/demo/ | Landing page only — credentials sent by email; Login nav broken; Submit fires window.alert() — crashes CLI daemon even with pre-stub; math captcha: read `#numb1 + #numb2`, fill sum into `#number` (`@e21`) before submit; **skip submit — map/fill only** | Submit crashes MCP session (websocket 1006) regardless of browser_click vs browser_evaluate vs pre-stub; MB3 setTimeout pattern also blocked; **skip submit — map/fill only** |
| Polymer Shop | https://shop.polymer-project.org/ | All UI in Web Components shadow DOM — `vibium map` returns nothing; traverse via `eval shadowRoot`; coordinate clicks for buttons; cart server-side | Same shadow DOM constraints; `shadowRoot.querySelector('button').click()` does NOT fire Polymer events — must use `browser_mouse_click` at computed bounding-box coordinates |
| Potion Shop | https://qe-at-cgi-fi.github.io/potion-shop/ | Medieval order form; 32 controls (radio buttons for potion type/size/potency, ingredient checkboxes, delivery options, textarea); `vibium fill` works including textarea (B7 fixed v26.5.31); Submit validates required fields | `browser_fill` works on all inputs including textarea; `browser_click` on Submit (@e29) works; radio buttons and checkboxes are obscured to `browser_click` — use `getBoundingClientRect` + `browser_mouse_click` at computed coords |
| Practice Software Testing | https://practicesoftwaretesting.com/ | Angular app; add to cart works without login; credentials: `customer@practicesoftwaretesting.com` / `welcome01`; Login form at `/auth/login` uses `input[data-test=email]` and `input[data-test=password]` — may need extra wait after Angular routing; Login submit is `input[type=submit]` | `browser_map` finds all 71 elements cleanly; `browser_click` on `input[type=submit]` works directly; `input[data-test=email]` and `input[data-test=password]` selectors work; add to cart via `button[data-test=add-to-cart]` on product detail page |
| Presta Shop | https://demo.prestashop.com/ | Store in iframe — get inner URL via `eval 'document.querySelector("#framelive")?.src'` after 5s wait; subdomains expire ~2 min; `vibium go` to subdomain pages deadlocks (B3) — use `eval 'location.href="..."'`; add-to-cart AJAX fails silently (cart stays 0) | `browser_navigate` to subdomain pages works without deadlock; same AJAX failure; same subdomain expiry; `browser_map` finds 106 elements |
| QA Practice | https://qa-practice.razvanvancea.ro/ | Login at homepage `#auth-shop` anchor (not `/ecommerce/` — 404); Login: `admin@admin.com` / `admin123`; ADD TO CART uppercase — use map refs (`button[type=button]` ADD TO CART refs); pre-stub alert/confirm before clicking alert buttons (B3 still open); checkout: Shipping Details form (phone, street, city, country) | Login at homepage then click `@e2` Ecommerce link (anchor `#auth-shop`); MB3 deadlock on direct Alert button click — use `browser_evaluate {setTimeout(...,300)}` + `browser_sleep {ms:350}` + `browser_dialog_accept {}`; ADD TO CART buttons appear after login as `button[type=button]` map refs; full e-commerce flow works |
| QA Training Simulator | https://bugeater.web.app/ | **BugEater 2.0** (as of 04.2026): challenges renumbered (#1.1–#7.6); `vibium fill` works on React inputs; cookie banner on homepage (`@e50` Accept all); navigate directly to `/app/list` — second cookie banner there (`@e34` Accept) must be dismissed before challenge links are clickable (obscured otherwise) | `browser_click @e50` on homepage cookie banner; navigate to `/app/list`; `browser_click @e34` Accept to dismiss second banner; then challenge links (`@e3`–`@e25`) become clickable; `browser_fill` works on React inputs |
| Random User Generator | https://randomuser.me/ | API testing site; API at `/api/`; `?results=0/abc/-1/5001` all silently return 1 result; `?format=csv` triggers download — crashes BiDi session; `vibium text` crashes on `?results=5000` — use `vibium eval 'JSON.parse(document.body.innerText)'`; `?inc=name,email` and `?seed=abc` work | `browser_get_text` on `?results=5000` → oversized output error (not crash, but unusable); use `browser_evaluate {JSON.parse(document.body.innerText)}` instead; skip `?format=csv` (download may crash session) |
| Real World Example Apps | https://codebase.show/projects/realworld | Requires GitHub OAuth; SvelteKit SPA needs ~3s after `wait load`; tabs: Frontend @e7, Backend @e8, Fullstack @e9, All @e10; language filters follow after (e.g. TypeScript @e11); sleep 3s after tab click too before re-mapping | Same tab/filter refs; `browser_sleep {ms:3000}` after tab click before next `browser_map`; 100 refs on full list; Sign in → GitHub OAuth |
| The Boozang Test Lab | https://thelab.boozang.com/ | React SPA; `vibium fill` works for inputs; Form Fill saves to shared DB — use unique test data; navigate to challenge pages via direct URL | Homepage `browser_map` returns only 10 elements — challenge section not visible; use direct URLs (e.g. `/formFill`, `/sortedList`); `browser_fill` and `browser_click` work cleanly |
| The iframe Search Engine | https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html | Use `vibium fill` (not type) for search input; select option label is "bing.com" (not "Bing") — use exact visible label; "Search" button loads iframe; "Go search" link opens new tab; Bing embeds; Google/DuckDuckGo block iframe | `browser_fill` works; `browser_select` by value "bing.com" works; "Go search" click opens new tab — verify via `browser_list_pages` (2 pages); non-existent option now errors |
| The Internet | http://the-internet.herokuapp.com/ | 44 examples; `vibium hover` fails on non-interactive elements — use `vibium mouse move x y`; `vibium frame` doesn't persist between CLI calls — use `eval contentDocument.body`; `vibium fill` fails on `input[type=range]` — use `eval .value + dispatchEvent`; `vibium check` fails on obscured checkboxes — use `vibium mouse click x y`; `vibium drag`/`upload`/`press` work; shadow_dom page 404 | `browser_map` returns all 44 links; `browser_drag` works; `browser_upload` works; `browser_press` works; `browser_fill` fails on range — use eval; `browser_check` fails obscured — use `browser_mouse_click` at coords; hover via `browser_mouse_move` to computed coords + `getComputedStyle()`; MB3 on direct alert click — use setTimeout+sleep+dialog_accept |
| The Random Number Service | https://www.random.org/ | Cookie banner on load — dismiss "Allow All"; generator forms not in `vibium map` — use URL params or `eval form.submit()`; inline `eval` with semicolons fails (shell quoting) — use direct URL params; validation: min>max/num>10000 → error; negative accepted; `?format=plain` returns raw text | same as CLI — cookie banner via `browser_click "Allow All"`; `browser_map` finds all nav links (81 refs); URL params work for all generator types; skip `?format=csv` (download may crash session) |
| testers.ai | https://testers.ai/testing/ | 59 refs total; @e1 is logo link — category cards start at @e2; each category has two links: the card (@e2, @e4, ...) and a "Checklist" link (@e3, @e5, ...); click Checklist link for the sub-page; sub-pages have checkbox inputs (12 for WCAG A) | same as CLI; `browser_map` returns all 59 refs; sub-page `browser_map` shows checkboxes; category card click goes to same sub-page as Checklist link |
| Test Track | https://testtrack.org/ | Structured training site; 19 refs on homepage; modules: Button Demo @e2, Text Input @e3, Login @e4, Dropdown @e5, Checkboxes @e6, Table @e7, Modal @e8, Alert @e9, File Upload @e10, Drag&Drop @e11, Frames @e12, Dynamic @e13, Canvas @e14, Multi-Window @e15, Adv.Buttons @e16, Vehicle Simulator @e17, 3D Chess @e18; after navigating back, re-map before clicking — refs reset | `browser_map` returns 19 refs; module links work via `browser_click`; after navigating back with `browser_navigate`, re-map before clicking next module; alert module — use setTimeout+sleep+dialog_accept (MB3 still open) |
| ToDo List | https://todolist.james.am/#/ | AngularJS app; 1 map ref (input only); checkbox (`.toggle`) obscured — get coords via `getBoundingClientRect` then `vibium mouse click x y` (confirmed coords ~325,206); `vibium dblclick` enters edit mode; BUG: counter shows "0" after adding 1 item (off by 1); BUG: `.destroy` button title "TODO:REMOVE THIS EVENTUALLY"; no localStorage persistence | same bugs confirmed; `browser_mouse_click {x:325, y:206}` for checkbox; delete title via `document.querySelector('.destroy').title`; `browser_press {key:"Enter"}` to submit new item |
| UI5 Demo Kit | https://ui5.sap.com/#/demoapps | SAP UI5 SPA; `vibium map` now returns **137 refs** (previous "returns nothing" is outdated); Shopping Cart card @e17, Open App @e19; `vibium find text "Shopping Cart"` also works; demo app "Open App" links open in **new tab** — eval click doesn't navigate current page | `browser_map` returns **128 refs** (cookie banner dismissed adds 9 more); Shopping Cart "Open App" (@e19) opens new tab; after tab opens, `browser_map` stays on Demo Kit — use `browser_switch_page` then `browser_close_page {index:0}` workaround; **after UI5 session ends, use `browser_new_page + close_page[0]` for next site** to avoid BiDi dead-frame |

### Automation Testing

| Name | URL | CLI Notes | MCP Notes |
|------|-----|-----------|-----------|
| Automation Bookstore | https://automationbookstore.dev/ | Filter-only SPA; all 8 book links `href="#"` (no detail page); case-insensitive real-time filter works; no "no results" message on empty filter | same as CLI; filter hides via CSS class not `style.display` — DOM style checks mislead; use screenshot to verify filter state |
| Automation Camp | https://play2.automationcamp.ir/ | Alert button + invalid login deadlock daemon — `eval` override does not prevent it; valid login: `test`/`test`; `input[type=date]` — use `eval .value =`; form submits as GET | same as CLI for daemon deadlock (B3 still open); `browser_fill` works on textarea (MB7 fixed v26.5.31); skip alert button (MB3 still open); date/range via eval |
| Applitools Demo | https://demo.applitools.com/ | Intentional visual bugs; login accepts any credentials; dashboard shows `$350%7` (corrupted — intentional); timestamps malformed; all action links dead (`href="#"`) | same as CLI — empty credentials login works; intentional bugs present; action links `href="#"` |
| Automation Exercise | https://www.automationexercise.com/ | Ad overlay intercepts nav clicks — use direct URLs; dismiss ad "Close" SVG before interacting; full e-commerce flow works; test cases at `/test_cases` | navigate to `/product_details/N` directly (clicking "View Product" div lands on wrapper, not link); ad is small bottom banner (not blocking); full search → add-to-cart → view cart flow confirmed |
| Automation in Testing | https://automationintesting.online/#/ | Check Availability obscured after date entry — use `eval '#booking button'.click()`; full booking flow works; admin at `/admin` (`admin`/`password`); `#description` is a framework-driven textarea — `vibium fill` may not trigger component state; use `eval + dispatchEvent(new Event("input",{bubbles:true}))` | `browser_fill` works on plain textarea (MB7 fixed v26.5.31); for framework-driven textareas use `browser_type` — fires key events that update component state; Submit button obscured — `eval '#contact form button'.click()`; full booking confirmed end-to-end |
| Automation Testing Practice | https://testautomationpractice.blogspot.com/ | `input[type=date]` not fillable — use `eval .value =`; datepicker `readonly` — calendar only; alert buttons deadlock — pre-stub (B3 still open); Colors dropdown has duplicate option values; broken links go to HTTP-only domain (Chrome blocks) | `browser_fill` works on textarea (MB7 fixed v26.5.31); alerts via setTimeout+sleep+dialog_accept (MB3 still open); date via eval; `browser_dblclick` on `button[ondblclick]` for copy-text; Colors duplicates confirmed |
| Automation Test Store | https://automationteststore.com/ | Full flow: search → detail → Add to Cart → Checkout; guest checkout via `accountFrm_accountguest` radio; search by URL params; `vibium select` for product variants by label or value (B5 fixed v26.5.31) | navigate product detail via `?rt=product/product&product_id=N`; cart checkout link zero-size — use eval click; guest checkout entry via `?rt=account/login`; `browser_select` by label or value |
| Automate Now Sandbox | https://automatenow.io/sandbox-automation-testing-practice-website/ | Sub-pages at `practice-automation.com/*`; homepage links obscured by ads — use `eval querySelectorAll("a")[N]?.click()`; Form Fields Submit fires `window.alert()` — pre-stub (B3 still open); `input[type=range]` needs `eval + dispatchEvent`; name input needs `vibium click` before `vibium fill` | `#name-input` obscured — `eval '#name-input'.click()` before `browser_fill`; `browser_fill` works on textarea (MB7 fixed v26.5.31); submit: pre-stub `window.alert = () => {}` (MB3 still open) |
| DemoQA | https://demoqa.com/ | 7 section cards (Elements, Forms, Alerts/Frames/Windows, Widgets, Interactions, Book Store); each section expands to many sub-pages; map works cleanly | `browser_map` returns 7 refs on homepage; sub-pages accessible via direct URL; `browser_fill` works on all form inputs; Book Store requires login for wishlist |
| Expand Testing | https://practice.expandtesting.com/ | Homepage links obscured by ads — navigate by direct URL; Login button obscured — `eval 'document.querySelector("button[type=submit]").click()'`; credentials: `practice` / `SuperSecretPassword!`; valid login → `/secure` | `browser_click` on submit works on first load; obscured after ad re-renders — use `eval '#submit-login'.click()` for reliability; navigate to `/logout` to clear session |
| ATM Practice App | https://qe-at-cgi-fi.github.io/atm/ | 4 elements: DEBUG @e1, ADMIN @e2, amount input @e3, WITHDRAW @e4; ADMIN panel opens inline (map expands to 14 refs — balance config inputs + APPLY + clock controls + amount input @e14 + WITHDRAW @e15); use @e14/@e15 after ADMIN opens | `browser_map` returns 4 refs; ADMIN click expands to 14 refs; `browser_fill @e14` + `browser_click @e15` for withdraw after ADMIN open |
| Coffee Cart | https://coffee-cart.app/ | Product cards not in `vibium map` — use `vibium find "[data-test='Espresso']"`; in-memory cart — use UI link, never `vibium go /cart`; checkout modal: name + email required; full flow works | same — product cards via `[data-test="ProductName"]`; checkout button via `eval '[data-test="checkout"]'.click()`; full purchase flow confirmed |
| Commit Quality | https://commitquality.com/ | `input[type=date]` — use `vibium type` not `fill`; date filter rejects today — use past dates; Login credentials not public | `browser_type` for date input (MMDDYYYY format); `browser_fill` for text; practice sub-pages work via direct URL; date filter: use past date (e.g. 2024-01-01) |
| Contact List App | https://thinking-tester-contact-list.herokuapp.com/ | Full CRUD; edit form fill by index via eval; delete triggers `window.confirm` — pre-stub (B3 still open); registration creates persistent account | full CRUD confirmed; delete: `window.confirm` pre-stub before delete click (MB3 still open); `browser_fill` works on all fields; unique email per test run to avoid duplicate account error |
| Demo SaaS | https://demo-saas.bugbug.io/ | Email verification required — dashboard inaccessible without real email; landing page and validation flows testable | landing page + validation (empty submit, invalid email) testable; dashboard requires real email verification — skip; Mantine UI IDs are dynamic — use `input[name=x]` selectors |
| GitHub Users Search | https://gh-users-search.netlify.app/ | React GitHub user search SPA; search input + submit; default user (ThaELL1) pre-loaded with 30 followers; `vibium fill` + `vibium press Enter` to search | `browser_fill` + `browser_click` on submit works; 34 MCP refs (search + 32 follower links); search any GitHub username |
| GreenKart | https://rahulshettyacademy.com/seleniumPractise/#/ | Ticker banner intercepts nav clicks — use `eval location.href=`; search: `vibium press Enter`; ADD TO CART: scroll into view first; drag: `mouse move/down/up` coords; Bugs: "Quantiry" typo, silent promo failure, Rice price inversion | use full URL for cart navigation (`browser_navigate` to `https://rahulshettyacademy.com/seleniumPractise/#/cart` — `eval location.href='/#/cart'` navigates to wrong domain); promo code `FRESH` functional; Bugs confirmed: "Quantiry" column header typo + "No. of Items: 0" despite cart having items |
| Global SQA Demo | http://www.globalsqa.com/demo-site/ | Component links redirect to ad — navigate sub-pages directly; widgets in iframes — navigate to iframe URL directly; `vibium drag @ref` fails — use mouse coords | nav links intercepted by ads — navigate sub-pages directly by URL; drag-and-drop: navigate directly to iframe src URL (e.g. `globalsqa.com/demoSite/practice/droppable/photo-manager.html`); `browser_drag` works when content is top-level |
| Hands-On Selenium WebDriver | https://bonigarcia.dev/selenium-webdriver-java/ | 30 sub-pages; `vibium fill` works on `<textarea>` (B7 fixed v26.5.31); calculator buttons are `span.btn` — use eval; login page slow — add `sleep 3` after submit | `browser_fill` works on textarea (MB7 fixed v26.5.31); dialogs via setTimeout+sleep+dialog_accept (MB3 still open); drag-and-drop `browser_drag` fires but jQuery UI droppable ignores it; slow calculator: eval `.find(b=>b.textContent.trim()==='N').click()`; login typo: site URL is `login-sucess.html` |
| Lambdatest Playground | https://ecommerce-playground.lambdatest.io/ | Nav obscured by sticky header — use direct URLs; Add to Cart fails for guests; "Size required!" blocks add to cart (no actual options); `window.cart.add(id,qty)` is the AJAX function | `browser_map` works (309 refs); nav links not obscured in MCP; use `eval cart.add('product_id')` to add items (bypasses size requirement); checkout redirects to cart for guests; inspect options with eval before `browser_select` |
| Let Code | https://letcode.in/test | Hub links redirect to ad — use direct URLs; `/alert` page deadlocks on load (native confirm fires immediately) — avoid or use MCP `browser_dialog_accept` | `/alert` page did NOT auto-fire confirm in MCP (no deadlock); dialogs via setTimeout+sleep+dialog_accept (MB3 still open); `browser_fill ""` throws "value is required" — use eval to clear; `browser_select` by visible label or numeric value (0/1/2); Angular buttons: use direct `setTimeout(() => alert(...))` not eval button.click |
| Locator Game | https://testsmith-io.github.io/locator-game/ | 13 levels; `vibium fill @e3 "selector"` + `vibium click @e5` to answer; CSS and XPath modes | `browser_fill` for selector input; Submit always obscured — `eval querySelector('button[type="submit"]').click()`; 3 levels solved: h3, #description, li.active ✓ |
| NearForm Testing Playground | https://nearform.github.io/testing-playground/ | 18 challenge cards; language switcher (English default); difficulty filter; search; challenges: Add/Remove, Checkbox, Drag & Drop, Dynamic Table, File Download/Upload, Login Form, Notifications, Radio Buttons, Sliders, Tooltips, Various Inputs | `browser_map` returns 18 challenge refs; language switcher + difficulty filter work via `browser_click`; `browser_fill` on search works; each challenge at direct URL |
| OrangeHRM | https://opensource-demo.orangehrmlive.com/ | HR management SPA; `vibium map` returns nothing — React renders after JS init; use `input[name=username]` + `input[name=password]`; login: Admin / admin123; after login `vibium map` shows full sidebar | `browser_map` returns nothing on load (same as CLI); use `browser_fill "input[name='username']"` + `browser_fill "input[name='password']"` + eval submit; after login map works |
| Practice Test Automation | https://practicetestautomation.com/practice/ | Login: `student`/`Password123`; `sleep 5` before `vibium url` after login (BiDi timing); exceptions page: Row 2 added dynamically after Add click (`sleep 2`) | `browser_fill` + `browser_click` on `#submit` works; `browser_sleep {ms:2000}` sufficient after login; Save button zero-size — `eval querySelector('#save_btn').click()`; BUG: Save confirmation says "Row 1 was saved" for all rows |
| Practice Automation | https://practice-automation.com/ | 28 nav links to sub-pages: delays, sliders, tables, iframes, forms, calendars, gestures, spinners, modals, hover, file up/download; Form Fields Submit → window.alert — pre-stub (B3 still open); `vibium fill` works on textarea (B7 fixed v26.5.31) | `browser_fill` works on text inputs and textarea (MB7 fixed v26.5.31); pre-stub `window.alert` before Submit (MB3 still open); `browser_map` returns 28 refs cleanly |
| QA Cloud | https://www.qacloud.dev/ | Multi-app QA platform; 38 elements (full nav + app cards); browse apps, API docs, and practice labs; Login/Register for account features | `browser_map` returns 38 refs; search bar functional; Login/Register modal via `browser_click`; app cards accessible without login |
| QE Buggy Todo | https://qe-at-cgi-fi.github.io/todo | Single-input todo app with intentional bugs; typo in placeholder "What need's to be done?"; `vibium fill` + `vibium press Enter` to add items; other bugs findable by interacting | `browser_fill` + `browser_press {key:"Enter"}` to add todo; 1 map ref only; placeholder typo confirmed; find additional bugs by adding/checking/deleting items |
| QA Playground | https://qaplayground.dev/ | 24 mini-apps; OTP needs `vibium type` not `fill`; shadow DOM, range slider, sortable list all need eval; no `vibium switch` — navigate directly | use `/apps/<name>/` URLs (not `/apps/<shortname>/`); OTP: eval pre-sets all values + `browser_type` on first input triggers verification; shadow DOM via `shadowRoot.querySelector`; `browser_drag` works on sortable list; range slider: eval + dispatchEvent(input/change) |
| React Shopping Cart | https://react-shopping-cart-67954.firebaseapp.com/ | Size filter checkboxes obscured — use `eval .click()`; cart drawer opened by last elem in `vibium map`; no real checkout | `browser_map` works (42 refs); `browser_click` on Add to Cart works; cart drawer opens automatically; checkboxes always obscured — `eval input.click()` only; `browser_check` always fails here |
| Selectors Hub | https://selectorshub.com/xpath-practice-page/ | Email input `readonly` — `eval .removeAttribute("readonly")`; open shadow DOM on `#userName`, closed on `#userPass`; nested and iframe shadow DOM scenarios | `browser_map` works (125 refs); `browser_fill` correctly rejects readonly with clear error; `eval .removeAttribute('readonly')` + `browser_fill` works; open shadow (`#userName`): eval accessible; closed shadow (`#userPass`): inaccessible; alert buttons — skip (hang risk) |
| SeleniumBase | https://seleniumbase.io/ | Docs site; 52+ demo pages listed (Coffee Cart, Drag & Drop, Calculator, Shadow DOM, CAPTCHA pages); links to W3Schools mirrors; live demo pages directly accessible via sub-URLs | `browser_map` returns 256 refs (full doc nav + demo links); all demo pages accessible via direct URL; CAPTCHA pages (Turnstile, reCAPTCHA) for bypass testing |
| Selenium Playground | https://www.lambdatest.com/selenium-playground/ | Demo links redirect to testmuai.com — blocked by Cloudflare bot protection; not accessible as of 2026-05-18 | NOW ACCESSIBLE — rebranded to TestMu AI at `testmuai.com`; `browser_map` works (156 refs); sub-pages work at `testmuai.com/selenium-playground/<demo>/`; `browser_fill` works on inputs; button result output blank (Simple Form Demo) — JS timing issue |
| Swag Labs | https://www.saucedemo.com/ | Credentials: `standard_user`/`secret_sauce`; cart icon not in `vibium map` — use `eval .click()`; sort by label ("Name (A to Z)") or value ("az"/"za"/"lohi"/"hilo"); problem_user has intentional image/sort bugs | full checkout confirmed: login → add to cart → `eval .shopping_cart_link.click()` → fill checkout form → finish → "Thank you for your order!" ✓; `browser_select` sort by label or value; `browser_click` on Add to Cart works directly |
| TestDino | https://storedemo.testdino.com/ | E-commerce SPA; `vibium map` returns nothing (React/Vue); 216 MCP elements (products repeat across carousels); full product listing, FAQ accordion, email subscribe | `browser_map` returns 216 refs (products duplicated across carousels — use first occurrence); `browser_fill` for email subscribe; `browser_click` on Add to Cart buttons works |
| Sweet Shop | https://sweetshop.netlify.app/ | "Add to Basket" not in `vibium map` — use `eval .click()`; two inputs with same `id="name"` — fill second via `eval querySelectorAll[1]`; delivery radio obscured — use `eval .click()` | "Add to Basket" links confirmed not in map — `eval Array.from(querySelectorAll('a')).find(a=>a.textContent.includes('Add to Basket')).click()`; delivery radios obscured — eval click; `browser_fill "#name"` fills first only; second via `eval querySelectorAll('#name')[1].value=...` |
| Tricentis Obstacle Course | https://obstaclecourse.tricentis.com/Obstacles | Obstacles randomized; success modal obscured — use `eval btn-success.click()`; drag-and-drop unresponsive to mouse events | success modal buttons directly clickable via `browser_find`+`browser_click` (CLI "obscured" note outdated); Red Stripe obstacle: eval getBoundingClientRect → `browser_scroll_into_view` → re-read rect → `browser_mouse_click {x,y}` → "Good job!" ✓ |
| Travel Agileway | http://travel.agileway.net/login | HTTP-only Ruby on Rails app; CLI BiDi error on navigate; login form with username, password, remember_me checkbox; credentials: `agileway`/`travel` (unverified) | `browser_navigate` silently loads the HTTP page (no BiDi error in MCP); 6-element map; `browser_fill` + eval submit |
| Weather Shopper | https://weathershopper.pythonanywhere.com/ | Temperature-based product selection; Stripe iframe cross-origin — not fillable via eval; test card: 4242 4242 4242 4242 / 12/26 / 123 | `browser_map` works; Add buttons clickable; `browser_frames` lists Stripe iframe; `browser_frame` returns metadata only — does NOT switch context; Stripe fields inaccessible |
| var.parts | https://var.parts/ | Vibium-branded robot parts shop; 41 elements (nav + 12 products with Add to Cart buttons); cart flow; used as MCP test reference site alongside testtrack.org | `browser_map` returns 41 refs cleanly; `browser_click` Add to Cart works; cart state tracked in session |
| XYZ Bank | https://www.globalsqa.com/angularJs-protractor/BankingProject/ | `vibium select` doesn't trigger ng-model — use `eval .value= + dispatchEvent(change)`; Add Customer fires `window.alert()` — pre-stub (B3 still open) | `browser_select` fails on Angular select (ng-model not updated) — `eval .value='2'+dispatchEvent(change)`; `browser_fill` works on number/text inputs; deposit+withdrawal confirmed; pre-stub `window.alert=()=>{}` before Add Customer submit (MB3 still open) |

### API Testing

| Name | URL | CLI Notes | MCP Notes |
|------|-----|-----------|-----------|
| JSON Placeholder | https://jsonplaceholder.typicode.com/ | Full CRUD via `$V eval 'fetch(...)'`; GET/POST/DELETE all work; writes return realistic responses but don't persist | Identical via `browser_evaluate`; `Promise.all()` allows parallel requests |
| Restful Booker | https://restful-booker.herokuapp.com/ | GET list/by-ID, POST auth (admin/password123), POST create booking all work; Heroku may cold-start | Identical via `browser_evaluate`; auth token pattern works |
| httpbin | https://httpbin.org/ | Full request inspection API; GET/POST/status codes/delay/IP all work; no auth | Identical via `browser_evaluate`; CORS-friendly |
| Swagger Petstore | https://petstore.swagger.io/ | GET findByStatus, POST pet, GET inventory all work; shared mutable state — counts vary | Identical results; slight count variance vs CLI due to concurrent external writes |
| Poké API | https://pokeapi.co/ | Read-only; GET pokemon by name/ID, list with pagination, type endpoint all work; no auth; aggressive caching | Identical; 1350 Pokémon in DB |
| Rick and Morty API | https://rickandmortyapi.com/graphql | Both GraphQL POST `/graphql` and REST `/api/character/N` work; 826 characters; no auth | Identical; browser navigates to GraphQL Playground UI but fetch still works against same endpoint |
| Airport Gap | https://airportgap.com/ | GET list (paginated), GET by IATA code, POST distance calculation all work; JSON:API format (`data.attributes.*`) | Identical; distance endpoint (KIX→SFO: 8692 km) confirmed |
| Automation Exercise API | https://www.automationexercise.com/api_list | GET products/brands, POST searchProduct (form-encoded), POST verifyLogin — all work; uses custom `responseCode` in body not HTTP status | Identical; POST endpoints use `application/x-www-form-urlencoded` not JSON |
| AP+ Developers | https://developer.bpaygroup.com.au/ | Australian payment network developer portal (BPAY, eftpos, NPP, ConnectID); registration required for API keys; 17 nav elements | same as CLI; `browser_map` returns 17 refs |
| Chuck Norris API | https://api.chucknorris.io/ | Random joke API; GET /jokes/random, GET /jokes/categories, GET /jokes/search?query=; no auth for GET; email subscription form present | `browser_evaluate` for fetch calls; 20 map refs; `browser_fill` on email field |
| Countries GraphQL | https://countries.trevorblades.com/ | Live GraphiQL interface; query countries/continents/languages; no auth; execute queries directly in textarea; schema explorer available | `browser_fill` on textarea for query; `browser_click` Execute button; `browser_evaluate` for programmatic fetch to `https://countries.trevorblades.com/graphql` |
| FakeRestAPI | https://fakerestapi.azurewebsites.net/ | Azure-hosted Swagger UI; Activities, Authors, Books, CoverPhotos, Users endpoints; Azure cold start may slow first request | Identical via `browser_evaluate`; Swagger UI 7 collapse buttons for endpoint groups |
| Go REST | https://gorest.co.in/ | Free REST API; public read endpoints require no auth; token auth for write ops; live code examples (CURL/JS/Python/Ruby/Go) with Run button | `browser_click` on Run button executes live request; `browser_evaluate` for custom fetch; token from account sign-in |
| ServeRest | https://serverest.dev/ | Brazilian Swagger API; users/products/shopping carts CRUD; Portuguese by default — language buttons at bottom; no auth for GET endpoints | `browser_click` on language button (PT/ES/EN); `browser_click` on endpoint expand buttons; `browser_evaluate` for direct fetch; 113 map refs |
| SpaceTraders | https://spacetraders.io/ | Space game REST API; register agent via POST /v2/register (callsign + faction); token returned on registration; 58-link docs site | `browser_click` Send Request button on homepage demo; `browser_evaluate` for custom requests; MCP was FASTER than CLI on this site (cold-start effect) |
| The Cat API | https://thecatapi.com/ | Cat image API; live Voting/Breeds/Favorites demo on homepage; free API key for write ops; 29 map refs | `browser_click` on Voting/Breeds/Favs tabs; `browser_evaluate` for programmatic API calls with key; `browser_click` upvote/downvote works |

### Performance Testing

| Name | URL | CLI Notes | MCP Notes |
|------|-----|-----------|-----------|
| Blaze Demo | http://blazedemo.com/index.php | Full booking flow works: 7 departure/destination options, reserve page (5 flights), purchase form (9 fields); submit via `eval select.value + button.click()` | Identical via `browser_evaluate`; same eval pattern |
| Demoblaze | https://demoblaze.com/ | Categories via `#itemc` (3s async load); product detail at `/prod.html?idp_=N` (use quotes to avoid zsh glob); **add-to-cart deadlocks daemon** — pre-stub `window.alert` before clicking (B3 still open); Demoblaze API at `api.demoblaze.com` | same deadlock on add-to-cart — pre-stub required (MB3 still open); `browser_map` misses async-loaded products initially |
| Pet Store Web | https://petstore.octoperf.com/actions/Catalog.action | Category nav via `area[href*=Category]` or direct URL (`?viewCategory=&categoryId=FISH`); login `j2ee`/`j2ee` → "Welcome ABC!"; jsessionid in URL (path-based, not cookie); `vibium map` misses image map areas | Identical — `browser_map` misses image areas; use `area[href]` selectors or direct URL navigation |

### Security Testing

| Name | URL | Notes |
|------|-----|-------|
| bWAPP | local only | Requires local Docker/Apache setup; no public demo; info at itsecgames.com; 100+ web vulnerabilities |
| Damn Vulnerable GraphQL Application (DVGA) | local only | Requires local Docker; GraphQL-specific vulnerabilities; no public hosted demo |
| Firing Range | https://public-firing-range.appspot.com/ | Google's XSS/CORS/Clickjacking test bed; CLI map: 10 entries on index; MCP map: 44 entries on DOM XSS sub-page; all links lead to specific vulnerability test cases |
| Gin & Juice Shop | https://ginandjuice.shop/ | PortSwigger's vulnerable e-commerce app; home page returns 500 — use `/catalog`; search + 17 product links work; designed for scanner testing |
| Google Gruyere | https://google-gruyere.appspot.com/ | Google security codelab; no unique session in public URL (use /start for isolated instance); 60 vulnerability topic links on index; covers XSS, XSRF, path traversal, code exec |
| LabEx Cybersecurity Labs | https://labex.io/ | Requires account; interactive cybersecurity learning paths; 403 on course pages without login |
| OWASP Juice Shop | https://demo.owasp-juice.shop/ | Angular app; **MCP loads fully** (15 products), **CLI gets Application Error** (Angular SSR timing issue); cookie banner + welcome modal on load; use eval+click to dismiss; add-to-basket obscured by modal |
| OWASP VWAD | https://owasp.org/www-project-vulnerable-web-applications-directory/ | Directory of vulnerable web apps — not itself a test target; links to all major vulnerable apps at vwad.owasp.org |
| Try Hack Me | https://tryhackme.com/ | Landing page accessible; labs/rooms require account; heavy Next.js app (7–15s load); 72 interactive elements on homepage; great for account-based security training |
| VAmPI | local only | Vulnerable REST API; requires local Docker; OWASP top 10 API vulnerabilities; no public hosted demo |
| Zero Bank | http://zero.webappsecurity.com/ | Micro Focus Fortify demo; **HTTP-only** — BiDi error in both CLI and MCP; accessible via curl (HTTP 200) but Chrome/BiDi blocks HTTP origins |

---

## Exploratory Test Protocol

When given a site to test, run this structured protocol. Skip steps that are not applicable (e.g. login for sites without auth).

Before Step 1, take a bracket snapshot for per-site token/time tracking:
```sh
BASE=$(python3 ~/.claude/skills/practice-testing/token_bracket.py --snapshot --time)
```
After completing the site test, compute the delta:
```sh
python3 ~/.claude/skills/practice-testing/token_bracket.py --diff "$BASE"
# → time:12847ms  input:142  write:1204  read:89241  output:318  total:90905  cost:$0.0087
```
Take a fresh snapshot before each site (CLI and MCP are separate brackets). Use `--json` for machine-readable output.

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
MCP `browser_get_text` returns `""` on blank pages (MB9 fixed v26.5.31).

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

### Token / Cost
- LLM turns: +X (CLI) / +X (MCP)
- Cost delta: +$X.XX (CLI) / +$X.XX (MCP)
- Ratio: X× cheaper via CLI

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
- Both `vibium select` (CLI) and `browser_select` (MCP) match by visible label OR value attribute (B5/engine fixed v26.5.31); both error on non-existent option
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
- Use `browser_dialog_accept` / `browser_dialog_dismiss` for native dialogs — but MB3 still open: direct `browser_click` on alert triggers deadlocks; use `browser_evaluate {setTimeout(...,300)}` + `browser_sleep {ms:350}` + `browser_dialog_accept {}` (#151 deferred)
- `browser_find` with `role="link"` times out on `<button>` elements — use `browser_map` refs or CSS selectors instead
- MCP `browser_map` finds more elements on some pages than CLI `vibium map` (e.g. puzzle index links, Angular Material list items)
- Stop/restart MCP browser session with `browser_stop` + `browser_start` when BiDi errors occur — this does NOT affect the CLI daemon

---

## CLI vs MCP — Behavioral Comparison

Compiled from practice-testing exercise across 99 sites (2026-04-22 → 2026-05-19). Updated for v26.5.31 (2026-06-01). Targeted rerun confirmed June 2, 2026: B5 select (8 sites), B7/MB7 textarea (5 sites) — all PASS. MB3 dialog deadlock confirmed still open (#151 deferred).
Organized by command/tool pair. Confirmed differences come from observed cross-site behavior, not docs.

### Paired Commands — Diffs and Samesies

#### navigate — `vibium go` / `browser_navigate`

| | CLI | MCP |
|---|---|---|
| HTTP-only URLs | BiDi error, page not loaded | Loads silently, no error |
| Subdomain pages | Deadlocks (B3) — must use `eval 'location.href="..."'` | Works without deadlock |
| Same-origin navigation | Same | Same |

**Verdict:** MCP wins on HTTP and subdomain navigation. CLI requires eval workaround for both.

---

#### map — `vibium map` / `browser_map`

| | CLI | MCP |
|---|---|---|
| Standard DOM | Returns interactive refs | Same |
| React/Angular SPAs (JS-heavy) | May return nothing on first map | Same |
| Some SPAs (Angular Material, SAP UI5, Black Box Puzzles) | Returns nothing or subset | Returns more elements — up to 128+ vs 0 |
| Shadow DOM pages (Polymer Shop) | Returns nothing | Same |
| Async-loaded content | Misses elements not yet rendered | Same |

**Verdict:** Same behavior in most cases. MCP `browser_map` finds more elements on a subset of pages where CLI returns nothing or a subset — not consistently across all frameworks.

---

#### get_text — `vibium text` / `browser_get_text`

| | CLI | MCP |
|---|---|---|
| Normal pages | Returns visible text | Same |
| Empty/blank/invisible pages | Works (returns empty string) | Works (returns empty string) — MB9 fixed in v26.5.31 |
| Very large text bodies (e.g. 5000 API results) | Crashes BiDi session | Returns oversized-output error (no crash) |

**Verdict:** Same on normal and empty pages. Different failure modes only on very large text — CLI crashes, MCP returns oversized error.

---

#### evaluate — `vibium eval 'expr'` / `browser_evaluate {expression}`

| | CLI | MCP |
|---|---|---|
| Multi-statement with semicolons | Fails due to shell quoting — split into separate calls | No shell quoting issue; all in one call |
| Expression returning `""` | Works | Works — MB6 fixed in v26.5.31 |
| Expression returning `null` | Works | Same |
| Parallel/async (`Promise.all`) | Limited | Works cleanly |

**Verdict:** CLI has shell quoting constraint only. Empty-string return now works in both.

---

#### fill — `vibium fill selector value` / `browser_fill {selector, value}`

| | CLI | MCP |
|---|---|---|
| Text inputs | Works | Same |
| `<textarea>` | Works — B7 fixed in v26.5.31 | Works — MB7 fixed in v26.5.31 |
| Fill with empty string to clear | Rejects `""` — use eval to clear (B20 open) | Throws "value is required" — use eval to clear |
| Framework-driven inputs (React, Angular) | May not trigger state update | Same; use `browser_type` for key-event-driven components |

**Verdict:** Same on standard inputs and textarea (both fixed). Neither can clear a field with empty string — use eval.

---

#### type — `vibium type selector value` / `browser_type {selector, value}`

| | CLI | MCP |
|---|---|---|
| Text inputs | Works | Same |
| `<textarea>` | Works | Same |
| Framework-driven textareas (React/Angular) | Works — fires events | Works — fires key events that update component state |
| Date inputs (`input[type=date]`) | Needs eval `.value =` (fill/type both fail) | Same — use eval |

**Verdict:** Same behavior across the board.

---

#### select — `vibium select selector value` / `browser_select {selector, value}`

| | CLI | MCP |
|---|---|---|
| Matching | Matches by visible label OR value attribute (B5 fixed v26.5.31) | Same (shared engine fix) |
| Non-existent value | Errors: `no <option> matches "..."` exit 1 (B5 fixed) | Same |
| Angular ng-model select | Fails — model not updated | Same failure — use `eval .value= + dispatchEvent(change)` |

**Verdict:** Identical behavior. Both now match by visible label OR value attribute; both error on no match. Angular ng-model limitation applies to both.

---

#### click — `vibium click selector` / `browser_click {selector}`

| | CLI | MCP |
|---|---|---|
| Standard interactive elements | Works | Same |
| `input[type=submit]` | Sometimes needs `eval .click()` | Works directly — no eval needed |
| Zero-size elements | Fails | Same |
| Elements obscured by overlay | Fails | Same; try `eval element.click()` |

**Verdict:** MCP `browser_click` succeeds on some elements (e.g. `input[type=submit]`) that CLI needs eval for.

---

#### check / uncheck — `vibium check` / `browser_check`, `vibium uncheck` / `browser_uncheck`

| | CLI | MCP |
|---|---|---|
| Visible checkboxes | Works | Same |
| Obscured checkboxes (ToDo List, React Shopping Cart) | Fails — use `vibium mouse click x y` | Fails — use `browser_mouse_click {x, y}` at computed coords |

**Verdict:** Same — both fail on obscured checkboxes; both need coordinate click workaround.

---

#### hover — `vibium hover` / `browser_hover`

| | CLI | MCP |
|---|---|---|
| Interactive elements | Works | Same |
| Non-interactive `<div>` elements | Works — B30 partial fix v26.5.31 | Same |
| Non-interactive `<img>` with external src | Fails: `visible check failed — zero size` (B30 still open) | Use `browser_mouse_move` to computed coords |
| Other non-interactive elements | Use `vibium mouse move x y` | Use `browser_mouse_move` to computed coords |

**Verdict:** CLI partial improvement — hover on `<div>` now works. Both still need coordinate mouse_move for `<img>` with external src and other non-interactive elements.

---

#### find — `vibium find {role, text}` / `browser_find {role, text}`

| | CLI | MCP |
|---|---|---|
| Finding by text | Works; returns outermost matching element | Same |
| `role="link"` on `<a>` | Works | Same |
| `role="link"` on `<button>` | Works | Times out — use `browser_map` ref or CSS selector instead |
| `role="button"` on `<button>` | Works | Same |

**Verdict:** MCP `browser_find {role: "link"}` times out on `<button>` elements. CLI handles it correctly.

---

#### drag — `vibium drag` / `browser_drag`

| | CLI | MCP |
|---|---|---|
| Standard HTML drag-and-drop | Works | Same |
| jQuery UI droppable | Fires events but framework ignores them | Same limitation |
| Polymer events | Not fired by standard drag | Not fired — must use coordinate mouse clicks at bounding-box coords |
| `vibium drag @ref` on some sites | Fails — use mouse coords | Works when content is top-level |

**Verdict:** Same framework limitations. Coordinate-based mouse events are the common fallback for both.

---

#### frames / frame — `vibium frames` / `browser_frames`, `vibium frame` / `browser_frame`

| | CLI | MCP |
|---|---|---|
| Listing frames | Works | Same |
| Entering frame context | Does NOT persist between calls | Returns metadata only; does NOT switch context |
| Workaround | `eval contentDocument.body` | `eval contentDocument.body` or navigate directly to iframe src URL |

**Verdict:** Same limitation. Neither properly persists frame context. Both need eval workarounds.

---

#### get_url — `vibium url` / `browser_get_url`

| | CLI | MCP |
|---|---|---|
| Normal read | Works | Same |
| Immediately after navigation (post-login) | BiDi timing issue — need `sleep 5` | No timing issue observed |

**Verdict:** CLI has post-navigation timing sensitivity. MCP doesn't.

---

#### stop / start — `vibium stop` / `browser_stop`, `vibium start` / `browser_start`

| | CLI | MCP |
|---|---|---|
| Scope | Restarts the CLI daemon | Restarts the MCP browser session |
| Cross-interface | No effect on MCP session | No effect on CLI daemon |

**Verdict:** Completely isolated sessions. Restarting one does not affect the other.

---

#### Dialog handling — no CLI tool / `browser_dialog_accept` + `browser_dialog_dismiss`

| | CLI | MCP |
|---|---|---|
| Native alert/confirm/prompt | Pre-stub BEFORE clicking: `eval 'window.alert=function(){}'` — clicking first deadlocks daemon (B3 still open) | Has native `browser_dialog_accept` / `browser_dialog_dismiss` |
| Direct click on alert trigger | Deadlocks daemon (B3 open) — requires `pkill -f vibium && sleep 2 && vibium daemon start` | Also deadlocks (MB3 open, deferred #151) — `browser_click` hangs until i/o timeout |
| Safe pattern | `eval 'window.alert=function(){}'` → then click | `browser_evaluate {setTimeout(..., 300)}` + `browser_sleep {ms: 350}` + `browser_dialog_accept {}` |

**Verdict:** MCP has native dialog tools; CLI must pre-stub via eval. Both deadlock if the click fires before the dialog handler is in place — same root constraint, different mitigation syntax. (#146, #151, #128 deferred.)

---

#### Samesies (no behavioral difference observed)

- `vibium title` / `browser_get_title` — identical
- `vibium screenshot` / `browser_screenshot` — identical
- `vibium diff map` / `browser_diff_map` — identical
- `vibium dblclick` / `browser_dblclick` — identical
- `vibium press` / `browser_press` — identical
- `vibium keys` / `browser_keys` — identical
- `vibium scroll` / `browser_scroll` — identical
- `vibium focus` / `browser_focus` — identical
- `vibium upload` / `browser_upload` — identical
- `vibium back` / `browser_back` — identical
- `vibium forward` / `browser_forward` — identical
- `vibium mouse move/click/down/up` / `browser_mouse_move/click/down/up` — identical

---

### MCP-Only Tools (no CLI equivalent)

| MCP Tool | Purpose |
|---|---|
| `browser_a11y_tree` | Accessibility tree dump |
| `browser_count {selector}` | Count matching elements — MB1 fixed in v26.5.31 |
| `browser_delete_cookies` | Delete cookies |
| `browser_dialog_accept` / `browser_dialog_dismiss` | Native dialog interception |
| `browser_download_set_dir` | Set download directory |
| `browser_emulate_media` | Media type emulation (print/screen) |
| `browser_find_all {selector}` | Find all matching elements (CLI `find` returns first only) |
| `browser_get_attribute {selector, name}` | Get element attribute (CLI needs `eval getAttribute(...)`) |
| `browser_get_cookies` / `browser_set_cookie` | Cookie read/write |
| `browser_get_html {selector}` | Get innerHTML/outerHTML |
| `browser_get_value {selector}` | Get input current value |
| `browser_get_viewport` / `browser_set_viewport` | Viewport dimensions |
| `browser_get_window` / `browser_set_window` | Window position/size |
| `browser_highlight {selector}` | Visual highlight in browser |
| `browser_is_checked` / `browser_is_enabled` / `browser_is_visible` | Boolean state queries (CLI needs eval) |
| `browser_list_pages` / `browser_new_page` / `browser_close_page` / `browser_switch_page` | Multi-tab management |
| `browser_pdf` | Export page as PDF |
| `browser_record_start` / `browser_record_stop` (+ chunk/group variants) | Session recording |
| `browser_reload` | Reload current page (CLI uses `eval 'location.reload()'`) |
| `browser_restore_storage` / `browser_storage_state` | localStorage/sessionStorage snapshot/restore |
| `browser_scroll_into_view {selector}` | Scroll element into viewport (CLI uses `eval scrollIntoView()`) |
| `browser_set_content {html}` | Replace page content with raw HTML |
| `browser_set_geolocation` | Spoof browser geolocation |
| `browser_sleep {ms}` | Wait in milliseconds (CLI uses shell `sleep N` — seconds only) |
| `browser_wait_for_fn {fn}` | Wait until JS expression is truthy |
| `browser_wait_for_text {text}` | Wait until text appears on page |
| `browser_wait_for_url {url}` | Wait until URL matches |
| `page_clock_install` / `page_clock_set_fixed_time` / `page_clock_set_system_time` / `page_clock_set_timezone` / `page_clock_pause_at` / `page_clock_resume` / `page_clock_fast_forward` / `page_clock_run_for` | Mock/control page clock |

---

### CLI-Only Behaviors

| Behavior | Notes |
|---|---|
| PATH prefix required | `export PATH="/usr/local/bin:$PATH"` to avoid Python vibium binary |
| Shell sleep | `sleep N` — integer seconds only; MCP `browser_sleep {ms}` is milliseconds |
| Daemon persistence | CLI daemon stays alive across Bash tool calls; MCP tools are stateless per-call |
| Alert pre-stub pattern | Must `eval 'window.alert=function(){}'` before any click that triggers a dialog |

---

### Cross-Cutting Samesies (confirmed identical across all sites)

- **select**: both match by visible label OR value attribute (B5/engine fixed v26.5.31); both error on non-existent option
- **textarea fill**: both work with `fill` (B7/MB7 fixed v26.5.31); `type` still works as alternative
- **obscured checkbox**: both fail with `check`; both need coordinate click
- **shadow DOM**: both return nothing from map; both need `eval shadowRoot`
- **Angular ng-model select**: both fail to trigger model update; both need eval + dispatchEvent
- **canvas/custom-painted elements**: both return nothing from map; both need coordinate click from getBoundingClientRect
- **frame context**: neither properly persists frame switch; both need eval workaround
- **jQuery UI droppable**: drag fires but framework ignores — eval workaround for both
- **BiDi session recovery**: both need stop + start after broken pipe
- **CSS text-transform**: both find by DOM text, not rendered text
- **Azure/Heroku hibernated backends**: same 3s wait + reload pattern needed
