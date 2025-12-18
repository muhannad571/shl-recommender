import pandas as pd
import requests
import json
from tqdm import tqdm


def generate_test_predictions():
    # Load test queries from Excel (Test-Set sheet)
    # Save the Test-Set sheet as test_queries.csv first

    # If you have the Excel file, use this:
    # df = pd.read_excel('Gen_AI Dataset.xlsx', sheet_name='Test-Set')
    # test_queries = df['Query'].tolist()

    # For now, using the test queries from the PDF
    test_queries = [
        "Looking to hire mid-level professionals who are proficient in Python, SQL and Java Script. Need an assessment package that can test all skills with max duration of 60 minutes.",
        "Job Description\n\n... (the long JD from PDF)",  # Add all 9 test queries here
        "I am hiring for an analyst and wants applications to screen using Cognitive and personality tests, what options are available within 45 mins.",
        # Add all 9 queries...
    ]

    # Make sure you have exactly 9 test queries
    print(f"Processing {len(test_queries)} test queries...")

    predictions = []
    api_url = "http://localhost:8000"

    for query in tqdm(test_queries, desc="Generating predictions"):
        try:
            response = requests.post(
                f"{api_url}/recommend",
                json={"query": query},
                timeout=60
            )

            if response.status_code == 200:
                data = response.json()
                # Get URLs of recommended assessments
                urls = [assessment['url'] for assessment in data['recommended_assessments']]
                predictions.append({
                    'query': query[:500],  # Truncate long queries
                    'predictions': ' | '.join(urls[:10])  # Max 10 URLs
                })
            else:
                print(f"Error for query: {response.status_code}")
                predictions.append({'query': query[:500], 'predictions': ''})

        except Exception as e:
            print(f"Exception for query: {e}")
            predictions.append({'query': query[:500], 'predictions': ''})

    # Save to CSV
    df_predictions = pd.DataFrame(predictions)
    df_predictions.to_csv('test_predictions.csv', index=False)
    print("\n✅ Predictions saved to test_predictions.csv")

    # Print sample
    print("\nSample predictions:")
    print(df_predictions.head())


if __name__ == "__main__":
    generate_test_predictions()