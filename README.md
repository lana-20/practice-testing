# Practice Testing — Test Reports

## Session: 2026-05-10 — Batch 7 (sites 31–35)

---

## Practice Test Report: Automation Testing Practice
URL: https://testautomationpractice.blogspot.com/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~3s

### Structure
- Navigation: Home, Udemy Courses, Online Trainings, Blog, PlaywrightPractice, GUI Elements; footer links to Hidden Elements & AJAX, Download Files, YouTube
- Forms: 1 main form (Name, Email, Phone, Address, Gender radios, Days checkboxes, Country dropdown, Colors multi-select, Sorted list, date pickers, file upload, copy text, drag & drop, Wikipedia search, alerts, section submit inputs)
- Interactive elements: 82 (full-page single-scroll with many sections)

### Navigation
[PASS] Footer "Hidden Elements & AJAX" → `/p/gui-elements-ajax-hidden.html` — toggle show/hide + AJAX load
[PASS] Other footer links (Home, Download Files, YouTube) work via `vibium click`

### Core Functionality
[PASS] Text/email/phone inputs — `vibium fill` works  
[PASS] Gender radios — `vibium check` works  
[PASS] Days checkboxes — `vibium check` works; multiple selections possible  
[PASS] Country dropdown — option values lowercase (e.g. `canada`); `vibium select` works  
[PASS] File upload — `vibium upload` works on `#singleFileInput`  
[PASS] Autocomplete (`#comboBox`) — `vibium fill` triggers suggestions  
[PASS] Hidden Elements & AJAX sub-page — Toggle Input Box 2 shows/hides correctly; Load AJAX Content updates status  
[BUG] Date picker (`#datepicker`) — `readonly` attribute; `vibium fill` fails — calendar widget only  
[BUG] `input[type=date]` Start/End Date — `vibium fill` fails with "not editable"; use `eval .value =`  
[BUG] Alert buttons — deadlock daemon; pre-stub `window.alert/confirm/prompt` via eval first  
[BUG] Broken links — point to `http://www.deadlinkcity.com` (HTTP-only); Chrome blocks, loads `chrome-error://`

### Bugs Found
1. **Duplicate option values in Colors dropdown** — `red` appears twice (values `red`, `red`) and `green` appears twice; second occurrence is indistinguishable via `vibium select`. Severity: Low
2. **Date picker is read-only** — `#datepicker` (jQuery UI) has `readonly` attribute; `vibium fill` fails with "readonly attribute". Only openable via calendar click. Severity: Low (workaround: eval or calendar interaction)
3. **`input[type=date]` not fillable via vibium** — Start Date / End Date fields error with "not editable"; use `eval 'document.querySelector("input[type=date]").value = "YYYY-MM-DD"'`. Severity: Low
4. **Broken links navigate to HTTP-only third-party domain** — `deadlinkcity.com` is HTTP; Chrome blocks with error page. Steps: click any "Errorcode NNN" link. Severity: Low (intentional — these are broken link practice targets)

### Notes
- Blogger-hosted; single long scrolling page with many independent sections
- `vibium select` requires lowercase option values for Country (`usa`, `canada`, etc.)
- Hidden Elements & AJAX sub-page is a separate URL — navigate via footer link or directly

---

## Practice Test Report: Automation Test Store
URL: https://automationteststore.com/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: Home, Apparel & Accessories, Makeup, Skincare, Fragrance, Men, Hair Care, Books; Account, Login, Cart, Checkout in top bar
- Forms: Login form, Guest checkout form (multi-step)
- Interactive elements: 40+ on homepage (nav, product cards, search, cart)

### Navigation
[PASS] Category links (Makeup, Skincare, etc.) → filtered product listing pages  
[PASS] Product search → `/index.php?rt=product/search&keyword=...`  
[PASS] Product detail → `/index.php?rt=product/product&product_id=N`

### Core Functionality
[PASS] Search ("lip") — returns 3 results: 2 shoe results + 1 lip product (cross-category matching)  
[PASS] Product detail — name, price, variant select (Color), qty, Add to Cart  
[PASS] Add to Cart — cart header updates immediately (1 ITEMS - $5.00)  
[PASS] Cart page (`/index.php?rt=checkout/cart`) — shows item table with name, model, unit price, qty, total  
[PASS] Checkout → login/register page; guest checkout radio (`#accountFrm_accountguest`) available  
[PASS] Guest checkout step 1 → `/index.php?rt=checkout/guest_step_1` — personal details form (First Name, Last Name, Email, Telephone)

### Bugs Found
None.

### Notes
- No login required to browse or add to cart
- Guest checkout avoids registration; select `#accountFrm_accountguest` radio then click Continue
- Product variant selects use option text values (e.g. "Viva Glam IV") — check with `vibium eval` first
- Search returns results across categories (shoes matched "lip" keyword) — possibly tag/description based

---

## Practice Test Report: Automate Now Sandbox
URL: https://automatenow.io/sandbox-automation-testing-practice-website/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: 19 section links (JavaScript Delays, Sliders, Tables, Ads, Click Events, Iframes, Accordions, Form Fields, Calendars, Window Operations, Gestures, Spinners, Broken Images, Popups, Modals, Hover, File Download, File Upload, Broken Links)
- Each section link navigates to a sub-page at `practice-automation.com/*`
- Interactive elements: 28 on landing page

### Navigation
[PASS] Sliders → `https://practice-automation.com/slider/`  
[PASS] Click Events → `https://practice-automation.com/click-events/`  
[PASS] Modals → `https://practice-automation.com/modals/`  
[PASS] Form Fields → `https://practice-automation.com/form-fields/`  
[BUG] Section links on landing page often report "element is obscured" — ad overlay blocks them; use `eval 'document.querySelectorAll("a")[N]?.click()'` to navigate

### Core Functionality
[PASS] Slider (`/slider/`) — `eval + dispatchEvent("input")` sets value; display updates live ("Current value: 75")  
[PASS] Click Events (`/click-events/`) — Cat/Dog/Pig/Cow buttons each show animal sound (Meow!/Woof!/Oink!/Moo!)  
[PASS] Simple Modal (`/modals/`) — `vibium click` on "Simple Modal" button opens modal; "Close" button dismisses it  
[PASS] Form Fields (`/form-fields/`) — checkboxes, radios, dropdown, email field work; name input requires `vibium click` first then `vibium fill`  
[BUG] Form Fields — textarea not fillable via `vibium fill` (throws "fill:" error)  
[BUG] Form Fields Submit — fires `window.alert("Message received!")` — pre-stub required; with stub, alert captured and form submits cleanly

### Bugs Found
1. **Section links blocked by ad overlay** — ad iframe positioned over the link grid; `vibium click @eN` reports "element is obscured". Use `eval 'document.querySelectorAll("a")[N]?.click()'`. Severity: Low (workaround exists)
2. **Textarea not fillable via `vibium fill`** — `fill:` error with no detail; workaround: `eval .value = "..." + dispatchEvent("input")`. Severity: Low (vibium limitation)
3. **Name input requires click before fill** — `vibium fill @e12` without a prior `vibium click @e12` fails with "not a text input element"; clicking first resolves it. Severity: Low (vibium quirk)

### Notes
- All sub-pages live at `practice-automation.com`, not `automatenow.io` — direct URL navigation works for all
- `input[type=range]` on slider page: `vibium fill` fails ("not editable"); use `eval + dispatchEvent(new Event("input", {bubbles:true}))`
- Modal close button (`#popmake-1318 > button`) accessible via `vibium map` and `vibium click` after modal opens

---

## Practice Test Report: Expand Testing
URL: https://practice.expandtesting.com/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: Practice, Demos, Tools, Tips, Test Cases, API Testing, About
- Apps listed: Web inputs, Login, Register, Forgot Password, OTP, Dynamic Table, Dynamic Pagination, Drag & Drop, Shadow DOM, Alerts, Iframes, Checkboxes, Dropdowns, Date Picker, File Upload, and more
- Interactive elements: 30+ on homepage; ad iframes present throughout

### Navigation
[PASS] Login page → `/login`  
[PASS] Inputs page → `/inputs`  
[PASS] Secure area → `/secure` (post-login)  
[BUG] Many homepage section links report "element is obscured" — ad iframes block clicks; navigate via direct URL

### Core Functionality
[PASS] Login with valid creds (`practice` / `SuperSecretPassword!`) — redirects to `/secure`; "You logged into a secure area!" shown  
[PASS] Login button obscured by ad — `eval 'document.querySelector("button[type=submit]").click()'` workaround works  
[PASS] Invalid login (`wrong`/`wrong`) — "Your password is invalid!" flash message  
[PASS] Inputs page (`/inputs`) — number, text, password, date fields; Display Inputs button shows all values in `#output-*` elements; Clear Inputs resets  
[PASS] Logout → redirects back to `/login` with flash message  

### Bugs Found
1. **Ad iframes obscure interactive elements throughout** — many `vibium click` calls fail with "element is obscured"; consistently reproducible on homepage and login page. Workaround: navigate by direct URL and use `eval click()` for buttons. Severity: Medium (requires workaround for most interactions)

### Notes
- Login credentials shown on the login page itself: `Username: practice` / `Password: SuperSecretPassword!`
- `eval 'document.querySelector("button[type=submit]").click()'` is the reliable pattern for submit buttons on this site
- Site has Swagger API docs; `/inputs` page is clean and fully testable without ad interference
- `input[type=date]` on inputs page: `vibium fill` fails — use `eval .value = "YYYY-MM-DD"`

---

## Practice Test Report: Coffee Cart
URL: https://coffee-cart.app/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~1s

### Structure
- Navigation: Menu, Cart, GitHub (top nav)
- Products: 9 drinks — Espresso ($10), Espresso Macchiato ($12), Cappuccino ($19), Mocha ($8), Flat White ($18), Americano ($7), Cafe Latte ($16), Espresso Con Panna ($14), Cafe Breve ($15)
- Interactive elements: 4 via `vibium map` on menu page (nav + checkout button); product cards not in map

### Navigation
[PASS] Menu → `/` (product listing)  
[PASS] Cart → `/cart` (cart table with quantity controls)

### Core Functionality
[PASS] Add to cart — product cards are `div[data-test=ProductName]`; click via `eval getBoundingClientRect()` + `vibium mouse click x y`  
[PASS] Cart page — items shown with unit price × qty; `+`/`-`/`×` buttons all in `vibium map` and clickable  
[PASS] Quantity increment/decrement — total updates correctly  
[PASS] Remove all (×) — item removed, total recalculates  
[PASS] Proceed to checkout — opens payment modal (Name, Email, promo checkbox)  
[PASS] Empty checkout submit — HTML5 validation fires ("Please fill out this field.")  
[PASS] Valid checkout submit — "Thanks for your purchase. Please check your email for payment." shown; cart resets to 0  
[PASS] Promo checkbox — `vibium check` works correctly  

### Bugs Found
None.

### Notes
- Product cards are Vue components rendered as `div[data-test="ProductName"]` — not exposed in `vibium map`
- Pattern: `vibium eval 'JSON.stringify(document.querySelector("[data-test=ProductName]").getBoundingClientRect())'` → `vibium mouse click x y`
- Cart page is the best-mapped page — all controls appear in `vibium map` with descriptive `aria-label` values ("Add one Espresso", "Remove one Mocha", etc.)
- Full purchase flow confirmed end-to-end with cart reset after order

---

## Session: 2026-05-10 — Batch 6 (sites 26–30)

---

## Practice Test Report: Automation Bookstore
URL: https://automationbookstore.dev/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: None (single page, no nav)
- Forms: 1 (search/filter input)
- Interactive elements: 10 (search input + 8 book links)

### Navigation
[N/A] Single-page app with no navigation

### Core Functionality
[PASS] Filter by keyword ("selenium") — shows matching books in real time, case-insensitive  
[PASS] Clear filter (via "Clear text" link) — restores full list  
[PASS] Filter with no match ("!!!") — displays empty list (no "no results" message shown)  
[PASS] Book links exist and are clickable — but all hrefs are `#`, no detail page navigation

### Bugs Found
1. **Book links are dead** — All 8 book `<a>` elements have `href="#"`, clicking them does nothing. No product detail page or external link. Severity: Medium
2. **No "no results" message** — Filtering to zero results shows a blank list with no feedback to the user. Severity: Low

### Notes
- Intentionally minimal site — filter is the only real interactive feature
- Case-insensitive search works correctly

---

## Practice Test Report: Automation Camp
URL: https://play2.automationcamp.ir/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: Contact, Home
- Forms: 2 (login form, main form)
- Interactive elements: 25 (alert button, double-click button, login, full form)

### Navigation
[PASS] Contact → `/contact.html`  
[PASS] Home → returns to index

### Core Functionality
[PASS] Double-click button — shows "Your Sample Double Click worked!" confirmation  
[PASS] Valid login (`test`/`test`) → navigates to `/login.html?uname=test&pwd=test` with "Login Successful :)"  
[PASS] Select dropdown — `vibium select` works with option value  
[PASS] Radio buttons — Male/Female/Other mutually exclusive  
[PASS] Drag and drop — pizza image drags into pizza box via CSS selectors (`[draggable=true]` → `[ondrop]`)  
[PASS] Form submission — submits GET request with all form field values in URL params  
[BUG] Alert button deadlocks daemon — `eval` override of `window.alert` does not prevent BiDi deadlock  
[BUG] Invalid login also triggers alert — same deadlock; daemon restart required  
[BUG] `input[type=date]` not fillable via `vibium fill` — use `eval .value =`

