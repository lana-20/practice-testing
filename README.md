# Practice Testing — Site Directory & CLI vs MCP Comparison

**[Live benchmark page →](https://lana-20.github.io/practice-testing/)** · **[CLI vs MCP behavioral comparison → SKILL.md](SKILL.md#cli-vs-mcp--behavioral-comparison)**

[<video src="cli_mcp_research.mp4" controls width="390"></video>](https://github.com/user-attachments/assets/6d5b211e-7615-4ef5-a9b8-2ad29d7ee622)

<!-- 99 sites across 5 categories · Tested 2026-04-22 to 2026-05-20 · Per-section token stats added 2026-06-01 · Behavioral notes updated for v26.5.31 (2026-06-01): B5 select now by label+value; B7/MB7 textarea fill fixed; MB5/MB6/MB9 MCP serialization fixed; B3/MB3 dialog deadlock still open (deferred) -->
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

| Category | Sites | CLI (ms) | MCP (ms) | Speed | Cost |
|----------|-------|----------|----------|-------|------|
| General Practice | 28 | 107,711 | 863,817 | CLI **8.0×** faster | CLI ~5× cheaper |
| Automation Testing | 41 | 255,969 | 1,066,307 | CLI **4.2×** faster¹ | CLI ~7× cheaper |
| Security Testing | 7 tested / 11 total | 20,946 | 108,500 | CLI **5.2×** faster | CLI ~2.4× cheaper |
| API Testing | 16 | 50,763 | 166,714 | CLI **3.3×** faster² | CLI ~6× cheaper |
| Performance Testing | 3 | 14,179 | 58,093 | CLI **4.1×** faster | CLI **6.1×** cheaper |
| **All sites** | **95 timed / 99 total** | **449,568** | **2,263,431** | **CLI 5.0× faster** | **CLI ~5–9× cheaper** |

¹ Automation Testing totals skewed by two anomalies: CLI Expand Testing daemon i/o timeout (87,302ms) and MCP Let Code repeated BiDi failures (211,405ms). Excluding both: CLI 5.4× faster.  
² API ratio narrows to 3.3× due to SpaceTraders anomaly (MCP faster than CLI — CLI cold start). Excluding SpaceTraders: CLI 4.8× faster.

**Key insight:** MCP time per site is fairly uniform (~7–50s regardless of site complexity). CLI time tracks actual site complexity (0.4s–88s). The simpler the site, the wider the ratio. The narrowest gaps occur when mandatory sleep floors (3–5s) absorb MCP's per-tool-call overhead.

Each section below includes an aggregate token/cost table — LLM turn counts and cost deltas measured from `~/.claude/projects/**/*.jsonl`.

---

## General Practice (28 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time | 107,711ms | 863,817ms | 8.0× faster |
| LLM turns | ~39 | ~301 | ~7.7× fewer |
| Cost | ~$2.09 | ~$10.44 | ~5× cheaper |

*Partial tracking: 23 of 28 sites — Batch 3 CLI data lost to session reset; A11y Coffee, Candy Mapper, Potion Shop, testers.ai, Test Track added without tracking.*

| Site | URL | CLI (ms) | MCP (ms) | Ratio | Key Finding |
|------|-----|----------|----------|-------|-------------|
| AcademyBugs | https://academybugs.com/ | 8,130 | 31,787 | 3.9× | Narrowest GP ratio — cookie banner + tutorial modal overhead equalizes both interfaces; dismiss before interacting; 25 planted bugs; sort select works by label or value (B5 fixed v26.5.31) |
| A11y Coffee | https://a11y.coffee/ | 2,477 | 7,322 | 3.0× | Accessibility learning resource; 13 nav links; dark/light toggle; static site; no mandatory waits |
| Basic Calculator | https://testsheepnz.github.io/BasicCalculator.html | 1,793 | 33,255 | 18.5× | Select operation by label ("Add", "Subtract", etc.) or value ("0"–"4") (B5 fixed v26.5.31); 9 prototype builds selectable; minimal form with no mandatory waits → high MCP overhead ratio |
| Black Box Puzzles | https://blackboxpuzzles.workroomprds.com/ | 1,565 | 19,275 | 12.3× | Most puzzles require Flash — only 7 work (22, 24, 26b, 29, 31, 33, 34); use `mouse click x y`, not map refs; no sleep floors so MCP overhead fully exposed |
| BookCart | https://bookcart.azurewebsites.net/ | 5,863 | 35,356 | 6.0× | Azure backend frequently hibernated — only 1 mat-card visible after 3s wait in both interfaces; 3s mandatory sleep floor compresses ratio |
| Candy Mapper | https://www.candymapper.net/ | 5,720 | 10,979 | 1.9× | UK testing sandbox; 54 MCP elements — county selector, contact form, social links, reCAPTCHA challenge; heavy page content compresses ratio to one of the narrowest in GP |
| Cnarios | https://www.cnarios.com/ | 2,471 | 15,238 | 6.2× | React SPA; homepage nav maps fine in both; challenge cards at /challenges/ not rendered (React routing bug — heading only) |
| Evil Tester | https://testpages.eviltester.com/styled/index.html | 7,429 | 19,491 | 2.6× | **Narrowest ratio in dataset** — alert pre-stub via eval nearly equalizes both interfaces; pre-stub window.alert/confirm/prompt BEFORE clicking any alert button |
| Gefälscht CompuTech | https://webtestingcourse.dequecloud.com/ | 1,288 | 18,556 | 14.4× | Intentionally inaccessible site for accessibility testing; contact form needs `input[name=x]` selectors; fast nav → high MCP overhead ratio |
| Parabank | https://parabank.parasoft.com/parabank/admin.htm | 4,825 | 84,782³ | 17.6×³ | CLI `input[name=customer.firstName]` fails (dot in name); MCP ID-based selectors work fine; run DB Initialize from admin panel before testing |
| Parking Cost Calculator | https://www.shino.de/parkcalc/ | 4,171 | 29,675 | 7.1× | Returns $0.00 consistently in both interfaces — AM/PM radio default or date parse bug on the site itself; select lot by visible label or value (B5 fixed v26.5.31); invalid dates → inline error |
| PHP Travels | http://phptravels.com/demo/ | 1,711 | 43,164 | 25.2× | Submit button deadlocks daemon — pre-stub dialogs first; Login nav link broken (redirects same page); 25.2× — minimal DOM, no mandatory waits |
| Polymer Shop | https://shop.polymer-project.org/ | 8,619 | 49,408 | 5.7× | All UI in Web Components shadow DOM — map returns nothing in both; eval+shadowRoot traversal required; mandatory 3–5s sleeps compress ratio to 5.7× |
| Potion Shop | https://qe-at-cgi-fi.github.io/potion-shop/ | 577 | 8,874 | 15.4× | Medieval order form; 32 form controls (radio for potion type/size/potency, ingredient checkboxes, delivery options, textarea); browser_fill works on all inputs |
| Practice Software Testing | https://practicesoftwaretesting.com/ | 4,905 | 30,944 | 6.3× | Angular; Login is `input[type=submit]` not button — use eval.click(); test login: customer@practicesoftwaretesting.com / welcome01; add to cart works without login |
| PrestaShop | https://demo.prestashop.com/ | 6,209 | 33,595 | 5.4× | Store in iframe — get inner URL via eval after 5s; subdomain expires in ~2min; use eval location.href for all navigation (vibium go deadlocks daemon); mandatory sleeps compress ratio |
| QA Practice | https://qa-practice.razvanvancea.ro/ | 784 | 27,047 | 34.5× | **Widest ratio in General Practice** (34.5×); CLI ~800ms total; ADD TO CART uses CSS uppercase — use map refs; pre-stub alert/confirm; login: admin@admin.com / admin123 |
| QA Training Simulator | https://bugeater.web.app/ | 2,651 | 39,670 | 15.0× | 23 challenges across 7 categories; cookie banners on homepage + /app/list; dismiss react-joyride overlay; scripted/functional/api routes crash if accessed directly — navigate from /app/list |
| Random User Generator | https://randomuser.me/ | 3,601 | 35,485 | 9.9× | URL-param API calls are the fastest pattern; ?format=csv triggers download and crashes BiDi session (restart required); use eval for large JSON (vibium text overflows at 5000 results) |
| Real World Example Apps | https://codebase.show/projects/realworld | 5,785 | 29,548 | 5.1× | SvelteKit SPA needs 3s sleep after wait load before content renders; GitHub OAuth required for Sign In; mandatory sleep floor narrows ratio to 5.1× |
| testers.ai | https://testers.ai/testing/ | 1,704 | 7,939 | 4.7× | 59-link checklist index covering WCAG A/AA/AAA, screen reader, keyboard, color, ARIA, forms, security, privacy, code quality, i18n, GenAI, DevOps, and more |
| Test Track | https://testtrack.org/ | 2,251 | 4,732 | 2.1× | Structured training site; 15 practice modules Basic→Intermediate→Advanced→Expert (buttons, inputs, login, dropdowns, checkboxes, tables, modals, alerts, drag & drop, frames, canvas, 3D chess); used as vibium reference site |
| The Boozang Test Lab | https://thelab.boozang.com/ | 2,565 | 45,367 | 17.7× | React SPA; 16 challenges; Form Fill saves to shared DB at api.boozang.com; vibium fill works on all inputs; vibium click works on all buttons |
| The iframe Search Engine | https://eviltester.github.io/TestingApp/apps/iframe-search/iframe-search.html | 5,257 | 37,780 | 7.2× | Use vibium fill for search input; select by visible label or full URL value; "Go search" link opens in a new tab; non-existent select value now errors (B5 fixed v26.5.31) |
| The Internet | http://the-internet.herokuapp.com/ | 2,514 | 50,177 | 20.0× | 44 examples; hover fails on non-interactive elements; vibium frame context resets per CLI call; TinyMCE iframe via contentDocument; input[type=range] needs eval+dispatchEvent |
| The Random Number Service | https://www.random.org/ | 1,875 | 27,220 | 14.5× | Cookie banner on load; generator forms not in map — use URL params or eval form.submit(); validation: min>max and num>10000 both trigger errors |
| ToDo List | https://todolist.james.am/#/ | 1,729 | 37,502 | 21.7× | AngularJS; **counter off-by-1 bug** (shows N-1 active items); dblclick label to enter edit mode; checkbox check "obscured" — use mouse click by coords; no localStorage persistence |
| UI5 Demo Kit | https://ui5.sap.com/#/demoapps | 9,242 | 49,649 | 5.4× | **Behavioral difference:** MCP browser_map finds 128 elements on main page; CLI vibium map returns nothing (SAP UI5 Web Components not exposed to CLI map); sleep 3s mandatory |

³ Parabank MCP inflated by 30s browser_find timeout on non-existent "Register" role. Without timeout: ~54,782ms (11.4×).

---

## Automation Testing (41 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time | 255,969ms | 1,066,307ms | 4.2× faster |
| LLM turns | ~46 | ~317 | ~6.9× fewer |
| Cost | ~$1.65 | ~$9.63 | ~6× cheaper |

*Partial tracking: 30 of 41 sites (Batches 6–11); 11 late-added sites not tracked.*

| Site | URL | CLI (ms) | MCP (ms) | Ratio | Key Finding |
|------|-----|----------|----------|-------|-------------|
| Applitools Demo | https://demo.applitools.com/ | 3,000 | 21,959 | 7.3× | Intentional visual testing site; any credentials accepted including empty; **dashboard shows $350%7** corrupted total (intentional bug); search non-functional; all action links dead (href="#") |
| ATM Practice App | https://qe-at-cgi-fi.github.io/atm/ | 383 | 6,301 | 16.4× | Minimal ATM simulator; 4 elements (DEBUG, ADMIN, number input, WITHDRAW); pure overhead exposure — one of the widest ratios for minimal-DOM sites |
| Automate Now Sandbox | https://automatenow.io/sandbox-automation-testing-practice-website/ | 1,777 | 29,648 | 16.7× | Submit fires window.alert — pre-stub required; slider needs eval+dispatchEvent; **MCP submit button obscured** (receivesEvents check failed) — use browser_evaluate fallback; name input needs click before fill |
| Automation Bookstore | https://automationbookstore.dev/ | 491 | 17,664 | 36.0× | **Widest ratio in Automation Testing** (36×); filter-only SPA; all 8 book hrefs="#" (no detail pages); CLI 491ms is the **fastest time in the entire dataset** |
| Automation Camp | https://play2.automationcamp.ir/ | 1,080 | 21,262 | 19.7× | Alert button deadlocks daemon — eval override doesn't prevent it, restart required; valid login: test/test; input[type=date] needs eval not fill |
| Automation Exercise | https://www.automationexercise.com/ | 6,995 | 28,363 | 4.1× | Ad overlay intercepts nav clicks on homepage — use direct URLs; dismiss "Close" SVG button before interacting; full e-commerce flow works; test cases at /test_cases |
| Automation in Testing | https://automationintesting.online/#/ | 2,755 | 31,544 | 11.5× | Full B&B booking site; Check Availability button obscured by calendar — use eval click; contact form #description is framework-driven textarea — use eval+dispatchEvent or browser_type for component state (B7/MB7 fill fix applies to plain textareas) |
| Automation Test Store | https://automationteststore.com/ | 8,175 | 42,741 | 5.2× | AbanteCart e-commerce; full flow: search → detail → cart → checkout; guest checkout available via accountFrm_accountguest radio; vibium select for product variants |
| Automation Testing Practice | https://testautomationpractice.blogspot.com/ | 1,565 | 28,244 | 18.1× | Blogger single long page; **CLI map returns nothing** — eval-only; **MCP map returns 82 elements**; date input needs eval; alert buttons deadlock — pre-stub; Colors dropdown has duplicate option values (red×2, green×2) |
| Coffee Cart | https://coffee-cart.app/ | 27,696⁴ | 35,598 | 1.3×⁴ | Vue SPA; product cards via data-test attribute (not class name); full checkout flow works; name+email required; CLI anomaly: cold server hit (27,696ms); **warm CLI ratio ~18×** |
| Commit Quality | https://commitquality.com/ | 1,689 | 16,517 | 9.8× | Clean React app; map correctly identifies nav + filter + product elements in both interfaces |
| Contact List App | https://thinking-tester-contact-list.herokuapp.com/ | 2,194 | 25,909 | 11.8× | Heroku app; login required for all operations; full CRUD contact management flow works |
| Demo SaaS | https://demo-saas.bugbug.io/ | 1,059 | 13,455 | 12.7× | Clean SPA; minimal interaction; MCP 13.5s is among the fastest MCP times in dataset; 12.7× pure overhead ratio |
| DemoQA | https://demoqa.com/ | 5,316 | 16,401 | 3.1× | Component library; 7 practice sections (Elements, Forms, Alerts/Frames/Windows, Widgets, Interactions, Book Store); many sub-pages; clean map in both interfaces |
| Expand Testing | https://practice.expandtesting.com/ | 87,302⁵ | 44,906 | 0.5×⁵ | Login button obscured — use eval click; valid login: practice / SuperSecretPassword!; **CLI anomaly: daemon i/o timeout** on first navigate (87,302ms); normal CLI ratio ~5.7× |
| GitHub Users Search | https://gh-users-search.netlify.app/ | 2,286 | 7,505 | 3.3× | React GitHub user search; default user pre-loaded; 34 elements (search input + submit + follower links); clean minimal SPA |
| Global SQA Demo | http://www.globalsqa.com/demo-site/ | 3,097 | 20,876 | 6.7× | **Key behavioral difference:** CLI gets BiDi error on http:// URL; **MCP silently follows HTTP→HTTPS redirect** and loads site successfully; MCP maps 49 interactive elements |
| GreenKart | https://rahulshettyacademy.com/seleniumPractise/#/ | 8,134 | 22,470 | 2.8× | Angular; 31 products; **MCP browser_map returns 126 elements** (31 products × 4 controls); large map call compresses ratio to 2.8× — one of the narrowest Automation ratios |
| Hands-On Selenium WebDriver | https://bonigarcia.dev/selenium-webdriver-java/ | 2,615 | 28,412 | 10.9× | Static site; 30 practice sub-pages at clean URLs; fill works on textarea (B7/MB7 fixed v26.5.31); calculator buttons are span.btn not button (use eval) |
| Lambdatest Playground | https://ecommerce-playground.lambdatest.io/ | 8,095 | 34,057 | 4.2× | OpenCart-based e-commerce; category nav obscured by sticky header — use direct URLs; **Add to Cart silently fails for guests** (no error); size select has no values (impossible to add Canon EOS 5D) |
| Let Code | https://letcode.in/test | 14,962 | 211,405⁶ | 14.1×⁶ | Angular; 22 practice sections; **MCP BiDi SSL/privacy error failures** inflated to 211s; clean MCP ratio ~4×; MCP map captures iframe ads, CLI map filters them |
| Locator Game | https://testsmith-io.github.io/locator-game/ | 2,897 | 20,819 | 7.2× | GitHub Pages static locator challenge; clean, no anomalies or mandatory waits |
| NearForm Testing Playground | https://nearform.github.io/testing-playground/ | 845 | 7,338 | 8.7× | 18 challenge cards (Add/Remove, Checkbox, Drag & Drop, Dynamic Table, File Up/Download, Login Form, Notifications, Radio Buttons, Sliders, Tooltips, Various Inputs); language switcher + difficulty filter |
| OrangeHRM | https://opensource-demo.orangehrmlive.com/ | 10,980 | 22,053 | 2.0× | HR management SPA; map returns nothing in both interfaces — eval required for all interactions; login: Admin / admin123; 2.0× reflects heavy JS init time equalizing overhead |
| Practice Automation | https://practice-automation.com/ | 1,933 | 7,553 | 3.9× | 28 nav links covering delays, sliders, tables, iframes, forms, calendars, gestures, spinners, modals, hover, file upload/download; sub-pages at practice-automation.com/* |
| Practice Test Automation | https://practicetestautomation.com/practice/ | 9,338 | 42,713 | 4.6× | Multiple practice pages; valid login: student / Password123!; 2–3s mandatory waits compress ratio to 4.6× |
| QA Cloud | https://www.qacloud.dev/ | 1,089 | 7,476 | 6.9× | Multi-app QA platform; 38 elements (full nav + app cards with Open App / Docs / API Docs links); Login/Register; search bar; no public API credentials needed for browsing |
| QA Playground | https://qaplayground.dev/ | 1,688 | 9,660 | 5.7× | Clean static site; 28+ challenge links; map works in both interfaces; no anomalies |
| QE Buggy Todo | https://qe-at-cgi-fi.github.io/todo | 882 | 7,059 | 8.0× | Single-input todo app with intentional bugs (placeholder typo "What need's to be done?"); 1 map element; minimal DOM → high overhead ratio |
| React Shopping Cart | https://react-shopping-cart-67954.firebaseapp.com/ | 1,744 | 15,338 | 8.8× | Firebase SPA; **MCP map enumerates all 16 products**; **CLI map returns 0** (styled-components hash classes change between builds); CLI still faster due to lower tool overhead |
| SeleniumBase | https://seleniumbase.io/ | 1,766 | 8,959 | 5.1× | Docs site with 256 MCP elements; 52+ demo pages (Coffee Cart, Drag & Drop, Calculator, Shadow DOM, CAPTCHA); CAPTCHA test pages for CF Turnstile, reCAPTCHA v2 |
| Selectors Hub | https://selectorshub.com/xpath-practice-page/ | 3,993 | 15,509 | 3.9× | 125-element XPath practice page; shadow DOM elements disabled; large map narrows ratio (MCP spends proportionally more time on map call itself) |
| Selenium Playground | https://www.lambdatest.com/selenium-playground/ | 5,130 | 20,952 | 4.1× | Cloudflare blocks sub-page navigation (/simple-form-demo) for both; main page maps 156 elements; use direct URL to /simple-form-demo page |
| Swag Labs | https://www.saucedemo.com/ | 1,667 | 18,498 | 11.1× | Clean login→inventory→add-to-cart; login: standard_user / secret_sauce; 6 inventory items; no mandatory sleeps → overhead fully exposed |
| Sweet Shop | https://sweetshop.netlify.app/ | 2,809 | 28,262 | 10.1× | addItem links invisible to both CLI and MCP map — eval required in both; full purchase flow works via eval |
| TestDino | https://storedemo.testdino.com/ | 982 | 7,450 | 7.6× | E-commerce demo; **MCP map: 216 elements** (products repeat across carousel sections); **CLI map returns nothing** (SPA); full product, cart, and FAQ sections accessible via MCP |
| Travel Agileway | http://travel.agileway.net/login | 3,203 | 8,475 | 2.6× | HTTP-only app; MCP silently loads the page (no BiDi error, unlike CLI); 6-element login form (username, password, remember_me, submit); credentials untested |
| Tricentis Obstacle Course | https://obstaclecourse.tricentis.com/Obstacles | 5,536 | 25,179 | 4.5× | Scroll-heavy; eval for next-link navigation; moderate interaction overhead |
| var.parts | https://var.parts/ | 2,199 | 8,271 | 3.8× | Vibium-branded robot parts shop; 41 elements (nav + 12 products with Add to Cart); clean e-commerce; used as vibium MCP test reference site |
| Weather Shopper | https://weathershopper.pythonanywhere.com/ | 2,834 | 36,811 | 13.0× | 3-page e-commerce flow (temperature check → product selection → checkout); no mandatory sleeps; 13.0× |
| XYZ Bank | https://www.globalsqa.com/angularJs-protractor/BankingProject/ | 3,788 | 42,695 | 11.3× | AngularJS; ng-model select needs eval+dispatchEvent; Login/Deposit buttons need eval click in MCP; 11.3× |

⁴ Coffee Cart CLI anomaly: cold server hit (27,696ms); MCP hit warmer server; warm CLI ratio ~18×.  
⁵ Expand Testing CLI anomaly: daemon i/o timeout on first navigate; MCP ran cleanly at 44,906ms. Normal CLI ratio ~5.7×.  
⁶ Let Code MCP anomaly: repeated BiDi navigation failures due to SSL/privacy errors; clean MCP ratio ~4×.

---

## Security Testing (11 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time | 20,946ms | 108,500ms | 5.2× faster |
| LLM turns | 19 | 48 | 2.5× fewer |
| Cost | $0.54 | $1.30 | 2.4× cheaper |

*Full tracking — 7 publicly accessible timed sites. Archive batch included Supercar Showdown (decommissioned); excluded from directory.*

*7 publicly accessible sites timed; 4 require local setup or account (marked —).*

| Site | URL | CLI (ms) | MCP (ms) | Ratio | Key Finding |
|------|-----|----------|----------|-------|-------------|
| bWAPP | local only | — | — | — | 100+ web vulnerabilities; requires local Docker/Apache setup; no public demo; info at itsecgames.com |
| DVGA | local only | — | — | — | Damn Vulnerable GraphQL Application; GraphQL-specific vulnerabilities; requires local Docker; no public hosted demo |
| Firing Range | https://public-firing-range.appspot.com/ | 959 | 11,346 | 11.8× | Google's XSS/CORS/Clickjacking test bed; **MCP map returns 44 DOM XSS entries** on sub-page vs CLI's 10 — MCP more comprehensive on categorized listing pages |
| Gin & Juice Shop | https://ginandjuice.shop/ | 3,137 | 22,635 | 7.2× | PortSwigger's vulnerable e-commerce; home → 500 server error — use /catalog; search + 17 products accessible; MCP found search form + category filters |
| Google Gruyere | https://google-gruyere.appspot.com/ | 1,103 | 11,006 | 10.0× | Google security codelab; 60 topic links covering XSS, XSRF, path traversal, code exec; use /start for an isolated session instance |
| LabEx Cybersecurity | https://labex.io/ | — | — | — | Account required; 403 on course pages without login; interactive cybersecurity learning paths |
| OWASP Juice Shop | https://demo.owasp-juice.shop/ | 5,116 | 33,161 | 6.5× | **Critical behavioral difference:** CLI receives Application Error (Angular SSR crash); **MCP fully loads the app** with 15 products — most significant cross-interface divergence in the dataset |
| OWASP VWAD | https://owasp.org/www-project-vulnerable-web-applications-directory/ | 1,573 | 7,273 | 4.6× | Directory of vulnerable web apps (not itself a test target); links to the full registry at vwad.owasp.org |
| Try Hack Me | https://tryhackme.com/ | 7,719 | 15,741 | 2.0× | **Narrowest ratio in Security batch** — heavy Next.js app (7–15s load time) narrows gap; landing page fully accessible; MCP map returns 72 elements; labs require account |
| VAmPI | local only | — | — | — | Vulnerable REST API; OWASP top 10 API vulnerabilities; requires local Docker; no public hosted demo |
| Zero Bank | http://zero.webappsecurity.com/ | 1,339 | 7,338 | 5.5× | Micro Focus Fortify demo; **HTTP-only** — BiDi error in both CLI and MCP; curl returns 200 but Chrome/BiDi blocks HTTP origins entirely |

---

## API Testing (16 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time | 50,763ms | 166,714ms | 3.3× faster |
| LLM turns | 3 | 37 | 12× fewer |
| Cost | $0.19 | $1.73 | 9.1× cheaper |

*Partial tracking: 9-site original batch (includes removed ReqRes, 8 of which are in this directory); 7 late-added sites not tracked.*

| Site | URL | CLI (ms) | MCP (ms) | Ratio | Key Finding |
|------|-----|----------|----------|-------|-------------|
| Airport Gap | https://airportgap.com/ | 1,372 | 9,317 | 7× | GET list, GET by IATA code, POST distance (KIX→SFO: 8,692km); JSON:API format (data.attributes.*); no auth required |
| AP+ Developers | https://developer.bpaygroup.com.au/ | 2,756 | 9,430 | 3.4× | Australian payment network developer portal (BPAY, eftpos, NPP, ConnectID); 17 elements; registration required for API access |
| Automation Exercise API | https://www.automationexercise.com/api_list | 4,862 | 13,186 | 3× | GET products/brands, POST searchProduct (form-encoded), POST verifyLogin; uses custom responseCode in body not HTTP status |
| Chuck Norris API | https://api.chucknorris.io/ | 2,517 | 7,332 | 2.9× | Joke API; 20 MCP elements; category browsing, free-text search, email subscription; no auth for GET endpoints |
| Countries GraphQL | https://countries.trevorblades.com/ | 1,848 | 7,441 | 4.0× | Live GraphiQL editor; query countries, continents, languages; no auth; execute queries directly in browser |
| FakeRestAPI | https://fakerestapi.azurewebsites.net/ | 8,648 | 16,171 | 1.9× | Azure-hosted Swagger UI; Activities, Authors, Books, CoverPhotos, Users endpoints; Azure cold start affects both CLI and MCP equally |
| Go REST | https://gorest.co.in/ | 2,141 | 9,044 | 4.2× | Free REST API; token auth for write operations; code tabs (CURL/JS/Python/Ruby/Go) with live Run button; public read endpoints require no auth |
| httpbin | https://httpbin.org/ | 1,422 | 12,752 | 9× | Full request inspection; GET/POST/status codes/delay/IP all work; CORS-friendly; no auth |
| JSON Placeholder | https://jsonplaceholder.typicode.com/ | 433 | 9,650 | 22× | **Widest API ratio** (22×); **CLI 433ms — fastest in dataset**; full CRUD works; writes return 201 but don't persist (shared mock state) |
| Poké API | https://pokeapi.co/ | 1,515 | 10,306 | 7× | Read-only; 1,350 Pokémon; aggressive caching; no auth |
| Restful Booker | https://restful-booker.herokuapp.com/ | 1,357 | 8,451 | 6× | GET list/by-ID, POST auth (admin/password123), POST create booking all work; Heroku cold-start possible |
| Rick and Morty API | https://rickandmortyapi.com/graphql | 2,895 | 9,873 | 3× | GraphQL POST /graphql + REST /api/character/N both work; 826 characters; no auth |
| ServeRest | https://serverest.dev/ | 1,502 | 7,671 | 5.1× | Brazilian Swagger API for users/products/shopping carts; 113 MCP elements (full Swagger UI); Portuguese/Spanish/English switcher; no auth needed for GET endpoints |
| SpaceTraders | https://spacetraders.io/ | 14,933 | 10,203 | 0.7×⁷ | Space game REST API; 58-link docs site; **MCP was faster than CLI** — unusual; CLI cold-start on this site unusually slow; register/play via API calls |
| Swagger Petstore | https://petstore.swagger.io/ | 1,347 | 17,599 | 13× | GET findByStatus, POST pet; shared mutable state — counts vary across sessions; no auth |
| The Cat API | https://thecatapi.com/ | 1,215 | 8,288 | 6.8× | Cat image API; live voting/breeds/favorites demo on homepage; 29 MCP elements; free API key for write operations |

**API testing note:** CLI is cheaper than MCP for API-only workflows. MCP overhead comes from the protocol layer — each `browser_navigate` + `browser_evaluate` pair generates its own LLM turn. CLI dispatches via bash and the LLM barely participates in execution.  
⁷ SpaceTraders: CLI cold-start unusually slow (14,933ms); excluding it the API batch ratio is 4.8×.

---

## Performance Testing (3 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time | 14,179ms | 58,093ms | 4.1× faster |
| LLM turns | 4 | 30 | 7.5× fewer |
| Cost | $0.25 | $1.53 | 6.1× cheaper |

*Full tracking — archived batch of 4 sites; Computer Database (DOWN) included in tracking but excluded from directory.*

| Site | URL | CLI (ms) | MCP (ms) | Ratio | Key Finding |
|------|-----|----------|----------|-------|-------------|
| Blaze Demo | http://blazedemo.com/index.php | 5,039 | 20,418 | 4× | Full booking flow: search → reserve (5 flights) → purchase form (9 fields); submit via eval select.value + button.click(); 7 departure/destination options |
| Demoblaze | https://demoblaze.com/ | 4,996 | 21,626 | 4× | Categories via #itemc (3s async load); **add-to-cart deadlocks daemon** — pre-stub window.alert before clicking in both interfaces (B3/MB3 still open, deferred); Demoblaze API at api.demoblaze.com |
| Pet Store Web | https://petstore.octoperf.com/actions/Catalog.action | 4,144 | 16,049 | 4× | Login: j2ee / j2ee → "Welcome ABC!"; jsessionid in URL (path-based session, not cookie); map misses image map areas — use area[href] selectors or direct URL navigation |
