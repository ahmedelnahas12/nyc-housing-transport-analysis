#!/usr/bin/env python
"""
Master execution script: Runs all 4 notebooks' logic in sequence
Generates: housing_cleaned.csv, traffic_cleaned.csv, traffic_yearly.csv, integrated_data.csv
"""
import pandas as pd
import numpy as np
from urllib.parse import urlencode
import warnings
import os
warnings.filterwarnings('ignore')

# Ensure output directories exist
os.makedirs("notebooks", exist_ok=True)
os.makedirs("website/data", exist_ok=True)

print("=" * 60)
print("NYC HOUSING & TRANSPORTATION - DATA PIPELINE")
print("=" * 60)

# ============================================================
# NOTEBOOK 1: Housing EDA & Cleaning (Member 1)
# ============================================================
print("\n[1/4] Loading & Cleaning Housing Data (H2: Affordable Housing)...")

housing_url = "https://data.cityofnewyork.us/resource/hg8x-zxpr.csv"
params = {'$limit': 50000, '$order': ':id'}
query = urlencode(params)
df_housing = pd.read_csv(f"{housing_url}?{query}", low_memory=False)
print(f"  Loaded: {df_housing.shape}")

# Standardize column names
df_housing.columns = (df_housing.columns
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('-', '_')
    .str.replace(r'[^a-z0-9_]', '', regex=True))

# Standardize borough
if 'borough' in df_housing.columns:
    df_housing['borough'] = df_housing['borough'].str.title().str.strip()

# Fix ZIP codes
if 'postcode' in df_housing.columns:
    df_housing['postcode'] = df_housing['postcode'].apply(
        lambda x: str(int(x)).zfill(5) if pd.notna(x) and str(x).replace('.', '').isdigit() else x
    )

# Parse dates
date_cols = [c for c in df_housing.columns if 'date' in c.lower()]
for col in date_cols:
    try:
        df_housing[col] = pd.to_datetime(df_housing[col], errors='coerce')
        year_col = col.replace('_date', '_year')
        df_housing[year_col] = df_housing[col].dt.year
    except:
        pass

# Drop rows missing both coordinates
if 'latitude' in df_housing.columns and 'longitude' in df_housing.columns:
    missing_both = df_housing['latitude'].isna() & df_housing['longitude'].isna()
    df_housing = df_housing[~missing_both].copy()

# Create total affordable units
income_cols = [c for c in df_housing.columns if c.endswith('_income_units')]
if income_cols:
    df_housing['total_affordable_units'] = df_housing[income_cols].sum(axis=1, skipna=True)

# Create total units by bedroom
br_cols = [c for c in df_housing.columns if c.endswith('_br_units') or c == 'studio_units']
if br_cols:
    df_housing['total_units_by_br'] = df_housing[br_cols].sum(axis=1, skipna=True)

# Save
df_housing.to_csv("notebooks/housing_cleaned.csv", index=False)
print(f"  Saved: housing_cleaned.csv ({df_housing.shape})")

# ============================================================
# NOTEBOOK 2: Transport EDA & Cleaning (Member 2)
# ============================================================
print("\n[2/4] Loading & Cleaning Traffic Data (T2: Traffic Volume)...")

traffic_url = "https://data.cityofnewyork.us/api/views/6fi9-q3ta/rows.csv?accessType=download"
df_traffic = pd.read_csv(traffic_url, low_memory=False)
print(f"  Loaded: {df_traffic.shape}")

# Standardize column names
df_traffic.columns = (df_traffic.columns
    .str.lower()
    .str.replace(' ', '_')
    .str.replace('-', '_')
    .str.replace(r'[^a-z0-9_]', '', regex=True))

# Parse datetime
if 'hour_beginning' in df_traffic.columns:
    df_traffic['hour_beginning'] = pd.to_datetime(df_traffic['hour_beginning'], errors='coerce')
    df_traffic['year'] = df_traffic['hour_beginning'].dt.year
    df_traffic['month'] = df_traffic['hour_beginning'].dt.month
    df_traffic['date'] = df_traffic['hour_beginning'].dt.date

# Map locations to boroughs
location_to_borough = {
    'brooklyn bridge': 'Brooklyn',
    'manhattan bridge': 'Manhattan',
    'williamsburg bridge': 'Brooklyn',
    'queensboro bridge': 'Queens',
    'rfk bridge': 'Manhattan',
    'verrazzano bridge': 'Staten Island',
    'henry hudson bridge': 'Manhattan',
    'cross bay bridge': 'Queens',
    'marine parkway bridge': 'Queens',
}
if 'location' in df_traffic.columns:
    df_traffic['location_lower'] = df_traffic['location'].str.lower().str.strip()
    df_traffic['borough'] = df_traffic['location_lower'].map(location_to_borough)

