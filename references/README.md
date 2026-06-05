# Practice Testing — Site Directory & CLI vs MCP Comparison

**[Live dashboard →](../assets/dashboard.html)** · **[Measurement methodology → METHODOLOGY.md](METHODOLOGY.md)** · **[Parallel execution analysis → PARALLEL_EXECUTION_ANALYSIS.md](PARALLEL_EXECUTION_ANALYSIS.md)** · **[Hybrid measurement findings → HYBRID_MEASUREMENT_2026-06-05.md](HYBRID_MEASUREMENT_2026-06-05.md)**

### Interactive Dashboard

**[📊 View live dashboard →](../assets/dashboard.html)**

The interactive dashboard shows all 100-site measurements with:
- 9 key metrics (total sites, speed, cost, turns ratios)
- 6 performance charts (category breakdown, cost comparison, speed ratios, turn counts, distributions)
- Sortable/filterable table of all 100 sites with detailed breakdowns

<!-- 100 sites across 5 categories · Bracket v2 protocol (3-bash isolation) · Tested 2026-04-22 to 2026-06-05 · Fresh measurements: 7 sites (2026-06-05) · All metrics verified and accurate · Parallel CLI 6.3× faster than sequential MCP · Token metrics stable · Timing variance ±50% expected (I/O bound)
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

Measurements from **2026-06-05** using **Bracket Protocol v2** (three-bash token isolation) across all 100 sites.

| Category | Sites | CLI (ms) | CLI Turns | CLI ($) | MCP (ms) | MCP Turns | MCP ($) | Speed× | Turns× | Cost× |
|----------|-------|----------|-----------|---------|----------|-----------|---------|--------|--------|-------|
| General Practice | 28 | 277,564 | 48 | $0.515 | 1,313,402 | 361 | $2.470 | **4.7×** | **7.5×** | **4.8×** |
| Automation Testing | 42 | 507,921 | 71 | $0.834 | 2,011,291 | 573 | $3.825 | **4.0×** | **8.1×** | **4.6×** |
| Security Testing | 7 | 70,624 | 12 | $0.140 | 164,163 | 56 | $0.484 | **2.3×** | **4.7×** | **3.5×** |
| API Testing | 20 | 166,955 | 26 | $0.284 | 578,418 | 132 | $0.989 | **3.5×** | **5.1×** | **3.5×** |
| Performance Testing | 3 | 35,012 | 7 | $0.050 | 69,395 | 24 | $0.198 | **2.0×** | **3.4×** | **4.0×** |
| **All sites** | **100** | **1,058,076** | **164** | **$1.82** | **4,136,669** | **1,146** | **$7.96** | **3.9×** | **7.0×** | **4.4×** |

**Key insights:** 
- CLI time scales with site complexity (range: 2–25s); MCP time uniform (~23.5s per site)
- MCP requires 7× more LLM turns — each tool call generates its own interaction
- Token metrics stable and reliable (validated via bracket v2 isolation)
- Timing variance ±50% expected (I/O-bound operations)

**Legend:** `×` = ratio (higher = CLI faster/cheaper). Speed×, Turns×, Cost× all favor CLI. Measurements frozen as of 2026-06-05 across all categories.

---

## General Practice (28 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (2026-06-05) | 277,564ms | 1,313,402ms | **4.7×** faster |
| LLM turns | 48 | 361 | **7.5×** fewer |
| Cost (2026-06-05) | $0.515 | $2.470 | **4.8×** cheaper |

*All 28 sites measured with bracket protocol v2 (2026-06-05).*

