# Practice Testing — Test Reports

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
