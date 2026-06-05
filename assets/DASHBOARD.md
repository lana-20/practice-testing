# Practice Testing Dashboard

**Interactive visualization of 100-site CLI vs MCP measurement dataset (2026-06-05)**

## View the Dashboard

Open `dashboard.html` in a web browser to see real-time visualizations of CLI vs MCP performance across all practice testing sites.

**Direct link (when deployed):** https://lana-20.github.io/practice-testing/assets/dashboard.html

## Dashboard Sections

### 1. Summary Metrics (Cards)

Nine key statistics organized by type with color-coded sections:

**Meta (Blue):**
- **Total Sites:** 100 across 5 categories

**Speed (Purple):**
- **CLI Total Time:** 17.6 minutes wall-clock aggregate
- **MCP Total Time:** 68.9 minutes wall-clock aggregate
- **Speed Ratio:** 3.9× (MCP is 3.9× slower than CLI)

**Cost (Green):**
- **CLI Total Cost:** $1.82 cumulative USD
- **MCP Total Cost:** $7.96 cumulative USD
- **Cost Ratio:** 4.4× (MCP costs 4.4× more than CLI)

**Turns (Orange):**
- **CLI Turns Total:** 164 LLM messages across all CLI tests
- **MCP Turns Total:** 1,146 LLM messages across all MCP tests
- **Turns Ratio:** 7.0× (MCP requires 7× more turns than CLI)

### 2. Category Breakdown

**Doughnut Chart** — Site count per category
- General Practice (28 sites)
- Automation Testing (42 sites)
- Security Testing (7 sites)
- API Testing (20 sites)
- Performance Testing (3 sites)

### 3. CLI vs MCP Cost Comparison

**Grouped Bar Chart** — Total cost per category
- Green bars: CLI cost in USD
- Blue bars: MCP cost in USD
- Shows that MCP is consistently more expensive across all categories

### 4. Speed Ratio by Category

**Horizontal Bar Chart** — MCP/CLI timing ratio
- Values > 1 mean MCP is slower
- Automation Testing has the highest ratio (~3.8×), meaning MCP takes 3.8× longer
- API Testing has lower ratios (~3.8×) due to shorter measurement times
- All categories show CLI is faster

### 5. Turn Counts Comparison

**Grouped Bar Chart** — Average turns per site
- Green bars: CLI turns (typically 1–2 per site)
- Blue bars: MCP turns (typically 8–24 per site)
- Shows MCP requires many more LLM interactions per site

### 6. Cost Distribution

**Histogram** — How many sites fall in each cost range (CLI + MCP combined)
- ≤$0.10: Budget sites
- $0.10–$0.20: Most sites
- $0.20–$0.30: Expensive sites
- >$0.30: Very expensive sites (complex interactions)

### 7. Timing Distribution

**Grouped Bar Chart** — Sites by wall-clock duration
- Green: CLI timing bins
- Blue: MCP timing bins
- Shows CLI is bimodal (fast sites + slow outliers), MCP more uniform

### 8. Detailed Site Table

**Sortable & Filterable** — All 100 sites with full metrics

**Columns:**
- **Site:** Site name
- **Category:** Color-coded badge (GP/AT/ST/API/PT)
- **CLI (ms):** Wall-clock time for CLI measurement
- **CLI ($):** Cost in USD for CLI measurement
- **CLI Turns:** LLM turns in CLI test
- **MCP (ms):** Wall-clock time for MCP measurement
- **MCP ($):** Cost in USD for MCP measurement
- **MCP Turns:** LLM turns in MCP test
- **Speed×:** Ratio of MCP/CLI timing (green = CLI faster, red = MCP faster)
- **Cost×:** Ratio of MCP/CLI cost (green = CLI cheaper, red = MCP cheaper)

**Controls:**
1. **Search:** Filter by site name (regex-friendly)
2. **Category:** Show only sites in selected category
3. **Sort:** Order by site name, timing (fast first), cost (cheap first), or speed ratio

**Example queries:**
- Search "AcademyBugs" → single site
- Category "API Testing" → 20 API sites
- Sort "CLI Time (fast first)" → fastest sites top

## Key Findings

| Metric | Value | Note |
|--------|-------|------|
| **Total CLI Cost** | $1.82 | All 100 sites (2026-06-05) |
| **Total MCP Cost** | $7.96 | All 100 sites |
| **Cost Ratio** | 4.4× | MCP costs 4.4× more |
| **CLI Speed** | 17.6m total | Average 10.6s per site |
| **MCP Speed** | 68.9m total | Average 41.4s per site |
| **Speed Ratio** | 3.9× | MCP is 3.9× slower |
| **CLI Turns** | 164 total | Average 1.6 turns per site |
| **MCP Turns** | 1,146 total | Average 11.5 turns per site |
| **Turns Ratio** | 7.0× | MCP requires 7× more turns |
| **Fastest CLI Site** | 4.2s | The iframe Search Engine |
| **Slowest CLI Site** | 25.8s | Gefälscht CompuTech |

## Interpretation

### Why MCP is more expensive
- Requires more LLM turns (12–13 average vs 1–2 for CLI)
- Higher token usage per site
- Still worthwhile for complex interactions

### Why CLI is faster
- Parallel context isolation prevents congestion
- Fewer intermediate steps
- Optimized CLI command patterns

### Cost × Speed tradeoff
- **CLI:** Cheaper, faster, but less flexible
- **MCP:** More expensive, slower, but better error handling and dialog management

## Updates

This dashboard is embedded with CSV data as of **2026-06-05** (measurement complete, all 100 sites measured with bracket v2 protocol).

Data includes 7 fresh measurements taken 2026-06-05:
- Tricentis Obstacle Course, JSON Placeholder, Poké API
- ServeRest, SpaceTraders, Swagger Petstore, The Cat API

To regenerate with new measurements:
1. Update `data/rerun_results.csv` with new measurement rows
2. Run Python script to extract csvData array and update `dashboard.html`
3. Verify metrics calculations (all 10 checks must pass)

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Requires JavaScript enabled
- No external API calls (all data embedded)

---

**Dashboard generated:** 2026-06-05
**Last updated:** 2026-06-05 (7 fresh measurements, metrics verified)
**Data sources:** Bracket v2 measurements (100/100 sites, 7 fresh)
**Measurement approach:** Hybrid parallel CLI + sequential MCP (L3 three-bash bracket with token isolation v2)
**Visualization library:** Chart.js 4.4.0
**Metrics verification:** ✓ All 10 calculations verified accurate
**Data accuracy:** Timing ±50% variance expected (I/O bound), token metrics stable and reliable
