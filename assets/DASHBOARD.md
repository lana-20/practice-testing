# Practice Testing — L3 Dashboard

**Interactive visualization of 100-site measurement dataset**

## View the Dashboard

Open `dashboard.html` in a web browser to see real-time visualizations of CLI vs MCP performance across all practice testing sites.

**Direct link (when deployed):** https://lana-20.github.io/practice-testing/assets/dashboard.html

## Dashboard Sections

### 1. Summary Metrics (Cards)

Eight key statistics at a glance:

- **Total Sites:** 100 across 5 categories
- **CLI Total Cost:** Cumulative USD for all CLI measurements
- **MCP Total Cost:** Cumulative USD for all MCP measurements
- **Cost Ratio:** How many times more expensive MCP is vs CLI (e.g., 11.3× means MCP costs 11× more)
- **CLI Total Time:** Wall-clock aggregate across all sites
- **MCP Total Time:** Wall-clock aggregate across all sites
- **Speed Ratio:** How many times slower MCP is vs CLI (e.g., 3.8× means MCP takes 3.8× longer)
- **CLI Turns Total:** LLM message count across all CLI tests

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
| **Total CLI Cost** | $2.07 | All 100 sites |
| **Total MCP Cost** | $23.32 | All 100 sites |
| **Cost Ratio** | 11.3× | MCP is ~11× more expensive |
| **CLI Speed** | 1,020s total | Average 10.2s per site |
| **MCP Speed** | 3,860s total | Average 38.6s per site |
| **Speed Ratio** | 3.8× | MCP is ~3.8× slower |
| **Highest Cost Site** | (varies) | Check dashboard |
| **Fastest CLI Site** | ~4s | Basic Calculator |
| **Slowest CLI Site** | ~26s | Gefälscht CompuTech |

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

This dashboard is embedded with CSV data as of **2026-06-05** (L3 complete).

To regenerate with new measurements:
1. Update `data/rerun_results.csv` with new rows
2. Run `scripts/populate_readme.py` to sync dashboard data
3. Rebuild `dashboard.html` or script data population step

## Browser Compatibility

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Requires JavaScript enabled
- No external API calls (all data embedded)

---

**Dashboard generated:** 2026-06-05
**Data sources:** L3 measurements (100/100 sites)
**Visualization library:** Chart.js 4.4.0
