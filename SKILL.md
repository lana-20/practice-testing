---
name: practice-testing
description: Explore and test QA practice sites. Pass a site name or URL to navigate, map, interact, and report bugs/observations. Use when asked to test practice sites or QA playgrounds.
---

# practice-testing

Run exploratory tests on QA practice sites using vibium browser automation.

## How to run

`/practice-testing [site-name-or-url]`

- `/practice-testing AcademyBugs` — test by name from the list below
- `/practice-testing Parabank` — test Parabank by name
- `/practice-testing https://example.com` — test any URL directly
- `/practice-testing` — list all available practice sites

## Site Directory

### General Practice

| Name | URL | Notes |
|------|-----|-------|
| AcademyBugs | https://academybugs.com/ | 25 real bugs planted; dismiss tutorial modal + cookie banner before interacting |
| Basic Calculator | https://testsheepnz.github.io/BasicCalculator.html | Prototype + builds 1–9; select operation by value ("0"–"4"), not text |
| Black Box Puzzles | https://blackboxpuzzles.workroomprds.com/ | Most puzzles need Flash — only 22, 24, 26b, 29, 31, 33, 34 work; use `mouse click x y` not map refs |
| BookCart | https://bookcart.azurewebsites.net/ | Azure-hosted; backend frequently hibernated — products may not load |
| Cnarios | https://www.cnarios.com/ | Challenges work; /concepts/* pages render blank (React routing bug) |
| Evil Tester | https://testpages.eviltester.com/styled/index.html | Stub alert/confirm/prompt via eval BEFORE clicking alert buttons |
| Gefälscht CompuTech | https://webtestingcourse.dequecloud.com/ | Intentionally inaccessible; contact form fields need `input[name=x]` selectors |
| Magento | https://magento.softwaretestingboard.com/ | DOWN — Cloudflare 526 SSL error as of 2026-04-22 |
| Parabank | https://parabank.parasoft.com/parabank/admin.htm | Run DB Initialize first; login broken — use for form/validation testing only |
| Parking Cost Calculator | https://www.shino.de/parkcalc/ | Use option values not text for lot dropdown; invalid dates cause blank page |
| PHP Travels | http://phptravels.com/demo/ | Landing page only — submit form to get emailed credentials; no public demo URL; Submit button deadlocks daemon — pre-stub dialogs; Login nav link is broken (redirects to same page) |
| Polymer Shop | https://shop.polymer-project.org/ | All UI in Web Components shadow DOM — `vibium map` returns nothing; use `eval + shadowRoot` traversal or coordinate clicks; cart is server-side |
| Practice Software Testing | https://practicesoftwaretesting.com/ | Angular app; add to cart works without login; test login: `customer@practicesoftwaretesting.com` / `welcome01` (may be locked); Login is `input[type=submit]` — use `eval.click()` not `vibium find role button` |
| Presta Shop | https://demo.prestashop.com/ | Store in iframe — get inner URL via `eval 'document.querySelector("#framelive")?.src'` after 5s wait; subdomains expire in ~2 min of active testing; `vibium go` to subdomain pages deadlocks daemon (B3) — use `eval 'location.href="..."'` + `vibium wait load` for all navigation; add-to-cart button permanently disabled after PS JS init (click via ref succeeds but AJAX fails silently); checkout unreachable without cart items |
| QA Practice | https://qa-practice.razvanvancea.ro/ | Moved from netlify.app; ecommerce login: `admin@admin.com` / `admin123`; ADD TO CART uses CSS uppercase — use map refs not `find text`; pre-stub alert/confirm before clicking; checkout hides products and shows Shipping Details form |
| QA Training Simulator | https://bugeater.web.app/ | 23 challenges across 7 categories: Learn Mode (4), Scripted (5), Test Case Generator (2), Gherkin (2), Functional (2), API Testing (2), Exploratory (6); `vibium fill` works on React inputs; only `learn/*`, `exploratory/*`, `gherkin/*` routes load on direct URL — `scripted/*`, `functional/*`, `api/*`, `testcase/*` crash with TypeError; navigate crashing routes from `/app/list` via `vibium eval 'link.click()'`; dismiss react-joyride tutorial overlay (Skip button) before using form; sidebar/drawer opened by hamburger @e1 — close with `vibium eval 'document.querySelector("button.btn-close")?.click()'`; two separate cookie banners: homepage and `/app/list` |
| Random User Generator | https://randomuser.me/ | API testing site; nav links work via `vibium click` (old "broken" note stale); API at `/api/` works; `?results=0`, `?results=abc`, `?results=-1`, `?results=5001` all silently return 1 result; `?format=xml` and `?format=pretty` work; `?format=csv` triggers download — crashes vibium BiDi session, restart daemon; `vibium text` crashes on `?results=5000` (buffer overflow) — use `vibium eval 'JSON.parse(document.body.innerText)'` for large responses; `?inc=name,email` field filtering and `?seed=abc` reproducible results work |
| Real World Example Apps | https://codebase.show/projects/realworld | Directory of RealWorld Conduit implementations; requires GitHub OAuth; SvelteKit SPA needs ~3s after `wait load` before content renders — add `vibium sleep 3000`; Sign in and Submit nav links now correctly redirect to GitHub OAuth (old "reload page" note stale); Frontend/Backend/Fullstack tabs and language filters work via `vibium click`; after `vibium back` from GitHub, sleep 3s again before interacting |
| The Boozang Test Lab | https://thelab.boozang.com/ | React SPA with 16 challenges; `vibium click` works on all buttons (eval.click() workaround no longer needed); Form Fill now has HTML5 required on all 4 fields — empty submit shows browser tooltip; no `#engines` select exists anywhere (old note stale); direct URLs work (e.g. `/formFill`, `/sortedList`); `vibium fill` works for inputs; Form Fill saves to shared DB at api.boozang.com/users — test data persists across sessions |
| The iframe Search Engine | https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html | URL moved — old compendiumdev.co.uk redirects here; Vanilla JS; `vibium click @e6` now works on Search button (eval workaround stale); use `vibium fill` (not type) for search input; `vibium select` with non-existent value reports success but sets `selectedIndex=-1` silently (B5 confirmed); use full URL as option value e.g. `"https://www.google.com/search?q="` not display name; "Go search" link opens search in a **new tab** — not the iframe; "Go search" href only updates after clicking Search; Bing embeds correctly; Google/DuckDuckGo block iframe (broken page icon) |
| The Internet | http://the-internet.herokuapp.com/ | 44 examples; `vibium hover` fails on non-interactive elements — use `vibium mouse move x y` for CSS `:hover` effects; `vibium frame` context doesn't persist between separate CLI invocations (each call resets to main frame) — use `vibium eval 'element.contentDocument.body'` for inline frame content or navigate directly to frame URL; TinyMCE iframe has empty src (id=`mce_0_ifr`) — `vibium frames` shows `about:blank`, `vibium frame` can't match it by name/URL — manipulate via `eval + contentDocument.body`; `vibium fill` fails on `input[type=range]` ("not editable") — use `eval` to set `.value` + dispatch `change`/`input` events; `vibium check` fails on toggle-all checkbox ("obscured") — use `vibium mouse click x y` on its label; `vibium drag` works for drag-and-drop; `vibium upload` works for file upload; `vibium press` captures key events (letters, Enter, Tab); shadow_dom page returns 404; nested frames: all frames listed flatly by `vibium frames` including nested |
| The Random Number Service | https://www.random.org/ | Cookie banner on load — dismiss with `vibium click "Allow All" button`; `vibium map` finds no nav elements — nav is anchor-based; `vibium find text` / `vibium click` work for nav; generator forms not found by `vibium map` (not in interactive scope) — submit via URL params (e.g. `?num=5&min=1&max=10&col=1&base=10&format=plain&rnd=new`) or `eval form.submit()`; inline `vibium eval` with semicolons fails (shell quoting) — use direct URL params for multi-field form submission; validation: min>max → error message; num>10000 → error; negative min/max accepted; `?format=plain` returns raw text; `?format=html` returns styled page |
| Testing Challenges | http://testingchallenges.thetestingmap.org/ | HTTP-only (no HTTPS); `vibium go` fails with BiDi "unknown error"; `eval + location.href` navigates to `chrome-error://chromewebdata/` (blank page) — Chrome blocks HTTP-only origin entirely; accessible via curl (HTTP 200) but Chrome refuses navigation; cannot be tested with vibium |
| ToDo List | https://todolist.james.am/#/ | AngularJS app; `vibium map` finds input + checkboxes; `vibium fill` + `vibium press "Enter"` adds todos; whitespace-only input silently rejected (no todo created); `vibium dblclick` on label enters edit mode — `vibium fill` + Enter saves; `vibium check` fails on todo checkboxes ("obscured") — use `vibium mouse click x y` on checkbox coords; `vibium check "#toggle-all"` fails ("obscured") — click its label by coordinates; **BUG**: item counter off by 1 (shows N-1 active items); **BUG**: delete button title exposed as "TODO:REMOVE THIS EVENTUALLY"; no persistence across page reloads (no localStorage); filter links (All/active/Completed) work via `vibium click`; Clear button removes completed items |
| UI5 Demo Kit | https://ui5.sap.com/#/demoapps | SAP UI5 SPA; main `#/demoapps` page: `vibium map` returns "No interactive elements found" but 72 links + 45 buttons exist in regular DOM; `vibium find text "NavLabel"` + `vibium click` works for top nav (Home/Documentation/Samples etc.); demo app links reachable via `vibium eval 'document.querySelector("a[href*=...]")?.click()'` or direct URL navigation; individual demo apps have regular DOM and `vibium map` works normally; Shopping Cart demo fully interactive — add to cart, cart panel, proceed work via `vibium click`; search input needs `vibium click` first then `vibium fill`; `?format=csv` download link has `href="#"` (JS download) — don't navigate directly |

