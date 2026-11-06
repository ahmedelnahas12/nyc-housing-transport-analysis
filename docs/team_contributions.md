# Team Contributions Log

**Project:** NYC Housing & Transportation Data Engineering & Visualization  
**Course:** GIU Data Engineering and Visualization, Winter 2026  
**Milestone:** 1 (Due: November 9, 2026)  
**Team Size:** 4 Members  

---

## Member 1 — Housing Dataset & Cleaning

**Primary Responsibility:** Select, load, explore, clean, and document the housing dataset (H2: Affordable Housing Production by Building). Develop 2 research questions + 2 visualizations using integrated data.

### Completed Tasks:
- [ ] **Dataset Selection:** Chose H2 (Affordable Housing Production by Building) from NYC Open Data
  - Dataset ID: `hg8x-zxpr` (SODA API)
  - 41 columns, building-level granularity
  - Integration fields: Borough, ZIP Code (postcode), Street Name, Building Completion Date, Latitude/Longitude, Community Board, Census Tract

- [ ] **Exploratory Data Analysis (EDA):**
  - Column inventory, data types, missing value analysis
  - Duplicate detection (exact rows + key columns)
  - Descriptive statistics (numeric & categorical)
  - Outlier detection via IQR on unit count columns

- [ ] **Pre-Integration Cleaning:**
  - Standardized column names to snake_case
  - Standardized borough names to title case
  - Fixed ZIP codes: converted float to zero-padded 5-digit strings
  - Parsed date columns to datetime, extracted year
  - Handled missing coordinates (dropped rows missing both lat/long)
  - Flagged outliers in unit counts (IQR method) — documented but not removed

- [ ] **Documentation:** All cleaning decisions justified in notebook with Markdown tables

- [ ] **Aggregated Fields for Integration:**
  - Created `total_affordable_units` (sum of income-level unit columns)
  - Created `total_units_by_br` (sum of bedroom-type columns)
  - Prepared for ZIP Code × Year aggregation

- [ ] **Validation Visualizations:**
  - Time series: Affordable units by year
  - Stacked bar: Affordable units by borough × year
  - Map: Geographic distribution of projects
  - Pie chart: Unit mix by income category

- [ ] **Research Questions & Visualizations (using integrated data):**
  1. **RQ1:** Which boroughs/ZIP codes saw the most affordable housing units completed per year?
     - Viz: Stacked bar chart (Year × Borough) + Heatmap (Top 20 ZIP × Year)
  2. **RQ2:** What building characteristics correlate with affordable unit production?
     - Viz: Scatter plot (Total Units vs Affordable Units) colored by Construction Type

- [ ] **Saved Output:** `housing_cleaned.csv` for Member 3 integration

---

## Member 2 — Transportation Dataset & Cleaning

**Primary Responsibility:** Select, load, explore, clean, and document the transportation dataset (T2: Traffic Volume Counts Historical). Develop 2 research questions + 2 visualizations using integrated data.

### Completed Tasks:
- [ ] **Dataset Selection:** Chose T2 (Traffic Volume Counts Historical) from NYC Open Data
  - Dataset ID: `6fi9-q3ta` (Views API)
  - 12 columns, hourly granularity per location
  - Integration fields: Location, Latitude/Longitude, Date (hour_beginning), Weather

- [ ] **Exploratory Data Analysis (EDA):**
  - Column inventory, data types, missing value analysis
  - Duplicate detection
  - Unique location identification
  - Descriptive statistics

- [ ] **Pre-Integration Cleaning:**
  - Standardized column names to snake_case
  - Parsed `hour_beginning` to datetime, extracted year/month/day/hour/date
  - Mapped location names to boroughs (Brooklyn Bridge → Brooklyn, etc.)
  - Validated coordinate bounds (NYC geographic limits)
  - Aggregated hourly data to yearly level per location for integration

- [ ] **Documentation:** All cleaning decisions justified in notebook

- [ ] **Validation Visualizations:**
  - Time series: Total annual vehicle volume (all locations)
  - Grouped bar: Annual volume by location
  - Line chart: Average hourly traffic pattern
  - Scatter: Traffic volume vs temperature (if weather data available)

- [ ] **Research Questions & Visualizations (using integrated data):**
  3. **RQ3:** How has traffic volume changed over time on major NYC corridors?
     - Viz: Multi-line chart (Year × Location) with trend lines
  4. **RQ4:** Which locations show the steepest traffic growth/decline?
     - Viz: Bar chart of % change (first year vs last year) by location

