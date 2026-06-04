# Practice Testing — Site Directory & CLI vs MCP Comparison

**[Live benchmark page →](https://lana-20.github.io/practice-testing/)** · **[CLI vs MCP behavioral comparison → SKILL.md](SKILL.md#cli-vs-mcp--behavioral-comparison)**

[<video src="cli_mcp_research.mp4" controls width="390"></video>](https://github.com/user-attachments/assets/6d5b211e-7615-4ef5-a9b8-2ad29d7ee622)

<!-- 104 sites across 5 categories · Tested 2026-04-22 to 2026-05-20 · Behavioral notes updated for v26.5.31 (2026-06-01) · Level 2 rerun complete (v26.5.31, 2026-06-03): 96/100 sites measured · Level 3 rerun in progress (2026-06-03+): fixed CLI bracket + turns tracking; fresh subagents per site; GP 28/28 done, AT 19/42 done; per-site data updated to L3 where available -->
<!--
  Machine:   Intel Core i9-10910 @ 3.60GHz · 10 cores / 20 threads · 64 GB RAM




  OS:        macOS 26.3.1 (Build 25D771280a)
  Node:      v25.8.0
  vibium:    v26.5.31 (timing data from v26.3.18 original run)
  Chrome:    148.0.7778.168
  Model:     claude-sonnet-4-6
  Network:   Wi-Fi · Router 10.0.0.1
  Methodology: wall-clock time per site (python3 time.time()*1000), bracketing navigate + primary interaction + verification.
               Token/cost delta from ~/.claude/projects/**/*.jsonl, deduplicated by message ID, sonnet-4-6 only.
-->

---

## Summary

| Category | Sites | CLI (ms) | CLI turns (v26.3.18) | CLI ($) | MCP (ms) | MCP turns (v26.3.18) | MCP ($) | Speed | Turns× | Cost× |
|----------|-------|----------|----------------------|---------|----------|----------------------|---------|-------|--------|-------|
| General Practice | 28 | 380,681 | ~39 | $0.573 | 1,313,402 | ~301 | $2.470 | CLI **3.5×** faster | **7.7×** fewer | **4.3×** cheaper |
| Automation Testing | 42 | 435,053 | ~46 | $1.229 | 1,705,242 | ~317 | $13.053 | CLI **3.9×** faster¹ | **6.9×** fewer | **10.6×** cheaper |
| Security Testing | 7 / 11 | 21,170 | 19 | $0.000 | 187,318 | 48 | $3.114 | CLI **8.8×** faster | **2.5×** fewer | N/A |
| API Testing | 20 | 136,558 | 3 | $0.079 | 515,684 | 37 | $7.280 | CLI **3.8×** faster² | **12×** fewer | **92.7×** cheaper |
| Performance Testing | 3 | 12,550 | 4 | $0.000 | 81,798 | 30 | $1.858 | CLI **6.5×** faster | **7.5×** fewer | N/A |
| **All sites** | **100 / 104** | **986,012** | **~111** | **$1.881** | **3,803,444** | **~733** | **$27.776** | **CLI 3.9× faster** | **6.6× fewer** | **14.8× cheaper** |

¹ Automation Testing L3 CLI costs now captured (sonnet-4-6 bracket); batch 9 (7 sites, originally run under Haiku 4.5) was rerun in Sonnet 4.6 on 2026-06-03 — costs now captured. Lambdatest Playground MCP requires `eval window.location.href` — dead-frame after stop/start.  
² API Testing L3 CLI ms elevated by httpbin (25,008ms cold-start); excluding httpbin: CLI 4.8× faster. API Challenges and QuickPizza are new sites with L3-only data.

**Key insight:** With L3 bracket fix (script-generation cost now inside the bracket), CLI costs are real and non-trivial for complex sites. MCP time per site is fairly uniform; CLI time tracks site complexity. Security and Performance Testing retain wide speed ratios; GP, AT, and API ratios narrowed in L3 due to longer CLI generation times captured.

**Legend:** `—` = site no longer accessible or local-only (permanent). `N/A` in Cost× = CLI cost is $0.000 (no LLM tokens consumed in CLI bracket — ratio undefined). `CLI/MCP turns (v26.3.18)` = interactive turn counts from the original run using per-command back-and-forth; L3 rerun turn counts are subagent-level and tracked separately. ms and $ are best-available: L3 where measured (GP all 28, AT 19/42, API 2/18 new sites), L2 elsewhere.

Each section below includes an aggregate token/cost table — turn counts from v26.3.18; ms and $ from best-available (L3 > L2).

---

## General Practice (31 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (best-available) | 427,101ms | 1,463,102ms | **3.4×** faster |
| LLM turns (v26.3.18) | ~39 | ~301 | ~7.7× fewer |
| Cost (best-available) | $0.633 | $2.752 | **4.3×** cheaper |

*Best-available data: L3 for all 31 sites (29 original L3✓✓ + BearQ, PromptQA, Bill Payment API L3-only).*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| AcademyBugs | https://academybugs.com/ | 10,356 | $0.018 | 61,013 | $0.109 | 5.9× | 5.9× | 25 planted bugs; dismiss cookie banner + tutorial modal before interacting; sort select works by label or value (B5 fixed v26.5.31) |
| A11y Coffee | https://a11y.coffee/ | 6,620 | $0.013 | 34,973 | $0.064 | 5.3× | 4.7× | Accessibility learning resource; 13 nav links; dark/light toggle; static site; no mandatory waits |
| Basic Calculator | https://testsheepnz.github.io/BasicCalculator.html | 9,469 | $0.018 | 44,934 | $0.069 | 4.7× | 3.8× | Select operation by label ("Add", "Subtract", etc.) or value ("0"–"4") (B5 fixed v26.5.31); 9 prototype builds selectable; minimal form with no mandatory waits → high MCP overhead ratio |
| Black Box Puzzles | https://blackboxpuzzles.workroomprds.com/ | 7,164 | $0.017 | 35,509 | $0.058 | 5.0× | 3.4× | **Site restored** (was redirecting to cnarios.com, back as of 2026-06-03); 44 CLI refs; puzzle interactions require coordinate clicks; Flash puzzles still non-functional |
| BookCart | https://bookcart.azurewebsites.net/ | 17,514 | $0.019 | 38,433 | $0.071 | 2.2× | 3.8× | **Site restored** (was redirecting to cnarios.com, back as of 2026-06-03); Angular Material; 13 CLI refs; search via `input[type=search]` + dispatchEvent |
| Candy Mapper | https://www.candymapper.net/ | 13,320 | $0.019 | 37,853 | $0.069 | 2.8× | 3.6× | UK testing sandbox; 54 MCP elements — county selector, contact form, social links, reCAPTCHA challenge; heavy page content compresses ratio to one of the narrowest in GP |
| Cnarios | https://www.cnarios.com/ | 45,098 | $0.018 | 41,276 | $0.064 | 0.9× | 3.6× | React SPA; homepage nav maps fine in both; challenge cards at /challenges/ not rendered (React routing bug — heading only) |
| Evil Tester | https://testpages.eviltester.com/styled/index.html | 10,515 | $0.022 | 44,361 | $0.140 | 4.2× | 6.4× | Pre-stub window.alert/confirm/prompt via eval BEFORE clicking any alert button (B3/MB3 deadlock still open); CLI eval pre-stub nearly equalizes costs (Cost× 1.5×) |
| Gefälscht CompuTech | https://webtestingcourse.dequecloud.com/ | 8,821 | $0.020 | 44,533 | $0.085 | 5.0× | 4.3× | Intentionally inaccessible site for accessibility testing; contact form needs `input[name=x]` selectors; fast nav → high MCP overhead ratio |
| Parabank | https://parabank.parasoft.com/parabank/admin.htm | 9,196 | $0.020 | 34,389 | $0.057 | 3.7× | 2.9× | CLI `input[name=customer.firstName]` fails (dot in name); MCP ID-based selectors work fine; run DB Initialize from admin panel before testing |
| Parking Cost Calculator | https://www.shino.de/parkcalc/ | 11,649 | $0.021 | 50,486 | $0.098 | 4.3× | 4.7× | Returns $0.00 consistently in both interfaces — AM/PM radio default or date parse bug on the site itself; select lot by visible label or value (B5 fixed v26.5.31); invalid dates → inline error |
| PHP Travels | http://phptravels.com/demo/ | 11,142 | $0.023 | 53,688 | $0.101 | 4.8× | 4.3× | **Site redesigned** (2026-06-03): submit no longer crashes — pre-stub `window.alert` then click `#demo`; 71 CLI refs; math captcha field `@e21` still present; fill first/last/email then click @e20 |
| Polymer Shop | https://shop.polymer-project.org/ | 8,928 | $0.014 | 31,033 | $0.058 | 3.5× | 4.1× | All UI in Web Components shadow DOM — map returns nothing in both; eval+shadowRoot traversal required; Polymer events need mouse_click at bounding-box coords — eval .click() does not fire component events |
| Potion Shop | https://qe-at-cgi-fi.github.io/potion-shop/ | 8,226 | $0.020 | 42,220 | $0.075 | 5.1× | 3.8× | Medieval order form; 32 form controls (radio for potion type/size/potency, ingredient checkboxes, delivery options, textarea); browser_fill works on all inputs |
| Practice Software Testing | https://practicesoftwaretesting.com/ | 15,241 | $0.020 | 61,556 | $0.129 | 4.0× | 6.4× | Angular; Login is `input[type=submit]` not button — use eval.click(); test login: customer@practicesoftwaretesting.com / welcome01; add to cart works without login |
| PrestaShop | https://demo.prestashop.com/ | 15,545 | $0.017 | 47,687 | $0.077 | 3.1× | 4.6× | Store in iframe — get inner URL via eval after 5s; subdomain expires in ~2min; use eval location.href for all navigation (vibium go deadlocks daemon); mandatory sleeps compress ratio |
| PromptQA Playground | https://playground.promptqa.dev/ | 8,197 | $0.023 | 64,915 | $0.096 | 7.9× | 4.3× | **New site (added 2026-06-03):** Shop + Clinic + Widgets + API + Locator Game; 69 refs on homepage, 76 in Shop; stable `data-testid` on all elements; tour overlay on first load — dismiss "Skip tour" before interacting |
| QA Practice | https://qa-practice.razvanvancea.ro/ | 11,520 | $0.016 | 52,303 | $0.109 | 4.5× | 6.9× | ADD TO CART uses CSS uppercase — use map refs not text; login at homepage #auth-shop anchor (not /ecommerce/ — 404); pre-stub alert/confirm; login: admin@admin.com / admin123 |
| QA Training Simulator | https://bugeater.web.app/ | 10,855 | $0.022 | 50,566 | $0.081 | 4.7× | 3.7× | BugEater 2.0 (renumbered #1.1–#7.6 as of 04.2026); two cookie banners (homepage + /app/list); dismiss react-joyride tutorial; direct URL to challenge routes now works — navigate from /app/list for the list |
| Random User Generator | https://randomuser.me/ | 11,859 | $0.017 | 43,690 | $0.083 | 3.7× | 4.9× | URL-param API calls are the fastest pattern; ?format=csv triggers download and crashes BiDi session (restart required); use eval for large JSON (vibium text overflows at 5000 results) |
| Real World Example Apps | https://codebase.show/projects/realworld | 13,480 | $0.043 | 42,298 | $0.089 | 3.1× | 2.1× | SvelteKit SPA needs 3s sleep after wait load before content renders; GitHub OAuth required for Sign In; mandatory 3s sleep floor narrows the ratio relative to similar-sized sites |
| testers.ai | https://testers.ai/testing/ | 9,442 | $0.025 | 41,875 | $0.067 | 4.4× | 2.7× | 59-link checklist index covering WCAG A/AA/AAA, screen reader, keyboard, color, ARIA, forms, security, privacy, code quality, i18n, GenAI, DevOps, and more |
| Test Track | https://testtrack.org/ | 27,166 | $0.020 | 57,440 | $0.111 | 2.1× | 5.7× | Structured training site; 15 practice modules Basic→Intermediate→Advanced→Expert (buttons, inputs, login, dropdowns, checkboxes, tables, modals, alerts, drag & drop, frames, canvas, 3D chess); used as vibium reference site |
| The Boozang Test Lab | https://thelab.boozang.com/ | 9,409 | $0.021 | 50,224 | $0.081 | 5.3× | 3.9× | React SPA; 16 challenges; Form Fill saves to shared DB at api.boozang.com; vibium fill works on all inputs; vibium click works on all buttons |
| The iframe Search Engine | https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html | 29,901 | $0.018 | 43,240 | $0.100 | 1.4× | 5.5× | Use vibium fill for search input; select by visible label or full URL value; "Go search" link opens in a new tab; non-existent select value now errors (B5 fixed v26.5.31) |
| The Internet | http://the-internet.herokuapp.com/ | 22,388 | $0.019 | 59,245 | $0.104 | 2.6× | 5.5× | 44 examples; hover fails on non-interactive elements; vibium frame context resets per CLI call; TinyMCE iframe via contentDocument; input[type=range] needs eval+dispatchEvent |
| The Random Number Service | https://www.random.org/ | 12,173 | $0.024 | 46,765 | $0.094 | 3.8× | 3.9× | Cookie banner on load; generator forms not in map — use URL params or eval form.submit(); validation: min>max and num>10000 both trigger errors |
| ToDo List | https://todolist.james.am/#/ | 11,844 | $0.015 | 59,299 | $0.084 | 5.0× | 5.5× | AngularJS; **counter off-by-1 bug** (shows N-1 active items); dblclick label to enter edit mode; checkbox check "obscured" — use mouse click by coords; no localStorage persistence |
| UI5 Demo Kit | https://ui5.sap.com/#/demoapps | 13,832 | $0.019 | 57,399 | $0.114 | 4.1× | 6.1× | **v26.5.31 update:** CLI vibium map now returns 137 refs (was nothing in older versions); MCP browser_map returns 128 refs; Shopping Cart "Open App" opens new tab — use browser_new_page for next site to avoid BiDi dead-frame |
| BearQ | https://angryweasel.com/bearq/ | 6,820 | $0.017 | 43,902 | $0.069 | 6.4× | 4.0× | **New site (added 2026-06-03):** Weasel Warren — 5 challenge sections (Form Validation, Input Types, Alerts & Dialogs, Basic Elements, Images & Media); 9 CLI/MCP nav refs on homepage; form validation page has email/username/password/confirm + Register button |
| Bill Payment API | https://gauravkhurana.in/practise-api/ | 19,411 | $0.036 | 45,997 | $0.145 | 2.4× | 4.0× | **New site (added 2026-06-03):** Docs page → "Launch the Practice UI" → full BillPay CRUD app at `/practise-api/ui`; 33 refs; Dashboard / Bills / Payments / Users / Billers / Settings / Practice Components sections; dark-mode toggle |

³ Parabank MCP inflated by 30s browser_find timeout on non-existent "Register" role. Without timeout: ~54,782ms (11.4×).

---

## Automation Testing (42 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (best-available) | 435,053ms | 1,705,242ms | **3.9×** faster |
| LLM turns (v26.3.18) | ~46 | ~317 | ~6.9× fewer |
| Cost (best-available) | $1.229 | $13.053 | **10.6×** cheaper |

*Best-available data: L3 for 19/42 sites (batches 9–11); L2 for remaining 23. Batch 9 (7 sites) rerun in Sonnet 4.6 on 2026-06-03; batch 11 (5 sites) run 2026-06-03.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| Applitools Demo | https://demo.applitools.com/ | 10,842 | $0.243 | 41,396 | $0.064 | 3.8× | 0.3× | Intentional visual testing site; any credentials accepted including empty; **dashboard shows $350%7** corrupted total (intentional bug); search non-functional; all action links dead (href="#") |
| ATM Practice App | https://qe-at-cgi-fi.github.io/atm/ | 6,200 | $0.112 | 37,400 | $0.077 | 6.0× | 0.7× | Minimal ATM simulator; 4 elements (DEBUG, ADMIN, number input, WITHDRAW); pure overhead exposure — one of the widest ratios for minimal-DOM sites |
| Automate Now Sandbox | https://automatenow.io/sandbox-automation-testing-practice-website/ | 33,486 | $0.301 | 30,727 | $0.053 | 0.9× | 0.2× | Submit fires window.alert — pre-stub required; slider needs eval+dispatchEvent; **MCP submit button obscured** (receivesEvents check failed) — use browser_evaluate fallback; name input needs click before fill |
| Automation Bookstore | https://automationbookstore.dev/ | 19,629 | $0.075 | 33,758 | $0.065 | 1.7× | 0.9× | Filter-only SPA; all 8 book hrefs="#" (no detail pages); case-insensitive real-time filter hides via CSS class — screenshot needed to verify filter state |
| Automation Camp | https://play2.automationcamp.ir/ | 11,173 | $0.057 | 43,601 | $0.066 | 3.9× | 1.2× | Alert button deadlocks daemon — eval override doesn't prevent it, restart required; valid login: test/test; input[type=date] needs eval not fill |
| Automation Exercise | https://www.automationexercise.com/ | 23,004 | $0.025 | 54,692 | $0.094 | 2.4× | 3.8× | Ad overlay intercepts nav clicks on homepage — use direct URLs; dismiss "Close" SVG button before interacting; full e-commerce flow works; test cases at /test_cases |
| Automation in Testing | https://automationintesting.online/#/ | 11,012 | $0.014 | 45,691 | $0.082 | 4.1× | 5.7× | Full B&B booking site; 33 MCP refs; contact form at @e17–@e22; #description textarea needs eval+dispatchEvent; Submit @e22 browser_click works directly |
| Automation Test Store | https://automationteststore.com/ | 14,071 | $0.028 | 53,344 | $0.101 | 3.8× | 3.7× | AbanteCart; search by keyword URL param; get product_id from search result href; Add to Cart via `eval document.querySelector('a.cart').click()` (browser_click fails — zero-size); full cart confirmed |
| Automation Testing Practice | https://testautomationpractice.blogspot.com/ | 9,892 | $0.020 | 53,389 | $0.084 | 5.4× | 4.3× | Blogger single long page; **both CLI and MCP map return 82 elements** (old "CLI returns nothing" note outdated); date input needs eval; radio/checkbox browser_click fails — use eval; alert buttons deadlock — pre-stub |
| Coffee Cart | https://coffee-cart.app/ | 21,244 | $0.016 | 60,082 | $0.115 | 2.8× | 7.2× | Vue SPA; 4 map refs only — product cards not in map; data-test attrs exist but `browser_click '[data-test=X]'` fails — use `eval querySelector.click()`; checkout Submit also needs eval click; checkout modal: name + email required |
| Commit Quality | https://commitquality.com/ | 9,202 | $0.018 | 49,518 | $0.134 | 5.4× | 7.5× | Clean React app; map correctly identifies nav + filter + product elements in both interfaces |
| Contact List App | https://thinking-tester-contact-list.herokuapp.com/ | 9,628 | $0.020 | 53,999 | $0.090 | 5.6× | 4.5× | Heroku app; login required for all operations; full CRUD contact management flow works |
| Demo SaaS | https://demo-saas.bugbug.io/ | 16,267 | $0.064 | 29,383 | $0.053 | 1.8× | 0.8× | Clean SPA; minimal interaction; MCP 13.5s is among the fastest MCP times in dataset; 12.7× pure overhead ratio |
| DemoQA | https://demoqa.com/ | 18,079 | $0.064 | 27,151 | $0.052 | 1.5× | 0.8× | Component library; 7 practice sections (Elements, Forms, Alerts/Frames/Windows, Widgets, Interactions, Book Store); many sub-pages; clean map in both interfaces |
| Expand Testing | https://practice.expandtesting.com/ | 16,807 | $0.019 | 50,277 | $0.084 | 3.0× | 4.5× | Login button obscured by ad — use `dispatchEvent(MouseEvent)` on submit; valid login: practice / SuperSecretPassword!; navigate directly to /login (not homepage) |
| GitHub Users Search | https://gh-users-search.netlify.app/ | 15,264 | $0.033 | 37,530 | $0.093 | 2.5× | 2.8× | React GitHub user search; default user pre-loaded; 34 elements (search input + submit + follower links); clean minimal SPA |
| Global SQA Demo | http://www.globalsqa.com/demo-site/ | 18,182 | $0.023 | 54,398 | $0.084 | 3.0× | 3.6× | **Key behavioral difference:** CLI gets BiDi error on http:// URL; **MCP silently follows HTTP→HTTPS redirect** and loads site successfully; MCP maps 49 interactive elements |
| GreenKart | https://rahulshettyacademy.com/seleniumPractise/#/ | 17,865 | $0.026 | 80,317 | $0.122 | 4.5× | 4.8× | Angular; 31 products; **MCP browser_map returns 126 elements** (31 products × 4 controls); large map call compresses ratio to 2.8× — one of the narrowest Automation ratios |
| Hands-On Selenium WebDriver | https://bonigarcia.dev/selenium-webdriver-java/ | 12,935 | $0.019 | 70,520 | $0.155 | 5.5× | 8.3× | Static site; 30 practice sub-pages at clean URLs; fill works on textarea (B7/MB7 fixed v26.5.31); calculator buttons are span.btn not button (use eval) |
| Lambdatest Playground | https://ecommerce-playground.lambdatest.io/ | 36,711 | $0.035 | 88,980 | $0.745 | 2.4× | 21.3× | OpenCart-based e-commerce; **MCP browser_navigate dead-frame after stop/start — use eval `window.location.href`**; CLI map and MCP map both return 308 refs; search is AJAX and stays on homepage; Add to Cart silently fails for guests |
| Let Code | https://letcode.in/test | 5,531 | $0.000 | 41,792 | $0.803 | 7.6× | N/A | Angular; 22 practice sections; **MCP BiDi SSL/privacy error failures** inflated to 211s; clean MCP ratio ~4×; MCP map captures iframe ads, CLI map filters them |
| Locator Game | https://testsmith-io.github.io/locator-game/ | 2,688 | $0.000 | 29,364 | $0.405 | 10.9× | N/A | GitHub Pages static locator challenge; clean, no anomalies or mandatory waits |
| NearForm Testing Playground | https://nearform.github.io/testing-playground/ | 2,424 | $0.000 | 34,847 | $0.430 | 14.4× | N/A | 18 challenge cards (Add/Remove, Checkbox, Drag & Drop, Dynamic Table, File Up/Download, Login Form, Notifications, Radio Buttons, Sliders, Tooltips, Various Inputs); language switcher + difficulty filter |
| OrangeHRM | https://opensource-demo.orangehrmlive.com/ | 5,096 | $0.000 | 28,046 | $0.676 | 5.5× | N/A | HR management SPA; map returns nothing in both interfaces — eval required for all interactions; login: Admin / admin123; Vue inputs require native HTMLInputElement value setter + dispatchEvent to trigger component state |
| Practice Automation | https://practice-automation.com/ | 6,976 | $0.000 | 35,702 | $0.662 | 5.1× | N/A | 28 nav links covering delays, sliders, tables, iframes, forms, calendars, gestures, spinners, modals, hover, file upload/download; sub-pages at practice-automation.com/* |
| Practice Test Automation | https://practicetestautomation.com/practice/ | 3,538 | $0.000 | 33,858 | $0.460 | 9.6× | N/A | Multiple practice pages; valid login: student / Password123 (no exclamation mark); 2–3s mandatory wait on login redirect narrows ratio relative to similar-sized sites |
| QA Cloud | https://www.qacloud.dev/ | 2,268 | $0.000 | 23,263 | $0.334 | 10.3× | N/A | Multi-app QA platform; 38 elements (full nav + app cards with Open App / Docs / API Docs links); Login/Register; search bar; no public API credentials needed for browsing |
| QA Playground | https://qaplayground.dev/ | 2,331 | $0.000 | 22,371 | $0.330 | 9.6× | N/A | Clean static site; 28+ challenge links; map works in both interfaces; no anomalies |
| QE Buggy Todo | https://qe-at-cgi-fi.github.io/todo | 2,453 | $0.000 | 22,854 | $0.415 | 9.3× | N/A | Single-input todo app with intentional bugs (placeholder typo "What need's to be done?"); 1 map element; minimal DOM → high overhead ratio |
| React Shopping Cart | https://react-shopping-cart-67954.firebaseapp.com/ | 2,012 | $0.000 | 27,200 | $0.502 | 13.5× | N/A | Firebase SPA; **MCP map enumerates all 16 products**; **CLI map returns 0** (styled-components hash classes change between builds); CLI still faster due to lower tool overhead |
| SeleniumBase | https://seleniumbase.io/ | 3,545 | $0.000 | 26,215 | $0.353 | 7.4× | N/A | Docs site with 256 MCP elements; 52+ demo pages (Coffee Cart, Drag & Drop, Calculator, Shadow DOM, CAPTCHA); CAPTCHA test pages for CF Turnstile, reCAPTCHA v2 |
| Selectors Hub | https://selectorshub.com/xpath-practice-page/ | 4,914 | $0.000 | 24,751 | $0.354 | 5.0× | N/A | 125-element XPath practice page; shadow DOM elements disabled; large map narrows ratio (MCP spends proportionally more time on map call itself) |
| Selenium Playground | https://www.lambdatest.com/selenium-playground/ | 7,181 | $0.000 | 32,016 | $0.463 | 4.5× | N/A | Cloudflare blocks sub-page navigation (/simple-form-demo) for both; main page maps 156 elements; use direct URL to /simple-form-demo page |
| Swag Labs | https://www.saucedemo.com/ | 2,894 | $0.000 | 33,173 | $0.452 | 11.5× | N/A | Clean login→inventory→add-to-cart; login: standard_user / secret_sauce; 6 inventory items; no mandatory sleeps → overhead fully exposed |
| Sweet Shop | https://sweetshop.netlify.app/ | 3,444 | $0.000 | 43,252 | $0.806 | 12.6× | N/A | addItem links invisible to both CLI and MCP map — eval required in both; full purchase flow works via eval |
| TestDino | https://storedemo.testdino.com/ | 2,649 | $0.000 | 29,272 | $0.476 | 11.1× | N/A | E-commerce demo; **MCP map: 216 elements** (products repeat across carousel sections); **CLI map returns nothing** (SPA); full product, cart, and FAQ sections accessible via MCP |
| Travel Agileway | http://travel.agileway.net/login | 4,205 | $0.000 | 29,234 | $0.574 | 7.0× | N/A | HTTP-only app; MCP silently loads the page (no BiDi error, unlike CLI); 6-element login form (username, password, remember_me, submit); credentials untested |
| Tricentis Obstacle Course | https://obstaclecourse.tricentis.com/Obstacles | 8,210 | $0.000 | 32,854 | $0.482 | 4.0× | N/A | Scroll-heavy; eval for next-link navigation; moderate interaction overhead |
| var.parts | https://var.parts/ | 3,251 | $0.000 | 52,735 | $0.482 | 16.2× | N/A | Vibium-branded robot parts shop; 41 elements (nav + 12 products with Add to Cart); clean e-commerce; used as vibium MCP test reference site |
| Weather Shopper | https://weathershopper.pythonanywhere.com/ | 2,699 | $0.000 | 26,494 | $0.688 | 9.8× | N/A | 3-page e-commerce flow (temperature check → product selection → checkout); no mandatory sleeps; 13.0× |
| XYZ Bank | https://www.globalsqa.com/angularJs-protractor/BankingProject/ | 2,863 | $0.000 | 20,551 | $0.389 | 7.2× | N/A | AngularJS; ng-model select needs eval+dispatchEvent; Login/Deposit buttons need eval click in MCP; 11.3× |

⁴ Expand Testing L3: navigate directly to /login; eval click on submit; valid login: practice / SuperSecretPassword! → /secure. MCP: eval '#submit-login'.click() for reliability after ad re-render.

---

## Security Testing (11 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (L2) | 21,170ms | 187,318ms | **8.8×** faster |
| LLM turns (v26.3.18) | 19 | 48 | 2.5× fewer |
| Cost (L2) | $0.000 | $3.114 | N/A |

*L2 data (no L3 rerun yet). 7 of 11 sites measured; 4 require local Docker (bWAPP, DVGA, VAmPI, LabEx Cybersecurity) — permanent —.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| bWAPP | local only | — | — | — | — | — | — | 100+ web vulnerabilities; requires local Docker/Apache setup; no public demo; info at itsecgames.com |
| DVGA | local only | — | — | — | — | — | — | Damn Vulnerable GraphQL Application; GraphQL-specific vulnerabilities; requires local Docker; no public hosted demo |
| Firing Range | https://public-firing-range.appspot.com/ | 1,663 | $0.000 | 26,402 | $0.591 | 15.9× | N/A | Google's XSS/CORS/Clickjacking test bed; **MCP map returns 44 DOM XSS entries** on sub-page vs CLI's 10 — MCP more comprehensive on categorized listing pages |
| Gin & Juice Shop | https://ginandjuice.shop/ | 4,052 | $0.000 | 25,193 | $0.397 | 6.2× | N/A | PortSwigger's vulnerable e-commerce; home → 500 server error — use /catalog; search + 17 products accessible; MCP found search form + category filters |
| Google Gruyere | https://google-gruyere.appspot.com/ | 1,741 | $0.000 | 40,519 | $0.499 | 23.3× | N/A | Google security codelab; 60 topic links covering XSS, XSRF, path traversal, code exec; use /start for an isolated session instance |
| LabEx Cybersecurity | https://labex.io/ | — | — | — | — | — | — | Account required; 403 on course pages without login; interactive cybersecurity learning paths |
| OWASP Juice Shop | https://demo.owasp-juice.shop/ | 4,567 | $0.000 | 22,760 | $0.405 | 5.0× | N/A | **Critical behavioral difference:** CLI receives Application Error (Angular SSR crash); **MCP fully loads the app** with 15 products — most significant cross-interface divergence in the dataset |
| OWASP VWAD | https://owasp.org/www-project-vulnerable-web-applications-directory/ | 2,599 | $0.000 | 20,456 | $0.407 | 7.9× | N/A | Directory of vulnerable web apps (not itself a test target); links to the full registry at vwad.owasp.org |
| Try Hack Me | https://tryhackme.com/ | 2,903 | $0.000 | 23,945 | $0.407 | 8.2× | N/A | **Narrowest ratio in Security batch** — heavy Next.js app (7–15s load time) narrows gap; landing page fully accessible; MCP map returns 72 elements; labs require account |
| VAmPI | local only | — | — | — | — | — | — | Vulnerable REST API; OWASP top 10 API vulnerabilities; requires local Docker; no public hosted demo |
| Zero Bank | http://zero.webappsecurity.com/ | 3,645 | $0.000 | 28,043 | $0.408 | 7.7× | N/A | Micro Focus Fortify demo; **HTTP-only** — BiDi error in both CLI and MCP; curl returns 200 but Chrome/BiDi blocks HTTP origins entirely |

---

## API Testing (18 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (best-available) | 112,526ms | 425,229ms | **3.8×** faster |
| LLM turns (v26.3.18) | 3 | 37 | 12× fewer |
| Cost (best-available) | $0.038 | $7.103 | **189.4×** cheaper |

*Best-available data: L3 for 2 new sites (API Challenges, QuickPizza); L2 for 16 original sites. CLI cost non-zero due to API Challenges and QuickPizza L3 brackets.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| Airport Gap | https://airportgap.com/ | 2,428 | $0.000 | 18,691 | $0.446 | 7.7× | N/A | GET list, GET by IATA code, POST distance (KIX→SFO: 8,692km); JSON:API format (data.attributes.*); no auth required |
| API Challenges | https://apichallenges.eviltester.com | 21,141 | $0.020 | 47,283 | $0.091 | 2.2× | 4.5× | **New site (added 2026-06-03):** Evil Tester; 4 sections: Simple API, API Challenges, API Simulator, HTTP Mirror; 15 refs on homepage; structured challenge format with auth, verb practice, payload manipulation |
| AP+ Developers | https://developer.bpaygroup.com.au/ | 3,016 | $0.000 | 20,971 | $0.451 | 7.0× | N/A | Australian payment network developer portal (BPAY, eftpos, NPP, ConnectID); 17 elements; registration required for API access |
| Automation Exercise API | https://www.automationexercise.com/api_list | 5,734 | $0.000 | 23,232 | $0.415 | 4.1× | N/A | GET products/brands, POST searchProduct (form-encoded), POST verifyLogin; uses custom responseCode in body not HTTP status |
| Chuck Norris API | https://api.chucknorris.io/ | 3,489 | $0.000 | 24,366 | $0.524 | 7.0× | N/A | Joke API; 20 MCP elements; category browsing, free-text search, email subscription; no auth for GET endpoints |
| Countries GraphQL | https://countries.trevorblades.com/ | 2,285 | $0.000 | 21,401 | $0.418 | 9.4× | N/A | Live GraphiQL editor; query countries, continents, languages; no auth; execute queries directly in browser |
| FakeRestAPI | https://fakerestapi.azurewebsites.net/ | 5,550 | $0.000 | 22,848 | $0.420 | 4.1× | N/A | Azure-hosted Swagger UI; Activities, Authors, Books, CoverPhotos, Users endpoints; Azure cold start affects both CLI and MCP equally |
| Go REST | https://gorest.co.in/ | 4,543 | $0.000 | 18,924 | $0.421 | 4.2× | N/A | Free REST API; token auth for write operations; code tabs (CURL/JS/Python/Ruby/Go) with live Run button; public read endpoints require no auth |
| httpbin | https://httpbin.org/ | 25,008 | $0.000 | 24,094 | $0.422 | 1.0× | N/A | Full request inspection; GET/POST/status codes/delay/IP all work; CORS-friendly; no auth |
| JSON Placeholder | https://jsonplaceholder.typicode.com/ | 2,400 | $0.000 | 20,272 | $0.423 | 8.4× | N/A | Full CRUD works; writes return 201 but don't persist (shared mock state); no auth; one of the fastest API sites in the dataset |
| Poké API | https://pokeapi.co/ | 3,964 | $0.000 | 24,014 | $0.426 | 6.1× | N/A | Read-only; 1,350 Pokémon; aggressive caching; no auth |
| QuickPizza | https://test-api.k6.io/ | 15,330 | $0.017 | 43,165 | $0.065 | 2.8× | 3.7× | **New site (added 2026-06-03):** Grafana k6 demo; **first WebSocket site in dataset** — live visitor count via WS; "Pizza, Please!" button returns pizza recommendation via REST; Login at `/my/login` (JWT); 6 refs; use eval click on button |
| Restful Booker | https://restful-booker.herokuapp.com/ | 2,185 | $0.000 | 19,457 | $0.539 | 8.9× | N/A | GET list/by-ID, POST auth (admin/password123), POST create booking all work; Heroku cold-start possible |
| Rick and Morty API | https://rickandmortyapi.com/graphql | 3,473 | $0.000 | 18,800 | $0.318 | 5.4× | N/A | GraphQL POST /graphql + REST /api/character/N both work; 826 characters; no auth |
| ServeRest | https://serverest.dev/ | 2,598 | $0.000 | 18,713 | $0.429 | 7.2× | N/A | Brazilian Swagger API for users/products/shopping carts; 113 MCP elements (full Swagger UI); Portuguese/Spanish/English switcher; no auth needed for GET endpoints |
| SpaceTraders | https://spacetraders.io/ | 3,827 | $0.000 | 18,587 | $0.430 | 4.9× | N/A | Space game REST API; 58-link docs site; register/play via API calls; no auth for documentation browsing |
| Swagger Petstore | https://petstore.swagger.io/ | 3,349 | $0.000 | 19,685 | $0.543 | 5.9× | N/A | GET findByStatus, POST pet; shared mutable state — counts vary across sessions; no auth |
| The Cat API | https://thecatapi.com/ | 2,206 | $0.000 | 20,726 | $0.321 | 9.4× | N/A | Cat image API; live voting/breeds/favorites demo on homepage; 29 MCP elements; free API key for write operations |

**API testing note:** CLI is cheaper than MCP for API-only workflows. MCP overhead comes from the protocol layer — each `browser_navigate` + `browser_evaluate` pair generates its own LLM turn. CLI dispatches via bash and the LLM barely participates in execution.  
⁵ httpbin (25,008ms CLI / 24,094ms MCP = 1.0×) is an outlier — CLI hit a slow-response `/delay` endpoint; warm CLI ratio ~10×. Excluding httpbin: API batch CLI 4.4× → 5.7× faster.

---

## Performance Testing (3 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (L2) | 12,550ms | 81,798ms | **6.5×** faster |
| LLM turns (v26.3.18) | 4 | 30 | 7.5× fewer |
| Cost (L2) | $0.000 | $1.858 | N/A |

*L2 data (no L3 rerun yet) — all 3 sites measured.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| Blaze Demo | http://blazedemo.com/index.php | 7,179 | $0.000 | 27,049 | $0.653 | 3.8× | N/A | Full booking flow: search → reserve (5 flights) → purchase form (9 fields); submit via eval select.value + button.click(); 7 departure/destination options |
| Demoblaze | https://demoblaze.com/ | 2,344 | $0.000 | 28,002 | $0.547 | 11.9× | N/A | Categories via #itemc (3s async load); **add-to-cart deadlocks daemon** — pre-stub window.alert before clicking in both interfaces (B3/MB3 still open, deferred); Demoblaze API at api.demoblaze.com |
| Pet Store Web | https://petstore.octoperf.com/actions/Catalog.action | 3,027 | $0.000 | 26,747 | $0.658 | 8.8× | N/A | Login: j2ee / j2ee → "Welcome ABC!"; jsessionid in URL (path-based session, not cookie); map misses image map areas — use area[href] selectors or direct URL navigation |
