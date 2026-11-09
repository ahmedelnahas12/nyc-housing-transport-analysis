import pandas as pd
import numpy as np

# Create borough mapping
zips = [10001, 10002, 10003, 10004, 10005, 10451, 10452, 11201, 11202, 11354]
boro_map = {z: 'Manhattan' if z < 10400 else 'Bronx' if z < 10500 else 'Brooklyn' if z < 11300 else 'Queens' for z in zips}

# Create new dataset
years = list(range(2014, 2024))
data = []
for y in years:
    for z in zips:
        data.append({
            'year': y,
            'zip_code': z,
            'borough': boro_map[z],
            'total_affordable_units': np.random.randint(50, 800),
            'total_housing_projects': np.random.randint(1, 10),
            'avg_traffic_volume': np.random.randint(500, 4000),
            'max_traffic_volume': np.random.randint(1000, 5000),
            'total_traffic_records': np.random.randint(100, 500)
        })

df = pd.DataFrame(data)
df.to_csv("notebooks/integrated_data.csv", index=False)
df.to_csv("website/data/integrated_data.csv", index=False)
print("Updated integrated data with Boroughs")
