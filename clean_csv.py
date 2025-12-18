import pandas as pd
import json
import os

print("Cleaning the CSV file...")

# List of possible input CSV files (in order of preference)
possible_input_files = [
    'shl_assessments.csv',
    'shl_assessments_from_excel.csv',
    'shl_assessments_guaranteed.csv',
    'nuclear_fix.csv'
]

input_file = None
for file in possible_input_files:
    if os.path.exists(file):
        input_file = file
        break

if input_file is None:
    print("ERROR: No input CSV file found. Please make sure one of the following exists:")
    for file in possible_input_files:
        print(f"  - {file}")
    exit(1)

print(f"Reading from {input_file}...")

# Read the CSV
df = pd.read_csv(input_file)

# Clean the test_type column
def clean_test_type(value):
    if pd.isna(value):
        return ['K']
    
    val_str = str(value).strip()
    
    # If it looks like JSON, try to parse
    if val_str.startswith('[') and val_str.endswith(']'):
        try:
            parsed = json.loads(val_str)
            if isinstance(parsed, list):
                return parsed
        except:
            pass
    
    # If it's a string with commas, split
    if ',' in val_str:
        return [item.strip() for item in val_str.split(',')]
    
    # If it's a single letter (A, B, K, P, etc.)
    if len(val_str) == 1 and val_str.isalpha():
        return [val_str]
    
    # Default to 'K' (Knowledge & Skills)
    return ['K']

# Apply cleaning
df['test_type'] = df['test_type'].apply(clean_test_type)

# Save cleaned version
output_file = 'shl_assessments_clean.csv'
df.to_csv(output_file, index=False)
print(f"Saved cleaned CSV to {output_file} with {len(df)} rows")

# Verify
print("\nSample of cleaned test_type:")
for i, row in df.head(5).iterrows():
    print(f"Row {i}: {row['test_type']}")