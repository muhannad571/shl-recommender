# convert_data.py
import pandas as pd

# Read the Excel file
xls = pd.ExcelFile('data/Gen_AI Dataset.xlsx')

# Save each sheet as CSV
train_df = pd.read_excel(xls, 'Train-Set')
test_df = pd.read_excel(xls, 'Test-Set')

train_df.to_csv('data/train.csv', index=False)
test_df.to_csv('data/test.csv', index=False)

print("✅ Data converted to CSV successfully!")
print(f"Train samples: {len(train_df)}")
print(f"Test samples: {len(test_df)}")