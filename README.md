# NYC Housing & Transportation Data Engineering Project

**Course:** Data Engineering and Visualization, Winter Semester 2026  
  


---

## Team Members (4 Members)

| Member | Role | Responsibilities |
|--------|------|------------------|
| **Member 1** | Housing Dataset & Cleaning | Select/load housing dataset, EDA, cleaning, documentation, 2 research questions + 2 visualizations |
| **Member 2** | Transportation Dataset & Cleaning | Select/load transport dataset, EDA, cleaning, documentation, 2 research questions + 2 visualizations |
| **Member 3** | Dataset Integration & Post-Join Cleaning | Identify integration key, perform join, post-join cleaning, validation, 2 research questions + 2 visualizations |
| **Member 4** | Research Analysis, Storytelling & Website Support | Overall research angle, 2 research questions + 2 visualizations, website story section, coordinate with Members 5/6 |

> **Note:** With 4 members, each contributes 2 research questions + 2 visualizations = **8 total questions & 8 visualizations**.

---

## Project Overview

This project investigates the relationship between **affordable housing development** and **traffic patterns** in New York City by integrating two NYC Open Data datasets:

| Domain | Dataset | API Endpoint |
|--------|---------|--------------|
| **Housing** | Affordable Housing Production by Building (H2) | `https://data.cityofnewyork.us/resource/hg8x-zxpr.csv` |
| **Transportation** | Traffic Volume Counts Historical (T2) | `https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=download` |

**Integration Key:** ZIP Code × Year (aggregated to common geographic-temporal level)

---

## Repository Structure

```
nyc-housing-transport-project/
├── .gitignore
├── README.md
├── requirements.txt
├── vercel.json
├── notebooks/
│   ├── 01_housing_eda_cleaning.ipynb      # Member 1
│   ├── 02_transport_eda_cleaning.ipynb    # Member 2
│   ├── 03_integration_postjoin.ipynb      # Member 3
│   ├── 04_research_questions_viz.ipynb    # Members 1-4 (shared)
│   └── integrated_data.csv                 # Output from Member 3
├── website/
│   ├── app.py                              # Main Dash application
│   ├── components/
│   │   ├── filters.py                      # Dropdown filters, search
│   │   ├── charts.py                       # Visualization components
│   │   └── layout.py                       # Page layout
│   ├── callbacks/
│   │   ├── filter_callbacks.py             # Filter & search logic
│   │   ├── report_callbacks.py             # Generate Report button
│   │   └── chart_callbacks.py              # Chart update logic
│   ├── assets/
│   │   └── style.css                       # Custom styling
│   └── data/
│       └── integrated_data.csv             # Copied from notebooks/
├── data/                                   # Raw data cache (gitignored)
└── docs/
    └── team_contributions.md               # Individual contribution log
```

---

## Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/ahmedelnahas12/nyc-housing-transport-analysis.git
cd nyc-housing-transport-project
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run Notebooks
```bash
jupyter lab notebooks/
```

### 4. Run Website Locally
```bash
cd website
python app.py
# Opens at http://localhost:8050
```

---

## Deployment (Vercel)

**Live Website:** https://nyc-housing-transport-analysis.vercel.app

1. Push to GitHub
2. Connect repo to Vercel
3. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Output Directory:** `website`
   - **Framework Preset:** Other
4. Deploy

---

## Deliverables Checklist

### Notebook & Data
- [ ] Dataset overview & selection rationale with links
- [ ] EDA, pre-integration cleaning (both datasets)
- [ ] Integration methodology & post-join cleaning
- [ ] Validation visualizations
- [ ] Descriptive Markdown documenting all decisions
- [ ] Dataset links and prompts used

### Analysis
- [ ] 8 research questions (2 per member)
- [ ] 8 visualizations (2 per member)
- [ ] At least 1 cross-domain visualization (housing ↔ transport)
- [ ] Story: findings, limitations, NYC impact

### Website
- [ ] Multiple dropdown filters (Borough, Year, Housing category, Transport category)
- [ ] Search mode (natural language queries)
- [ ] Generate Report button (updates all visualizations)
- [ ] Interactive charts (hover, zoom, filter updates)
- [ ] User-friendly, visually consistent layout
- [ ] Deployed on Vercel/Render/Heroku

### Submission
- [ ] GitHub repository with all code
- [ ] README with setup, deployment, team contributions
- [ ] Submission email with team IDs, repo link, deployment link, dataset links

---

## Team Contribution Log

See `docs/team_contributions.md` for detailed breakdown of each member's work.

---

## License

Educational project for GIU Data Engineering and Visualization course.
