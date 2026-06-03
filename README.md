# Practice Testing — Site Directory & CLI vs MCP Comparison

**[Live benchmark page →](https://lana-20.github.io/practice-testing/)** · **[CLI vs MCP behavioral comparison → SKILL.md](SKILL.md#cli-vs-mcp--behavioral-comparison)**

[<video src="cli_mcp_research.mp4" controls width="390"></video>](https://github.com/user-attachments/assets/6d5b211e-7615-4ef5-a9b8-2ad29d7ee622)

<!-- 99 sites across 5 categories · Tested 2026-04-22 to 2026-05-20 · Behavioral notes updated for v26.5.31 (2026-06-01) · Level 2 rerun complete (v26.5.31, 2026-06-03): 94/99 sites measured with per-site CLI ($) / MCP ($) costs via token_bracket.py; 4 local-only security sites permanent —; 1 AT site (Lambdatest Playground) timing-only from original run -->
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
| General Practice | 28 | 198,144 | ~39 | $0.851 | 2,186,552 | ~301 | $15.818 | CLI **11.0×** faster | **7.7×** fewer | **18.6×** cheaper |
| Automation Testing | 41 | 215,251 | ~46 | $0.035 | 1,661,488 | ~317 | $21.783 | CLI **7.7×** faster¹ | **6.9×** fewer | N/A |
| Security Testing | 7 / 11 | 21,170 | 19 | $0.000 | 187,318 | 48 | $3.114 | CLI **8.8×** faster | **2.5×** fewer | N/A |
| API Testing | 16 | 76,055 | 3 | $0.000 | 334,781 | 37 | $6.947 | CLI **4.4×** faster² | **12×** fewer | N/A |
| Performance Testing | 3 | 12,550 | 4 | $0.000 | 81,798 | 30 | $1.858 | CLI **6.5×** faster | **7.5×** fewer | N/A |
| **All sites** | **95 / 99** | **523,170** | **~111** | **$0.886** | **4,451,937** | **~733** | **$49.521** | **CLI 8.5× faster** | **6.6× fewer** | **55.9× cheaper** |

¹ Automation Testing now complete (41/41). Lambdatest Playground MCP requires `eval window.location.href` — `browser_navigate` fails with dead-frame after `browser_stop`/`browser_start`. Expand Testing CLI (13,143ms) elevated due to ad-overlay retries.  
² API ratio narrows due to httpbin serving locally-cached responses (CLI 25,008ms cold-start — warm ratio ~10×). Excluding httpbin: CLI 5.7× faster.

**Key insight:** MCP time per site is fairly uniform (~18–221s regardless of site complexity). CLI time tracks actual site complexity (1.6–25s). The simpler the site, the wider the ratio. The narrowest gaps occur when mandatory sleep floors (3–5s) or large DOM maps absorb MCP's per-tool-call overhead.

**Legend:** `—` = site no longer accessible or local-only (permanent). `N/A` in Cost× = CLI cost is $0.000 (no LLM tokens consumed in CLI bracket — ratio undefined). `CLI/MCP turns (v26.3.18)` = interactive turn counts from the original run using per-command back-and-forth; Level 2 rerun used batch bash scripts so turn counts are not comparable. ms and $ are from the Level 2 v26.5.31 rerun (2026-06-03).

Each section below includes an aggregate token/cost table — turn counts from v26.3.18; ms and $ from Level 2 rerun.

---

## General Practice (28 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (Level 2) | 198,144ms | 2,186,552ms | **11.0×** faster |
| LLM turns (v26.3.18) | ~39 | ~301 | ~7.7× fewer |
| Cost (Level 2) | $0.851 | $15.818 | **18.6×** cheaper |

*Level 2 rerun (v26.5.31, 2026-06-03) — all 28 sites measured.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| AcademyBugs | https://academybugs.com/ | 17,318 | $0.056 | 121,737 | $0.232 | 7.0× | 4.2× | 25 planted bugs; dismiss cookie banner + tutorial modal before interacting; sort select works by label or value (B5 fixed v26.5.31) |
| A11y Coffee | https://a11y.coffee/ | 7,864 | $0.025 | 104,888 | $0.300 | 13.3× | 12.2× | Accessibility learning resource; 13 nav links; dark/light toggle; static site; no mandatory waits |
| Basic Calculator | https://testsheepnz.github.io/BasicCalculator.html | 14,384 | $0.074 | 136,991 | $0.416 | 9.5× | 5.6× | Select operation by label ("Add", "Subtract", etc.) or value ("0"–"4") (B5 fixed v26.5.31); 9 prototype builds selectable; minimal form with no mandatory waits → high MCP overhead ratio |
| Black Box Puzzles | https://blackboxpuzzles.workroomprds.com/ | 3,355 | $0.000 | 28,265 | $0.699 | 8.4× | N/A | **Site restored** (was redirecting to cnarios.com, back as of 2026-06-03); 44 CLI refs; puzzle interactions require coordinate clicks; Flash puzzles still non-functional |
| BookCart | https://bookcart.azurewebsites.net/ | 5,041 | $0.000 | 21,177 | $0.584 | 4.2× | N/A | **Site restored** (was redirecting to cnarios.com, back as of 2026-06-03); Angular Material; 13 CLI refs; search via `input[type=search]` + dispatchEvent |
| Candy Mapper | https://www.candymapper.net/ | 11,367 | $0.112 | 221,227 | $0.493 | 19.5× | 4.4× | UK testing sandbox; 54 MCP elements — county selector, contact form, social links, reCAPTCHA challenge; heavy page content compresses ratio to one of the narrowest in GP |
| Cnarios | https://www.cnarios.com/ | 9,859 | $0.193 | 170,408 | $0.549 | 17.3× | 2.8× | React SPA; homepage nav maps fine in both; challenge cards at /challenges/ not rendered (React routing bug — heading only) |
| Evil Tester | https://testpages.eviltester.com/styled/index.html | 8,528 | $0.193 | 109,603 | $0.287 | 12.9× | 1.5× | Pre-stub window.alert/confirm/prompt via eval BEFORE clicking any alert button (B3/MB3 deadlock still open); CLI eval pre-stub nearly equalizes costs (Cost× 1.5×) |
| Gefälscht CompuTech | https://webtestingcourse.dequecloud.com/ | 3,310 | $0.053 | 42,087 | $0.085 | 12.7× | 1.6× | Intentionally inaccessible site for accessibility testing; contact form needs `input[name=x]` selectors; fast nav → high MCP overhead ratio |
| Parabank | https://parabank.parasoft.com/parabank/admin.htm | 8,975 | $0.000 | 64,745 | $0.128 | 7.2× | N/A | CLI `input[name=customer.firstName]` fails (dot in name); MCP ID-based selectors work fine; run DB Initialize from admin panel before testing |
| Parking Cost Calculator | https://www.shino.de/parkcalc/ | 5,540 | $0.076 | 53,313 | $0.416 | 9.6× | 5.5× | Returns $0.00 consistently in both interfaces — AM/PM radio default or date parse bug on the site itself; select lot by visible label or value (B5 fixed v26.5.31); invalid dates → inline error |
| PHP Travels | http://phptravels.com/demo/ | 12,444 | $0.000 | 36,815 | $0.703 | 3.0× | N/A | **Site redesigned** (2026-06-03): submit no longer crashes — pre-stub `window.alert` then click `#demo`; 71 CLI refs; math captcha field `@e21` still present; fill first/last/email then click @e20 |
| Polymer Shop | https://shop.polymer-project.org/ | 2,463 | $0.000 | 58,708 | $0.446 | 23.8× | N/A | All UI in Web Components shadow DOM — map returns nothing in both; eval+shadowRoot traversal required; Polymer events need mouse_click at bounding-box coords — eval .click() does not fire component events |
| Potion Shop | https://qe-at-cgi-fi.github.io/potion-shop/ | 2,645 | $0.000 | 67,655 | $0.559 | 25.6× | N/A | Medieval order form; 32 form controls (radio for potion type/size/potency, ingredient checkboxes, delivery options, textarea); browser_fill works on all inputs |
| Practice Software Testing | https://practicesoftwaretesting.com/ | 12,386 | $0.069 | 72,014 | $0.640 | 5.8× | 9.2× | Angular; Login is `input[type=submit]` not button — use eval.click(); test login: customer@practicesoftwaretesting.com / welcome01; add to cart works without login |
| PrestaShop | https://demo.prestashop.com/ | 14,854 | $0.000 | 107,277 | $0.442 | 7.2× | N/A | Store in iframe — get inner URL via eval after 5s; subdomain expires in ~2min; use eval location.href for all navigation (vibium go deadlocks daemon); mandatory sleeps compress ratio |
| QA Practice | https://qa-practice.razvanvancea.ro/ | 4,331 | $0.000 | 80,698 | $0.955 | 18.6× | N/A | ADD TO CART uses CSS uppercase — use map refs not text; login at homepage #auth-shop anchor (not /ecommerce/ — 404); pre-stub alert/confirm; login: admin@admin.com / admin123 |
| QA Training Simulator | https://bugeater.web.app/ | 5,626 | $0.000 | 60,147 | $0.552 | 10.7× | N/A | BugEater 2.0 (renumbered #1.1–#7.6 as of 04.2026); two cookie banners (homepage + /app/list); dismiss react-joyride tutorial; direct URL to challenge routes now works — navigate from /app/list for the list |
| Random User Generator | https://randomuser.me/ | 5,984 | $0.000 | 44,359 | $0.425 | 7.4× | N/A | URL-param API calls are the fastest pattern; ?format=csv triggers download and crashes BiDi session (restart required); use eval for large JSON (vibium text overflows at 5000 results) |
| Real World Example Apps | https://codebase.show/projects/realworld | 6,351 | $0.000 | 54,924 | $0.489 | 8.6× | N/A | SvelteKit SPA needs 3s sleep after wait load before content renders; GitHub OAuth required for Sign In; mandatory 3s sleep floor narrows the ratio relative to similar-sized sites |
| testers.ai | https://testers.ai/testing/ | 2,536 | $0.000 | 46,662 | $0.495 | 18.4× | N/A | 59-link checklist index covering WCAG A/AA/AAA, screen reader, keyboard, color, ARIA, forms, security, privacy, code quality, i18n, GenAI, DevOps, and more |
| Test Track | https://testtrack.org/ | 4,845 | $0.000 | 67,995 | $0.953 | 14.0× | N/A | Structured training site; 15 practice modules Basic→Intermediate→Advanced→Expert (buttons, inputs, login, dropdowns, checkboxes, tables, modals, alerts, drag & drop, frames, canvas, 3D chess); used as vibium reference site |
| The Boozang Test Lab | https://thelab.boozang.com/ | 3,873 | $0.000 | 45,876 | $0.555 | 11.8× | N/A | React SPA; 16 challenges; Form Fill saves to shared DB at api.boozang.com; vibium fill works on all inputs; vibium click works on all buttons |
| The iframe Search Engine | https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html | 2,459 | $0.000 | 53,985 | $0.607 | 22.0× | N/A | Use vibium fill for search input; select by visible label or full URL value; "Go search" link opens in a new tab; non-existent select value now errors (B5 fixed v26.5.31) |
| The Internet | http://the-internet.herokuapp.com/ | 9,110 | $0.000 | 79,572 | $1.007 | 8.7× | N/A | 44 examples; hover fails on non-interactive elements; vibium frame context resets per CLI call; TinyMCE iframe via contentDocument; input[type=range] needs eval+dispatchEvent |
| The Random Number Service | https://www.random.org/ | 4,118 | $0.000 | 52,957 | $0.685 | 12.9× | N/A | Cookie banner on load; generator forms not in map — use URL params or eval form.submit(); validation: min>max and num>10000 both trigger errors |
| ToDo List | https://todolist.james.am/#/ | 4,254 | $0.000 | 68,317 | $0.796 | 16.1× | N/A | AngularJS; **counter off-by-1 bug** (shows N-1 active items); dblclick label to enter edit mode; checkbox check "obscured" — use mouse click by coords; no localStorage persistence |
| UI5 Demo Kit | https://ui5.sap.com/#/demoapps | 4,324 | $0.000 | 114,150 | $1.319 | 26.4× | N/A | **v26.5.31 update:** CLI vibium map now returns 137 refs (was nothing in older versions); MCP browser_map returns 128 refs; Shopping Cart "Open App" opens new tab — use browser_new_page for next site to avoid BiDi dead-frame |

³ Parabank MCP inflated by 30s browser_find timeout on non-existent "Register" role. Without timeout: ~54,782ms (11.4×).

---

## Automation Testing (41 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (Level 2) | 215,251ms | 1,661,488ms | **7.7×** faster |
| LLM turns (v26.3.18) | ~46 | ~317 | ~6.9× fewer |
| Cost (Level 2) | $0.035 | $21.783 | N/A |

*Level 2 rerun (v26.5.31, 2026-06-03) — all 41 sites measured.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| Applitools Demo | https://demo.applitools.com/ | 4,059 | $0.000 | 53,709 | $0.746 | 13.2× | N/A | Intentional visual testing site; any credentials accepted including empty; **dashboard shows $350%7** corrupted total (intentional bug); search non-functional; all action links dead (href="#") |
| ATM Practice App | https://qe-at-cgi-fi.github.io/atm/ | 3,181 | $0.000 | 61,111 | $0.944 | 19.2× | N/A | Minimal ATM simulator; 4 elements (DEBUG, ADMIN, number input, WITHDRAW); pure overhead exposure — one of the widest ratios for minimal-DOM sites |
| Automate Now Sandbox | https://automatenow.io/sandbox-automation-testing-practice-website/ | 7,819 | $0.000 | 65,191 | $0.510 | 8.3× | N/A | Submit fires window.alert — pre-stub required; slider needs eval+dispatchEvent; **MCP submit button obscured** (receivesEvents check failed) — use browser_evaluate fallback; name input needs click before fill |
| Automation Bookstore | https://automationbookstore.dev/ | 3,423 | $0.000 | 34,130 | $0.304 | 10.0× | N/A | Filter-only SPA; all 8 book hrefs="#" (no detail pages); case-insensitive real-time filter hides via CSS class — screenshot needed to verify filter state |
| Automation Camp | https://play2.automationcamp.ir/ | 4,086 | $0.000 | 55,109 | $0.375 | 13.5× | N/A | Alert button deadlocks daemon — eval override doesn't prevent it, restart required; valid login: test/test; input[type=date] needs eval not fill |
| Automation Exercise | https://www.automationexercise.com/ | 6,301 | $0.000 | 104,327 | $0.791 | 16.6× | N/A | Ad overlay intercepts nav clicks on homepage — use direct URLs; dismiss "Close" SVG button before interacting; full e-commerce flow works; test cases at /test_cases |
| Automation in Testing | https://automationintesting.online/#/ | 3,901 | $0.000 | 59,422 | $0.745 | 15.2× | N/A | Full B&B booking site; 33 MCP refs; contact form at @e17–@e22; #description textarea needs eval+dispatchEvent; Submit @e22 browser_click works directly |
| Automation Test Store | https://automationteststore.com/ | 5,741 | $0.000 | 48,482 | $0.539 | 8.4× | N/A | AbanteCart; search by keyword URL param; get product_id from search result href; Add to Cart via `eval document.querySelector('a.cart').click()` (browser_click fails — zero-size); full cart confirmed |
| Automation Testing Practice | https://testautomationpractice.blogspot.com/ | 3,215 | $0.000 | 39,710 | $0.415 | 12.4× | N/A | Blogger single long page; **both CLI and MCP map return 82 elements** (old "CLI returns nothing" note outdated); date input needs eval; radio/checkbox browser_click fails — use eval; alert buttons deadlock — pre-stub |
| Coffee Cart | https://coffee-cart.app/ | 3,138 | $0.000 | 55,061 | $0.693 | 17.5× | N/A | Vue SPA; 4 map refs only — product cards not in map; data-test attrs exist but `browser_click '[data-test=X]'` fails — use `eval querySelector.click()`; checkout Submit also needs eval click; checkout modal: name + email required |
| Commit Quality | https://commitquality.com/ | 2,954 | $0.000 | 41,571 | $0.473 | 14.1× | N/A | Clean React app; map correctly identifies nav + filter + product elements in both interfaces |
| Contact List App | https://thinking-tester-contact-list.herokuapp.com/ | 2,993 | $0.000 | 60,554 | $0.686 | 20.2× | N/A | Heroku app; login required for all operations; full CRUD contact management flow works |
| Demo SaaS | https://demo-saas.bugbug.io/ | 3,519 | $0.000 | 47,499 | $0.591 | 13.5× | N/A | Clean SPA; minimal interaction; MCP 13.5s is among the fastest MCP times in dataset; 12.7× pure overhead ratio |
| DemoQA | https://demoqa.com/ | 8,549 | $0.000 | 42,296 | $0.488 | 4.9× | N/A | Component library; 7 practice sections (Elements, Forms, Alerts/Frames/Windows, Widgets, Interactions, Book Store); many sub-pages; clean map in both interfaces |
| Expand Testing | https://practice.expandtesting.com/ | 13,143 | $0.000 | 29,170 | $0.485 | 2.2× | N/A | Login button obscured by ad — use `dispatchEvent(MouseEvent)` on submit; valid login: practice / SuperSecretPassword!; navigate directly to /login (not homepage) |
| GitHub Users Search | https://gh-users-search.netlify.app/ | 3,550 | $0.000 | 34,797 | $0.498 | 9.8× | N/A | React GitHub user search; default user pre-loaded; 34 elements (search input + submit + follower links); clean minimal SPA |
| Global SQA Demo | http://www.globalsqa.com/demo-site/ | 6,171 | $0.000 | 33,769 | $0.375 | 5.5× | N/A | **Key behavioral difference:** CLI gets BiDi error on http:// URL; **MCP silently follows HTTP→HTTPS redirect** and loads site successfully; MCP maps 49 interactive elements |
| GreenKart | https://rahulshettyacademy.com/seleniumPractise/#/ | 8,351 | $0.000 | 29,658 | $0.446 | 3.6× | N/A | Angular; 31 products; **MCP browser_map returns 126 elements** (31 products × 4 controls); large map call compresses ratio to 2.8× — one of the narrowest Automation ratios |
| Hands-On Selenium WebDriver | https://bonigarcia.dev/selenium-webdriver-java/ | 3,274 | $0.000 | 27,098 | $0.396 | 8.3× | N/A | Static site; 30 practice sub-pages at clean URLs; fill works on textarea (B7/MB7 fixed v26.5.31); calculator buttons are span.btn not button (use eval) |
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

⁴ Expand Testing CLI (13,143ms) is elevated due to ad-overlay retries before login form is reachable. MCP navigates directly (29,170ms). All Level 2 values are from clean runs.

---

## Security Testing (11 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (Level 2) | 21,170ms | 187,318ms | **8.8×** faster |
| LLM turns (v26.3.18) | 19 | 48 | 2.5× fewer |
| Cost (Level 2) | $0.000 | $3.114 | N/A |

*Level 2 rerun (v26.5.31, 2026-06-03) — 7 of 11 sites measured. 4 require local Docker setup (bWAPP, DVGA, VAmPI, LabEx Cybersecurity) — permanent —.*

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

## API Testing (16 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (Level 2) | 76,055ms | 334,781ms | **4.4×** faster |
| LLM turns (v26.3.18) | 3 | 37 | 12× fewer |
| Cost (Level 2) | $0.000 | $6.947 | N/A |

*Level 2 rerun (v26.5.31, 2026-06-03) — all 16 sites measured.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| Airport Gap | https://airportgap.com/ | 2,428 | $0.000 | 18,691 | $0.446 | 7.7× | N/A | GET list, GET by IATA code, POST distance (KIX→SFO: 8,692km); JSON:API format (data.attributes.*); no auth required |
| AP+ Developers | https://developer.bpaygroup.com.au/ | 3,016 | $0.000 | 20,971 | $0.451 | 7.0× | N/A | Australian payment network developer portal (BPAY, eftpos, NPP, ConnectID); 17 elements; registration required for API access |
| Automation Exercise API | https://www.automationexercise.com/api_list | 5,734 | $0.000 | 23,232 | $0.415 | 4.1× | N/A | GET products/brands, POST searchProduct (form-encoded), POST verifyLogin; uses custom responseCode in body not HTTP status |
| Chuck Norris API | https://api.chucknorris.io/ | 3,489 | $0.000 | 24,366 | $0.524 | 7.0× | N/A | Joke API; 20 MCP elements; category browsing, free-text search, email subscription; no auth for GET endpoints |
| Countries GraphQL | https://countries.trevorblades.com/ | 2,285 | $0.000 | 21,401 | $0.418 | 9.4× | N/A | Live GraphiQL editor; query countries, continents, languages; no auth; execute queries directly in browser |
| FakeRestAPI | https://fakerestapi.azurewebsites.net/ | 5,550 | $0.000 | 22,848 | $0.420 | 4.1× | N/A | Azure-hosted Swagger UI; Activities, Authors, Books, CoverPhotos, Users endpoints; Azure cold start affects both CLI and MCP equally |
| Go REST | https://gorest.co.in/ | 4,543 | $0.000 | 18,924 | $0.421 | 4.2× | N/A | Free REST API; token auth for write operations; code tabs (CURL/JS/Python/Ruby/Go) with live Run button; public read endpoints require no auth |
| httpbin | https://httpbin.org/ | 25,008 | $0.000 | 24,094 | $0.422 | 1.0× | N/A | Full request inspection; GET/POST/status codes/delay/IP all work; CORS-friendly; no auth |
| JSON Placeholder | https://jsonplaceholder.typicode.com/ | 2,400 | $0.000 | 20,272 | $0.423 | 8.4× | N/A | Full CRUD works; writes return 201 but don't persist (shared mock state); no auth; one of the fastest API sites in the dataset |
| Poké API | https://pokeapi.co/ | 3,964 | $0.000 | 24,014 | $0.426 | 6.1× | N/A | Read-only; 1,350 Pokémon; aggressive caching; no auth |
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
| Time (Level 2) | 12,550ms | 81,798ms | **6.5×** faster |
| LLM turns (v26.3.18) | 4 | 30 | 7.5× fewer |
| Cost (Level 2) | $0.000 | $1.858 | N/A |

*Level 2 rerun (v26.5.31, 2026-06-03) — all 3 sites measured.*

| Site | URL | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Key Finding |
|------|-----|----------|---------|----------|---------|-------|-------|-------------|
| Blaze Demo | http://blazedemo.com/index.php | 7,179 | $0.000 | 27,049 | $0.653 | 3.8× | N/A | Full booking flow: search → reserve (5 flights) → purchase form (9 fields); submit via eval select.value + button.click(); 7 departure/destination options |
| Demoblaze | https://demoblaze.com/ | 2,344 | $0.000 | 28,002 | $0.547 | 11.9× | N/A | Categories via #itemc (3s async load); **add-to-cart deadlocks daemon** — pre-stub window.alert before clicking in both interfaces (B3/MB3 still open, deferred); Demoblaze API at api.demoblaze.com |
| Pet Store Web | https://petstore.octoperf.com/actions/Catalog.action | 3,027 | $0.000 | 26,747 | $0.658 | 8.8× | N/A | Login: j2ee / j2ee → "Welcome ABC!"; jsessionid in URL (path-based session, not cookie); map misses image map areas — use area[href] selectors or direct URL navigation |
