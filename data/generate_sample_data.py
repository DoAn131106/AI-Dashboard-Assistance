import pandas as pd

data = {
    "region": ["East", "West", "North", "East", "South"],
    "quarter": ["Q2", "Q2", "Q1", "Q2", "Q1"],
    "year": [2024, 2024, 2024, 2023, 2023],
    "sales": [10000, 8000, 9000, 9500, 7000],
    "profit": [3000, 2000, 2500, 2800, 1800],
}

df = pd.DataFrame(data)
df.to_excel("data/sample_data.xlsx", index=False)

