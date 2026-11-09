import nbformat as nbf

def create_notebook_4():
    nb = nbf.v4.new_notebook()
    nb.cells = [
        nbf.v4.new_markdown_cell("""# Notebook 4: Research Analysis & Data Storytelling (8 Questions & Visualizations)
**Authors:** Members 1, 2, 3, 4 (2 Questions & 2 Visualizations per Member)

---

## Overview
This notebook presents the complete analytical study containing 8 distinct research questions and 8 corresponding data visualizations addressing the impact of NYC housing developments on urban mobility and traffic patterns.

---

### Member 1: Housing Dynamics
#### RQ1: How has affordable housing unit production evolved year-over-year in NYC?
#### RQ2: Which ZIP codes received the highest concentration of new affordable housing units?

### Member 2: Mobility Trends
#### RQ3: How do average traffic volumes vary historically across different operational periods?
#### RQ4: Is there a significant seasonal variation in city traffic patterns?

### Member 3: Cross-Domain & Spatial Correlations
#### RQ5: What is the correlation between new housing unit additions and average traffic volume in matching years?
#### RQ6: Do high-density housing additions correspond to peak traffic volume spikes?

### Member 4: Policy Impact & Data Storytelling
#### RQ7: Did affordable housing unit growth outpace or lag behind changes in traffic density?
#### RQ8: How can city planners optimize future transit corridors based on affordable housing development hubs?
"""),
        nbf.v4.new_code_cell("""import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sns.set_theme(style="whitegrid")

# Load integrated dataset
df = pd.read_csv("integrated_data.csv")
df.head()
"""),
        nbf.v4.new_markdown_cell("""---
## Visualizations 1 & 2 (Member 1)
"""),
        nbf.v4.new_code_cell("""# Viz 1: Yearly Affordable Housing Production
plt.figure(figsize=(10, 4))
sns.barplot(data=df, x='year', y='total_affordable_units', palette='Blues_d')
plt.title('RQ1: Annual Production of Affordable Housing Units')
plt.xlabel('Year')
plt.ylabel('Total Units')
plt.tight_layout()
plt.show()

# Viz 2: Top Housing Concentration by ZIP Code
plt.figure(figsize=(10, 4))
top_zips = df.groupby('zip_code')['total_affordable_units'].sum().nlargest(10).reset_index()
sns.barplot(data=top_zips, x='zip_code', y='total_affordable_units', palette='viridis')
plt.title('RQ2: Top 10 ZIP Codes by Total Affordable Units')
plt.xlabel('ZIP Code')
plt.ylabel('Units')
plt.tight_layout()
plt.show()
"""),
        nbf.v4.new_markdown_cell("""---
## Visualizations 3 & 4 (Member 2)
"""),
        nbf.v4.new_code_cell("""# Viz 3: Historical Traffic Volume Trend
plt.figure(figsize=(10, 4))
sns.lineplot(data=df, x='year', y='avg_traffic_volume', marker='o', color='crimson', linewidth=2.5)
plt.title('RQ3: Historical Average Traffic Volume Trend')
plt.xlabel('Year')
plt.ylabel('Average Volume')
plt.tight_layout()
plt.show()

# Viz 4: Max vs Average Traffic Volume Comparison
plt.figure(figsize=(10, 4))
plt.plot(df['year'], df['avg_traffic_volume'], label='Average Traffic', marker='o')
plt.plot(df['year'], df['max_traffic_volume'], label='Peak Traffic', marker='s', linestyle='--')
plt.title('RQ4: Peak vs Average Traffic Volumes per Year')
plt.xlabel('Year')
plt.ylabel('Volume')
plt.legend()
plt.tight_layout()
plt.show()
"""),
        nbf.v4.new_markdown_cell("""---
## Visualizations 5 & 6 (Member 3 - Integration & Correlation)
"""),
        nbf.v4.new_code_cell("""# Viz 5: Cross-Domain Correlation Scatter Plot
plt.figure(figsize=(8, 5))
sns.regplot(data=df, x='total_affordable_units', y='avg_traffic_volume', color='teal', scatter_kws={'s':50})
plt.title('RQ5: Correlation Between Affordable Units and Traffic Volume')
plt.xlabel('Total Affordable Units')
plt.ylabel('Average Traffic Volume')
plt.tight_layout()
plt.show()

# Viz 6: Dual Axis Trend Analysis
fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df['year'], df['total_affordable_units'], color='blue', marker='o', label='Affordable Units')
ax1.set_ylabel('Total Units', color='blue')

ax2 = ax1.twinx()
ax2.plot(df['year'], df['avg_traffic_volume'], color='red', marker='s', label='Traffic Volume')
ax2.set_ylabel('Avg Traffic Volume', color='red')

plt.title('RQ6: Dual Trend Analysis of Housing vs Traffic Density')
fig.tight_layout()
plt.show()
"""),
        nbf.v4.new_markdown_cell("""---
## Visualizations 7 & 8 (Member 4 - Data Story & Policy Impact)
"""),
        nbf.v4.new_code_cell("""# Viz 7: Relative Growth Index (Normalized comparison)
df_norm = df.copy()
df_norm['housing_norm'] = df_norm['total_affordable_units'] / df_norm['total_affordable_units'].max()
df_norm['traffic_norm'] = df_norm['avg_traffic_volume'] / df_norm['avg_traffic_volume'].max()

plt.figure(figsize=(10, 4))
plt.plot(df_norm['year'], df_norm['housing_norm'], label='Normalized Housing Growth', marker='o')
plt.plot(df_norm['year'], df_norm['traffic_norm'], label='Normalized Traffic Load', marker='^', linestyle='--')
plt.title('RQ7: Normalized Growth Rate: Housing Production vs Traffic Load')
plt.xlabel('Year')
plt.ylabel('Normalized Metric (0 to 1)')
plt.legend()
plt.tight_layout()
plt.show()

# Viz 8: High Impact Zone Quadrant Analysis
plt.figure(figsize=(8, 5))
sns.scatterplot(data=df, x='total_housing_projects', y='avg_traffic_volume', size='total_affordable_units', hue='year', palette='magma', sizes=(40, 400))
plt.title('RQ8: Transit Planning Impact Matrix (Projects vs Traffic)')
plt.xlabel('Total Housing Projects')
plt.ylabel('Average Traffic Volume')
plt.tight_layout()
plt.show()
""")
    ]

    with open("04_research_questions_viz.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)

create_notebook_4()
print("Created 04_research_questions_viz.ipynb")
