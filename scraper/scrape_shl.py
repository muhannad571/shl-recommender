import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://www.shl.com"
CATALOG_URL = "https://www.shl.com/solutions/products/product-catalog/"

def scrape_catalog():
    response = requests.get(CATALOG_URL)
    soup = BeautifulSoup(response.text, "html.parser")

    records = []

    for card in soup.select("a.product-card"):
        title = card.get_text(strip=True)
        url = BASE_URL + card.get("href")

        # Ignore pre-packaged solutions
        if "pre-packaged" in title.lower():
            continue

        records.append({
            "assessment_name": title,
            "assessment_url": url
        })

    df = pd.DataFrame(records)
    df.to_csv("shl_catalog.csv", index=False)
    print(f"Saved {len(df)} assessments")

if __name__ == "__main__":
    scrape_catalog()
