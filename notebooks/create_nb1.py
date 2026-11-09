import json
import nbformat as nbf

def create_notebook_1():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Notebook 1: Housing Dataset Exploratory Data Analysis & Cleaning
**Author:** Member 1
**Domain:** Housing
**Dataset:** Affordable Housing Production by Building (NYC Open Data `hg8x-zxpr`)

---

## 1. Dataset Overview & Selection Rationale
- **Dataset Title:** Affordable Housing Production by Building
- **Source:** NYC Open Data (Department of Housing Preservation and Development - HPD)
- **API / Download URL:** `https://data.cityofnewyork.us/resource/hg8x-zxpr.csv`
- **Rationale:** This dataset contains detailed building-level records of affordable housing projects across NYC, including total units, affordable units, borough, ZIP code, and completion dates. It allows temporal and spatial aggregation essential for integrating with city traffic volume data.
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_theme(style="whitegrid")

# Define data path
RAW_DIR = Path("../data/raw")
PROCESSED_DIR = Path("../data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

HOUSING_FILE = RAW_DIR / "housing_raw.csv"

# Load Raw Dataset
if HOUSING_FILE.exists():
    df_housing = pd.read_csv(HOUSING_FILE, low_memory=False)
else:
    # Fallback direct download if local raw file is not present
    url = "https://data.cityofnewyork.us/resource/hg8x-zxpr.csv?$limit=50000"
    df_housing = pd.read_csv(url, low_memory=False)

print("Raw Housing Dataset Shape:", df_housing.shape)
df_housing.head()
"""),
        nbf.v4.new_markdown_cell("""## 2. Exploratory Data Analysis (EDA)
Inspect schema, missing values, data types, and initial distribution of housing units across boroughs and completion years.
"""),
        nbf.v4.new_code_cell("""# Summary Information & Missing Values
print("--- Info ---")
print(df_housing.info())

print("\n--- Missing Value Count ---")
print(df_housing.isnull().sum()[df_housing.isnull().sum() > 0])
"""),
        nbf.v4.new_markdown_cell("""## 3. Data Cleaning & Standardization
- Convert completion/project dates to `datetime` and extract `project_year`.
- Clean and standardize ZIP Codes (`postcode` / `zip_code` field to 5-digit string format).
- Filter out records with invalid or missing ZIP codes and dates.
- Standardize Borough names.
"""),
        nbf.v4.new_code_cell("""# Cleaning logic
df_clean = df_housing.copy()

# Date handling
date_col = 'project_completion_date' if 'project_completion_date' in df_clean.columns else 'building_completion_date'
if date_col in df_clean.columns:
    df_clean['completion_date'] = pd.to_datetime(df_clean[date_col], errors='coerce')
    df_clean['year'] = df_clean['completion_date'].dt.year

# ZIP Code cleaning
zip_col = 'postcode' if 'postcode' in df_clean.columns else 'zip_code'
if zip_col in df_clean.columns:
    df_clean['zip_code'] = df_clean[zip_col].astype(str).str.extract(r'(\d{5})')[0]

# Units numeric check
unit_col = 'all_counted_units' if 'all_counted_units' in df_clean.columns else 'total_units'
if unit_col in df_clean.columns:
    df_clean['total_units'] = pd.to_numeric(df_clean[unit_col], errors='coerce').fillna(0)

# Drop records lacking key temporal/spatial keys
df_clean = df_clean.dropna(subset=['year', 'zip_code'])
df_clean['year'] = df_clean['year'].astype(int)

print("Cleaned Housing Dataset Shape:", df_clean.shape)

# Save processed housing dataset
df_clean.to_csv(PROCESSED_DIR / "housing_cleaned.csv", index=False)
print("Saved cleaned housing dataset to data/processed/housing_cleaned.csv")
"""),
        nbf.v4.new_markdown_cell("""## 4. Descriptive Summary & Initial EDA Visualizations
Visualizing total housing production by year and top boroughs.
"""),
        nbf.v4.new_code_cell("""plt.figure(figsize=(10, 4))
df_clean.groupby('year')['total_units'].sum().plot(kind='bar', color='skyblue')
plt.title('Total Housing Units Completed by Year')
plt.xlabel('Year')
plt.ylabel('Total Units')
plt.tight_layout()
plt.show()
""")
    ]

    with open("01_housing_eda_cleaning.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)

create_notebook_1()
print("Created 01_housing_eda_cleaning.ipynb")
