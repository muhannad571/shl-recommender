import pandas as pd
import requests

API_URL = "http://localhost:8000/recommend"  # change to Render URL later

# Load unlabeled test queries
test_df = pd.read_excel("Gen_AI Dataset.xlsx", sheet_name="test")

rows = []

for query in test_df["Query"]:
    response = requests.post(
        API_URL,
        json={"query": query}
    ).json()

    for rec in response["recommendations"]:
        rows.append({
            "Query": query,
            "Assessment_url": rec["assessment_url"]
        })

output_df = pd.DataFrame(rows)
output_df.to_csv("firstname_lastname.csv", index=False)

print("Prediction file created: firstname_lastname.csv")
