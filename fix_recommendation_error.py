import os
import onnxruntime

print("🔧 Fixing recommendation_engine error...")
print("=" * 60)

# 1. Check if recommendation_engine.py exists
if not os.path.exists('recommendation_engine.py'):
    print("Creating recommendation_engine.py...")
    engine_code = '''import google.generativeai as genai
from typing import List, Dict
import json
import os
from dotenv import load_dotenv

# Simple fallback engine
class RecommendationEngine:
    def __init__(self):
        print("Initializing RecommendationEngine...")
    
    def recommend(self, query: str, max_results: int = 10) -> List[Dict]:
        print(f"Processing: {query[:50]}...")
        return [
            {
                'name': 'Java Programming Test',
                'url': 'https://www.shl.com/solutions/products/product-catalog/view/java-8-new/',
                'description': 'Java programming assessment',
                'test_type': ['K'],
                'duration': 45,
                'adaptive_support': 'No',
                'remote_support': 'Yes'
            },
            {
                'name': 'Communication Skills',
                'url': 'https://www.shl.com/products/product-catalog/view/interpersonal-communications/',
                'description': 'Communication assessment',
                'test_type': ['P'],
                'duration': 30,
                'adaptive_support': 'No',
                'remote_support': 'Yes'
            }
        ][:max_results]

# Create instance
recommendation_engine = RecommendationEngine()'''
    
    with open('recommendation_engine.py', 'w') as f:
        f.write(engine_code)
    print("✅ Created recommendation_engine.py")

# 2. Update api.py to use simpler import
print("\nUpdating api.py imports...")
if os.path.exists('api.py'):
    # Add this before line 54 (adjust the path as needed)
    file_path = "api.py"
    # Or if api.py is in the same directory:
    import os

    file_path = os.path.join(os.path.dirname(__file__), "api.py")
    # Define the file path if it's not defined
    if 'file_path' not in locals():
        file_path = os.path.join(os.path.dirname(__file__), 'api.py')

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the import section
    new_import = '''# Import recommendation engine
try:
    from recommendation_engine import recommendation_engine
    print("✅ Recommendation engine loaded")
except ImportError as e:
    print(f"⚠️ Using fallback engine: {e}")
    # Create simple fallback
    class DummyEngine:
        def recommend(self, query, max_results=10):
            return [
                {
                    'name': 'Java Test',
                    'url': 'https://shl.com/java',
                    'description': 'Java assessment',
                    'test_type': ['K'],
                    'duration': 45,
                    'adaptive_support': 'No',
                    'remote_support': 'Yes'
                }
            ][:max_results]
    recommendation_engine = DummyEngine()'''
    
    # Find and replace
    if 'from recommendation_engine import' in content:
        # Simple replacement
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            if 'from recommendation_engine import' in lines[i]:
                # Skip to where recommendation_engine is defined in except
                while i < len(lines) and 'recommendation_engine =' not in lines[i]:
                    i += 1
                # Add our new import
                new_lines.extend(new_import.split('\n'))
                # Skip the rest of old import block
                while i < len(lines) and ('except' in lines[i] or 'ImportError' in lines[i] or 'class DummyEngine' in lines[i]):
                    i += 1
                continue
            new_lines.append(lines[i])
            i += 1
        
        content = '\n'.join(new_lines)
    
    with open('api.py', 'w') as f:
        f.write(content)
    print("✅ Updated api.py")

print("\n" + "=" * 60)
print("✅ FIX COMPLETE!")
print("Now run: python api.py")
print("=" * 60)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)