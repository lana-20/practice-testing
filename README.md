# Practice Testing — Test Reports

## Session: 2026-04-22 — Batch 3 (3 sites completed, 1 partial)

---

### 11. PHP Travels
**URL:** http://phptravels.com/demo/
**Type:** Travel booking SaaS marketing/demo page

#### Reachability
[PASS] Site loaded in ~3s

#### Structure
- Navigation: Product (dropdown), Features, Company, Blog, Demo, Pricing, Login, Talk to Sales
- Forms: 0 — inputs exist but no `<form>` element; JS-handled submission
- Interactive elements: 65 (nav links, form inputs, FAQ accordions, zoom buttons)

#### Navigation
[PASS] Blog → https://phptravels.com/blog
[PASS] Pricing → https://phptravels.com/pricing
[BUG] Login nav link → redirects back to demo page (https://phptravels.com/demo/), not a login page

#### Core Functionality
| Action | Result | Notes |
|--------|--------|-------|
| Submit form empty | PASS | HTML5 validation — WhatsApp field required error shown |
| Country select | PASS (not required) | Country is `required=false` — can submit without it |
| FAQ accordion via vibium click | FAIL | `aria-expanded` stays `false`; content max-height stays 0 |
| FAQ accordion via eval click | PASS | `aria-expanded` flips to `true`; content renders correctly |
| Submit button click | BUG | Deadlocks vibium daemon socket (B3); pre-stub dialogs required |

#### Bugs Found
1. **Login nav link broken** — Steps: click "Login" in header nav → redirects to `phptravels.com/demo/` instead of a login form — Severity: High
2. **FAQ accordion: vibium click ignored** — Steps: click FAQ button via `vibium click @eN` → `aria-expanded` remains `false`, panel stays collapsed; eval click works — Severity: Medium
3. **Submit button deadlocks daemon** — Steps: `vibium click @e20` (Submit) → i/o timeout; daemon hangs — workaround: pre-stub `window.alert = () => {}` — Severity: High (B3 repro)
4. **Country field not required** — Form shows WhatsApp + Email + name fields as required, but Country (marked with asterisk visually) has `required=false` — Severity: Low

#### Notes
- This is a lead-generation landing page, not an accessible demo. Actual travel booking demo requires form submission and credentials sent by email; no public demo URL.
- The form has no `<form>` element — all 6 inputs are in a `<div id="demo-form">` with JS submit handler.
- Navigation works for Blog and Pricing. The dropdown menus (Product, Features, Company) were not fully tested as they use hover + JS expansion.

---

### 12. Polymer Shop
**URL:** https://shop.polymer-project.org/
**Type:** E-commerce demo built with Polymer Web Components

#### Reachability
[PASS] Site loaded in ~2s; Web Components initialized in ~5s total

#### Structure
- Navigation: Home, Men's Outerwear, Ladies Outerwear, Men's T-Shirts, Ladies T-Shirts (all via shadow DOM)
- Forms: 1 (checkout — in shadow DOM)
- Interactive elements: 0 via `vibium map` (all elements inside shadow DOM; map returns nothing)

#### Navigation
[PASS] Men's Outerwear → https://shop.polymer-project.org/list/mens_outerwear (via direct URL)
[PASS] Product detail → https://shop.polymer-project.org/detail/mens_outerwear/Men+s+Tech+Shell+Full-Zip
[PASS] Cart → https://shop.polymer-project.org/cart
[PASS] Checkout → https://shop.polymer-project.org/checkout

#### Core Functionality
| Action | Result | Notes |
|--------|--------|-------|
| vibium map on any page | FAIL | Returns "No interactive elements found" — all UI in shadow DOM |
| Get nav links via eval | PASS | `shadowRoot.querySelectorAll("a")` returns 8 links |
| Product listing (16 items) | PASS | Loaded via direct URL; names and hrefs accessible via eval |
| Product detail (name, price) | PASS | "Men's Tech Shell Full-Zip" — $50.20; selects for Size (XS–XL) and Qty (1–5) |
| Add to Cart (via coordinates) | PASS | `getBoundingClientRect()` → `vibium mouse click 813 752`; cart showed 1 item |
| Cart total | PASS | $50.20 correct in cart shadow DOM |
| Checkout button (via coordinates) | PASS | Navigated to /checkout |
| Checkout empty-submit validation | PASS | 9 `input:invalid` entries: email, phone, shipAddress, shipCity, shipState, shipZip, ccName, ccNumber, ccCVV |

#### Bugs Found
1. **vibium map completely non-functional** — Steps: `vibium map` on any page → "No interactive elements found"; all elements rendered inside `<shop-app>` custom element's shadow DOM — Severity: High (automation limitation, not a site bug)

#### Notes
- Entire UI is inside nested shadow DOMs: `shop-app > shop-list/shop-detail/shop-cart/shop-checkout`, each with its own `shadowRoot`. Normal vibium map, click, fill, find commands are all ineffective.
- Workaround chain: `eval 'shadowRoot.querySelectorAll(...)` to find elements → `getBoundingClientRect()` for coords → `vibium mouse click x y` to interact.
- Cart is server-side — direct URL navigation to `/cart` is safe.
- Checkout form has 9 required fields. Month expiry select uses numeric values (1–12). No real payment processing.

---

### 13. Practice Software Testing
**URL:** https://practicesoftwaretesting.com/
**Type:** Angular e-commerce (Toolshop) — hand tools, power tools, rentals

#### Reachability
[PASS] Site loaded in ~2s

#### Structure
- Navigation: Home, Categories (dropdown), Contact, Sign in, Language selector
- Forms: Login form, Search form, Checkout wizard (4 steps)
- Interactive elements: 71 on homepage (nav, product cards, filters, pagination)

#### Navigation
[PASS] Contact → https://practicesoftwaretesting.com/contact
[PASS] Sign in → https://practicesoftwaretesting.com/auth/login
[PASS] Categories dropdown → Hand Tools / Power Tools / Other / Special Tools / Rentals

#### Core Functionality
| Action | Result | Notes |
|--------|--------|-------|
| Product listing | PASS | 9 products visible with names, prices, star ratings; pagination works (5 pages) |
| Product detail | PASS | Name, price, qty +/-, Add to cart, favourites, compare, related products |
| Add to cart (no login) | PASS | Cart badge shows "1" after click — no login required to add |
| Search "pliers" | PASS | Returns 5 results: Combination Pliers, Long Nose Pliers, Pliers, Slip Joint Pliers, Leather toolbelt |
| Brand filter checkbox | PASS | Products filtered to matching brand on check |
| Login empty submit | PASS | "Email is required" error shown |
| Login with test credentials | FAIL/BUG | `customer@practicesoftwaretesting.com` / `welcome01` → "Account locked, too many failed attempts" |
| Login with admin credentials | FAIL | `admin@practicesoftwaretesting.com` / `AKZBr3!2` → "Invalid email or password" |
| Checkout wizard navigation | PASS | Step 1 (Cart) → Step 2 (Sign in) → Steps 3–4 require login |
| `vibium find role button --name "Login"` | FAIL | Login submit is `input[type=submit]`, not a button — element not found; use `eval.click()` |

#### Bugs Found
1. **Test account locked** — `customer@practicesoftwaretesting.com` locked due to too many failed attempts; shared demo accounts vulnerable to lock-out — Severity: Medium (environment state issue, not app bug)
2. **Login `input[type=submit]` not findable by `vibium find role button`** — Steps: `vibium find role button --name "Login"` → timeout; workaround: `vibium eval 'document.querySelector("input[type=submit][value=Login]").click()'` — Severity: Low (vibium B5/selector limitation)

#### Notes
- Add to cart works without login — cart badge increments to "1" immediately. Login is only required to proceed past cart step in checkout wizard.
- The 4-step checkout wizard: Cart → Sign in → Billing Address → Payment. Steps are labeled clearly with numbered indicators.
- Search results include "Leather toolbelt" for "pliers" — possible relevance ranking issue or tag-based matching.
- Login submit is `input[type=submit]` not `button` — `vibium find role button --name "Login"` fails with timeout; must use `eval.click()`.
- Swagger API available at https://api.practicesoftwaretesting.com/api/documentation — not tested this session.

---

### 14. PrestaShop (partial)
**URL:** https://demo.prestashop.com/ → inner store `barbarous-grass.demo.prestashop.com/en/`
**Type:** PrestaShop e-commerce demo (wrapped in iframe)

#### Reachability
[PASS] Outer wrapper loaded; inner store URL obtained via `eval '#framelive'?.src` after 4s wait

#### Structure (confirmed from inner store)
- Navigation: Clothes, Accessories, Art; Sign in, Contact us
- Products: Hummingbird t-shirt, sweater, framed posters; quantity controls; Add to cart on listing page
- Interactive elements: 80 (all accessible via vibium map — shadow DOM not used)

#### Notes
- Testing interrupted before completing core flows. Inner store `vibium map` works correctly — all 80 elements detected.
- This site is fully documented in `/cart-patrol` skill with complete flow scripts.
- Subdomains expire in ~2–5 minutes. `barbarous-grass` was the active instance on 2026-04-22.
---

### 15. QA Practice
**URL:** https://qa-practice.razvanvancea.ro/ (moved from qa-practice.netlify.app)
**Type:** Multi-section QA playground — forms, bugs challenge, ecommerce e2e, web elements

#### Reachability
[PASS] Site loaded. Domain migrated from Netlify to razvanvancea.ro — old URL still resolves.

#### Structure
- Navigation: 18 collapsible sidebar sections (Forms, Buttons, Actions, Dropdowns, Iframes, Alerts, File Upload, Date Pickers, Loader, Pagination, Ecommerce, Bugs Challenge, GraphQL, API, Products, etc.)
- Pages: separate `.html` files per section
- Interactive elements: 58 mapped on home; ecommerce has 20-page pagination

#### Navigation
[PASS] All sidebar accordion items expand correctly  
[PASS] Direct URL navigation to all `.html` pages works  
[PASS] Sub-menu links (Forms → Login/Register/Recover Password) functional  

#### Core Functionality

**Register Form** (`/register.html`)
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Empty submit | HTML5 native validation stops at email (required) |
| BUG | Optional fields | First name, phone, country have no `required` — form submits without them despite being labeled |
| PASS | Valid fill + submit | "The account has been successfully created!" shown |
| BUG | Country after submit | Country dropdown resets to blank after successful registration |
| BUG | Success banner color | Pink/red — should be green |

**Bugs Challenge Form** (`/bugs-form.html`) — 15 intentional bugs
| # | Bug |
|---|-----|
| 1 | Email `type="text"` not `type="email"` — "notanemail" accepted without format check |
| 2 | Password `type="text"` not `type="password"` — plaintext visible while typing |
| 3 | Label typo: "Phone nunber" (missing 'm') |
| 4 | Last Name marked `*` mandatory but form submits without it |
| 5 | Phone data corruption: entered "12345678901", summary shows "12345678902" (last digit changes) |
| 6 | Error and success banners share the same pink color |
| 7 | Country placeholder "Select a country…" shown verbatim in success summary |

**Ecommerce Flow** (`/auth_ecommerce.html`)
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Login | `admin@admin.com` / `admin123` → product listing with cart |
| PASS | Add to Cart | Cart updates with item name, price, qty 1, correct total |
| PASS | Proceed to Checkout | Hides product section, reveals Shipping Details form |
| PASS | Submit Order | Confirmation: "Congrats! Your order of $9.99 has been registered..." |
| NOTE | Session | localStorage-based; page refresh loses login state |

**Dropdowns** (`/dropdowns.html`)
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Simple select | Country dropdown selects correctly |
| PASS | Multi-level Bootstrap dropdown | Opens submenu with nested options |

**Alerts** (`/alerts.html`)
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Alert button | Fires `window.alert` — pre-stub required before clicking |
| PASS | Confirm button | Fires `window.confirm` — pre-stub required before clicking |

#### Bugs Found (non-challenge pages)
1. Register — First name/phone/country not required despite being labeled — Low
2. Register — Country resets after submit — Medium (data loss)
3. Register — Success banner is red/pink — Low (visual)

#### Automation Notes
- `ADD TO CART` uses CSS `text-transform: uppercase` — DOM text is lowercase; `vibium find text "ADD TO CART"` fails. Use `vibium map` refs instead.
- Pre-stub `window.alert`/`window.confirm` before clicking any Alert/Confirm buttons.
- Ecommerce login: `admin@admin.com` / `admin123`; after login, ADD TO CART buttons appear as `@e27`–`@e36` in map.
- "PROCEED TO CHECKOUT" toggles parent `display:none → block`; product section hides simultaneously.

---

## Session: 2026-04-22 — Batch 2 (5 sites)

---

### 6. Evil Tester
**URL:** https://testpages.eviltester.com/styled/index.html
**Type:** Multi-section automation & exploratory testing practice (Pages, Apps, Challenges)

#### Reachability
[PASS] Site loaded. Well-organized index with tag cloud and category filters.

#### Structure
- Sections: Pages (Basics, Input Elements, Forms, CSS, Navigation, Embedded Content, Files, Storage, Interaction, Mobile, Errors, Auth, Web Components), Apps, Challenges (Locator + Synchronization), Reference
- Content volume: 22 Basics, 17 Intermediate, 11 Advanced, 12 Challenges, 24 Micro Apps

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Site navigation | All top-level sections reachable, sidebar collapses/expands correctly |
| PASS | JS Alerts page | alert(), confirm(), prompt() all trigger and respond correctly |
| NOTE | JS Alerts with vibium | Must stub `window.alert/confirm/prompt` via eval BEFORE clicking — clicking first blocks the socket |
| PASS | HTML Form submit | All field types present (text, password, textarea, file, checkbox, radio, multi-select, dropdown, image, reset, submit) |
| BUG | HTML Form — textarea fill | `vibium fill` fails on textarea; must use `vibium click` + `vibium type` instead (appends, doesn't clear) |
| BUG | HTML Form — textarea placeholder persists | Textarea has "Comments..." placeholder that gets included in submitted value when using `type` |
| BUG | HTML Form — cb3 pre-checked | Checkbox 3 is pre-checked by default without any visible indication |
| PASS | Dynamic Buttons 01 challenge | All 4 sequential buttons clicked using `vibium wait "#buttonNN"` — "All Buttons Clicked" confirmed |

#### Bugs Found
1. **`vibium fill` fails on textarea elements** — `fill` throws an error on the textarea; `type` must be used instead, which appends rather than replaces. Workaround: `click` then `type`. — Severity: **Low** (vibium limitation, not site bug)
2. **Textarea placeholder text included in submission** — "Comments..." placeholder is not cleared on type, appearing in submitted value as "Comments...Test comment". — Severity: **Medium**
3. **Checkbox 3 pre-checked by default** — cb3 is checked on page load with no visual indicator or label marking it as default. Submitted data includes cb3 even without user interaction. — Severity: **Low**

#### Notes
- JS Alerts: `vibium click` on an alert-triggering button blocks the socket indefinitely. Daemon must be killed and restarted. Workaround: call `vibium eval 'window.alert = () => {}; window.confirm = () => true; window.prompt = () => "val"'` BEFORE clicking.
- Synchronization Challenges are well-suited for automation practice — dynamic buttons respond correctly to `vibium wait "#id"` + `vibium click`
- Site is actively maintained (converted to Javalin 2026-02-01, new Infinite Scroll challenge added)
- Form submit with image button (`input[type=image]`) also works as a submit trigger

---

### 7. Gefälscht CompuTech
**URL:** https://webtestingcourse.dequecloud.com/
**Type:** Fake e-commerce site by Deque Systems — intentionally inaccessible for accessibility training

#### Reachability
[PASS] Site loaded.

#### Structure
- Nav: Home, Laptops & Notebooks, Desktops, Cart, Support, Contact
- Products: 3 laptops (Fregatte 17, Abgenutzt 15, Backstein 21), 3 desktops
- Cart: pre-populated with 3 items ($1234.56 each, subtotal $3703.68)
- Contact form: Name, Email, Message fields (not mapped by vibium — no labels/ids)
- Search: returns placeholder result page

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Navigation | All nav links functional |
| PASS | Product listing page | Loads with 3 products and specs |
| BUG | Product detail page | No "Add to Cart" button — no way to add products to cart from product pages |
| BUG | Cart pre-populated | Cart shows 3 items at $1234.56 each with no way to add/remove them from the UI |
| BUG | Breadcrumb on Cart page | Shows "Home > Category > Topic" instead of "Home > Cart" |
| PASS | Search | Executes query (URL params correct), returns graceful placeholder message |
| PASS | Contact form | Submits successfully to /thanks.php with honest "fake form" message |
| BUG | Contact form fields | Not accessible — no labels, no ids; vibium map omits them; must use `input[name=x]` selectors |

#### Bugs Found (intentional accessibility issues)
1. **No Add to Cart button on product pages** — product pages show specs only; no mechanism to add to cart. — Severity: **High** (intentional for training)
2. **Cart pre-populated with hardcoded items** — cart always shows 3 items regardless of user actions. — Severity: **High** (intentional for training)
3. **Breadcrumb shows generic "Category > Topic" placeholder** — not specific to the actual page. — Severity: **Medium** (intentional for training)
4. **Contact form fields have no labels or ids** — inaccessible; only reachable by `name` attribute selectors. — Severity: **High** (intentional for accessibility training)

#### Notes
- This site is intentionally inaccessible — all "bugs" are by design for Deque accessibility training
- Good practice site for: missing labels, inaccessible navigation, breadcrumb testing, fake search
- Prices are uniform ($1234.56 for every product) — another intentional signal

---

### 8. Magento Demo Store
**URL:** https://magento.softwaretestingboard.com/
**Type:** E-commerce demo store

#### Reachability
[FAIL] Site down — Cloudflare Error 526 (Invalid SSL certificate). Both HTTPS and HTTP return the same error.

#### Bugs Found
1. **SSL certificate expired or invalid** — Cloudflare 526 on all requests. Site completely inaccessible. — Severity: **Critical**

#### Notes
- This is an infrastructure issue, not an application bug
- Re-test at a later date; SSL issues on demo/free-tier hosting are common

---

### 9. Parabank
**URL:** https://parabank.parasoft.com/parabank/admin.htm
**Type:** Simulated bank website by Parasoft

#### Reachability
[PASS] Admin page, registration, login, and lookup pages all load.

#### Structure
- Pages: Home, Admin, Register, Login, Customer Lookup, Account Services (Open Account, Overview, Transfer, Bill Pay, Find Transactions, Update Contact, Request Loan)
- Admin controls: DB Initialize, DB Clean, JMS status, Data Access Mode (SOAP/REST XML/REST JSON/JDBC), endpoint config, loan settings

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Admin page loads | DB Initialize button works — "Database Initialized" confirmed |
| PASS | Registration form | All fields map correctly; submission creates user and shows "Account Services" nav |
| BUG | Registration auto-login | After successful registration, auto-login fails — redirects to login page with error |
| BUG | Login with any credentials | "An internal error has occurred and has been logged." — backend auth broken |
| BUG | Accounts Overview | "An internal error has occurred" — authenticated page broken |
| BUG | Open New Account | "An internal error has occurred" — authenticated page broken |
| PASS | Empty login form | Correct validation: "Please enter a username and password." |
| PASS | Customer Lookup empty submit | Field-level validation: all 7 required fields show individual error messages |
| PASS | Customer Lookup with data | Returns graceful "could not be found" when account doesn't exist |

#### Bugs Found
1. **Login always fails with internal error** — no credentials work (john/demo, newly registered users). Backend authentication endpoint returning 500. — Severity: **Critical**
2. **Registration auto-login broken** — after successful user creation, the automatic login redirect fails. User must log in manually but manual login also fails. — Severity: **High**
3. **All authenticated pages return internal error** — Accounts Overview, Open New Account inaccessible. Backend API down for all account operations. — Severity: **Critical**

#### Notes
- DB Initialize must be run from /parabank/admin.htm before testing — resets to default state
- After DB reinit, any previously registered users are wiped
- Data access mode switching (SOAP/REST/JDBC) does not fix the login issue
- Registration form itself works correctly — the bug is in the post-registration auth flow and the login endpoint
- Customer Lookup form has the best validation on the site — all fields individually validated

---

### 10. Parking Cost Calculator
**URL:** https://www.shino.de/parkcalc/
**Type:** Simple PHP web app — date/time-based parking cost calculator

#### Reachability
[PASS] Site loaded.

#### Structure
- Parking lots: Valet, Short-Term, Economy, Long-Term Garage, Long-Term Surface
- Inputs: entry date, entry time (AM/PM), leaving date, leaving time (AM/PM)
- Output: estimated cost + duration breakdown

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Valet 2h stay | $12.00 (correct — 5h or less flat rate) |
| PASS | Short-Term 2h stay | $4.00 (correct — $2 first hour + $1 each additional half-hour) |
| PASS | Short-Term 24h stay | $24.00 (correct — daily maximum applied) |
| PASS | Economy 7-day stay | $54.00 (correct — weekly rate) |
| BUG | Leaving time before entry time | Shows "-1 Days, 22 Hours, 0 Minutes" and $0.00 — no validation |
| BUG | Invalid date input ("not-a-date") | Blank white page returned — server error with no error message |
| NOTE | Dropdown selection | Must use option value ("Short", "Economy", "Long-Garage") not display text |

#### Bugs Found
1. **No validation for leaving time before entry time** — negative duration "-1 Days, 22 Hours" displayed; cost shows $0.00. User gets no error. — Severity: **High**
2. **Invalid date input causes blank page** — entering non-date strings renders a blank white page (PHP error suppressed). No error message shown. — Severity: **High**

#### Notes
- Calculator is otherwise accurate across all 5 lot types and multiple duration scenarios
- Weekly rates applied correctly (e.g. Economy $54/week, Long-Term Garage $72/week)
- AM/PM radios use separate `name` attributes per field — `vibium check` works correctly

---

## Session: 2026-04-22 — Batch 1 (5 sites)

---

### 1. AcademyBugs
**URL:** https://academybugs.com/
**Type:** Bug-hunting (25 planted bugs)

#### Reachability
[PASS] Site loaded. Tutorial modal appears on first load and blocks all clicks until dismissed.

#### Structure
- Navigation: Examples of Bugs, Types of Bugs, Find Bugs, Report Bugs
- Products: 18 items (clothing, accessories, coats) across a single shop page
- Sidebar: currency selector, product search, store menu, price filter, cart, account login

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Add to Cart (from listing) | Item added, success toast shown, cart count increments |
| PASS | Product detail page | Opens correctly, quantity +/- and Add to Cart present |
| BUG | Add to Cart (from product detail) | After submit, main content disappears — only sidebar renders |
| BUG | Sort dropdown | "Price Low-High" has no effect — order unchanged ($45, $46, $15.14…) |
| BUG | View N filter | Clicking "10" still shows all 18 results |
| BUG | Login page language | "NEW USER" section contains Russian text mixed with English |

#### Bugs Found
1. **Sort dropdown non-functional** — selecting any sort order leaves products in default order. Steps: go to /find-bugs/, select "Price Low-High" from dropdown. Expected: products sorted ascending. Actual: order unchanged. — Severity: **High**
2. **View-per-page filter ignored** — clicking 10/25/50 has no effect. Steps: click "10" link. Expected: 10 products shown. Actual: still shows all 18. — Severity: **Medium**
3. **Product detail Add to Cart breaks layout** — Steps: open any product detail page, click Add to Cart. Expected: confirmation shown or redirect to cart. Actual: page re-renders with main content gone, only sidebar visible. — Severity: **High**
4. **Mixed-language content on login page** — "NEW USER" label is English but description reads "Не зарегистрированы? Нажмите кнопку ниже" (Russian). Steps: click "Login for Pricing" on Dark Blue Denim Jeans. — Severity: **Medium**

#### Notes
- "Login for Pricing" on Dark Blue Denim Jeans correctly redirects to /account/ — intentional behaviour
- Cookie consent banner must be dismissed before nav links are clickable (banner obscures them)
- Product descriptions use Lorem Ipsum placeholder text

---

### 2. Basic Calculator
**URL:** https://testsheepnz.github.io/BasicCalculator.html
**Type:** Calculator with Prototype + 9 intentionally buggy builds

#### Reachability
[PASS] Site loaded.

#### Structure
- Build selector: Prototype, 1–9
- Inputs: First number, Second number, Operation (Add/Subtract/Multiply/Divide/Concatenate)
- Output: Answer field, Integers only checkbox

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Prototype: 10 + 5 | = 15 |
| PASS | Prototype: 10 − 5 | = 5 (must select by value "1", not text "Subtract") |
| BUG | Prototype: 10 / 0 | "Divide by zero error!" shown; answer shows "Calculating…" and never resolves |
| BUG | Prototype: Calculate after divide-by-zero | Button permanently disabled until page reload, even with new valid inputs |
| BUG | Build 1: non-numeric input | "abc" accepted, result is "NaN" — no validation error shown |
| BUG | Build 2: 5 + 3 | Returns "53" — string concatenation instead of addition |

#### Bugs Found
1. **Prototype: divide-by-zero leaves Calculate permanently disabled** — Steps: enter 10 / 0, click Calculate. Then enter 10 / 5. Calculate button is disabled and can't be clicked. Requires page reload. — Severity: **Medium**
2. **Build 1: no input validation** — non-numeric inputs accepted without error; result is NaN. Intentional per design (this is Build 1's planted bug). — Severity: **High** (intentional)
3. **Build 2: addition concatenates strings** — 5 + 3 = "53". Intentional per design (this is Build 2's planted bug). — Severity: **High** (intentional)

#### Notes
- `vibium select` with text label (e.g. "Subtract") does not work — operation dropdown option values are "0"–"4", not text. Use `vibium select @ref "1"` for Subtract.
- Prototype build otherwise behaves correctly for Add, Subtract, Multiply, Divide with valid inputs

---

### 3. Black Box Puzzles
**URL:** https://blackboxpuzzles.workroomprds.com/
**Type:** Exploratory testing challenges — discover what each puzzle does

#### Reachability
[PASS] Index page loaded.

#### Structure
- 25+ puzzles indexed. Older puzzles (1–18) require Adobe Flash — **not playable in modern browsers**.
- Flash-free puzzles: 22, 24, 26b, 29, 31, 33, 34
- Each puzzle is a self-contained mini-app with no instructions beyond a short hint

#### Core Functionality — Puzzle 29
Explored using `vibium mouse click x y` (elements are `<li>` nodes rendered as circles; standard map/find do not expose them as clickable).

| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Click white circle | Turns blue |
| PASS | All 4 lower circles blue | Top-row circles 1 and 4 turn red with glow |
| PASS | Click dark/non-red circle | No effect |
| PASS | Click red circle | No effect (state is read-only) |

Apparent principle: the lower 2×2 grid drives the upper row via some adjacency or XOR-style logic. Circles 1 and 4 lit when all 4 lower buttons active.

#### Notes
- `vibium map` returns no interactive refs inside puzzles — canvas/custom rendering
- Use `vibium eval getBoundingClientRect()` on `<li>` elements to get coordinates, then `vibium mouse click x y`
- Flash dependency blocks ~75% of the catalog
- Site notes: "The puzzles may well have bugs, but I've not put those bugs in on purpose" — treat anomalies as actual bugs if found

---

### 4. BookCart
**URL:** https://bookcart.azurewebsites.net/
**Type:** E-commerce bookstore (Angular + .NET API on Azure)

#### Reachability
[PASS] Site shell loads. **Product data does not load** — API returns empty/malformed response.

#### Structure
- Nav: logo, search bar, cart count, Login button, Swagger link, GitHub link
- Sidebar: category filters (Biography, Fiction, Mystery, Fantasy, Romance), price range slider
- Main: product grid (empty on every visit)

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| BUG | Product listing | "No books found." on all categories and searches — API broken |
| BUG | Login with wrong credentials | No error message shown — form stays silent |
| BUG | Login with empty fields | No validation errors shown on required fields |
| BUG | Register with empty fields | No validation errors shown on required fields |
| PASS | Register: duplicate username | "User Name is not available" error shown correctly |
| BUG | Register: successful submission | Form clears silently — no success message, no redirect |

#### Bugs Found
1. **Product catalog API broken** — all categories and search return "No books found." API call returns empty/malformed JSON. Azure backend likely hibernated or misconfigured. — Severity: **Critical**
2. **Login failure gives no feedback** — wrong credentials accepted silently; user has no indication login failed. — Severity: **High**
3. **Empty form submission shows no validation** — both login and registration forms accept submission with blank required fields, showing no error messages. — Severity: **Medium**
4. **Registration success shows no confirmation** — after submitting valid registration data, form clears but no success message or redirect occurs. — Severity: **Medium**

#### Notes
- The backend is partially alive: duplicate username check works, suggesting the .NET API is running but the book data endpoint is broken
- Azure free-tier hibernation may explain intermittent product load failures — test again at a different time before confirming #1 as a permanent bug

---

### 5. Cnarios
**URL:** https://www.cnarios.com/
**Type:** Automation practice platform (React SPA) — concepts + challenges

#### Reachability
[PASS] Home page loaded.

#### Structure
- Pages: Home, Explore, Concepts (listing), Challenges (listing + detail pages), Blogs
- Concepts: 22 topics (Button, Form, Checkbox, Radio, Date Picker, Dropdown, iFrame, Modal, Tooltip, Drag & Drop, Keyboard Events, Table, Multi Window, Slider, Scroll, Links, File Upload, Wait, Shadow DOM, and more)
- Challenges: 8 scenarios (E-commerce Pagination, Product Filtering, Login Flow, E2E Purchasing, Social Media Feed, Shadow DOM Login, Search Engine, Job Application Form)

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Home page | Renders correctly |
| PASS | /explore | Renders correctly |
| PASS | /concepts listing | Renders correctly — all 22 concept cards visible |
| BUG | /concepts/iframe | Blank page — React root has 0 innerHTML |
| BUG | /concepts/button | Blank page — same issue |
| BUG | All /concepts/* routes | Confirmed blank via both direct URL and SPA in-app navigation |
| PASS | /challenges listing | Renders correctly |
| PASS | Challenge detail page | Renders correctly (tested product-listing-pagination) |
| PASS | Pagination — Next/Prev | Navigate between pages correctly |
| PASS | Pagination — numbered pages | Jump to specific page works |
| PASS | Pagination — Next on last page | Button correctly disabled on page 5 of 5 |

#### Bugs Found
1. **All /concepts/* pages render blank** — React app fails to render on any concept route. `document.getElementById("root").innerHTML.length === 0` confirmed. Occurs on both direct URL navigation and SPA link clicks. Affects 22 concept pages — a major portion of the site's value. — Severity: **Critical**

#### Notes
- Category labels in the challenge (BOOKS, SPORTS, etc.) are CSS `text-transform: uppercase` on lowercase DOM text — `vibium find text "BOOKS"` fails; search for "Books" or use coordinate clicks
- The challenges section is well-built and functional — good for automation practice
- `/concepts` listing shows all 22 cards correctly, so the routing issue is specific to child routes, not the listing itself
