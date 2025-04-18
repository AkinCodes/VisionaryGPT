import pandas as pd

df = pd.read_csv("netflix_titles.csv")
print("📁 CSV Columns:\n", df.columns.tolist())