- [ ] **Saved Outputs:** 
  - `traffic_cleaned.csv` (raw cleaned)
  - `traffic_yearly.csv` (aggregated to yearly per location) for Member 3

---

## Member 3 — Dataset Integration & Post-Join Cleaning

**Primary Responsibility:** Identify integration key, perform join, post-join cleaning, validation. Develop 2 research questions + 2 visualizations (cross-domain).

### Completed Tasks:
- [ ] **Integration Strategy:** ZIP Code × Year (with Borough cross-check)
  - Justification: Housing has ZIP + year; Traffic has lat/long + year → spatial join to ZIP
  - Aggregation level balances granularity of both datasets

- [ ] **Spatial Join:**
  - Loaded NYC ZIP code boundaries from Open Data (`pri4-ifjk.geojson`)
  - Created GeoDataFrame from traffic points (lat/long)
  - Spatial join (predicate='within') to assign ZIP codes to traffic locations
  - Fallback: manual bridge-to-ZIP mapping for unmatched points

- [ ] **Aggregation to Common Granularity:**
  - Housing: Building-level → ZIP × Year (sum units, count projects/buildings)
  - Traffic: Hourly per location → ZIP × Year (sum volumes across locations in ZIP)

- [ ] **Join Execution:**
  - Outer join on `zip_code`, `year`, `borough` (preserves all ZIP×Year from both)
  - Merge indicator tracked: both / housing-only / traffic-only

- [ ] **Post-Join Cleaning:**
  - Housing-only ZIP×Year: traffic metrics = 0
  - Traffic-only ZIP×Year: housing metrics = 0
  - Dropped merge indicator column
  - Ensured consistent types (year=int, zip_code=string)
  - Derived cross-domain metrics:
    - `affordable_units_per_1k_vehicles`
    - `vehicles_per_affordable_unit`

- [ ] **Validation Visualizations:**
  - Scatter: Housing units vs Traffic volume (cross-domain) with OLS trendline
  - Faceted time series: Housing & traffic trends by borough
  - Heatmaps: Housing units by ZIP×Year, Traffic volume by ZIP×Year

- [ ] **Research Questions & Visualizations (Cross-Domain):**
  5. **RQ5:** Do ZIP codes with more affordable housing completions see larger traffic volume changes?
     - Viz: Scatter plot (ΔHousing% vs ΔTraffic%) by ZIP with trendline
  6. **RQ6:** Is new affordable housing concentrated near high-traffic or low-traffic corridors?
     - Viz: Map with affordable housing projects overlaid on traffic context

- [ ] **Saved Output:** `integrated_data.csv` (copied to `website/data/` for dashboard)

---

## Member 4 — Research Analysis, Storytelling & Website Support

**Primary Responsibility:** Define overall research angle, develop 2 research questions + 2 visualizations (cross-domain), write website story section, coordinate with website team.

### Completed Tasks:
- [ ] **Overall Research Question:** "How does affordable housing development relate to traffic patterns in NYC neighborhoods?"

- [ ] **Research Questions & Visualizations (Cross-Domain):**
  7. **RQ7:** How does traffic volume around new affordable housing compare to citywide averages?
     - Viz: Box plot comparing traffic volume in ZIPs with vs without new affordable housing
  8. **RQ8:** Which communities gained affordable housing but lack transit capacity (low traffic = poor access)?
     - Viz: Quadrant chart (Housing vs Traffic) highlighting "High Housing / Low Traffic" ZIPs

- [ ] **Story Section Content (for Website):**
  - Research question statement
  - Key findings (dynamic, populated from filtered data)
  - Limitations (5 documented items)
  - Impact for NYC (4 stakeholder groups)

- [ ] **Website Coordination:**
  - Provided all 8 chart specifications to Members 5/6
  - Defined filter requirements (Borough, Year, ZIP, Housing Metric, Traffic Metric)
  - Defined search query patterns for natural language search
  - Reviewed dashboard layout and interactivity

- [ ] **Documentation:**
  - Summary table of all 8 RQs + visualizations
  - Cross-domain count: 4/8 visualizations (RQ5, RQ6, RQ7, RQ8) ✅

---

## Members 5 & 6 — Website Interface, Filters, Reports, Deployment