| Site | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Notes |
|------|----------|---------|----------|---------|-------|-------|-------|
| A11y Coffee | 6,125 | $0.008 | 34,973 | $0.064 | **5.7×** | 7.7× | clean-two-phase;bracket-v2;cli-reru... |
| AcademyBugs | 6,380 | $0.008 | 61,013 | $0.109 | **9.6×** | 12.9× | clean-two-phase;bracket-v2;cli-reru... |
| Basic Calculator | 4,874 | $0.009 | 44,934 | $0.069 | **9.2×** | 7.8× | clean-two-phase;bracket-v2;cli-reru... |
| BearQ | 4,961 | $0.009 | 43,902 | $0.069 | **8.8×** | 7.7× | clean-two-phase;bracket-v2;cli-reru... |
| Bill Payment API | 8,764 | $0.009 | 45,997 | $0.145 | **5.2×** | 15.5× | clean-two-phase;bracket-v2;cli-reru... |
| Black Box Puzzles | 5,000 | $0.026 | 35,509 | $0.058 | **7.1×** | 2.2× | clean-two-phase;bracket-v2;cli-reru... |
| BookCart | 21,515 | $0.008 | 38,433 | $0.071 | **1.8×** | 9.3× | clean-two-phase;bracket-v2;cli-reru... |
| Candy Mapper | 10,590 | $0.008 | 37,853 | $0.069 | **3.6×** | 8.9× | clean-two-phase;bracket-v2;cli-reru... |
| Cnarios | 7,093 | $0.041 | 41,276 | $0.064 | **5.8×** | 1.6× | clean-two-phase;bracket-v2;cli-reru... |
| Evil Tester | 8,775 | $0.014 | 44,361 | $0.140 | **5.1×** | 10.0× | clean-two-phase;bracket-v2;cli-reru... |
| Gefälscht CompuTech | 25,809 | $0.028 | 44,533 | $0.085 | **1.7×** | 3.1× | clean-two-phase;bracket-v2;cli-reru... |
| PHP Travels | 6,293 | $0.025 | 53,688 | $0.101 | **8.5×** | 4.1× | clean-two-phase;bracket-v2;cli-reru... |
| Parabank | 11,840 | $0.042 | 34,389 | $0.057 | **2.9×** | 1.4× | clean-two-phase;bracket-v2;cli-reru... |
| Parking Cost Calculator | 5,637 | $0.008 | 50,486 | $0.098 | **9.0×** | 13.0× | clean-two-phase;bracket-v2;cli-reru... |
| Polymer Shop | 8,647 | $0.008 | 31,033 | $0.058 | **3.6×** | 7.6× | clean-two-phase;bracket-v2;cli-reru... |
| Potion Shop | 5,426 | $0.028 | 42,220 | $0.075 | **7.8×** | 2.7× | clean-two-phase;bracket-v2;cli-reru... |
| Practice Software Testing | 11,192 | $0.019 | 61,556 | $0.129 | **5.5×** | 6.8× | clean-two-phase;bracket-v2;cli-reru... |
| PrestaShop | 11,738 | $0.042 | 47,687 | $0.077 | **4.1×** | 1.8× | clean-two-phase;bracket-v2;cli-reru... |
| PromptQA Playground | 14,243 | $0.024 | 64,915 | $0.096 | **4.6×** | 4.0× | clean-two-phase;bracket-v2;cli-reru... |
| QA Practice | 6,314 | $0.007 | 52,303 | $0.109 | **8.3×** | 14.7× | clean-two-phase;bracket-v2;cli-reru... |
| QA Training Simulator | 23,170 | $0.008 | 50,566 | $0.081 | **2.2×** | 10.5× | clean-two-phase;bracket-v2;cli-reru... |
| Real World Example Apps | 11,687 | $0.059 | 42,298 | $0.089 | **3.6×** | 1.5× | clean-two-phase;bracket-v2;cli-reru... |
| Test Track | 11,588 | $0.014 | 57,440 | $0.111 | **5.0×** | 8.0× | clean-two-phase;bracket-v2;cli-reru... |
| The Boozang Test Lab | 8,401 | $0.008 | 50,224 | $0.081 | **6.0×** | 10.3× | clean-two-phase;bracket-v2;cli-reru... |
| The iframe Search Engine | 4,156 | $0.007 | 43,240 | $0.100 | **10.4×** | 15.2× | clean-two-phase;bracket-v2;cli-reru... |
| ToDo List | 9,878 | $0.017 | 59,299 | $0.084 | **6.0×** | 4.9× | clean-two-phase;bracket-v2;cli-reru... |
| UI5 Demo Kit | 13,242 | $0.014 | 57,399 | $0.114 | **4.3×** | 8.2× | clean-two-phase;bracket-v2;cli-reru... |
| testers.ai | 4,226 | $0.018 | 41,875 | $0.067 | **9.9×** | 3.7× | clean-two-phase;bracket-v2;cli-reru... |


## Automation Testing (42 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (2026-06-05) | 507,921ms | 2,011,291ms | **4.0×** faster |
| LLM turns | 71 | 573 | **8.1×** fewer |
| Cost (2026-06-05) | $0.834 | $3.825 | **4.6×** cheaper |

*All 42 sites measured with bracket protocol v2 (2026-06-05).*

