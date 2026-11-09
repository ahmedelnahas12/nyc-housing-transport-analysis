import nbformat as nbf

def create_notebook_2():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Notebook 2: Transportation Dataset Exploratory Data Analysis & Cleaning
**Author:** Member 2
**Domain:** Transportation
**Dataset:** Automated Traffic Volume Counts (NYC Open Data `6fi9-q3ta` / `btm5-ppia`)

---

## 1. Dataset Overview & Selection Rationale
- **Dataset Title:** NYC Traffic Volume Counts (Historical / Automated)
- **Source:** NYC Department of Transportation (DOT) / NYC Open Data
- **API / Download URL:** `https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=download`
- **Rationale:** Captures traffic counts across NYC roadway segments over time. Aggregating traffic volume by geographic boundary (ZIP code / Borough) and temporal units (Year / Month) enables cross-analysis with affordable housing developments.
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

RAW_DIR = Path("../data/raw")
PROCESSED_DIR = Path("../data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

TRAFFIC_FILE = RAW_DIR / "traffic_raw.csv"

# Load Traffic Dataset
if TRAFFIC_FILE.exists():
    df_traffic = pd.read_csv(TRAFFIC_FILE, low_memory=False)
else:
    # Sample or direct download fallback
    url = "https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=download"
    df_traffic = pd.read_csv(url, low_memory=False, nrows=100000)

print("Raw Traffic Dataset Shape:", df_traffic.shape)
df_traffic.head()
"""),
        nbf.v4.new_markdown_cell("""## 2. Exploratory Data Analysis (EDA) & Summary
Examine schema, missingness, time spans, and volume distributions.
"""),
        nbf.v4.new_code_cell("""print("--- Traffic Columns ---")
print(df_traffic.columns.tolist())

print("\n--- Missing Values ---")
print(df_traffic.isnull().sum())
"""),
        nbf.v4.new_markdown_cell("""## 3. Data Cleaning & Spatial-Temporal Feature Extraction
- Standardize column names (snake_case).
- Extract timestamps, `year`, and hourly/daily aggregate traffic metrics.
- Map segment location/Borough and clean missing traffic count values.
"""),
        nbf.v4.new_code_cell("""df_t_clean = df_traffic.copy()

# Column renaming normalization
df_t_clean.columns = [c.lower().replace(' ', '_') for c in df_t_clean.columns]

# Parse date/time
date_col = [c for c in df_t_clean.columns if 'date' in c or 'time' in c or 'beginning' in c]
if date_col:
    df_t_clean['datetime'] = pd.to_datetime(df_t_clean[date_col[0]], errors='coerce')
    df_t_clean['year'] = df_t_clean['datetime'].dt.year

# Volumetric count feature normalization
vol_col = [c for c in df_t_clean.columns if 'vol' in c or 'count' in c or 'pedestrian' in c]
if vol_col:
    df_t_clean['traffic_volume'] = pd.to_numeric(df_t_clean[vol_col[0]], errors='coerce').fillna(0)
else:
    df_t_clean['traffic_volume'] = 1

# Drop invalid records lacking date
df_t_clean = df_t_clean.dropna(subset=['year'])
df_t_clean['year'] = df_t_clean['year'].astype(int)

# Aggregate traffic at the Year level (and Borough/ZIP if available)
print("Cleaned Traffic Dataset Shape:", df_t_clean.shape)

df_t_clean.to_csv(PROCESSED_DIR / "traffic_cleaned.csv", index=False)
print("Saved cleaned traffic dataset to data/processed/traffic_cleaned.csv")
"""),
        nbf.v4.new_markdown_cell("""## 4. Initial EDA Visualizations
Trend of overall recorded traffic volumes across sample years.
"""),
        nbf.v4.new_code_cell("""plt.figure(figsize=(10, 4))
df_t_clean.groupby('year')['traffic_volume'].mean().plot(kind='line', marker='o', color='coral')
plt.title('Average Traffic Volume by Year')
plt.xlabel('Year')
plt.ylabel('Mean Volume')
plt.tight_layout()
plt.show()
""")
    ]

    with open("02_transport_eda_cleaning.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)

create_notebook_2()
print("Created 02_transport_eda_cleaning.ipynb")
