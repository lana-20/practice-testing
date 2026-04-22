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
| Evil Tester | https://testpages.eviltester.com/styled/index.html | Automation & exploratory testing pages |
| Gefälscht CompuTech | https://webtestingcourse.dequecloud.com/ | Fake site by Deque Systems |
| Magento | https://magento.softwaretestingboard.com/ | Demo store, no orders fulfilled |
| Parabank | https://parabank.parasoft.com/parabank/admin.htm | Bank website for testing |
| Parking Cost Calculator | https://www.shino.de/parkcalc/ | Simple web app for exploration |
| PHP Travels | http://phptravels.com/demo/ | Demo travel site |
| Polymer Shop | https://shop.polymer-project.org/ | E-commerce for testing |
| Practice Software Testing | https://practicesoftwaretesting.com/ | Angular app + REST API + Swagger |
| Presta Shop | https://demo.prestashop.com/#/en/front | E-commerce demo |
| QA Practice | https://qa-practice.netlify.app/ | Web elements, buggy forms, e-commerce e2e |
| QA Training Simulator | https://bugeater.web.app/ | Manual testing for beginners |
| Random User Generator | https://randomuser.me/ | API for random user data |
| Real World Example Apps | https://codebase.show/projects/realworld | Same app in different frameworks |
| The Boozang Test Lab | https://thelab.boozang.com/ | Web automation practice |
| The iframe Search Engine | http://compendiumdev.co.uk/apps/iframe-search/iframe-search.html | iframe testing |
| The Internet | http://the-internet.herokuapp.com/ | Checkboxes, hovers, redirects, etc. |
| The Random Number Service | https://www.random.org/ | Exploratory testing practice |
| Testing Challenges | http://testingchallenges.thetestingmap.org/ | Puzzles and challenges |
| ToDo List | https://todolist.james.am/#/ | Todo app with bugs |
| UI5 Demo Kit | https://ui5.sap.com/#/demoapps | SAP UI5 demo apps |

### Automation Testing

| Name | URL |
|------|-----|
| Automation Bookstore | https://automationbookstore.dev/ |
| Automation Camp | https://play2.automationcamp.ir/ |
| Applitools Demo | https://demo.applitools.com/ |
| Automation Exercise | https://www.automationexercise.com/ |
| Automation in Testing | https://automationintesting.online/#/ |
| Automation Testing Practice | https://testautomationpractice.blogspot.com/ |
| Automation Test Store | https://automationteststore.com/ |
| Automate Now Sandbox | https://automatenow.io/sandbox-automation-testing-practice-website/ |
| Expand Testing | https://practice.expandtesting.com/ |
| Coffee Cart | https://coffee-cart.app/ |
| Commit Quality | https://commitquality.com/ |
| Contact List App | https://thinking-tester-contact-list.herokuapp.com/ |
| Demo SaaS | https://demo-saas.bugbug.io/ |
| GreenKart | https://rahulshettyacademy.com/seleniumPractise/#/ |
| Global SQA Demo | http://www.globalsqa.com/demo-site/ |
| Hands-On Selenium WebDriver | https://bonigarcia.dev/selenium-webdriver-java/ |
| Lambdatest Playground | https://ecommerce-playground.lambdatest.io/ |
| Let Code | https://letcode.in/test |
| Locator Game | https://testsmith-io.github.io/locator-game/ |
| Practice Test Automation | https://practicetestautomation.com/practice/ |
| QA Playground | https://qaplayground.dev/ |
| React Shopping Cart | https://react-shopping-cart-67954.firebaseapp.com/ |
| Selectors Hub | https://selectorshub.com/xpath-practice-page/ |
| Selenium Playground | https://www.lambdatest.com/selenium-playground/ |
| Swag Labs | https://www.saucedemo.com/ |
| Sweet Shop | https://sweetshop.netlify.app/ |
| Tricentis Obstacle Course | https://obstaclecourse.tricentis.com/Obstacles |
| UI Test Automation Playground | http://uitestingplayground.com/ |
| Weather Shopper | https://weathershopper.pythonanywhere.com/ |
| XYZ Bank | https://www.globalsqa.com/angularJs-protractor/BankingProject/ |

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