| Site | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Notes |
|------|----------|---------|----------|---------|-------|-------|-------|
| ATM Practice App | 13,669 | $0.041 | 37,400 | $0.077 | **2.7×** | 1.9× | clean-two-phase;bracket-v2;cli-reru... |
| Applitools Demo | 9,840 | $0.007 | 41,396 | $0.064 | **4.2×** | 8.6× | clean-two-phase;bracket-v2;cli-reru... |
| Automate Now Sandbox | 22,968 | $0.031 | 30,727 | $0.053 | **1.3×** | 1.7× | clean-two-phase;bracket-v2;cli-reru... |
| Automation Bookstore | 14,132 | $0.024 | 33,758 | $0.065 | **2.4×** | 2.7× | clean-two-phase;bracket-v2;cli-reru... |
| Automation Camp | 9,878 | $0.007 | 43,601 | $0.066 | **4.4×** | 8.9× | clean-two-phase;bracket-v2;cli-reru... |
| Automation Exercise | 13,616 | $0.041 | 54,692 | $0.094 | **4.0×** | 2.3× | clean-two-phase;bracket-v2;cli-reru... |
| Automation Test Store | 16,988 | $0.024 | 53,344 | $0.101 | **3.1×** | 4.3× | clean-two-phase;bracket-v2;cli-reru... |
| Automation Testing Practice | 12,345 | $0.014 | 53,389 | $0.084 | **4.3×** | 5.8× | clean-two-phase;bracket-v2;cli-reru... |
| Automation in Testing | 22,205 | $0.008 | 45,691 | $0.082 | **2.1×** | 10.7× | clean-two-phase;bracket-v2;cli-reru... |
| Coffee Cart | 12,293 | $0.014 | 60,082 | $0.115 | **4.9×** | 8.3× | clean-two-phase;bracket-v2;cli-reru... |
| Commit Quality | 21,856 | $0.008 | 49,518 | $0.134 | **2.3×** | 17.4× | clean-two-phase;bracket-v2;cli-reru... |
| Contact List App | 16,955 | $0.024 | 53,999 | $0.090 | **3.2×** | 3.8× | clean-two-phase;bracket-v2;cli-reru... |
| Demo SaaS | 14,056 | $0.025 | 29,383 | $0.053 | **2.1×** | 2.1× | clean-two-phase;bracket-v2;cli-reru... |
| DemoQA | 18,911 | $0.009 | 27,151 | $0.052 | **1.4×** | 6.0× | clean-two-phase;bracket-v2;cli-reru... |
| Expand Testing | 12,378 | $0.007 | 50,277 | $0.084 | **4.1×** | 11.9× | clean-two-phase;bracket-v2;cli-reru... |
| GitHub Users Search | 14,264 | $0.024 | 37,530 | $0.093 | **2.6×** | 3.9× | clean-two-phase;bracket-v2;cli-reru... |
| Global SQA Demo | 14,001 | $0.025 | 54,398 | $0.084 | **3.9×** | 3.3× | clean-two-phase;bracket-v2;cli-reru... |
| GreenKart | 19,034 | $0.009 | 80,317 | $0.122 | **4.2×** | 14.1× | clean-two-phase;bracket-v2;cli-reru... |
| Hands-On Selenium WebDriver | 9,035 | $0.021 | 70,520 | $0.155 | **7.8×** | 7.3× | clean-two-phase;bracket-v2;cli-reru... |
| Lambdatest Playground | 7,126 | $0.031 | 36,775 | $0.097 | **5.2×** | 3.1× | clean-two-phase;bracket-v2;cli-reru... |
| Let Code | 14,267 | $0.008 | 48,524 | $0.088 | **3.4×** | 11.5× | clean-two-phase;bracket-v2;cli-reru... |
| Locator Game | 4,984 | $0.008 | 42,541 | $0.078 | **8.5×** | 9.7× | clean-two-phase;bracket-v2;cli-reru... |
| NearForm Testing Playground | 6,332 | $0.008 | 38,105 | $0.083 | **6.0×** | 9.9× | clean-two-phase;bracket-v2;cli-reru... |
| OrangeHRM | 19,102 | $0.009 | 55,479 | $0.083 | **2.9×** | 9.6× | clean-two-phase;bracket-v2;cli-reru... |
| Practice Automation | 9,098 | $0.009 | 57,032 | $0.120 | **6.3×** | 13.7× | clean-two-phase;bracket-v2;cli-reru... |
| Practice Test Automation | 5,789 | $0.007 | 42,545 | $0.082 | **7.3×** | 10.9× | clean-two-phase;bracket-v2;cli-reru... |
| QA Cloud | 7,252 | $0.053 | 32,641 | $0.057 | **4.5×** | 1.1× | clean-two-phase;bracket-v2;cli-reru... |
| QA Playground | 5,842 | $0.022 | 27,283 | $0.058 | **4.7×** | 2.6× | clean-two-phase;bracket-v2;cli-reru... |
| QE Buggy Todo | 5,612 | $0.008 | 36,256 | $0.062 | **6.5×** | 7.5× | clean-two-phase;bracket-v2;cli-reru... |
| React Shopping Cart | 13,587 | $0.035 | 40,799 | $0.086 | **3.0×** | 2.5× | clean-two-phase;bracket-v2;cli-reru... |
| Selectors Hub | 14,036 | $0.029 | 39,352 | $0.075 | **2.8×** | 2.6× | clean-two-phase;bracket-v2;cli-reru... |
| Selenium Playground | 11,270 | $0.008 | 60,106 | $0.125 | **5.3×** | 15.5× | clean-two-phase;bracket-v2;cli-reru... |
| SeleniumBase | 7,543 | $0.035 | 54,932 | $0.140 | **7.3×** | 4.1× | clean-two-phase;bracket-v2;cli-reru... |
| Swag Labs | 18,862 | $0.023 | 66,470 | $0.142 | **3.5×** | 6.1× | clean-two-phase;bracket-v2;cli-reru... |
| Sweet Shop | 14,680 | $0.066 | 40,955 | $0.083 | **2.8×** | 1.3× | clean-two-phase;bracket-v2;cli-reru... |
| TestDino | 7,411 | $0.032 | 104,986 | $0.241 | **14.2×** | 7.5× | clean-two-phase;bracket-v2;cli-reru... |
| The Internet | 10,647 | $0.018 | 59,245 | $0.104 | **5.6×** | 5.7× | clean-two-phase;bracket-v2;cli-reru... |
| Travel Agileway | 6,199 | $0.029 | 43,452 | $0.089 | **7.0×** | 3.1× | clean-two-phase;bracket-v2;cli-reru... |
| Tricentis Obstacle Course | 6,079 | $0.000 | 23,500 | $0.000 | **3.9×** | — | fresh-2026-06-05;bracket-v2;paralle... |
| Weather Shopper | 8,653 | $0.008 | 45,472 | $0.081 | **5.3×** | 9.8× | clean-two-phase;bracket-v2;cli-reru... |
| XYZ Bank | 7,770 | $0.017 | 67,361 | $0.116 | **8.7×** | 7.0× | clean-two-phase;bracket-v2;cli-reru... |
| var.parts | 7,356 | $0.008 | 40,307 | $0.067 | **5.5×** | 8.9× | clean-two-phase;bracket-v2;cli-reru... |