### Bugs Found
1. **Alert button deadlocks vibium daemon** — Native `window.alert()` blocks BiDi even after `eval` override. Daemon must be killed and restarted. Severity: High
2. **Invalid login triggers alert dialog** — Wrong credentials fire `alert()` which also deadlocks daemon. Severity: High
3. **Date input not fillable via vibium fill** — `input[type=date]` reports "not editable". Severity: Low (workaround via eval)

### Notes
- Alert handling is the main obstacle; pre-stubbing `window.alert` via eval does not work on this site
- Form submits as GET with all values visible in URL — useful for verifying field state

---

## Practice Test Report: Applitools Demo
URL: https://demo.applitools.com/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: Login page → dashboard
- Forms: 1 (login form)
- Interactive elements: 8 on login; ~17 on dashboard

### Navigation
[PASS] Login → `/app.html` (dashboard)  
[PASS] Sidebar links present but no navigation — all resolve to `app.html#`

### Core Functionality
[PASS] Login with empty credentials → bypasses auth, lands on dashboard (intentional demo behavior)  
[PASS] Login with any credentials → same dashboard, no validation  
[PASS] Search bar — accepts input but does not filter transaction list  
[PASS] Recent Transactions table — 6 rows with status, date, description, category, amount

### Bugs Found
1. **Total Balance displays `$350%7`** — corrupted value; intentional visual regression bug. Severity: High (intentional)
2. **No authentication validation** — login accepts any input including empty. Severity: Medium (intentional)
3. **Search bar non-functional** — typing has no effect on transactions shown. Severity: Medium
4. **All action links are dead** — Make Payment, View Statement, Add Account, Request Increase, Pay Now all go to `app.html#`. Severity: Low (intentional demo limitation)
5. **Transaction timestamps malformed** — "Today1:52am", "Jan 23rd2:7pm" — missing space separator. Severity: Low (intentional visual bug)

### Notes
- Site is designed for visual testing with Applitools; bugs are intentionally planted for visual diff detection
- `$350%7` is a classic intentional visual bug (bad format string)

---

## Practice Test Report: Automation Exercise
URL: https://www.automationexercise.com/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~3s (ad overlay present on load)

### Structure
- Navigation: Home, Products, Cart, Signup/Login, Test Cases, API Testing, Video Tutorials, Contact us
- Forms: 1 (newsletter email)
- Interactive elements: 70+ (products, category filters, newsletter)

### Navigation
[PASS] Products → `/products` — full product catalog  
[PASS] Product search ("jeans") — 3 results: Soft Stretch Jeans, Regular Fit Straight Jeans, Grunt Blue Slim Fit Jeans  
[PASS] View Product → `/product_details/N` — detail page with name, category, price, availability, brand, quantity selector  
[BUG] Products nav on homepage → ad redirect to `/#google_vignette`; use direct URL navigation

### Core Functionality
[PASS] Add to cart (qty=2) — "Added! Your product has been added to cart." modal  
[PASS] View Cart → `/view_cart` — product shown with correct qty, price  
[PASS] Category filters (Women/Men/Kids) and brand filters (Polo, H&M, etc.) present and clickable

### Bugs Found
1. **Ad overlay intercepts nav clicks** — clicking Products nav on homepage triggers Google ad redirect. Workaround: direct URL navigation. Severity: High
2. **Ad iframe on every page load** — must dismiss "Close" SVG button before interacting. Severity: Medium

### Notes
- Full e-commerce flow (browse → detail → add to cart → view cart) works correctly
- Test cases at `/test_cases`, API list at `/api_list`
- Login required for checkout at `/login`

---

## Practice Test Report: Automation in Testing (Shady Meadows B&B)
URL: https://automationintesting.online/#/
Date: 2026-05-10

### Reachability
[PASS] Site loaded in ~3s

### Structure
- Navigation: Rooms, Booking, Amenities, Location, Contact, Admin
- Forms: 2 (availability checker, contact form)
- Interactive elements: 33

### Navigation
[PASS] Rooms → `#rooms` (scroll)  
[PASS] Booking → `#booking` (scroll)  
[PASS] Admin → `/admin` (separate panel)

### Core Functionality
[PASS] Check Availability — dates accepted (DD/MM/YYYY via fill); button requires `eval click()` after date entry (obscured by calendar)  
[PASS] Book now (Single room) → `/reservation/1?checkin=...&checkout=...`  
[PASS] Calendar date picker — click start/end dates; shows "£100 x 4 nights", total £440  
[PASS] Reserve Now form — fills Firstname, Lastname, Email, Phone; submits successfully  
[PASS] Booking Confirmed — "2026-05-31 - 2026-06-04" shown  
[PASS] Admin login (`admin`/`password`) → `/admin/rooms` — room list (101 Single, 102 Double, 103 Suite)  
[PASS] Admin Messages — shows 3 messages; test booking created "Jane Doe — You have a new booking!"  
[BUG] Contact form `#description` textarea — `vibium fill` fails; use `eval .value = "..." + dispatchEvent`  
[BUG] Check Availability button — "obscured" by calendar overlay after date entry; use `eval 'document.querySelector("#booking button").click()'`

### Bugs Found
1. **Textarea not fillable via `vibium fill`** — `#description` throws `fill:` error; React-aware eval + dispatchEvent workaround required. Severity: Low (vibium limitation)
2. **Check Availability button obscured** — calendar picker overlay blocks click; eval workaround works. Severity: Low

### Notes
- Full booking flow confirmed end-to-end with confirmation page
- Admin panel accessible with default credentials (`admin`/`password`)
- "Messages N" badge updates live after test bookings — good state verification anchor

---

## Session: 2026-04-27 — Batch 5 (sites 21–25)

---

## Practice Test Report: The Internet
URL: http://the-internet.herokuapp.com/
Date: 2026-04-27

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: 44 example links on homepage
- Forms: varies per example page
- Interactive elements: 1 link (Elemental Selenium) on homepage + 44 example links

### Navigation
[PASS] Checkboxes → /checkboxes (checkbox 1 unchecked by default, checkbox 2 checked)
[PASS] JavaScript Alerts → /javascript_alerts (alert/confirm/prompt all work with pre-stubbing)
[PASS] Form Authentication → /login (tomsmith / SuperSecretPassword! → /secure with flash message)
[PASS] Dropdown → /dropdown (option values "1"/"2"; `vibium select` works)
[PASS] Frames → /iframe (TinyMCE editor; see Bugs)
[PASS] Hovers → /hovers (CSS hover via `vibium mouse move x y`)
[PASS] Drag and Drop → /drag_and_drop (`vibium drag` swaps columns A/B correctly)
[PASS] Dynamic Controls → /dynamic_controls (Add/Remove and Enable/Disable work; `vibium wait text` catches async messages)
[PASS] Nested Frames → /nested_frames (`vibium frames` lists all 5 frames flatly)
[FAIL] Shadow DOM → /shadow_dom (404 Not Found)
[PASS] Horizontal Slider → /horizontal_slider (range input; see Bugs)
[PASS] Key Presses → /key_presses (letters, Enter, Tab detected correctly)
[PASS] Redirect Link → /redirector (redirects to /status_codes)
[PASS] Status Codes → /status_codes (200/301/404/500 pages all load with correct messages)
[PASS] File Upload → /upload (`vibium upload` + submit works)
[PASS] Sortable Tables → /tables (click header sorts asc; click again sorts desc)

### Core Functionality
| Action | Result |
|--------|--------|
| Checkbox check/uncheck | PASS — `vibium check`/`vibium uncheck` work |
| JS alert stub + click | PASS — stub via eval BEFORE click |
| Login with valid creds | PASS — redirects to /secure |
| Drag column A → B | PASS — columns swap to B, A |
| Remove/Add checkbox dynamically | PASS — `vibium wait text "It's gone!"` works |
| Enable/disable input dynamically | PASS — `vibium is enabled` returns correct state |
| Hover reveals figcaption | PASS — `vibium mouse move x y` triggers CSS :hover |
| TinyMCE iframe edit | PASS (eval only) — `eval + contentDocument.body.innerHTML` |
| Nested frame content access | PARTIAL — `vibium frame` context doesn't persist across invocations |
| Range slider | PASS (eval only) — `eval` + dispatch change/input events |
| Key press detection | PASS — `vibium press` captures all keys |
| File upload | PASS — `vibium upload` works |
| Table column sort | PASS — click `th` toggles asc/desc |

### Bugs Found
1. `vibium hover` fails on non-interactive elements (CSS-styled divs/images) — use `vibium mouse move x y` instead — Severity: Low (workaround exists)
2. `vibium frame` context doesn't persist between separate CLI invocations — each new vibium command resets to main frame — Severity: Medium (no workaround for interactive frame control; must use `eval + contentDocument`)
3. TinyMCE iframe has empty `src` (id=`mce_0_ifr`) — `vibium frames` shows `about:blank`, `vibium frame` can't match by name — Severity: Low (use `eval + contentDocument.body`)
4. `vibium fill` fails on `input[type=range]` with "not editable" error — Severity: Low (use eval + dispatchEvent)
5. `vibium check "#toggle-all"` fails with "obscured" — Severity: Low (click label by coordinates instead)
6. Shadow DOM page (/shadow_dom) returns 404 — site bug — Severity: Low

### Notes
- `vibium drag` works reliably for HTML5 drag-and-drop
- `vibium upload` + `vibium click submit` is the correct file upload pattern
- `vibium wait text "..."` reliably catches async DOM updates after button clicks

---

## Practice Test Report: The Random Number Service
URL: https://www.random.org/
Date: 2026-04-27

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: 8 top-level nav links (Home, Games, Numbers, Lists & More, Drawings, Web Tools, Statistics, Testimonials/Learn More/Login)
- Forms: search form on homepage; generator forms on sub-pages (Integer, String, etc.)
- Interactive elements: 81 total (nav links, cookie banner, generator links)

### Navigation
[PASS] Integers → /integers/ (loaded with generator form)
[PASS] Strings → /strings/ (loaded with string generator form)
[PASS] Nav links (Games, Numbers, etc.) work via `vibium click @eN` after `vibium map`

### Core Functionality
| Action | Result |
|--------|--------|
| Cookie banner | PASS — `vibium click "Allow All"` button (@e19) works |
| Integer generator (defaults) | PASS — 100 integers generated via URL params |
| Integer generator (negative range) | PASS — min=-100, max=100 works |
| Integer generator (min > max) | PASS — validation error shown |
| Integer generator (num > 10000) | PASS — validation error: must be in [1,10000] |
| Plain text format | PASS — `?format=plain` returns raw numbers |
| String generator | PASS — `?format=plain` returns 5 random strings |

### Bugs Found
None.

### Notes
- Generator forms are NOT found by `vibium map` — use URL parameters to submit (e.g. `?num=5&min=1&max=10&col=1&base=10&format=plain&rnd=new`)
- Inline `vibium eval` with semicolons fails due to shell quoting; use heredoc or URL-based params
- `vibium find text` + `vibium click` works for nav; `vibium map` only finds search input + cookie buttons on homepage

---

## Practice Test Report: Testing Challenges
URL: http://testingchallenges.thetestingmap.org/
Date: 2026-04-27

### Reachability
[FAIL] Site unreachable via Chrome/vibium — HTTP-only, no HTTPS

### Structure
N/A — site blocked by Chrome

### Navigation
N/A

### Core Functionality
N/A

### Bugs Found
N/A

### Notes
- `vibium go` fails with BiDi "unknown error" on http:// URL
- `eval + location.href` navigates but Chrome shows `chrome-error://chromewebdata/` (blank page)
- Site responds HTTP 200 via curl (PHP/Apache server) — accessible via CLI tools, blocked by Chrome's security policy for HTTP-only origins
- Cookie `TestingChallenge=You_have_checked_the_cookie_content._Add_oi32jnxd42390slk345_in_the_First_Name_field_to_mark_this_case.` is set — a hint challenge embedded in the response headers

---

## Practice Test Report: ToDo List
URL: https://todolist.james.am/#/
Date: 2026-04-27

### Reachability
[PASS] Site loaded in ~2s

### Structure
- Navigation: filter links (All, active, Completed)
- Forms: 1 input for adding todos
- Interactive elements: 1 text input, checkboxes per todo, Clear button, filter links

### Navigation
[PASS] All / active / Completed filters work via `vibium click`

### Core Functionality
| Action | Result |
|--------|--------|
| Add todo | PASS — `vibium fill` + Enter adds item |
| Add whitespace todo | PASS — silently rejected (no item created) |
| Mark todo complete | PASS — `vibium mouse click x y` on checkbox coords |
| Edit todo (dblclick) | PASS — `vibium dblclick label` opens edit; `vibium fill` + Enter saves |
| Delete todo | PASS — delete button clickable via `vibium click @eN` |
| Mark all complete | PASS — `vibium mouse click` on label coords (checkbox obscured) |
| Clear completed | PASS — `vibium click @eN` on Clear button |
| Filter: active | PASS — shows only unchecked items |
| Filter: completed | PASS — shows only checked items |
| Persistence | FAIL — no localStorage; todos lost on page reload |

### Bugs Found
1. Item counter off by 1 — shows `N-1` active items instead of `N` (e.g. "0 items left" with 1 active item) — Steps: add 1 todo, observe counter — Severity: Medium
2. Delete button title exposed as developer note `"TODO:REMOVE THIS EVENTUALLY"` — Severity: Low
3. Typo in placeholder: `"What need's to be done?"` (stray apostrophe) — Severity: Low
4. Typo in footer: `"Double-click to edit a toodo"` (double 'o') — Severity: Low