### Automation Testing

| Name | URL | Notes |
|------|-----|-------|
| Automation Bookstore | https://automationbookstore.dev/ | Filter-only single-page app; all 8 book links have `href="#"` (no detail page); case-insensitive real-time filter works; no "no results" message on empty filter |
| Automation Camp | https://play2.automationcamp.ir/ | Alert button and invalid login both deadlock daemon (native `alert()`) — `eval` override does not prevent it, restart required; valid login: `test`/`test`; double-click, drag-and-drop (CSS selectors), radio buttons, select all work; `input[type=date]` not fillable via `vibium fill` — use `eval .value =`; form submits as GET |
| Applitools Demo | https://demo.applitools.com/ | Intentional visual testing site; login accepts any credentials including empty; dashboard shows `$350%7` (corrupted total balance — intentional bug); transaction timestamps malformed ("Today1:52am"); search bar non-functional; all action links dead (`href="#"`) |
| Automation Exercise | https://www.automationexercise.com/ | Ad overlay intercepts nav clicks on homepage — use direct URLs (e.g. `/products`); dismiss ad "Close" SVG button before interacting; full e-commerce flow works: search → detail → add to cart (qty supported) → view cart; test cases at `/test_cases`, API list at `/api_list` |
| Automation in Testing | https://automationintesting.online/#/ | Full B&B booking site (Shady Meadows); Check Availability button obscured by calendar after date entry — use `eval 'document.querySelector("#booking button").click()'`; full booking flow works end-to-end with confirmation; admin panel at `/admin` (`admin`/`password`) with rooms, report, branding, messages; contact form `#description` textarea not fillable via `vibium fill` — use `eval + dispatchEvent(new Event("input", {bubbles:true}))` |
| Automation Testing Practice | https://testautomationpractice.blogspot.com/ | Blogger-hosted single long page; sections: form (text/radio/checkbox/dropdown/date/file/autocomplete), Wikipedia search widget, drag & drop, alerts, copy text, broken links, hidden elements & AJAX sub-page; `input[type=date]` not fillable via `vibium fill` — use `eval .value =`; datepicker field is `readonly` — calendar widget only; alert buttons deadlock daemon — pre-stub; Colors dropdown has duplicate option values (`red` × 2, `green` × 2); broken links point to `deadlinkcity.com` (HTTP, Chrome blocks); footer "Hidden Elements & AJAX" sub-page has toggle show/hide + AJAX load buttons; `vibium select` works with lowercase option values |
| Automation Test Store | https://automationteststore.com/ | AbanteCart e-commerce demo; full flow works: search → product detail (with color variant select) → Add to Cart → Cart → Checkout; guest checkout available (`accountFrm_accountguest` radio); login page at `/index.php?rt=account/login`; search by URL params (`?rt=product/search&keyword=...`); cart count and total update in header; `vibium select` for product variants; no credentials needed for browsing |
| Automate Now Sandbox | https://automatenow.io/sandbox-automation-testing-practice-website/ | Landing page links to sub-pages at `practice-automation.com/*`; sections: JavaScript Delays, Sliders, Tables, Ads, Click Events, Iframes, Accordions, Form Fields, Calendars, Window Operations, Gestures, Spinners, Broken Images, Popups, Modals, Hover, File Download, File Upload, Broken Links; homepage section links often obscured by ads — use `eval 'document.querySelectorAll("a")[N]?.click()'`; Form Fields (`/form-fields/`) — textarea fill fails, Submit fires `window.alert("Message received!")` — pre-stub required; Slider (`/slider/`) — `input[type=range]` needs `eval + dispatchEvent`; Click Events (`/click-events/`) — buttons show animal sounds on click; Modals (`/modals/`) — `vibium click` works on modal trigger and Close button; name input on Form Fields requires `vibium click` first before `vibium fill` works |
| Expand Testing | https://practice.expandtesting.com/ | Feature-rich practice site; many homepage links obscured by ads — navigate by direct URL; login at `/login` (credentials: `practice` / `SuperSecretPassword!`) — Login button also obscured, use `eval 'document.querySelector("button[type=submit]").click()'`; valid login → `/secure` with "You logged into a secure area!"; invalid login → "Your password is invalid!" flash message; Inputs page at `/inputs` — number/text/password/date fields, Display Inputs button shows all values in output fields; also has register, forgot password, OTP, dynamic table, pagination, drag & drop, shadow DOM, alerts, iframes, and more; API docs at Swagger |
| Coffee Cart | https://coffee-cart.app/ | Clean Vue SPA; 9 drinks listed (Espresso $10–Cappuccino $19); product cards are `div[data-test=ProductName]` — not in `vibium map` but reachable via `vibium find "[data-test='Espresso']" && vibium click @e1` (underscores for spaces: `Flat_White`, `Cafe_Latte`); cart nav at `/cart` shows items with `+`/`-`/`×` buttons — all accessible via `vibium map` and `vibium click`; in-memory cart — navigate via UI link, never `vibium go /cart`; checkout modal: name + email required (HTML5 validation), promo checkbox optional; successful submit → "Thanks for your purchase. Please check your email for payment." and cart resets to 0; full flow works end-to-end |
| Commit Quality | https://commitquality.com/ | |
| Contact List App | https://thinking-tester-contact-list.herokuapp.com/ | |
| Demo SaaS | https://demo-saas.bugbug.io/ | |
| GreenKart | https://rahulshettyacademy.com/seleniumPractise/#/ | |
| Global SQA Demo | http://www.globalsqa.com/demo-site/ | |
| Hands-On Selenium WebDriver | https://bonigarcia.dev/selenium-webdriver-java/ | |
| Lambdatest Playground | https://ecommerce-playground.lambdatest.io/ | |
| Let Code | https://letcode.in/test | |
| Locator Game | https://testsmith-io.github.io/locator-game/ | |
| Practice Test Automation | https://practicetestautomation.com/practice/ | |
| QA Playground | https://qaplayground.dev/ | |
| React Shopping Cart | https://react-shopping-cart-67954.firebaseapp.com/ | |
| Selectors Hub | https://selectorshub.com/xpath-practice-page/ | |
| Selenium Playground | https://www.lambdatest.com/selenium-playground/ | |
| Swag Labs | https://www.saucedemo.com/ | |
| Sweet Shop | https://sweetshop.netlify.app/ | |
| Tricentis Obstacle Course | https://obstaclecourse.tricentis.com/Obstacles | |
| UI Test Automation Playground | http://uitestingplayground.com/ | |
| Weather Shopper | https://weathershopper.pythonanywhere.com/ | |
| XYZ Bank | https://www.globalsqa.com/angularJs-protractor/BankingProject/ | |

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
```sh
vibium go <url>
vibium wait load --timeout 10000
vibium title
vibium screenshot -o step1-load.png
```
Record: loaded / timed out / error page.

