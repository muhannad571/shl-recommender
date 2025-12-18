# Simple recommendation engine
class RecommendationEngine:
    def __init__(self):
        print("Initializing RecommendationEngine...")
    
    def recommend(self, query, max_results=10):
        print(f"Processing query: {query}")
        # Return sample data
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
recommendation_engine = RecommendationEngine()