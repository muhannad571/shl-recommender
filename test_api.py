import requests
import json

# Test the API
def test_api():
    base_url = "http://localhost:8000"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        health_response = requests.get(f"{base_url}/health")
        print(f"Health status: {health_response.json()}")
    except:
        print("❌ API not running!")
        return
    
    # Test recommendation endpoint
    test_queries = [
        "I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes.",
        "I want to hire new graduates for a sales role in my company, the budget is for about an hour for each test.",
        "Content Writer required, expert in English and SEO."
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Testing query: {query[:100]}...")
        
        response = requests.post(
            f"{base_url}/recommend",
            json={"query": query}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Got {len(data['recommended_assessments'])} recommendations")
            for i, rec in enumerate(data['recommended_assessments'][:3], 1):
                print(f"  {i}. {rec['name']} ({rec['test_type']})")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    test_api()