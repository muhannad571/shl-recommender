import pandas as pd

df = pd.read_csv("shl_catalog.csv")

assert len(df) >= 377, "Catalog too small"

df.drop_duplicates(inplace=True)
df.dropna(inplace=True)

df.to_csv("catalog_clean.csv", index=False)
print("Catalog cleaned and validated")
