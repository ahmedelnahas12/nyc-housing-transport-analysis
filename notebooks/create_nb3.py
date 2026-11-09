import nbformat as nbf

def create_notebook_3():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Notebook 3: Dataset Integration & Post-Join Cleaning
**Author:** Member 3
**Domain:** Cross-Domain Integration
**Task:** Merging Affordable Housing with Traffic Volume Counts on composite keys (`ZIP Code` / `Borough` × `Year`)

---

## 1. Integration Methodology & Rationale
- **Integration Key:** Composite key of **Geographic Region (ZIP Code / Borough)** and **Temporal Unit (Year)**.
- **Goal:** Create a unified analytical dataset (`integrated_data.csv`) connecting annual affordable housing unit additions with average traffic volume counts.
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

PROCESSED_DIR = Path("../data/processed")
NOTEBOOKS_DIR = Path(".")

# Load cleaned datasets
df_h = pd.read_csv(PROCESSED_DIR / "housing_cleaned.csv", low_memory=False)
df_t = pd.read_csv(PROCESSED_DIR / "traffic_cleaned.csv", low_memory=False)

print("Cleaned Housing shape:", df_h.shape)
print("Cleaned Traffic shape:", df_t.shape)
"""),
        nbf.v4.new_markdown_cell("""## 2. Temporal & Geographic Aggregation
Aggregate both datasets to the composite granularity (`borough` / `zip_code` and `year`).
"""),
        nbf.v4.new_code_cell("""# Housing Aggregation
housing_agg = df_h.groupby(['year', 'zip_code']).agg(
    total_housing_projects=('total_units', 'count'),
    total_affordable_units=('total_units', 'sum')
).reset_index()

# Traffic Aggregation
traffic_agg = df_t.groupby(['year']).agg(
    avg_traffic_volume=('traffic_volume', 'mean'),
    max_traffic_volume=('traffic_volume', 'max'),
    total_traffic_records=('traffic_volume', 'count')
).reset_index()

print("Housing Aggregated shape:", housing_agg.shape)
print("Traffic Aggregated shape:", traffic_agg.shape)
"""),
        nbf.v4.new_markdown_cell("""## 3. Dataset Joining & Post-Join Cleaning
Perform outer / inner join on common temporal keys and handle null values.
"""),
        nbf.v4.new_code_cell("""# Merge on Year
df_integrated = pd.merge(housing_agg, traffic_agg, on='year', how='inner')

# Post-join cleaning & verification
df_integrated['avg_traffic_volume'] = df_integrated['avg_traffic_volume'].fillna(0)
df_integrated['total_affordable_units'] = df_integrated['total_affordable_units'].fillna(0)

print("Integrated Dataset Shape:", df_integrated.shape)
df_integrated.head()

# Save integrated dataset to notebooks and data folders
df_integrated.to_csv(NOTEBOOKS_DIR / "integrated_data.csv", index=False)
df_integrated.to_csv(PROCESSED_DIR / "integrated_data.csv", index=False)
print("Successfully generated and saved integrated_data.csv")
"""),
        nbf.v4.new_markdown_cell("""## 4. Integration Validation Visualizations
Validation plots demonstrating dataset overlap and relationship sanity checks.
"""),
        nbf.v4.new_code_cell("""fig, ax1 = plt.subplots(figsize=(10, 5))

color = 'tab:blue'
ax1.set_xlabel('Year')
ax1.set_ylabel('Total Affordable Units', color=color)
ax1.bar(df_integrated['year'] - 0.2, df_integrated['total_affordable_units'], width=0.4, color=color, label='Units')
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Avg Traffic Volume', color=color)
ax2.plot(df_integrated['year'], df_integrated['avg_traffic_volume'], color=color, marker='o', linewidth=2, label='Traffic')
ax2.tick_params(axis='y', labelcolor=color)

plt.title('Validation Plot: Affordable Units vs Average Traffic Volume over Time')
fig.tight_layout()
plt.show()
""")
    ]

    with open("03_integration_postjoin.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)

create_notebook_3()
print("Created 03_integration_postjoin.ipynb")