# Aggregate to yearly per location
agg_cols = [c for c in ['towards_manhattan', 'towards_brooklyn', 'pedestrians'] if c in df_traffic.columns]
traffic_yearly = df_traffic.groupby(['location', 'year', 'borough', 'lat', 'long'])[agg_cols].sum().reset_index()
traffic_yearly['total_vehicle_volume'] = traffic_yearly['towards_manhattan'] + traffic_yearly['towards_brooklyn']

# Save
df_traffic.to_csv("notebooks/traffic_cleaned.csv", index=False)
traffic_yearly.to_csv("notebooks/traffic_yearly.csv", index=False)
print(f"  Saved: traffic_cleaned.csv ({df_traffic.shape}), traffic_yearly.csv ({traffic_yearly.shape})")

# ============================================================
# NOTEBOOK 3: Integration & Post-Join (Member 3)
# ============================================================
print("\n[3/4] Integrating Datasets (Borough x Year)...")

# Load cleaned data
housing = pd.read_csv("notebooks/housing_cleaned.csv", low_memory=False)
traffic = pd.read_csv("notebooks/traffic_yearly.csv", low_memory=False)

# Aggregate housing to Borough x Year (more reliable than ZIP matching)
housing_agg = housing.groupby(['borough', 'building_completion_year']).agg(
    total_affordable_units=('total_affordable_units', 'sum'),
    total_units=('total_units', 'sum') if 'total_units' in housing.columns else ('total_affordable_units', 'sum'),
    project_count=('project_id', 'nunique'),
    building_count=('building_id', 'nunique'),
    avg_units_per_building=('total_affordable_units', 'mean')
).reset_index()
housing_agg.rename(columns={'building_completion_year': 'year'}, inplace=True)

# Aggregate traffic to Borough x Year
traffic_agg = traffic.groupby(['borough', 'year']).agg(
    total_vehicle_volume=('total_vehicle_volume', 'sum'),
    towards_manhattan=('towards_manhattan', 'sum'),
    towards_brooklyn=('towards_brooklyn', 'sum'),
    total_pedestrians=('pedestrians', 'sum'),
    location_count=('location', 'nunique')
).reset_index()

# Outer join on Borough x Year
integrated = pd.merge(
    housing_agg, traffic_agg,
    on=['borough', 'year'],
    how='outer', indicator=True
)

# Post-join cleaning
housing_cols = ['total_affordable_units', 'total_units', 'project_count', 'building_count', 'avg_units_per_building']
traffic_cols = ['total_vehicle_volume', 'towards_manhattan', 'towards_brooklyn', 'total_pedestrians', 'location_count']

integrated[traffic_cols] = integrated[traffic_cols].fillna(0)
integrated[housing_cols] = integrated[housing_cols].fillna(0)
integrated.drop(columns=['_merge'], inplace=True)

# Derived metrics
integrated['year'] = integrated['year'].astype(int)

integrated['affordable_units_per_1k_vehicles'] = np.where(
    integrated['total_vehicle_volume'] > 0,
    (integrated['total_affordable_units'] / integrated['total_vehicle_volume']) * 1000,
    np.nan
)
integrated['vehicles_per_affordable_unit'] = np.where(
    integrated['total_affordable_units'] > 0,
    integrated['total_vehicle_volume'] / integrated['total_affordable_units'],
    np.nan
)

# Save integrated data
integrated.to_csv("notebooks/integrated_data.csv", index=False)
integrated.to_csv("website/data/integrated_data.csv", index=False)
print(f"  Saved: integrated_data.csv ({integrated.shape})")
print(f"  Borough×Year combos: {len(integrated)}")
print(f"  Both domains present: {((integrated['total_affordable_units']>0) & (integrated['total_vehicle_volume']>0)).sum()}")

# ============================================================
# NOTEBOOK 4: Research Questions (Members 1-4) - Just verify data
# ============================================================
print("\n[4/4] Verifying Integrated Data for Research Questions...")

print(f"  Years: {sorted(integrated['year'].unique())}")
print(f"  Boroughs: {integrated['borough'].dropna().unique()}")
print(f"  Total affordable units: {integrated['total_affordable_units'].sum():,.0f}")
print(f"  Total vehicle volume: {integrated['total_vehicle_volume'].sum():,.0f}")

# Quick cross-domain check
both = integrated[(integrated['total_affordable_units']>0) & (integrated['total_vehicle_volume']>0)]
if len(both) > 2:
    corr = both['total_affordable_units'].corr(both['total_vehicle_volume'])
    print(f"  Correlation (housing vs traffic): {corr:.3f}")

print("\n" + "=" * 60)
print("ALL DONE! Data files ready for website.")
print("=" * 60)