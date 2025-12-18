import os
import re

def update_file(filename, old_pattern, new_pattern):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.read()
        
        # Use regex to replace the pattern
        new_content = re.sub(old_pattern, new_pattern, content)
        
        with open(filename, 'w') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"{filename} does not exist, skipping.")

# Update vector_store.py
# We are going to replace the CSV loading section to use shl_assessments_from_excel.csv
# We'll look for the pattern that loads the CSV and replace it with a fixed one.
# Since the code might vary, we do a more targeted replacement.

# First, let's read the current vector_store.py and find the line with pd.read_csv
vector_store_file = 'vector_store.py'
if os.path.exists(vector_store_file):
    with open(vector_store_file, 'r') as f:
        lines = f.readlines()
    
    # Find the line with self.df = pd.read_csv
    for i, line in enumerate(lines):
        if 'self.df = pd.read_csv' in line:
            # Replace that line with a fixed one
            lines[i] = "        self.df = pd.read_csv('shl_assessments_from_excel.csv')\n"
            break
    
    # Write back
    with open(vector_store_file, 'w') as f:
        f.writelines(lines)
    print("Updated vector_store.py to use shl_assessments_from_excel.csv")
else:
    print("vector_store.py not found")

# Update extract_from_excel.py
extract_file = 'extract_from_excel.py'
if os.path.exists(extract_file):
    with open(extract_file, 'r') as f:
        content = f.read()
    
    # Replace the output CSV filename
    # Look for the pattern of to_csv with any filename and replace with our desired one.
    # We'll use regex to capture the current filename and replace it.
    # But note: we want to change the output file, so we look for lines with to_csv and replace the filename.
    # We'll do a simple string replacement for the common pattern.
    new_content = content.replace("to_csv('shl_assessments.csv'", "to_csv('shl_assessments_from_excel.csv'")
    new_content = new_content.replace('to_csv("shl_assessments.csv"', 'to_csv("shl_assessments_from_excel.csv"')
    
    with open(extract_file, 'w') as f:
        f.write(new_content)
    print("Updated extract_from_excel.py to output shl_assessments_from_excel.csv")

# Check other files for hardcoded CSV references
other_files = ['clean_csv.py', 'api.py', 'recommendation_engine.py', 'test_api.py']
for file in other_files:
    if os.path.exists(file):
        with open(file, 'r') as f:
            content = f.read()
        if 'catalog.csv' in content or 'shl_assessments.csv' in content:
            print(f"Warning: {file} contains hardcoded CSV references. Please check manually.")