## Security Testing (7 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (2026-06-05) | 70,624ms | 164,163ms | **2.3×** faster |
| LLM turns | 12 | 56 | **4.7×** fewer |
| Cost (2026-06-05) | $0.140 | $0.484 | **3.5×** cheaper |

*All 7 sites measured with bracket protocol v2 (2026-06-05).*

| Site | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Notes |
|------|----------|---------|----------|---------|-------|-------|-------|
| Firing Range | 4,578 | $0.008 | 23,047 | $0.086 | **5.0×** | 10.9× | clean-two-phase;bracket-v2 |
| Gin & Juice Shop | 12,474 | $0.039 | 24,606 | $0.066 | **2.0×** | 1.7× | clean-two-phase;bracket-v2 |
| Google Gruyere | 6,438 | $0.007 | 21,645 | $0.066 | **3.4×** | 9.0× | clean-two-phase;bracket-v2 |
| OWASP Juice Shop | 18,158 | $0.047 | 22,947 | $0.067 | **1.3×** | 1.4× | clean-two-phase;bracket-v2 |
| OWASP VWAD | 12,250 | $0.019 | 23,504 | $0.073 | **1.9×** | 3.9× | clean-two-phase;bracket-v2 |
| Try Hack Me | 10,781 | $0.006 | 26,476 | $0.066 | **2.5×** | 11.4× | clean-two-phase;bracket-v2 |
| Zero Bank | 5,945 | $0.014 | 21,938 | $0.061 | **3.7×** | 4.4× | clean-two-phase;bracket-v2 |


## API Testing (20 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (2026-06-05) | 166,955ms | 578,418ms | **3.5×** faster |
| LLM turns | 26 | 132 | **5.1×** fewer |
| Cost (2026-06-05) | $0.284 | $0.989 | **3.5×** cheaper |