### Step 2 — Page structure
```sh
vibium text
vibium map
```
Note: main navigation links, prominent headings, form count, interactive element count.

### Step 3 — Navigation smoke test
Click 2–3 main nav links. After each:
```sh
vibium click @eN
vibium diff map
vibium url
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
```sh
vibium screenshot -o final.png --full-page
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

- Always re-map after clicking navigation or submitting forms — refs expire on page change
- Use `vibium find text` / `find role` instead of hardcoded refs for reliability
- Sites marked "with bugs" are intentionally broken — report bugs as findings, not failures
- For sites requiring login, check the site's About/Demo page for credentials first
- iframes require `vibium frames` then `vibium frame "<name>"` before interacting inside them
- Dismiss cookie banners and modals early — they obscure elements and block clicks
- `vibium select` matches by option `value` attribute, not display text; use `vibium eval` to inspect option values first if unsure
- Elements styled with CSS `text-transform: uppercase` cannot be found by `vibium find text "UPPERCASE"` — search for the actual DOM text (e.g. "Books" not "BOOKS")
- Canvas-rendered and custom-painted UIs won't appear in `vibium map` — use `vibium eval getBoundingClientRect()` to locate elements, then `vibium mouse click x y`
- Azure/Heroku-hosted demo sites may hibernate — if products or data don't load, wait 5s and reload once before reporting a bug
- For React SPAs, always test routes via in-app navigation first; direct URL navigation may fail if the server doesn't handle client-side routes
