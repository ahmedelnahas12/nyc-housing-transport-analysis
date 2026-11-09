import pandas as pd
import numpy as np

# Create synthetic baseline integrated dataset matching schema
years = list(range(2014, 2024))
zips = [10001, 10002, 10003, 10004, 10005, 10451, 10452, 11201, 11202, 11354]

data = []
for y in years:
    for z in zips:
        units = int(np.random.randint(50, 800))
        projects = int(np.random.randint(1, 10))
        traffic = int(np.random.randint(500, 4000) + (y - 2014) * 50)
        data.append({
            "year": y,
            "zip_code": z,
            "total_housing_projects": projects,
            "total_affordable_units": units,
            "avg_traffic_volume": traffic,
            "max_traffic_volume": traffic + np.random.randint(200, 1000),
            "total_traffic_records": np.random.randint(100, 500)
        })

df = pd.DataFrame(data)
df.to_csv("integrated_data.csv", index=False)
print("Wrote integrated_data.csv successfully")
