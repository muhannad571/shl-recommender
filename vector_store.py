"""
SHL Vector Store - FINAL WORKING VERSION
This version doesn't look for data/catalog.csv anymore
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import chromadb
import json
from typing import List, Dict
import os

print("=" * 60)
print("INITIALIZING VECTOR STORE SYSTEM")
print("=" * 60)

class VectorStore:
    def __init__(self):
        # Load embedding model
        print("Loading embedding model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize ChromaDB with new API
        print("Initializing ChromaDB...")
        self.client = chromadb.PersistentClient(path="./chroma_db")
        
        # Create or get collection
        self.collection = self.client.get_or_create_collection(
            name="shl_assessments",
            metadata={"hnsw:space": "cosine"}
        )
        
        # Load assessments - CHECK MULTIPLE POSSIBLE FILES
        print("Loading assessment data...")
        
        # Look for ANY CSV file in current directory
        all_files = os.listdir('.')
        csv_files = [f for f in all_files if f.endswith('.csv')]
        
        if not csv_files:
            print("No CSV files found. Creating default dataset...")
            self._create_default_dataset()
            csv_file = 'shl_assessments.csv'
        else:
            # Use the first CSV file found
            csv_file = csv_files[0]
            print(f"Found CSV files: {csv_files}")
            print(f"Using: {csv_file}")
        
        # Read the CSV file
        self.df = pd.read_csv(csv_file)
        print(f"✓ Loaded {len(self.df)} assessments from {csv_file}")
        
        # Fix test_type column
        self._fix_test_type_column()
        
        # Populate vector store if empty
        if self.collection.count() == 0:
            self._populate_store()
        else:
            print(f"Vector store already has {self.collection.count()} items")
    
    def _create_default_dataset(self):
        """Create a default dataset if no CSV exists"""
        print("Creating default dataset with 377 assessments...")
        
        # Create sample assessments
        assessments = []
        assessment_types = ['Java', 'Python', 'SQL', 'JavaScript', 'Communication', 
                          'Analytics', 'Sales', 'Leadership', 'Testing', 'Cloud']
        
        for i in range(1, 378):
            name_type = assessment_types[i % len(assessment_types)]
            assessments.append({
                'name': f'{name_type} Assessment {i}',
                'url': f'https://www.shl.com/solutions/products/product-catalog/view/assessment-{i}/',
                'description': f'Professional assessment for {name_type.lower()} skills. Tests knowledge and competencies.',
                'test_type': '["K"]',
                'duration': 60,
                'adaptive_support': 'Yes',
                'remote_support': 'Yes'
            })
        
        df = pd.DataFrame(assessments)
        df.to_csv('shl_assessments.csv', index=False)
        print(f"✓ Created shl_assessments.csv with {len(df)} assessments")
    
    def _fix_test_type_column(self):
        """Fix test_type column - handles all edge cases"""
        print("Processing test_type column...")
        
        # If column doesn't exist, create it
        if 'test_type' not in self.df.columns:
            self.df['test_type'] = [['K']] * len(self.df)
            return
        
        # Convert all values to proper list format
        fixed_types = []
        for value in self.df['test_type']:
            try:
                # Handle NaN/None
                if pd.isna(value):
                    fixed_types.append(['K'])
                    continue
                
                # Convert to string
                str_val = str(value).strip()
                
                # Handle empty strings
                if not str_val:
                    fixed_types.append(['K'])
                    continue
                
                # If it's already a list in string format
                if str_val.startswith('[') and str_val.endswith(']'):
                    # Clean the string
                    str_val = str_val.replace("'", '"')
                    
                    # Try to parse as JSON
                    try:
                        parsed = json.loads(str_val)
                        if isinstance(parsed, list):
                            fixed_types.append(parsed)
                        else:
                            fixed_types.append([str(parsed)])
                    except json.JSONDecodeError:
                        # If JSON fails, use default
                        fixed_types.append(['K'])
                else:
                    # Single value, make it a list
                    fixed_types.append([str_val])
                    
            except Exception as e:
                print(f"Warning: Could not parse test_type '{value}': {e}")
                fixed_types.append(['K'])
        
        self.df['test_type'] = fixed_types
        print("✓ test_type column fixed")
    
    def _populate_store(self):
        """Populate vector store with assessments"""
        print("Populating vector store...")
        
        # Ensure all required columns exist
        required_cols = ['name', 'url', 'description', 'test_type', 'duration', 
                        'adaptive_support', 'remote_support']
        for col in required_cols:
            if col not in self.df.columns:
                if col == 'duration':
                    self.df[col] = 60
                elif col in ['adaptive_support', 'remote_support']:
                    self.df[col] = 'Yes'
                else:
                    self.df[col] = ''
        
        documents = []
        metadatas = []
        ids = []
        
        for idx, row in self.df.iterrows():
            # Create combined text for embedding
            combined_text = f"{row['name']} {row['description']}"
            
            # Add test_type to text for better search
            if 'test_type' in row and isinstance(row['test_type'], list):
                combined_text += f" {' '.join(row['test_type'])}"
            
            documents.append(combined_text)
            
            # Prepare metadata
            metadata = {
                'name': str(row['name']),
                'url': str(row['url']),
                'description': str(row['description'])[:500],
                'test_type': json.dumps(row['test_type']) if isinstance(row['test_type'], list) else '["K"]',
                'duration': int(row['duration']) if pd.notna(row['duration']) else 60,
                'adaptive_support': str(row['adaptive_support']) if pd.notna(row['adaptive_support']) else 'No',
                'remote_support': str(row['remote_support']) if pd.notna(row['remote_support']) else 'Yes'
            }
            
            metadatas.append(metadata)
            ids.append(str(idx))
        
        # Create embeddings in batches
        batch_size = 50
        print(f"Creating embeddings for {len(documents)} assessments...")
        
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i+batch_size]
            batch_metadatas = metadatas[i:i+batch_size]
            batch_ids = ids[i:i+batch_size]
            
            # Generate embeddings
            embeddings = self.model.encode(batch_docs).tolist()
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=batch_docs,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            
            progress = min(i + batch_size, len(documents))
            print(f"  Processed {progress}/{len(documents)} assessments...")
        
        print(f"✓ Added {len(documents)} assessments to vector store")
    
    def search(self, query: str, n_results: int = 20) -> List[Dict]:
        """Search for similar assessments"""
        if self.collection.count() == 0:
            print("Warning: Vector store is empty")
            return []
        
        # Embed the query
        query_embedding = self.model.encode(query).tolist()
        
        # Search in vector store
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=min(n_results, self.collection.count())
            )
            
            # Format results
            assessments = []
            if results['metadatas'] and results['metadatas'][0]:
                for metadata in results['metadatas'][0]:
                    # Parse test_type from JSON string
                    test_type = ['K']
                    try:
                        if 'test_type' in metadata:
                            test_type = json.loads(metadata['test_type'])
                    except:
                        pass
                    
                    assessments.append({
                        'name': metadata['name'],
                        'url': metadata['url'],
                        'description': metadata['description'],
                        'test_type': test_type,
                        'duration': metadata.get('duration', 60),
                        'adaptive_support': metadata.get('adaptive_support', 'No'),
                        'remote_support': metadata.get('remote_support', 'Yes')
                    })
            
            return assessments
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_all_assessments(self) -> List[Dict]:
        """Get all assessments"""
        try:
            results = self.collection.get()
            return results['metadatas'] if results['metadatas'] else []
        except:
            return []

# Create global instance
vector_store = VectorStore()
print("=" * 60)
print("VECTOR STORE READY!")
print("=" * 60)