**Shared Responsibility:** Build website, implement filters/search/report, deploy, finalize repo.

### Completed Tasks:
- [ ] **Project Structure Created:**
  ```
  website/
  ├── app.py                          # Main Dash application
  ├── components/
  │   ├── filters.py                  # Dropdown filters, search input, parsing
  │   ├── charts.py                   # 9 chart functions + registry
  │   └── layout.py                   # Main layout structure
  ├── callbacks/
  │   ├── filter_callbacks.py         # Filter & search logic
  │   ├── chart_callbacks.py          # Generate Report → chart updates
  │   └── report_callbacks.py         # Story section updates
  └── assets/
      └── style.css                   # Custom styling
  ```

- [ ] **Filter Components (`filters.py`):**
  - Borough dropdown (multi-select)
  - Year dropdown (multi-select)
  - ZIP Code dropdown (multi-select)
  - Housing Metric dropdown
  - Traffic Metric dropdown
  - Natural language search input + button
  - Generate Report button (primary action)
  - Active filters display
  - Search query parser (extracts borough, year, ZIP, focus keywords)

- [ ] **Chart Components (`charts.py`):**
  - 9 chart functions covering all 8 RQs + faceted time series
  - Chart registry for dynamic loading
  - Consistent styling, hover data, trend lines

- [ ] **Layout (`layout.py`):**
  - Responsive Bootstrap grid (2-column charts, full-width cross-domain)
  - Loading spinners on all charts
  - Story section with 4 panels (Question, Findings, Limitations, Impact)
  - Footer with data source links

- [ ] **Filter Callbacks (`filter_callbacks.py`):**
  - Load full data to browser store on init
  - Apply dropdown filters → filtered data store
  - Parse search query → override dropdowns
  - Sync dropdowns from search
  - Active filters display update

- [ ] **Chart Callbacks (`chart_callbacks.py`):**
  - Generate Report button triggers all 9 charts simultaneously
  - Uses filtered data (or full data if no filters)
  - Error handling per chart

- [ ] **Report Callbacks (`report_callbacks.py`):**
  - Generate Report updates story section
  - Dynamic findings from filtered data:
    - Correlation coefficient
    - Top borough by housing
    - Traffic trend direction
    - Quadrant insight (high housing/low traffic ZIPs)
  - Static limitations & impact lists

- [ ] **Deployment Configuration:**
  - `vercel.json` for Vercel deployment
  - Health check endpoint
  - Requirements.txt with all dependencies

- [ ] **Repository Finalization:**
  - README.md with setup, deployment, team contributions
  - .gitignore for data, venv, IDE files
  - This contributions log

---

## Summary: Deliverables Checklist

| Deliverable | Status | Notes |
|-------------|--------|-------|
| **Notebook 1** - Housing EDA & Cleaning | ✅ | `notebooks/01_housing_eda_cleaning.ipynb` |
| **Notebook 2** - Transport EDA & Cleaning | ✅ | `notebooks/02_transport_eda_cleaning.ipynb` |
| **Notebook 3** - Integration & Post-Join | ✅ | `notebooks/03_integration_postjoin.ipynb` |
| **Notebook 4** - Research Qs & Visualizations | ✅ | `notebooks/04_research_questions_viz.ipynb` |
| **Integrated Dataset** | ✅ | `notebooks/integrated_data.csv` + `website/data/` |
| **8 Research Questions** | ✅ | 2 per member, 4 cross-domain |
| **8 Visualizations** | ✅ | 2 per member, variety of chart types |
| **Website - Filters & Search** | ✅ | 5 dropdowns + natural language search |
| **Website - Generate Report** | ✅ | Updates all 9 charts + story section |
| **Website - Story Section** | ✅ | Dynamic findings, static limitations/impact |
| **Website - Deployed** | ⏳ | Pending Vercel deployment |
| **GitHub Repository** | ⏳ | Pending push |
| **README.md** | ✅ | Complete with setup & contributions |

---

## Submission Package

- **GitHub Repository:** `https://github.com/ahmedelnahas12/nyc-housing-transport-analysis`
- **Deployment Link:** [To be added after Vercel deployment]
- **Dataset Links:**
  - Housing: `https://data.cityofnewyork.us/resource/hg8x-zxpr.csv`
  - Transportation: `https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=download`
- **Team Member IDs:** [To be filled]

---

*Last updated: November 6, 2026*