### Notes
- `vibium check`/`vibium uncheck` fail on todo checkboxes ("obscured by label") — use `vibium mouse click x y` with coords from `eval getBoundingClientRect()`
- AngularJS app; all state is in-memory only

---

## Practice Test Report: UI5 Demo Kit
URL: https://ui5.sap.com/#/demoapps
Date: 2026-04-27

### Reachability
[PASS] Site loaded in ~3s (needs 3s sleep after `wait load` before interacting)

### Structure
- Navigation: Home, Documentation, API Reference, Samples, Demo Apps, Resources
- Demo apps: 18+ demo apps listed (Shopping Cart, Browse Orders, Team Calendar, TypeScript Hello World, etc.)
- Interactive elements: 72 links + 45 buttons in DOM; `vibium map` returns "No interactive elements found" on main page

### Navigation
[PASS] `vibium find text "Samples"` + `vibium click` → navigates to /controls
[PASS] Direct URL navigation to demo app sub-pages works

### Core Functionality
| Action | Result |
|--------|--------|
| Main page `vibium map` | FAIL — returns "No interactive elements found" despite 72 links in DOM |
| Nav via `vibium find text` + click | PASS — works for top nav items |
| Open demo app (direct URL) | PASS — Shopping Cart, Team Calendar load correctly |
| Shopping Cart: `vibium map` | PASS — 37+ interactive elements found in sub-app |
| Shopping Cart: add to cart | PASS — `vibium click "Add to Shopping Cart"` works |
| Shopping Cart: open cart panel | PASS — cart shows item, price, Proceed button |
| Shopping Cart: search input | PASS — `vibium click` first, then `vibium fill` |
| Shopping Cart: search results | PASS (no match for "laptop" — expected) |

### Bugs Found
None in vibium behavior; site-level:
1. `vibium map` returns empty on main SAP UI5 SPA page — vibium doesn't detect UI5-rendered elements as interactive. Use `vibium find text` + click or direct URL navigation — Severity: Low (workaround: `vibium find text`)

### Notes
- `vibium map` works normally inside individual SAP UI5 demo apps (regular DOM rendering)
- Main Demo Kit page links accessible via `vibium eval 'document.querySelector("a[href*=...]")?.click()'` or by navigating directly to `test-resources/...` URLs
- `vibium find text "NavLabel"` is the recommended approach for top-nav interaction

---

## Session: 2026-04-27 — Batch 4 (5 sites)

---

### 16. QA Training Simulator
**URL:** https://bugeater.web.app/
**Type:** Gamified QA/BA/PM training platform (BugEater) — challenges across 7 test types

#### Reachability
[PASS] Site loaded in ~2s. Cookie banner on homepage + separate cookie banner on `/app/list`.

#### Structure
- Navigation (homepage): Home, Trails, Pricing, Demo, QA Game, Login
- Challenge list at `/app/list`: 23 challenges across 7 categories
  - Learn Mode (4): Number Addition, Division, Password Restore, Update Profile
  - Scripted Testing (5): Multiplication, Division, Password Validation, Create Profile, Currency Converter
  - Test Case Generator (2): Number Multiplication (Learn), Number Summation
  - Gherkin Scenarios (2): Number Subtraction (Learn), Number Summation
  - Functional Testing (2): Book Hotel, Todo List
  - API Testing (2, marked New): Testing Calculator API (Learn), Testing User API
  - Exploratory Testing (6): Calculator, Restore Password, Book a Desk, Division, Email Validation, Triangle
- Sidebar/drawer: hamburger @e1 opens Bootstrap offcanvas; react-joyride tutorial modal on first challenge visit

