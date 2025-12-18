import pandas as pd
import numpy as np
from sklearn.metrics import precision_score, recall_score
import re


def calculate_recall():
    """
    Calculate Recall@10 for your predictions
    """
    # Load your predictions
    try:
        predictions_df = pd.read_csv('test_predictions.csv')
    except:
        print("Error: Need to generate predictions first")
        return

    # Load ground truth (train set from Excel)
    # Note: For test set, we don't have ground truth
    # This is for demonstration on train set

    # For actual evaluation, you would compare with human-labeled test set
    print("For actual evaluation:")
    print("1. You need human-labeled test data")
    print("2. Compare your predicted URLs with ground truth URLs")
    print("3. Calculate Recall@10 = (Relevant items in top 10) / (Total relevant items)")

    # Example calculation
    print("\n📊 Example Recall@10 Calculation:")
    print("Query: 'Java developer with collaboration skills'")
    print("Ground truth relevant assessments: 8")
    print("Your top 10 recommendations contain: 6 of those 8")
    print("Recall@10 = 6/8 = 0.75")

    print("\n✅ To avoid rejection:")
    print("1. Ensure your system recommends EXACT URL matches")
    print("2. Balance technical and behavioral assessments")
    print("3. Meet all API response format requirements")
    print("4. Include at least 5 recommendations per query")


if __name__ == "__main__":
    calculate_recall()