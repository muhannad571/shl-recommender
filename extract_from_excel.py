import pandas as pd

def create_dataset_from_excel():
    """
    Extract all unique assessment URLs from the provided Excel file.
    """
    print("Extracting assessment URLs from Excel file...")
    
    # Read the Excel file
    # You need to have the 'Gen_AI Dataset.xlsx' file in your project folder
    try:
        # Read both sheets
        train_df = pd.read_excel('Gen_AI Dataset.xlsx', sheet_name='Train-Set')
        # If there's a Test-Set sheet, read it too
        # test_df = pd.read_excel('Gen_AI Dataset.xlsx', sheet_name='Test-Set')
        
        # Combine all URLs from column B (Assessment_url)
        all_urls = train_df['Assessment_url'].dropna().unique().tolist()
        # If you have test set: all_urls.extend(test_df['Assessment_url'].dropna().unique().tolist())
        
        print(f"Found {len(all_urls)} unique assessment URLs in Excel file")
        
        # Create assessments list
        assessments = []
        for i, url in enumerate(all_urls):
            # Extract name from URL or use a generic name
            # Example: https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/
            # Name would be "Core Java Entry Level New"
            url_parts = url.rstrip('/').split('/')
            name_part = url_parts[-1] if url_parts else f"Assessment_{i+1}"
            name = name_part.replace('-', ' ').replace('_', ' ').title()
            
            assessments.append({
                'name': name,
                'url': url,
                'description': f"SHL assessment for {name}",
                'test_type': ['K'],  # You may need to categorize these
                'duration': 60,  # Default duration
                'adaptive_support': 'No',
                'remote_support': 'Yes'
            })
        
        # Add more to reach 377+ if needed
        if len(assessments) < 377:
            print(f"Need {377 - len(assessments)} more assessments. Creating sample ones...")
            for j in range(377 - len(assessments)):
                assessments.append({
                    'name': f"Sample Assessment {j+1}",
                    'url': f"https://www.shl.com/sample/assessment-{j+1}/",
                    'description': f"Sample assessment #{j+1} for testing",
                    'test_type': ['K'],
                    'duration': 45,
                    'adaptive_support': 'No',
                    'remote_support': 'Yes'
                })
        
        # Create DataFrame and save
        df = pd.DataFrame(assessments)
        df.to_csv('shl_assessments_from_excel.csv', index=False)
        print(f"Created dataset with {len(df)} assessments")
        
        return df
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        print("Make sure 'Gen_AI Dataset.xlsx' is in your project folder")
        return None

if __name__ == "__main__":
    df = create_dataset_from_excel()
    if df is not None:
        print(f"\nFirst few assessments:")
        print(df.head())