#### Navigation
[PASS] Demo nav → `/app/list` (challenge list loads correctly)
[PASS] learn/* and exploratory/* and gherkin/* routes load on direct URL
[FAIL] scripted/*, functional/*, api/*, testcase/* routes crash on direct URL — "Unexpected Application Error: Cannot read properties of undefined (reading 'pageTitle')"

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Navigate to challenge from `/app/list` | `vibium eval 'link.click()'` pattern works for all categories |
| PASS | `vibium fill` on React inputs | Fill works correctly — `vibium type` workaround not needed |
| PASS | Dismiss react-joyride tutorial (Skip) | `vibium click` on Skip button works; form usable after |
| PASS | Challenge 1.1 — Number Addition | Enter 1+2, Calculate → result "3" shown; step counter advances |
| BUG | Direct URL to scripted/functional/api/testcase routes | TypeError crash — "Cannot read properties of undefined (reading 'pageTitle')" |
| BUG | Sidebar close button via `vibium click @ref` | Fails with "timeout after 0s"; must use `vibium eval 'document.querySelector("button.btn-close")?.click()'` |

#### Bugs Found
1. **Direct URL crash for most challenge types** — `scripted/*`, `functional/*`, `api/*`, `testcase/*` routes crash with TypeError on direct load. Only `learn/*`, `exploratory/*`, `gherkin/*` survive. Steps: `vibium go https://bugeater.web.app/app/challenge/scripted/multiplication` — Severity: **High**
2. **Sidebar close button not clickable via ref** — `vibium click @eN` on the × button times out; `eval.click()` on `button.btn-close` works. — Severity: **Low** (vibium limitation)

#### Notes
- Site rebranded from "QA Training Simulator" to "BugEater" — challenge area unchanged
- Two separate cookie banners: one on landing page, one on `/app/list`; accept independently
- Test Case Generator is a new category (not present in earlier notes) — UI shows inline dropdowns to build test cases alongside the form under test
- `vibium fill` works on React controlled inputs — old note advising `vibium type` was stale

---

### 17. Random User Generator
**URL:** https://randomuser.me/
**Type:** API testing — random user data generation REST API

#### Reachability
[PASS] Site loaded in ~1s. Ads present but non-blocking.

#### Structure
- Navigation: Home, User Photos, Documentation, Change Log, Stats & Graphs, Donate, Copyright Notice, Photoshop Extension
- API endpoint: `/api/` returns JSON user object(s)
- Supported params: `results`, `gender`, `nat`, `seed`, `inc`, `exc`, `format`, `page`, `noinfo`

#### Navigation
[PASS] All nav links work via `vibium click` from homepage (old "broken links" note stale)
[PASS] User Photos → `/photos`, Documentation → `/documentation`, Change Log → `/changelog`, Stats → `/stats`

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | `/api/` base call | Returns 1 random user in JSON |
| PASS | `?results=5&gender=male&nat=us` | Returns 5 male US users correctly |
| PASS | `?seed=abc&results=3` | Returns same 3 users on repeated calls |
| PASS | `?inc=name,email` | Response contains only `name` and `email` fields |
| PASS | `?format=xml` | Returns valid XML user data |
| PASS | `?format=pretty` | Returns indented JSON |
| BUG | `?results=0` | Returns 1 result — silently ignores 0 |
| BUG | `?results=abc` | Returns 1 result — silently ignores invalid value |
| BUG | `?results=-1` | Returns 1 result — silently ignores negative |
| BUG | `?results=5001` | Returns 1 result — silently ignores above-max value |
| BUG | `?format=csv` | Triggers file download — crashes vibium BiDi session; daemon restart required |
| BUG | `?results=5000` + `vibium text` | "bufio.Scanner: token too long" — response too large for vibium's text buffer |

#### Bugs Found (API edge cases)
1. **Invalid `results` values silently default to 1** — `0`, negative, `abc`, and above-max (5001) all return exactly 1 result with no error. Steps: `vibium go "https://randomuser.me/api/?results=0"` → `info.results=1`. — Severity: **Medium**
2. **`?format=csv` crashes vibium daemon** — triggers browser file download dialog; vibium BiDi connection breaks. Steps: `vibium go "https://randomuser.me/api/?format=csv"` → BiDi error; run `vibium daemon stop && vibium daemon start` to recover. — Severity: **Medium** (vibium limitation)
3. **`vibium text` buffer overflow on max results** — `?results=5000` response too large; `vibium text` throws "bufio.Scanner: token too long". Use `vibium eval 'JSON.parse(document.body.innerText)'` instead. — Severity: **Low** (vibium limitation)

#### Notes
- Nav links work via `vibium click` — previous note about broken links is no longer valid
- `?inc` and `?exc` for field filtering work correctly
- For large API responses, use `vibium eval 'JSON.parse(document.body.innerText).info.results'` — more reliable than `vibium text`

---

### 18. Real World Example Apps
**URL:** https://codebase.show/projects/realworld
**Type:** Directory of RealWorld Conduit implementations — same app in 100+ frameworks

#### Reachability
[PASS] Page shell loads immediately; content renders ~3s after `wait load` (SvelteKit hydration). Taking a screenshot immediately after `wait load` shows a blank/black page.

#### Structure
- Navigation: Create (→ docs), Submit (→ GitHub OAuth), Sign in (→ GitHub OAuth)
- Filter tabs: Frontend, Backend, Fullstack
- Language filters: TypeScript, JavaScript, Kotlin, ClojureScript, Elm, PureScript, Rust, C#, Dart, Mint, Swift, ReScript, Android Native
- Implementation list: 100+ rows with framework name, repo link, and language tag

#### Navigation
[PASS] Frontend/Backend/Fullstack tabs filter list correctly via `vibium click`
[PASS] Language filter links work via `vibium click`
[PASS] Sign in → redirects to GitHub OAuth (`github.com/login?client_id=...`)
[PASS] Submit → redirects to GitHub OAuth with redirect back to `/projects/realworld/implementations/submit`
[NOTE] Old note about "Sign in/Submit reload page instead of redirecting" — no longer accurate; both correctly redirect to GitHub OAuth

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Page renders after 3s sleep | Full implementation list visible with language tags |
| PASS | Backend tab | URL becomes `?category=backend`; list filters to backend implementations |
| PASS | Language filter | URL gains `&language=java`; list filters correctly |
| PASS | Sign in link | Navigates to GitHub OAuth flow |
| BUG | Screenshot immediately after `wait load` | Blank/black page — content not yet rendered |

#### Bugs Found
1. **Page appears blank immediately after `wait load`** — SvelteKit hydration takes ~3s after DOM ready. Screenshotting without a sleep shows a black page. Steps: `vibium go url && vibium wait load && vibium screenshot` → black image. Workaround: `vibium sleep 3000`. — Severity: **Low** (SPA hydration timing)

#### Notes
- Always add `vibium sleep 3000` after `wait load` before mapping or interacting
- After `vibium back` from GitHub OAuth, sleep 3s again before interacting — SPA re-hydrates
- `vibium back` navigation works; `wait load` + `sleep 3000` is sufficient to restore the page
- Requires GitHub account for Sign in and Submit — no public demo credentials exist

---

### 19. The Boozang Test Lab
**URL:** https://thelab.boozang.com/
**Type:** React SPA — 16 automation practice challenges across 8 categories

#### Reachability
[PASS] Site loaded in ~1s.

#### Structure
- Menu (hamburger): Getting Started (Home, Introduction, Overview), Timing (Speed Game, Wait Game), Conditional Logic (Yellow or Blue, Cat or Dog), Lists/Forms/Tables (Sorted List, Form Fill, Cat Shelter, Tables), Bug Reporting (Visual Bugs), DOM Changes (Scramble Items), Using Data (Concat Strings), Games (Collecting Kittens, Canvas Game)
- Total: 16 challenges
- All routes accessible via direct URL (e.g. `/formFill`, `/sortedList`, `/yellowOrBlue`)

#### Navigation
[PASS] Hamburger menu (@e1) opens correctly via `vibium click`
[PASS] All 16 challenge links in sidebar navigate correctly
[PASS] Direct URL navigation works for all routes

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | Form Fill — valid submit | All 4 fields filled → "Data saved to DB" confirmation shown |
| PASS | Form Fill — empty submit | Browser HTML5 validation tooltip on first empty required field |
| PASS | Sorted List — delete item | `vibium click @eN` on Delete todo works correctly |
| PASS | Sorted List — add item | `vibium fill` + `vibium click` on Add todo works correctly |
| PASS | Yellow or Blue — Generate Color | `vibium click @e3` works; shows color buttons |
| PASS | Yellow or Blue — color choice | `vibium click @e4/5` works; shows "Try again!" or success |
| NOTE | `#engines` select | Does not exist on any challenge page — old note is stale |

#### Bugs Found
None — all previously documented automation limitations are resolved.

#### Notes
- `vibium click` works on all buttons — old note about needing `eval.click()` is no longer accurate
- Form Fill now has `required=true` on all 4 fields (firstname, lastname, email, password) — old note about "no required field validation" is stale
- `#engines` select no longer exists anywhere in the site — the old `vibium select` note for it is stale
- Form Fill saves to shared DB at `api.boozang.com/users` — data from test runs persists; avoid PII
- `vibium fill` works correctly on all input fields

---

### 20. The iframe Search Engine
**URL:** https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html
**Type:** Vanilla JS search tool — practice site for iframe, select, and search button testing

#### Reachability
[PASS] Site loaded. Note: old URL `http://compendiumdev.co.uk/apps/iframe-search/iframe-search.html` now redirects here.

#### Structure
- Controls: engine select dropdown (16 options), search text input, Search button, Go search link
- Engines: bing.com (default), dogpile, baidu.com, duckduckgo.com, wolframalpha, info.com, hotbot.com, Gigablast.com, WebCrawler.com, uk.ask.com, ask.com, aol.co.uk, aol.com, yahoo.com, google.com, google.co.uk
- Iframe: full-page below controls; displays search results

#### Navigation
[PASS] Index, Apps, Games nav links in header navigate correctly

#### Core Functionality
| Result | Action | Observation |
|--------|--------|-------------|
| PASS | `vibium fill` on search input | Works correctly; `vibium type` not needed |
| PASS | `vibium click @e6` (Search button) | Works directly — iframe loads Bing results |
| PASS | `vibium select` with full URL value | `vibium select @e4 "https://www.google.com/search?q="` correctly selects Google |
| PASS | Bing search in iframe | Loads and renders correctly |
| FAIL | Google in iframe | Blocked — iframe shows broken page icon (X-Frame-Options) |
| FAIL | DuckDuckGo in iframe | Blocked — same broken page icon |
| BUG | `vibium select` with non-existent value | Reports "Selected value" success but sets `selectedIndex=-1`, value=`""` — silently broken (B5) |
| BUG | "Go search" href stale until Search clicked | `Go search` link href reflects last triggered search, not current input state |
| NOTE | "Go search" link | Opens search in a **new browser tab**, not in the iframe |

#### Bugs Found
1. **`vibium select` silently fails on non-existent option value** — Reports "Selected value" success but `selectedIndex` becomes -1 and actual value is empty string. Steps: `vibium select @e4 "nonexistent"` → `vibium eval 'document.querySelector("#engines").selectedIndex'` → `-1`. — Severity: **Medium** (B5 confirmed)
2. **Google/DuckDuckGo block iframe embedding** — Both return `X-Frame-Options: SAMEORIGIN` or equivalent; iframe renders as broken page. Steps: select google.com, search, wait 2s → blank grey iframe with broken-page icon. — Severity: **Low** (by design, not a site bug)
3. **"Go search" href only updates after clicking Search** — Changing the select or typing in the input does not update the `Go search` link. Steps: change select to Bing, type "abc", check `Go search` href — still shows previous search URL. Must click Search first. — Severity: **Low**

#### Notes
- **URL has moved** — `http://compendiumdev.co.uk/apps/iframe-search/iframe-search.html` redirects to `https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html`; update any bookmarks
- `vibium click @e6` now fires the Search button correctly — old note about needing `vibium eval 'searchTool.changeUrlFromForm()'` is stale
- `vibium select` requires the full URL as the option value — use `"https://www.google.com/search?q="` not `"google.com"`
- `searchTool.changeUrlFromForm()` is still useful for updating the `Go search` href without triggering iframe navigation
- "Go search" opens a new tab (`window.open`) — use `vibium page close 1` to dismiss it

---

## Session: 2026-04-22/25 — Batch 3 (5 sites — 4 complete, #14 checkout blocked)

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

### 14. PrestaShop
**URL:** https://demo.prestashop.com/ → inner store `{subdomain}.demo.prestashop.com/en/`
**Type:** PrestaShop e-commerce demo (wrapped in iframe)

#### Reachability
[PASS] Outer wrapper loaded; inner store URL obtained via `eval 'document.querySelector("#framelive")?.src'` after 5s wait

#### Structure
- Navigation: Clothes (→/3-clothes), Accessories (→/6-accessories), Art; Sign in, Contact us; Language selector (45 languages)
- Products: Hummingbird t-shirt (€22.94/€28.68 regular), Brown bear sweater, 2x Framed posters; qty controls on homepage cards
- Interactive elements: 80 on homepage, 50 on product detail page
- Forms: 1 per product (`id="add-to-cart-or-refresh"`, `action="/cart"`)

#### Core Functionality
| Action | Result | Notes |
|--------|--------|-------|
| Product listing (homepage) | PASS | 4 featured products visible with names and prices |
| Product detail — Hummingbird t-shirt | PASS | Name, price (€22.94 sale / €28.68 regular), Size select (S/M/L/XL), Color radios (White/Black) |
| Add to cart — product detail | BUG | Button disabled after PS JS init; vibium click via ref succeeds but cart stays at 0 |
| Add to cart — homepage cards | BUG | Same — button disabled; click registered but no cart update |
| Cart page (empty) | PASS | "There are no more items in your cart" correct empty state shown |
| Checkout (`/en/order` with empty cart) | BLOCKED | Redirects to `/cart?action=show` — cannot reach checkout form |
| Direct AJAX POST to `/cart` | BUG | Returns HTML error page, not JSON — cart API blocked |

#### Bugs Found
1. **Add to cart permanently disabled** — `[data-button-action=add-to-cart]` shows `disabled=false` briefly on load, then becomes `disabled=true` after PS JS initializes. Affects all add-to-cart buttons site-wide (product detail + homepage cards). — Severity: **Critical**
2. **Checkout form untestable** — add to cart is broken so cart is always empty; `/en/order` redirects to empty cart. — Severity: **High** (blocked by bug #1)

#### Notes
- Subdomains expire in ~2 min of active testing (shorter than the 2–5 min estimate)
- `vibium go` to any subdomain page deadlocks the daemon (B3 pattern) — use `vibium eval 'location.href = "..."'` + `vibium wait load` for all in-store navigation
- Product URLs: `/{subdomain}/1-1-hummingbird-printed-t-shirt.html`, `/2-9-brown-bear-printed-sweater.html`
- Variant selectors: Size = `#input_1_1` (`name="group[1]"`, values 1–4 for S/M/L/XL); Color = `input[name="group[2]"]` (val=8 White, val=11 Black)
- `document.querySelector('form#add-to-cart-or-refresh').submit()` navigates to cart but cart remains empty
- This site is also documented in `/cart-patrol` skill with complete flow scripts

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

---

## Batch 8 — 2026-05-18

Sites 36–40: Commit Quality, Contact List App, Demo SaaS, GreenKart, Global SQA Demo

---

### Site 36 — Commit Quality
URL: https://commitquality.com/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s

#### Structure
- Navigation: Products, Login nav links + Practice Card section links (Add Product, Practice Testing, etc.)
- Forms: Product filter form (search, category dropdown, date range, stock toggle), Login form, Add Product form
- Interactive elements: 20+

#### Navigation
[PASS] Products → `/products` — product listing with filters
[PASS] Login → `/login` — login form renders
[PASS] Practice cards → each links to a dedicated practice section

#### Core Functionality
[PASS] Product filter — keyword search filters list in real time
[PASS] Category dropdown filter — filters by category
[PASS] In-stock toggle — filters to in-stock products
[PASS] Reset filters — clears all filter state
[PASS] Show More / pagination — loads additional products
[PASS] Login form — shows error on invalid credentials
[PASS] Add Product form — validates required fields; submits successfully with valid data
[BUG] Date filter (`input[type=date]`) — not fillable via `vibium fill` ("not editable"); requires `vibium type` workaround on fresh field; React state does not update from DOM setter alone
[BUG] Date "must not be in the future" validation — using today's date (2026-05-18) rejected; past dates (e.g. 2024-01-15) required

#### Bugs Found
1. **Date input not fillable via `vibium fill`** — React-controlled `input[type=date]` rejects fill. `vibium type` works on a fresh field only (accumulates on repeat). — Steps: navigate to Products, click date field, `vibium fill @eN "01/15/2024"` → "not editable" error. Severity: **Low** (automation-only issue)
2. **Today's date rejected in date filter** — Entering current date returns "must not be in the future" validation error. — Severity: **Low** (possibly intentional)

#### Notes
- Login credentials not publicly documented; login form shows validation errors correctly
- `vibium type` is the workaround for React date inputs — use a past date value
- Product listing and filter functionality is well-built; good for practicing filter automation

---

### Site 37 — Contact List App
URL: https://thinking-tester-contact-list.herokuapp.com/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s (Heroku, may be slow after idle)

#### Structure
- Navigation: Login, Sign Up links; Contact table with Add/Edit/Delete actions
- Forms: Login, Register, Add Contact, Edit Contact
- Interactive elements: Table rows, action buttons, form inputs

#### Navigation
[PASS] Sign Up → `/addUser` — registration form with firstName, lastName, email, password
[PASS] Login → redirects to `/contactList` on success
[PASS] Add Contact → `/addContact` — contact form with all fields

#### Core Functionality
[PASS] Register new user — form submits and creates account
[PASS] Login with valid credentials — redirects to contact list
[PASS] Login with invalid credentials — "Incorrect username or password" message
[PASS] Add contact — all fields (name, DOB, email, phone, address, city, state/province, postal code, country) accepted
[PASS] View contact detail — click contact row opens detail view
[PASS] Edit contact — Edit button opens form; fields updatable via eval (form renders without placeholders after edit click)
[PASS] Delete contact — deletes successfully; requires `vibium eval 'window.confirm = () => true'` pre-stub to avoid dialog block
[PASS] Logout — returns to login page

#### Bugs Found
None found — all CRUD operations functional.

#### Notes
- Edit form inputs have no placeholder text — `vibium fill "input[placeholder='...']"` fails; use index-based eval: `document.querySelectorAll("input")[N].value = "..."` + dispatchEvent
- Delete triggers `window.confirm` dialog — pre-stub with `vibium eval 'window.confirm = () => true'` before clicking Delete
- Registration creates a persistent account (Heroku app, not reset between sessions)
- Test credentials from registration persist; good site for full CRUD practice

---

### Site 38 — Demo SaaS
URL: https://demo-saas.bugbug.io/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s

#### Structure
- Navigation: Login, Sign Up links; marketing landing page
- Forms: Sign Up (name, email, password), Login (email, password), Forgot Password
- Interactive elements: 10 (nav links, form inputs, submit buttons)

#### Navigation
[PASS] Sign Up → signup form renders
[PASS] Login → login form renders
[PASS] Forgot Password → password reset form renders

#### Core Functionality
[PASS] Sign Up empty submit — shows "This field is required" validation on all fields
[PASS] Sign Up invalid email — shows email format validation error
[PASS] Login empty submit — shows validation errors
[PASS] Forgot Password empty submit — shows validation error
[FAIL] Dashboard — requires email verification after signup; dashboard not accessible without completing email verification flow
[SKIP] Authenticated features — not testable without real email access

#### Bugs Found
None found in accessible flows.

#### Notes
- Email verification is required to access the dashboard — blocks testing of all authenticated features
- Validation messages are clear and properly triggered
- Site is React/SPA; all forms found by `vibium map`; no dialog interception issues

---

### Site 39 — GreenKart
URL: https://rahulshettyacademy.com/seleniumPractise/#/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s

#### Structure
- Navigation: Top Deals (`#/offers`), Flight Booking (external link)
- Product grid: 12+ vegetables/fruits with qty controls and ADD TO CART
- Cart: `#/cart` — table with qty controls, promo code input, summary, Place Order
- Scrolling ticker banner at top (impacts nearby button clicks)

#### Navigation
[PASS] Home (`#/`) — product grid loads
[PASS] Top Deals (`#/offers`) — sortable/paginated/searchable table
[NOTE] Top Deals nav click intercepted by ticker banner — must navigate via `vibium eval 'location.href="...#/offers"'`; `vibium click @eN` clicks ticker instead

#### Core Functionality
[PASS] Search — `vibium press Enter "input[type=search]"` filters products (NOT button click — ticker banner blocks)
[PASS] Add to cart — requires `vibium scroll "into-view"` before click (zero-size issue)
[PASS] Proceed to Checkout — use `vibium eval '[...document.querySelectorAll("button")].find(b=>b.textContent.includes("PROCEED"))?.click()'` (ticker intercepts `vibium find text`)
[PASS] Cart table — shows product, qty, price, total correctly
[PASS] Qty controls in cart (+ / –) — adjust quantity and update total
[PASS] Place Order → country selection page (`#/country`)
[PASS] Country dropdown — 200+ countries, select works
[PASS] T&C checkbox → Proceed — completes order; "Thank you, your order has been placed successfully"
[PASS] Top Deals table — search filter, page size selector, pagination, column sorting all work
[BUG] Promo code — no visual feedback on invalid code; discount stays 0%, no error message shown
[BUG] "Quantiry" typo in cart table header (column header reads "Quantiry" instead of "Quantity")
[BUG] Rice discount price (46) higher than regular price (37) on Top Deals page — discount column value is incorrect

#### Bugs Found
1. **"Quantiry" typo in cart table header** — Column header `<th>` reads "Quantiry" instead of "Quantity". — Severity: **Low**
2. **Promo code silent failure** — Entering any invalid promo code and clicking Apply shows no error message; discount stays at 0% with no feedback. — Severity: **Medium**
3. **Rice discount price > regular price on Top Deals** — Wheat: 67→28, Tomato: 37→26, Rice: 37→**46** (discount is higher than original). — Severity: **Medium**

#### Notes
- Ticker banner (`scrolling` element) intercepts clicks on nearby buttons — use eval-based navigation and button clicks throughout
- ADD TO CART requires scroll-into-view before click due to zero-size detection
- Cart item count = unique products, not total units
- `vibium drag` with `@ref` targets fails ("timeout after 0s") — use coordinate-based drag: `vibium mouse move X Y && vibium mouse down && vibium mouse move X2 Y2 && vibium mouse up`

---

### Site 40 — Global SQA Demo
URL: http://www.globalsqa.com/demo-site/ (redirects to HTTPS)
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s — HTTP URL auto-redirects to HTTPS (no Chrome block unlike Testing Challenges)

#### Structure
- Navigation: Main nav (About, CheatSheets, etc.) + component grid links (Tabs, Slider, AlertBox, DialogBox, etc.)
- Components: 16+ demo widgets across 4 tiers (First Step through Last Step)
- Projects: AngularJS Site, E-Commerce Site, Photography Site
- Interactive elements: 47+ (mostly nav links, no complex controls on landing page)

#### Navigation
[PASS] Accordion and Tabs → `/demo-site/accordion-and-tabs/`
[PASS] DropDown → `/demo-site/select-dropdown-menu/`
[PASS] AlertBox → `/demo-site/alertbox/`
[PASS] Drag and Drop → `/demo-site/draganddrop/`
[PASS] AngularJS Protractor Practice Site → `/angularjs-protractor-practice-site/`
[BUG] All component nav links on main page intercept to `#google_vignette` (ad redirect) — must navigate to sub-page URLs directly

#### Core Functionality
[PASS] Accordion (Simple) — jQuery accordion: click section header expands content, collapses previous — tested at `/demoSite/practice/accordion/collapsible.html`
[PASS] DropDown — HTML `<select>` with 249 countries; `vibium select` works
[PASS] AlertBox (Simple) — `myFunctionTab1()` fires `alert("Welcome to GlobalSQA...")` — captured via `window.alert` override
[PASS] Drag and Drop — photo-manager demo: coordinate-based drag moves image to trash; delete icon click also removes from gallery
[BUG] Confirmation Box (`myFunctionTab2()`) — calling directly via `vibium eval` throws "script exception"; native `confirm()` dialog cannot be called from eval context even after `window.confirm` override
[NOTE] All demo widgets are embedded in iframes — navigate to iframe URL directly (e.g. `/demoSite/practice/accordion/collapsible.html`) rather than trying to use `vibium frame` (frame context doesn't persist in CLI)
[NOTE] E-CommerceSite link on demo landing page points back to the same page (`/demo-site/`) — appears to be a dead/placeholder link

#### Bugs Found
1. **Ad redirect on all nav link clicks from main page** — clicking any component link (Tabs, Slider, etc.) navigates to `#google_vignette` instead of the target page. Workaround: navigate directly to sub-page URL. — Severity: **Medium**
2. **E-CommerceSite link is broken** — points to the same demo landing page, not an e-commerce site. — Severity: **Low**
3. **`myFunctionTab2()` (Confirmation Box) blocked in eval** — native `confirm()` dialog throws "script exception" when called via `vibium eval`, even after `window.confirm` override. `window.alert` override works correctly for simple alerts. — Severity: **Low** (automation-only limitation)

#### Notes
- HTTP-only URL redirects to HTTPS automatically — Chrome does NOT block this site (unlike testingchallenges.thetestingmap.org)
- All demo widgets are in iframes — use `vibium frames` to find iframe URL, then navigate there directly
- `vibium frame <url>` doesn't actually switch eval/click context in CLI — navigate to iframe URL instead
- Drag using `vibium drag @src @target` fails with "timeout" when target is non-interactive — use `vibium mouse move/down/up` with coordinates
- AngularJS Protractor Practice Site at `/angularjs-protractor-practice-site/` is a separate companion site with ng elements for Protractor/Selenium practice

---

## Batch 9 — 2026-05-18

Sites 41–45: Hands-On Selenium WebDriver, Lambdatest Playground, Let Code, Locator Game, Practice Test Automation

---

### Site 41 — Hands-On Selenium WebDriver with Java
URL: https://bonigarcia.dev/selenium-webdriver-java/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s

#### Structure
- Navigation: Home page with 30 section links across 7 chapters (WebDriver Fundamentals, Browser-Agnostic, Browser-Specific, POM, Testing Framework, Third-Party)
- Forms: Web form, Login form, Slow calculator, Dialog boxes, and more
- Interactive elements: 31 links on homepage; each sub-page has its own elements

#### Navigation
[PASS] Web form → `/web-form.html` — full form with text, password, textarea, select, file, checkbox, radio, color, date, range
[PASS] Login form → `/login-form.html` — username/password + Submit
[PASS] Dialog boxes → `/dialog-boxes.html` — alert, confirm, prompt, modal
[PASS] Drag and drop → `/drag-and-drop.html` — jQuery UI draggable panel
[PASS] Slow calculator → `/slow-calculator.html` — configurable delay calculator

#### Core Functionality
[PASS] Web form submit — fills all fields and POSTs to `/submitted-form.html`; params visible in URL; "Form submitted / Received!" shown
[PASS] `vibium fill` works on text/password inputs; `vibium fill` fails on `textarea` — use `vibium type` instead
[PASS] Login with `user`/`user` → `/login-sucess.html` "Login successful"; empty submit → "Invalid credentials" (no page reload)
[PASS] Dialog boxes — alert/confirm/prompt fire correctly; modal opens and closes via Close button; pre-stub dialogs with eval before clicking
[PASS] Drag and drop — coordinate-based drag works: element moved from x:42 to x:370
[PASS] Slow calculator — buttons are `span.btn` (not `button`) — use eval find; 7+3=10 computed correctly after 1s delay

#### Bugs Found
None found.

#### Notes
- `vibium fill @ref` fails on `<textarea>` ("fill:") — use `vibium type @ref "text"` instead
- Calculator buttons are `span.btn`, not `button` — `vibium map` returns only 2 interactive elements; find buttons via `vibium eval '[...document.querySelectorAll("span.btn")].find(b=>b.textContent.trim()==="7")?.click()'`
- Login page slow to declare readyState 'complete' — `vibium wait load` may timeout but page is functional; add `sleep 3` before `vibium url`
- All 30 practice sub-pages at clean URLs (e.g. `/web-form.html`, `/drag-and-drop.html`) — no ad overlays, no login required

---

### Site 42 — Lambdatest Playground (ecommerce)
URL: https://ecommerce-playground.lambdatest.io/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~3s (OpenCart-based store)

#### Structure
- Navigation: Categories sidebar (Cameras, Phones, Software, Laptops, etc.), Quick Links (Special, Wishlist, Compare, My Account, Blog), Cart panel
- Products: Large catalog (75+ cameras alone); product detail pages with name, brand, price, availability, qty, Add to Cart
- Cart: Server-side session via AJAX (`window.cart.add()`)
- Forms: Login, Register, Review

#### Navigation
[PASS] Category pages via direct URL (e.g. `/index.php?route=product/category&path=33`) — render correctly
[PASS] Product detail at `/index.php?route=product/product&product_id=N`
[PASS] Cart page at `/index.php?route=checkout/cart`
[BUG] Category nav links on homepage intercepted by sticky header — `vibium click @eN` fails ("element is obscured"); use direct URL navigation

#### Core Functionality
[PASS] Product listing — category pages show products with name, price
[PASS] Product detail — name, brand, availability, price, qty, Add to Cart visible
[PASS] Registration — creates account; redirects to `/account/success` with "Your Account Has Been Created!"
[PASS] Login — shows "Warning: No match for E-Mail Address and/or Password." on invalid credentials
[PASS] Add to Cart (logged in, in-stock, no required options) — success toast: "You have added HP LP3065 to your shopping cart!"; cart counter updates
[FAIL] Add to Cart (not logged in) — silently fails; `window.cart.add()` and eval `.click()` both return without error but cart remains empty; requires login
[FAIL] Add to Cart on products with "Size" select (Canon EOS 5D, Nikon D300) — "Size required!" validation; size select only has "--- Please Select ---" (no actual options) — data issue, impossible to satisfy
[PASS] Out-of-stock products — show "OUT OF STOCK" button; can still be added to cart (appear in cart with `***` marker and warning banner)

#### Bugs Found
1. **Add to Cart silently fails for guests** — no error message shown; cart stays empty. No "please login" prompt. — Severity: **Medium**
2. **Size option select has no values** — Canon EOS 5D and similar products have "Size required!" validation but size select only contains "--- Please Select ---" with no values. Impossible to add these products to cart. — Severity: **High** (blocks core flow)
3. **Out-of-stock items addable to cart** — products marked "Out Of Stock" appear in cart with `***` and warning "Products marked with *** are not available in the desired quantity or not in stock!" — Severity: **Low** (intentional for practice)

#### Notes
- All nav links obscured by sticky header overlay — navigate all pages via direct URL
- Account registration creates a real account; use a throwaway email
- `vibium mouse click x y` at button coordinates works for in-stock Add to Cart; eval `.click()` also works
- `window.cart.add(productId, qty)` is the AJAX call; returns null but doesn't actually add if not logged in

---

### Site 43 — Let Code
URL: https://letcode.in/test
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s (Angular app)

#### Structure
- Navigation: Work-Space hub at `/test` with 22 section links (Input, Button, Dropdown, Alert, Frame, Radio, Window, Elements, Drag/Drop/Sort/Select/Slider, Waits, Table, Calendar, Forms, File, Shadow DOM, POM)
- Each section is a separate page at a clean URL (e.g. `/edit`, `/button`, `/dropdowns`)
- Interactive elements: 25+ on hub page; each sub-page has exercise-specific elements

#### Navigation
[PASS] Hub → direct URL navigation works for all sections
[PASS] `/edit` (Input) — text inputs, append-and-tab, pre-filled, disabled, readonly
[PASS] `/button` — Goto Home, Find Location, color/size query, disabled button
[PASS] `/dropdowns` — 4 selects (fruit, superheroes multi, language, country)
[PASS] `/table` — simple 5-row price table
[PASS] `/forms` (All in One) — full form with text, email, phone, address, DOB, gender radio, T&C checkbox, submit
[PASS] `/window` — Open Home Page, Multiple Windows buttons
[BUG] `/alert` page deadlocks vibium daemon on navigation — fires a native dialog on page load; daemon restart required

#### Core Functionality
[PASS] Input page — fill name, append text + press Tab, `getAttribute` returns pre-filled value, disabled=true, readOnly=true all confirmed
[PASS] Dropdown page — `vibium select @eN "value"` works for all 4 dropdowns
[PASS] Table page — `vibium text table` returns clean table data
[PASS] Forms submit — form submits (reloads page); no success message shown
[BUG] Alert page — navigating to `/alert` fires a native browser `confirm()` on page load, deadlocking the daemon (same pattern as sites that call `alert()` immediately); pre-stubbing via eval is not possible before load

#### Bugs Found
1. **`/alert` page deadlocks daemon on navigation** — native confirm dialog fires on load, cannot be pre-stubbed. — Steps: `vibium go "https://letcode.in/alert"` → daemon deadlocks; restart required. Severity: **Medium** (workaround: avoid this page or use MCP dialog_accept before navigating)

#### Notes
- All section links on the hub page redirect to `#google_vignette` (ad overlay) — navigate all sections via direct URL (e.g. `vibium go "https://letcode.in/edit"`)
- Ad iframes present on all pages but don't block main content
- Forms page submit reloads same page — no dedicated success page; `vibium wait load` timeout on POST redirect is normal (page reloads faster than listener catches)

---

### Site 44 — Locator Game
URL: https://testsmith-io.github.io/locator-game/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~1s (GitHub Pages, static)

#### Structure
- Navigation: None — single-page game with 13 levels (0–12)
- Controls: CSS/XPath selector toggle, locator input, Try! link, Submit button, Prev/Next navigation
- Tutorial overlay on first load (End tour button to dismiss)

#### Navigation
N/A — single page

#### Core Functionality
[PASS] Tutorial overlay dismisses via "End tour" button
[PASS] Level 0 (Select all titles) — CSS `h3` → Submit → advances to Level 1
[PASS] Level 1 (Select description text) — CSS `#description` → Submit → advances to Level 2
[PASS] Level 2 (Select active list item) — CSS `.active` → Submit → advances to Level 3
[PASS] Try! button — evaluates locator and highlights matched elements in Rendered HTML preview
[PASS] Prev/Next navigation — moves between levels

#### Bugs Found
None found.

#### Notes
- Submit with correct locator immediately advances to next level — no "correct!" confirmation message
- No penalty for wrong answers — incorrect locator just stays on same level
- 13 levels total (0–12); levels increase in complexity (element type → ID → class → nested → attribute selectors)
- CSS and XPath modes switchable via `vibium select @e2 "XPath"`
- Clean static site — no ads, no login, no network issues

---

### Site 45 — Practice Test Automation
URL: https://practicetestautomation.com/practice/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded in ~2s

#### Structure
- Navigation: Home, Practice, Courses, Blog, Contact + 3 practice cards (Test Login Page, Test Exceptions, Test Table)
- Forms: Login form; Exceptions page (add row); Table page (filter controls)
- Interactive elements: 12 on practice hub

#### Navigation
[PASS] Test Login Page → `/practice-test-login/` — username/password form with credentials shown on page
[PASS] Test Exceptions → `/practice-test-exceptions/` — food list with Add/Edit/Remove
[PASS] Test Table → `/practice-test-table/` — sortable/filterable course table

#### Core Functionality
[PASS] Login — invalid username → "Your username is invalid!"; valid username + wrong password → "Your password is invalid!"; valid `student`/`Password123` → `/logged-in-successfully/` "Congratulations student. You successfully logged in!"
[PASS] Exceptions — Row 1 pre-populated with "Pizza"; clicking Add dynamically adds Row 2 with Save/Remove buttons; `vibium map` updates to reflect new row
[PASS] Table filter — language radio (Java/Python) filters table rows correctly; Python shows 2 courses, Java shows 6
[PASS] Table sorting — `select` for sort column present; table is pre-sorted by ID

#### Bugs Found
None found.

#### Notes
- Login page declares readyState 'complete' slowly after successful submit — `vibium url` after click returns "BiDi unknown error"; add `sleep 5` before reading URL post-submit
- Valid login credentials displayed on the login page itself: `student`/`Password123`
- Exceptions page row 2 appears via delayed JS — Row 2 input has zero getBoundingClientRect height initially but `vibium map` detects it after the animation; use `sleep 2` after clicking Add
- Table language filter uses radio buttons (`name="lang"`); level filter uses checkboxes (`name="level"`)
- All 3 sub-pages at clean direct URLs — no ad overlays

---

## Batch 10 — 2026-05-18 (sites 46–50)

### Site 46 — QA Playground
URL: https://qaplayground.dev/
Date: 2026-05-18

#### Reachability
[PASS] Site loaded instantly; static HTML with 24 mini-apps listed

#### Structure
- Navigation: Home, Apps (anchor), GitHub test suite links per mini-app
- Forms: per-app (no global form)
- Interactive elements: 24 mini-app cards linking to `/apps/<name>/`

#### Navigation
[PASS] All mini-app URLs reachable via direct navigation (pattern: `/apps/<slug>/`)

#### Core Functionality (11 mini-apps sampled)
[PASS] Dynamic Table — `vibium text` finds table; Spider-Man row located by text match
[PASS] Verify Account — OTP input requires `vibium type`, not `vibium fill`; "Success" shown after correct code
[PASS] Tags Input Box — add/remove tags work via `vibium fill` + Enter
[PASS] Multi Level Dropdown — nested Animals submenu accessible; `vibium click` on items
[PASS] Budget Tracker — entry added, Total updates to $1,000.00
[PASS] Shadow DOM — `document.querySelector("progress-bar")?.shadowRoot?.querySelector("button")?.click()`; progress → 95%
[PASS] Covered Elements — hidden `#fugitive` link found by `vibium map`; click shows "Mission accomplished"
[PASS] Range Slider — use `eval s.value=50; dispatchEvent(input/change)`; "Send Feedback" shows after slider move (pre-stub alert); "Thank you for your feedback!" shown
[PASS] Onboarding Modal — CSS checkbox toggle (`#active`); set checked=true to open, false to close; title changes to "Application successfully launched! 🚀"
[PASS] Sortable List — direct DOM manipulation via eval: collect `.draggable` refs by name, reappend to `li[data-index]` in correct order; Check Order shows all 10 green
[PASS] New Tab — `vibium pages` lists new tab at `/apps/new-tab/new-page`; navigate directly for assertion

#### Bugs Found
None found.

#### Notes
- `vibium type` required for OTP inputs (Verify Account) — `vibium fill` doesn't trigger keyup events needed for code validation
- Sortable list drag-and-drop: `vibium drag` not needed; rearrange `.draggable` children in `#draggable-list li` elements via eval; correct order from source: Jeff Bezos, Bill Gates, Warren Buffett, Bernard Arnault, Carlos Slim Helu, Amancio Ortega, Larry Ellison, Mark Zuckerberg, Michael Bloomberg, Larry Page
- Range slider: `vibium fill` fails on `input[type=range]`; use `eval .value= + dispatchEvent(new Event("input"/{change}))` 
- New tab: `vibium switch N` doesn't exist in CLI; use `vibium go` to the new page URL directly
- `vibium find "text"` returns nil on most mini-apps — use `vibium map` for refs

---

### Site 47 — React Shopping Cart
URL: https://react-shopping-cart-67954.firebaseapp.com/
Date: 2026-05-18

#### Reachability
[PASS] Firebase-hosted React SPA loads instantly; 16 products displayed

#### Structure
- Navigation: none (single-page app)
- Filters: 7 size checkboxes (XS/S/M/ML/L/XL/XXL) in left sidebar
- Interactive elements: 16 "Add to cart" buttons, cart count button, size filter checkboxes

#### Navigation
[PASS] Single-page app; no route navigation

#### Core Functionality
[PASS] Size filter — `vibium check @eN` fails ("obscured"); use `eval document.querySelectorAll("input[type=checkbox]")[0].click()`; XS filter reduces 16 → 1 product
[PASS] Add to cart — `vibium click @eN` on "Add to cart" button; cart count increments (0 → 1)
[PASS] Cart drawer — clicking cart count button (@e42) opens right-side drawer; shows item name, price, quantity, subtotal
[PASS] Cart content — "Cropped Stay Groovy off white" $10.90; SUBTOTAL: $10.90; CHECKOUT button visible

#### Bugs Found
None found (frontend demo, no real checkout).

#### Notes
- Cart button ref is the last element in `vibium map` (shows count as text, e.g. "1")
- Size filter checkboxes are obscured — `vibium check` fails; use `eval .click()`
- No checkout flow beyond the button (frontend-only demo)
- Promo banner at top (recruiter ad) — not interactive

---

### Site 48 — Selectors Hub
URL: https://selectorshub.com/xpath-practice-page/
Date: 2026-05-18

#### Reachability
[PASS] WordPress site loads with sticky promo banner and countdown timer

#### Structure
- Navigation: Products, Pro Plans, Courses, Practice Page, Resources
- Forms: 1 Dummy Form (email, password, company, mobile, country, submit)
- Interactive elements: form fields, shadow DOM elements, iframe links, table, download/upload, alert buttons

#### Navigation
[PASS] Nav links work; sub-pages open in new tabs or scroll to sections

#### Core Functionality
[PASS] Dummy Form fill — email input has `readonly` attribute; remove via `eval document.querySelector("input[type=email]").removeAttribute("readonly")` first; then `vibium fill` works
[PASS] Form submit — `vibium click` on Submit button; `document.body.textContent.includes("success")` → true
[PASS] Shadow DOM — `#userName` element has open shadow root with username input, nested shadow DOM (`#app2`, `#concepts`); `#userPass` has closed shadow root (password input)
[PASS] Select dropdown — `#cars` select with 4 car options; `vibium select @e46 "saab"` works

#### Bugs Found
None found (practice site with intentional challenges).

#### Notes
- Email input is readonly by default (intentional XPath challenge) — remove attribute before filling
- Shadow DOM has both open and closed modes; closed mode requires storing shadowRoot reference before page initializes (cannot access via `querySelector().shadowRoot` after closed)
- Page includes: iframe inside shadow DOM, shadow DOM inside iframe, nested iframe scenarios
- All section links in the practice list work as direct URL anchors
- Countdown timer and promo overlay may interfere with clicks near top of page

---

### Site 49 — Selenium Playground
URL: https://www.lambdatest.com/selenium-playground/
Date: 2026-05-18

#### Reachability
[PASS] Main index page loads; lists 40+ demo categories
[FAIL] All demo sub-page links redirect to `testmuai.com` which blocks headless browsers with Cloudflare protection

#### Structure
- Navigation: 40+ demo links on index page
- Forms: none on index; all forms on inaccessible sub-pages
- Interactive elements: index links only

#### Navigation
[FAIL] All sub-page links (Ajax Form, Bootstrap Alerts, etc.) redirect to `www.testmuai.com` domain; Cloudflare bot protection returns "Performing security verification" indefinitely — not accessible to automation

#### Core Functionality
[FAIL] Cannot test any demo — sub-pages blocked by Cloudflare on testmuai.com

#### Bugs Found
None applicable (site inaccessible).

#### Notes
- Index page at lambdatest.com/selenium-playground/ loads fine
- All 40+ demo hrefs now point to `testmuai.com` (rebrand/migration); testmuai.com has Cloudflare bot protection that blocks headless Chrome permanently
- `eval location.href = "..."` navigation also blocked; Ray IDs increment confirming new requests blocked
- Site was previously testable on lambdatest.com — migration to testmuai.com broke automation access

---

### Site 50 — Swag Labs
URL: https://www.saucedemo.com/
Date: 2026-05-18

#### Reachability
[PASS] Site loads instantly; React SPA login page

#### Structure
- Navigation: login → inventory → product detail → cart → checkout → confirmation
- Forms: login (username/password), checkout step 1 (first name, last name, zip), checkout step 2 (overview)
- Interactive elements: login form, 6 product "Add to cart" buttons, sort dropdown, cart icon, checkout form

#### Navigation
[PASS] Login → /inventory.html
[PASS] Cart → /cart.html (via eval click on `.shopping_cart_container a`, not direct `vibium go`)
[PASS] Checkout → /checkout-step-one.html → /checkout-step-two.html → /checkout-complete.html

#### Core Functionality
[PASS] Standard user login — `standard_user` / `secret_sauce` → inventory page
[PASS] Locked out user — "Epic sadface: Sorry, this user has been locked out."
[PASS] Add to cart — `vibium click @eN` on "Add to cart"; button changes to "Remove"
[PASS] Sort by price — `vibium select @e2 "lohi"` → prices $7.99, $9.99, $15.99, $15.99, $29.99, $49.99 (ascending)
[PASS] Full checkout flow — name/last/zip → overview (SauceCard #31337, Free Pony Express Delivery) → Finish → "Thank you for your order!"
[BUG] Problem user — all 6 product images show same broken image (`sl-404.168b1cce10384b857a6f.jpg`) — intentional
[BUG] Problem user — Sort Z-A returns items in A-Z order (sort non-functional) — intentional

#### Bugs Found
1. `problem_user`: All product images replaced with same broken 404 image — Severity: High (intentional planted bug)
2. `problem_user`: Sort dropdown non-functional — selecting Z-A keeps items in A-Z order — Severity: Medium (intentional planted bug)

#### Notes
- Cart icon link has no `href` attribute and doesn't appear in `vibium map`; navigate via `eval document.querySelector(".shopping_cart_container a")?.click()`
- `vibium go "https://www.saucedemo.com/cart.html"` fails with BiDi unknown error after logout — use eval cart click from inventory page instead
- `vibium find "Finish"` returns nil — use `vibium map` to get button ref
- Side menu opened by "Open Menu" button; close via Logout/About/Reset App State links
- 6 user types: standard (fully functional), locked_out (blocked), problem (broken images + sort), performance_glitch (slow), error, visual (visual diffs)
- After daemon restart, refs expire — always `vibium map` before interacting

---

## Batch 11 — 2026-05-18 (sites 51–55)

### Site 51 — Sweet Shop
URL: https://sweetshop.netlify.app/
Date: 2026-05-18

#### Reachability
[PASS] Netlify static site loads instantly

#### Structure
- Navigation: Sweet Shop, Sweets, About, Login, Basket
- Forms: basket checkout form (billing address + payment), login form
- Interactive elements: "Add to Basket" links (homepage + /sweets), checkout form, login form

#### Navigation
[PASS] /sweets — 16 products listed
[PASS] /basket — basket with items, delivery options, billing form, payment form
[PASS] /login — email + password login form
[PASS] /about — "An intentionally broken web application to help demonstrate Chrome DevTools"

#### Core Functionality
[PASS] Add to Basket — basket count increments (0 → 1 → 2); `vibium map` does NOT show Add to Basket links (no `href`); use `vibium eval 'document.querySelector(".addItem").click()'` or `document.querySelector(".addItem[data-id=\"2\"]").click()`
[PASS] Basket page — shows item name, unit price, total (GBP); delivery radio (Collect FREE / Standard Shipping £1.99)
[PASS] Promo code field — shows "Please input a valid promo code." on submit with empty code (client-side validation)
[PASS] Checkout form — 0 validation errors when all fields filled correctly; form submits as GET to `/basket?` (no backend, page reloads)
[FAIL] Login form — submits with no visible success/error feedback (static demo, no backend)

#### Bugs Found
1. Two form inputs both have `id="name"` (First Name and Last Name fields) — `vibium map` shows only one of them; Last Name field never receives focus via `vibium fill @ref` — fill via `document.querySelectorAll("input#name")[1].value = "..."` — Severity: Medium (intentional practice challenge or page bug)
2. Delivery radio buttons obscured (`vibium check` fails) — use `eval document.querySelector("input[name=exampleRadios]").click()` — Severity: Low

#### Notes
- "Add to Basket" links use `data-id`, `data-name`, `data-price` attributes + JS click handler; no `href` — `vibium map` skips them
- Cart state persists across same-session navigation (localStorage)
- Checkout is a GET form — form data submitted as URL params, page reloads at `/basket?`; no confirmation page exists
- Login has no test credentials and no feedback — static frontend only
- About page explicitly states the app is intentionally broken for DevTools practice

---

### Site 52 — Tricentis Obstacle Course
URL: https://obstaclecourse.tricentis.com/Obstacles
Date: 2026-05-18

#### Reachability
[PASS] Site loads instantly; each visit shows a random obstacle

#### Structure
- Navigation: Home, Obstacle Course, Search
- Forms: answer input, date input, various obstacle-specific inputs
- Interactive elements: answer input, "try again" link, "next one" link, obstacle-specific controls

#### Navigation
[PASS] Home / Obstacle Course navigation works
[PASS] "next one" link available after each attempt; use `vibium eval 'document.querySelector("a[href*=next]").click()'` (vibium click @eN fails when page is scrolled)

#### Core Functionality
[PASS] Meeting Scheduler obstacle — `vibium fill @eN "Open"` + `vibium press "Enter"` answers and advances to next obstacle
[PASS] Confusing Dates obstacle — click calendar button to generate date; calculate first of second following month in ISO; `vibium fill` + click Done; "Good job!" modal confirms success
[PASS] Fun with Tables obstacle — `vibium map` finds Remove/Edit buttons; target correct row via `eval Array.from(document.querySelectorAll("table tr")).find(r=>...)?.querySelectorAll("button")[1]?.click()`; "Good job!" modal
[SKIP] Drag-and-drop obstacle (ToscaBot Can Fly) — mouse drag and HTML5 drag events both fail to trigger success; obstacle requires proprietary Tosca event handling

#### Bugs Found
None found (obstacle failures are expected automation challenges).

#### Notes
- Answer input `@e7` (resulttext) works with `vibium fill` + `vibium press "Enter"` for text-answer obstacles
- Success modal buttons ("Hit me with the next riddle!") obscured — use `vibium eval 'document.querySelector("button.btn-success").click()'`; if that fails too, reload and click "next one" link
- Drag obstacles: HTML5 DragEvent API and mouse events both fail — the site likely uses Tosca-specific drag handling that doesn't respond to standard browser events
- Obstacles are randomized on each page load — same URL always gives a different challenge
- Date calculation: `var d = new Date("M/D/YYYY"); d.setMonth(d.getMonth() + 2); d.setDate(1); d.toISOString().split("T")[0]`

---

### Site 53 — UI Test Automation Playground
URL: http://uitestingplayground.com/
Date: 2026-05-18

#### Reachability
[FAIL] HTTP-only site — Chrome blocks navigation via BiDi; `vibium go` returns "BiDi error: unknown error"; `eval location.href` navigates to `chrome-error://chromewebdata/`; accessible via curl (HTTP 200) but Chrome refuses completely

#### Structure
N/A — could not load in browser

#### Core Functionality
[FAIL] Cannot test — Chrome blocks HTTP-only origin

#### Bugs Found
None applicable (site inaccessible).

#### Notes
- Same pattern as Testing Challenges (testingchallenges.thetestingmap.org) — HTTP-only domains are blocked by Chrome's BiDi security model
- Site responds on port 80 (Microsoft-IIS/10.0 / Express) but has no HTTPS equivalent

---

### Site 54 — Weather Shopper
URL: https://weathershopper.pythonanywhere.com/
Date: 2026-05-18

#### Reachability
[PASS] PythonAnywhere-hosted site loads instantly

#### Structure
- Navigation: temperature display → moisturizers or sunscreens page → cart → Stripe checkout
- Forms: no login; product "Add" buttons; Stripe payment iframe
- Interactive elements: "Buy moisturizers" / "Buy sunscreens" buttons, "Add" buttons per product, cart button (navbar), "Pay with Card" (Stripe button)

#### Navigation
[PASS] /moisturizer — 6 moisturizer products with Add buttons
[PASS] /sunscreen — 6 sunscreen products with Add buttons
[PASS] /cart — shows items, total in Rupees, Stripe "Pay with Card" button

#### Core Functionality
[PASS] Temperature display (49°C shown) — determines which products to buy (>34°C = sunscreens)
[PASS] Add to cart — cart button updates count: "Cart - Empty" → "Cart - 2 item(s)"
[PASS] Cart page — correct items listed with prices; total calculated (Rupees 300)
[PASS] Pay with Card — opens Stripe TEST MODE modal (email + card number + MM/YY + CVC); shows "Pay INR ₹300.00"; `vibium frames` lists stripe_checkout_app iframe
[SKIP] Stripe payment submission — Stripe modal is cross-origin iframe (checkout.stripe.com); fields not fillable via CLI eval

#### Bugs Found
None found.

#### Notes
- Cart count button is `@e1` in vibium map; click it to navigate to /cart (not via direct URL)
- Stripe modal opens as a cross-origin iframe in the current page (not a new tab)
- Use Stripe test card 4242 4242 4242 4242, MM/YY 12/26, CVC 123 for manual testing
- Temperature is live from an external API — value changes each visit; both product pages accessible directly at /moisturizer and /sunscreen regardless of temperature

---

### Site 55 — XYZ Bank
URL: https://www.globalsqa.com/angularJs-protractor/BankingProject/
Date: 2026-05-18

#### Reachability
[PASS] AngularJS SPA loads at the login page (#/login)

#### Structure
- Navigation: Home, Customer Login, Bank Manager Login
- Customer flow: select customer → account dashboard → Deposit / Withdrawal / Transactions
- Manager flow: Add Customer / Open Account / Customers list

#### Navigation
[PASS] Customer Login → dropdown of 5 customers → Login → account page
[PASS] Bank Manager → Add Customer / Open Account / Customers tabs

#### Core Functionality
[PASS] Customer select — `vibium select @e2 "Harry Potter"` doesn't trigger AngularJS change binding; use `eval document.querySelector("#userSelect").value="2"; + dispatchEvent(new Event("change",{bubbles:true}))` to show Login button
[PASS] Deposit — fill amount + click Deposit; balance updates immediately; "Deposit Successful" message shown
[PASS] Withdrawal — balance decreases correctly (1000 → 750 after 250 withdrawal)
[PASS] Transactions — Credit/Debit entries visible with date-time, amount, type
[PASS] Add Customer (Manager) — pre-stub alert before clicking "Add Customer" submit; alert message: "Customer added successfully with customer id :N"
[PASS] Delete Customer — `eval Array.from(querySelectorAll("button")).find(b=>b.textContent.includes("Delete") && b.closest("tr")?.textContent.includes("Jane"))?.click()`; customer removed from list

#### Bugs Found
None found.

#### Notes
- `vibium select` on AngularJS `ng-model` select doesn't trigger change binding — Login button won't appear; must use eval to set value AND dispatch `change` event
- Add Customer submit triggers `window.alert()` — pre-stub `window.alert = function(msg){window.__lastAlert=msg}` before clicking
- Account switch (tabs 1004/1005/1006) works via `vibium select @e3 "1005"` but same AngularJS issue applies — use eval if button doesn't appear
- Search box in Customers list works for filtering by name (`vibium fill` works)
- SPA routes: `#/login`, `#/account`, `#/manager`

---

## MCP Batch 1 Re-run — Sites 1–5 (vibium MCP tools)

*Re-tested 2026-05-18 using `mcp__vibium__browser_*` MCP tools. Compare with CLI Batch 1 reports above.*

---

## Practice Test Report: AcademyBugs (MCP)
URL: https://academybugs.com/
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; title "AcademyBugs.com – Academy Bugs"

### Structure
- Navigation: Examples of Bugs, Types of Bugs, Find Bugs, Report Bugs
- Interactive elements: 21 on homepage (map includes cookie banner + tutorial modal)
- Products: 18 products at /find-bugs/ (all pages: shoes, jeans, t-shirts, hoodies, bags, coats)

### Navigation
[PASS] Find Bugs → https://academybugs.com/find-bugs/ (product grid loaded)
[PASS] Account (Login for Pricing) → https://academybugs.com/account/ (login form loaded)

### Core Functionality
[PASS] Dismiss tutorial modal — `browser_click @e20` (× button) worked cleanly by CSS selector
[PASS] Dismiss cookie banner — `browser_click @e3` (Accept cookies) worked
[BUG] View filter (10/25/50) — clicking "25" still shows 18 products; no change in displayed count
[PASS] Sort dropdown — `browser_select {selector: "select#sortfield", value: "3"}` correctly sorted Title A-Z (first product changed from "DNK Yellow Shoes" to "Black Over-the-shoulder Handbag"); Price Low-High (value "1") sorted $15.14, $45.00, $46.00 ✓
[PASS] Product detail page loaded at /store/dnk-yellow-shoes/
[PASS] Add to Cart — redirected to /my-cart/ (no layout break observed in MCP; CLI showed main content disappearing)
[BUG] Cart total calculation — Grand Total $152.99 for $45.00 item + $7.99 shipping (expected $52.99)
[BUG] Russian text on login page — "Не зарегистрированы? Нажмите кнопку ниже" at /account/

### Bugs Found
1. **View filter non-functional** — clicking "25" shows same 18 products. Steps: /find-bugs/ → click "25" link. Severity: Low
2. **Cart total calculation error** — Grand Total = $152.99 for $45.00 + $7.99 shipping (off by $100). Steps: add any product to cart → view /my-cart/. Severity: High
3. **Mixed-language login page** — "NEW USER" section contains Russian text. Steps: navigate to /account/. Severity: Medium

### MCP vs CLI Comparison
| Finding | CLI | MCP |
|---------|-----|-----|
| Sort dropdown | Appeared non-functional (select by text failed) | Works correctly — select by value ("1"–"4") |
| Add to cart | Layout break: main content disappeared | Normal redirect to /my-cart/ (no layout break) |
| Cart total bug | Not found | Found: $152.99 for $45+$7.99 |
| View filter | Non-functional | Non-functional (same) |
| Russian text | Confirmed | Confirmed (same) |
| Dialog handling | No native dialogs on this site | No native dialogs on this site |

### Notes
- Key MCP advantage: `browser_select` uses option `value` attribute directly — select with value "3" for Title A-Z works; CLI was selecting by text label which failed
- MCP `browser_map` correctly identified all 21 elements on homepage including banner dismissal buttons
- The "Add to Cart layout break" CLI bug was NOT reproduced with MCP — redirect to cart behaved normally; may be intermittent or session-state dependent

---

## Practice Test Report: Basic Calculator (MCP)
URL: https://testsheepnz.github.io/BasicCalculator.html
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; title "Basic Calculator"

### Structure
- Navigation: TestSheepNZ header links
- Interactive elements: 14 (build select, number inputs x2, operation select, calculate button, answer field, integer-only checkbox, clear button)

### Core Functionality
[BUG] Divide by zero — Prototype build: 5 ÷ 0 → answer blank, Calculate button permanently disabled
[BUG] Build 1 NaN — "abc" + 5 = "NaN" (should reject or error)
[BUG] Build 2 string concatenation — 3 + 4 = "34" (should = 7)

### Bugs Found
1. **Divide-by-zero disables Calculate button** — Steps: select Divide (value "3"), enter 5 and 0, click Calculate → button disabled permanently until build is changed. Severity: High
2. **Build 1 accepts non-numeric input** — "abc" + 5 = NaN instead of validation error. Severity: Medium
3. **Build 2 string concatenation bug** — addition concatenates strings: 3 + 4 = "34". Severity: High

### MCP vs CLI Comparison
| Finding | CLI | MCP |
|---------|-----|-----|
| All 3 bugs | Confirmed | Confirmed (identical behavior) |
| browser_select by value | N/A | Works: value "3" = Divide, value "1" = Build 1 |
| browser_fill | N/A | Fills `#number1Field` / `#number2Field` by ID |

### Notes
- All bugs identical between CLI and MCP — no behavioral differences observed
- `browser_select` with numeric values ("0"–"4" for operations, "0"–"9" for builds) works cleanly
- Switching builds re-enables a disabled Calculate button (workaround for the divide-by-zero lock)

---

## Practice Test Report: Black Box Puzzles (MCP)
URL: https://blackboxpuzzles.workroomprds.com/
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; title "Black Box Puzzles"

### Structure
- Navigation: 44 interactive elements found by `browser_map` (puzzle links, external links)
- **MCP advantage**: `browser_map` returns all numbered puzzle links (1, 2, 3, 4, 6a, 7…34) on the index page

### Navigation
[PASS] Puzzle 29 → https://blackboxpuzzles.workroomprds.com/puzzle29/ (puzzle loaded)

### Core Functionality
[PASS] Puzzle 29 loaded with 4 dark lamp circles + 4 white button circles
[PASS] Coordinate click at (486, 589) → buttonA2 turned blue (visual state change confirmed)
[NOTE] Most puzzles (not 22, 24, 26b, 29, 31, 33, 34) require Flash — render as blank areas

### MCP vs CLI Comparison
| Finding | CLI | MCP |
|---------|-----|-----|
| Index page map | `vibium map` returns nothing | `browser_map` returns all 44 puzzle nav links |
| Puzzle element map | Nothing (custom elements) | Nothing (same) |
| Coordinate clicks | Required via `vibium mouse click x y` | Required via `browser_mouse_click {x, y}` |
| Puzzle navigation | Must construct URL manually | Can click numbered links from map |

### Notes
- MCP `browser_map` is significantly more capable on the index page — CLI returned nothing; MCP found all puzzle navigation links
- Inside individual puzzles, elements are inside `<puzzle>/<puzzleui>` custom HTML elements — not found by either CLI or MCP map; both require coordinate clicks
- `getBoundingClientRect()` eval works identically in both modes for locating puzzle circles
- Flash-only puzzles render blank in Chrome regardless of mode

---

## Practice Test Report: BookCart (MCP)
URL: https://bookcart.azurewebsites.net/
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; title "Home"; Angular Material UI rendered

### Structure
- Navigation: Book Cart, Search, Cart (0), Login, Swagger, GitHub
- Categories: All Categories, Biography, Fiction, Mystery, Fantasy, Romance
- Interactive elements: 13 found by `browser_map`

### Core Functionality
[BUG] Products not loaded — "No books found." shown after 5s wait (Azure backend hibernated)
[BUG] Login empty submit — form shows red borders on required fields; no error message text
[BUG] Login invalid credentials — silent failure; page stays on login with no error/snackbar
[PASS] Duplicate username check — registering as "admin" shows "User Name is not available" snackbar

### Bugs Found
1. **Azure backend hibernated** — products API down; "No books found." on all categories. Severity: High (environment)
2. **Silent login validation** — empty submit highlights fields in red but shows no error message. Severity: Medium
3. **Silent invalid login failure** — no error message on wrong credentials (API down). Severity: Medium (masked by backend issue)

### MCP vs CLI Comparison
| Finding | CLI | MCP |
|---------|-----|-----|
| Backend down | Confirmed | Confirmed (same) |
| Silent validation | Confirmed | Confirmed (same) |
| Duplicate username snackbar | Confirmed | Confirmed: "User Name is not available" |
| Login button selector | `vibium find role button` | `browser_map` → @e4 (button, not link) |
| `browser_find role=link text=Login` | N/A | Times out 30s — Login is `<button>` not `<a>` |

### Notes
- **MCP-specific finding**: `browser_find {role: "link", text: "Login"}` timed out with 30s wait — the Login control is rendered as `<button>` by Angular Material, not `<a>`; must use `browser_map` refs or CSS selector
- Angular Material inputs fill by `#mat-input-N` IDs (auto-assigned)
- `browser_map` correctly identifies `mat-list-item` elements for categories (CLI equivalent unclear)

---

## Practice Test Report: Cnarios (MCP)
URL: https://www.cnarios.com/
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; title "Cnarios | Free Real-World Automation Testing Practice"

### Structure
- Navigation: Features, How it works?, Contact Us, Blogs, Start Exploring, Challenges
- Footer links: Iframes, Multi Window, Links, Table, E-commerce Pagination, E-commerce Filters, HTML Basics, Locator Strategies
- Interactive elements: 26 on homepage

### Navigation
[PASS] Challenges → https://www.cnarios.com/challenges (8 challenge cards loaded)
[BUG] /concepts/iframe → completely blank page (React routing bug)
[BUG] `browser_get_text` on blank page → MCP schema error ("Invalid input: expected string, received undefined")

### Core Functionality
[PASS] Challenges page — filter inputs, 8 "View Challenge" buttons visible
[PASS] Challenge detail — "E-commerce Product Listing & Pagination" at /challenges/product-listing-pagination loaded
[BUG] All /concepts/* pages render blank

### Bugs Found
1. **React routing bug on /concepts/*** — direct navigation to any /concepts/* URL renders blank page; `#root` has 0 children. Steps: click any footer link (Iframes, Multi Window, etc.). Severity: Medium
2. **vibium bug MB9: `browser_get_text` invalid_union on blank pages** — throws "Invalid input: expected string, received undefined" when `document.body.innerText` returns `""`. Not a site bug — vibium MCP bug (same root cause as MB6). Workaround: `browser_evaluate { expression: "document.body.innerText || null" }`. Filed as MB9.

### MCP vs CLI Comparison
| Finding | CLI | MCP |
|---------|-----|-----|
| /concepts/* blank | Confirmed | Confirmed (same) |
| Blank page text | Returns empty string | Throws schema error |
| Challenges section | Functional | Functional (same) |
| Challenge detail pages | Functional | Functional (same) |

### Notes
- **MCP-specific finding**: `browser_get_text` throws a schema validation error when page content is empty (null/undefined return). CLI `vibium text` returns empty string gracefully. Workaround: use `browser_evaluate` with `document.body.innerText + ''` (string coercion prevents null return)
- This is a known MCP tool behavior gap — document in SKILL.md tips

---

## MCP Batch 1 — Cross-Site Comparison Summary

| Site | CLI Bugs | MCP Bugs | MCP-Only Findings | CLI-Only Findings |
|------|----------|----------|-------------------|-------------------|
| AcademyBugs | Sort non-functional, view filter, layout break, Russian text | View filter, cart total error, Russian text | Cart total bug ($152.99); sort IS functional via value | Layout break (not reproduced) |
| Basic Calculator | Div/0, NaN, concatenation | Div/0, NaN, concatenation | None | None |
| Black Box Puzzles | Map empty, Flash puzzles | Flash puzzles | Index page map works | Index map empty |
| BookCart | Backend down, silent validation | Backend down, silent validation | `browser_find role=link` timeout on buttons | None |
| Cnarios | /concepts blank | /concepts blank | `browser_get_text` schema error on blank pages | None |

### Key MCP vs CLI Behavioral Differences

1. **`browser_select` vs `vibium select`**: Both match by option `value` attribute. AcademyBugs sort appeared broken in CLI because the old CLI notes said it was non-functional — with value-based selection, sort works correctly. Both tools behave the same when used correctly.

2. **`browser_map` coverage**: MCP `browser_map` found navigation links on the Black Box Puzzles index where CLI `vibium map` returned nothing. MCP is more inclusive of plain `<a>` links in non-standard page structures.

3. **`browser_find` role matching**: MCP `browser_find {role: "link"}` strictly matches ARIA `role=link` — Angular Material buttons and `<button>` elements time out. CLI `vibium find role button` is more forgiving. Use `browser_map` refs or CSS selectors in MCP instead.

4. **Blank page handling**: CLI returns empty string on blank pages. MCP `browser_get_text` throws a schema error. Always coerce eval return values to strings in MCP mode.

5. **Dialog handling**: Not tested in batch 1 (no native dialogs triggered). MCP uses `browser_dialog_accept`/`browser_dialog_dismiss` vs CLI pre-stubbing. No deadlock risk with MCP.

6. **Session isolation**: MCP browser and CLI daemon are separate — `browser_stop`/`browser_start` does not affect the CLI session.

---

## MCP Batch 2 Re-run — Sites 6–10 (vibium MCP tools)

*Tested 2026-05-18 using `mcp__vibium__browser_*` MCP tools.*

---

## Practice Test Report: Evil Tester (MCP)
URL: https://testpages.eviltester.com/styled/index.html
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; title "Evil Tester Test and Practice Web Pages"

### Structure
- Navigation: 79 interactive elements (links + buttons via `browser_map`)
- Main sections: HTML forms, JavaScript, HTTP, General, Frames, iFrames, File Upload, Proxy Intercept, Experimental

### Navigation
[PASS] Direct URL loaded index page with all section links accessible via map refs
[PASS] `browser_map` found all nav links — more reliable than `browser_find {role: "link"}` for plain anchors

### Core Functionality
[PASS] Alert handling (setTimeout workaround) — `browser_evaluate { expression: "setTimeout(() => alert('test'), 300)" }` + `browser_sleep {ms: 350}` + `browser_dialog_accept {}` → "Dialog accepted"
[PASS] Confirm dismiss — `browser_evaluate { expression: "setTimeout(() => confirm('test'), 300)" }` + `browser_sleep {ms: 350}` + `browser_dialog_dismiss {}` → "Dialog dismissed"
[BUG/MB3] Direct click on "Click for JS Alert" button → `browser_click` deadlocked indefinitely; required `browser_stop` + `browser_start` to recover. MB3 confirmed on MCP same as CLI.

### Bugs Found
1. MB3 — `browser_click` deadlock on native alert trigger — Steps: navigate to Alerts page, click alert button directly — Severity: High (requires session restart)

### Notes
- setTimeout+sleep workaround (300ms eval + 350ms sleep + accept) is reliable across all three dialog types (alert/confirm/prompt)
- `browser_find {role: "button", text: "..."}` times out on plain `<button>` elements; use `browser_map` refs or CSS selector directly
- Pre-stub pattern (`eval window.alert = () => {}`) works as alternative to setTimeout but requires executing before the click

---

## Practice Test Report: Gefälscht CompuTech (MCP)
URL: https://webtestingcourse.dequecloud.com/
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; intentionally inaccessible e-commerce demo

### Structure
- Navigation: Home, Products, Support, Contact links
- Interactive elements: header nav + product cards + form fields
- Purpose: accessibility testing target (intentionally broken a11y)

### Navigation
[PASS] Home → `/` (product grid)
[PASS] Contact nav link → `/contact.php` (correct URL)
[FAIL] Direct URL `/contact/` → 404 (trailing slash path does not exist; must use `/contact.php`)

### Core Functionality
[PASS] Contact form fields accessible via `browser_map` refs — no CSS name selectors needed (MCP advantage over CLI which required `input[name=x]` selectors)
[PASS] Form fields: Full Name, Email Address, Subject, Message all fillable via map refs
[PASS] Form submit button found and clickable via map ref

### Bugs Found
None beyond intentional inaccessibility. Note: site is designed to have a11y issues, not functional bugs.

### Notes
- MCP `browser_map` finds form fields without needing `input[name=...]` CSS selectors — simpler than CLI approach
- `/contact/` (trailing slash) returns 404; always navigate via the Contact nav link or use `/contact.php` directly
- Intentional a11y issues: missing labels, low contrast, keyboard traps — outside scope of MCP functional testing

---

## Practice Test Report: Magento (MCP)
URL: https://magento.softwaretestingboard.com/
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[FAIL] Site DOWN — Cloudflare 526 SSL error (invalid SSL certificate on origin server)

### Notes
- Confirmed DOWN as of 2026-04-22 (CLI batch) and 2026-05-18 (MCP batch)
- No testing possible; skip this site until restored

---

## Practice Test Report: Parabank (MCP)
URL: https://parabank.parasoft.com/parabank/admin.htm
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Admin page loaded; title "ParaBank | Administration"

### Structure
- Admin page: Database Initialization button, JMS/SOAP service controls
- Main site: Login form, Register link, navigation (About, Services, Products, Locations, Admin)

### Navigation
[PASS] DB Initialize → POST to `/parabank/admin.htm` → "Database Initialized" confirmation
[PASS] Register link → `/parabank/register.htm` (registration form loaded)
[PASS] Login page → `/parabank/login.htm`

### Core Functionality
[BUG] Any-credentials login — after DB initialize, any username/password combination logs in successfully; login is not validated (e.g. `user: "test123", password: "test123"` → logged in as "test123")
[PASS] Registration validation — empty form submit shows validation errors on required fields
[PASS] Registration with mismatched passwords → "Passwords did not match" error displayed
[PASS] Registration with valid data (unique username) → account created successfully
[PASS] Form fields accessible via `browser_map` refs — clean MCP experience

### Bugs Found
1. Any-credentials login — after DB initialize, login accepts any username/password without validation — Steps: initialize DB, enter any credentials, click Login — Severity: High (authentication completely bypassed)

### Notes
- DB must be initialized before login works at all (otherwise may show stale data errors)
- The any-creds login bug is likely intentional for demo purposes — parabank is a demo banking app
- Use Parabank for form validation and UI testing, not auth flow testing
- Registration form: First Name, Last Name, Address, City, State, Zip, Phone, SSN, Username, Password, Confirm — all required

---

## Practice Test Report: Parking Cost Calculator (MCP)
URL: https://www.shino.de/parkcalc/
Date: 2026-05-18
Mode: vibium MCP

### Reachability
[PASS] Site loaded; title "Parking Cost Calculator"

### Structure
- Form: ParkingLot (select), StartingDate, StartingTime, AM/PM radio, LeavingDate, LeavingTime, AM/PM radio, Submit button
- Parking lots: Valet, Short-Term, Economy, Long-Term Garage, Long-Term Surface

### Core Functionality
[PASS] Economy 2-day calculation — 05/18 08:00 AM → 05/20 08:00 AM → $18.00 (2 × $9 daily max) ✓
[PASS] Valet 2-day calculation — same dates, Valet lot → $36.00 (2 × $18/day) ✓
[PASS] Valet ≤5h flat rate — 08:00 → 11:00 (3h) → $12.00 flat ✓
[PASS] Valet 5h boundary — 08:00 → 13:00 (exactly 5h) → $12.00 (boundary inclusive) ✓
[PASS] Valet >5h → daily rate — 08:00 → 13:30 (5h 30min) → $18.00 (daily rate kicks in) ✓
[PASS] Invalid date (leaving before starting) → inline error message "ERROR! YOUR LEAVING DATE OR TIME IS BEFORE YOUR STARTING DATE OR TIME" displayed on same page
[PASS] `browser_select {value: "Economy"}` and `{value: "Valet"}` work correctly by option value
[PASS] `browser_fill` works on all text inputs (name-cased: `StartingDate`, not `startingDate`)

### Bugs Found
None. All rates and validations match documented rate card.

### Notes
- Input name attributes are PascalCase (`StartingDate`, `LeavingTime`) — CSS selectors must match exactly
- SKILL.md note "invalid dates cause blank page" is **incorrect** — invalid date shows inline error message, page remains intact
- Valet boundary: ≤5h = $12 flat; >5h = $18/day (strict boundary at exactly 5h00m)
- `browser_select` with option value works for all 5 lot types

---

## MCP Batch 2 — Cross-site Comparison

| Site | Reachability | Core Flow | MCP vs CLI Difference |
|------|-------------|-----------|----------------------|
| Evil Tester | PASS | PASS (with workaround) | setTimeout+sleep workaround required for dialogs; MB3 deadlock same as CLI on direct click |
| Gefälscht CompuTech | PASS | PASS | `browser_map` refs work for form fields; CLI needed `input[name=x]` selectors |
| Magento | FAIL (DOWN) | N/A | Same as CLI — site still down |
| Parabank | PASS | PASS (with noted bug) | Any-creds login bug present; DB init required first |
| Parking Cost Calculator | PASS | PASS | Input names are PascalCase; `browser_fill` works cleanly |

### Key MCP vs CLI Behavioral Differences (Batch 2)

1. **Form field access**: MCP `browser_map` refs work on Gefälscht CompuTech without knowing CSS name selectors. CLI required `input[name=fieldname]` approach.

2. **Dialog deadlock (MB3)**: Confirmed in MCP mode same as CLI — `browser_click` on a native `alert()` trigger hangs indefinitely. The setTimeout+sleep workaround (300ms delay + 350ms sleep + `browser_dialog_accept`) is the correct MCP pattern.

3. **Invalid date error**: Parking Cost Calculator shows inline error message for invalid date ranges — not a blank page as noted in SKILL.md. SKILL.md note needs correction.

4. **Parabank any-creds bug**: Reproduced in MCP mode. Likely intentional demo behavior but worth noting as a testing target.