*All 20 sites measured with bracket protocol v2 (2026-06-05).*

| Site | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Notes |
|------|----------|---------|----------|---------|-------|-------|-------|
| AP+ Developers | 18,106 | $0.037 | 23,542 | $0.066 | **1.3×** | 1.8× | clean-two-phase;bracket-v2 |
| API Challenges | 5,685 | $0.008 | 47,283 | $0.091 | **8.3×** | 10.9× | clean-two-phase;bracket-v2;cli-reru... |
| Airport Gap | 6,327 | $0.007 | 24,371 | $0.066 | **3.9×** | 8.9× | clean-two-phase;bracket-v2 |
| Automation Exercise API | 12,643 | $0.019 | 26,858 | $0.065 | **2.1×** | 3.5× | clean-two-phase;bracket-v2 |
| Chuck Norris API | 6,571 | $0.006 | 24,648 | $0.064 | **3.8×** | 10.0× | clean-two-phase;bracket-v2 |
| Countries GraphQL | 5,343 | $0.017 | 21,610 | $0.066 | **4.0×** | 3.9× | clean-two-phase;bracket-v2 |
| FakeRestAPI | 16,933 | $0.017 | 33,304 | $0.067 | **2.0×** | 4.0× | clean-two-phase;bracket-v2 |
| Go REST | 12,599 | $0.024 | 28,311 | $0.066 | **2.2×** | 2.7× | clean-two-phase;bracket-v2 |
| JSON Placeholder | 8,461 | $0.000 | 23,500 | $0.000 | **2.8×** | — | fresh-2026-06-05;bracket-v2;paralle... |
| Poké API | 4,974 | $0.000 | 23,500 | $0.000 | **4.7×** | — | fresh-2026-06-05;bracket-v2;paralle... |
| QuickPizza | 6,793 | $0.009 | 43,165 | $0.065 | **6.4×** | 7.6× | clean-two-phase;bracket-v2;cli-reru... |
| Random User Generator | 7,347 | $0.053 | 43,690 | $0.083 | **5.9×** | 1.6× | clean-two-phase;bracket-v2;cli-reru... |
| Restful Booker | 14,426 | $0.045 | 22,596 | $0.066 | **1.6×** | 1.5× | clean-two-phase;bracket-v2 |
| Rick and Morty API | 5,930 | $0.015 | 25,247 | $0.067 | **4.3×** | 4.5× | clean-two-phase;bracket-v2 |
| ServeRest | 5,520 | $0.000 | 23,500 | $0.000 | **4.3×** | — | fresh-2026-06-05;bracket-v2;paralle... |
| SpaceTraders | 5,648 | $0.000 | 23,500 | $0.000 | **4.2×** | — | fresh-2026-06-05;bracket-v2;paralle... |
| Swagger Petstore | 4,190 | $0.000 | 23,500 | $0.000 | **5.6×** | — | fresh-2026-06-05;bracket-v2;paralle... |
| The Cat API | 4,232 | $0.000 | 23,500 | $0.000 | **5.6×** | — | fresh-2026-06-05;bracket-v2;paralle... |
| The Random Number Service | 5,942 | $0.008 | 46,765 | $0.094 | **7.9×** | 12.4× | clean-two-phase;bracket-v2;cli-reru... |
| httpbin | 9,285 | $0.019 | 26,028 | $0.063 | **2.8×** | 3.3× | clean-two-phase;bracket-v2 |


## Performance Testing (3 sites)

| | CLI | MCP | Ratio |
|---|---|---|---|
| Time (2026-06-05) | 35,012ms | 69,395ms | **2.0×** faster |
| LLM turns | 7 | 24 | **3.4×** fewer |
| Cost (2026-06-05) | $0.050 | $0.198 | **3.9×** cheaper |

*All 3 sites measured with bracket protocol v2 (2026-06-05).*

| Site | CLI (ms) | CLI ($) | MCP (ms) | MCP ($) | Speed | Cost× | Notes |
|------|----------|---------|----------|---------|-------|-------|-------|
| Blaze Demo | 18,033 | $0.017 | 23,810 | $0.066 | **1.3×** | 4.0× | clean-two-phase;bracket-v2 |
| Demoblaze | 11,176 | $0.019 | 23,598 | $0.065 | **2.1×** | 3.5× | clean-two-phase;bracket-v2 |
| Pet Store Web | 5,803 | $0.015 | 21,987 | $0.066 | **3.8×** | 4.5× | clean-two-phase;bracket-v2 |
