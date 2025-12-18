# test_api.py
import requests
import json

def test_api():
    base_url = "http://localhost:5000"
    
    # Test health endpoint
    print("1️⃣ Testing health endpoint...")
    response = requests.get(f"{base_url}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print()
    
    # Test recommendation endpoint
    print("2️⃣ Testing recommendation endpoint...")
    
    test_queries = [
        "Java developer with collaboration skills, 40 minute test",
        "Python and SQL data analyst",
        "Sales role for new graduates, 30 minutes",
        "Cognitive and personality tests for analysts"
    ]
    
    for query in test_queries:
        print(f"   Query: {query}")
        response = requests.post(
            f"{base_url}/recommend",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Success! Got {len(data.get('recommended_assessments', []))} recommendations")
            # Show first recommendation
            if data['recommended_assessments']:
                first = data['recommended_assessments'][0]
                print(f"   📊 Sample: {first['name']} ({first['duration']} min)")
        else:
            print(f"   ❌ Error {response.status_code}: {response.text}")
        print()
    
    # Test GET method
    print("3️⃣ Testing GET method...")
    response = requests.get(f"{base_url}/recommend?q=Java%20developer")
    print(f"   Status: {response.status_code}")
    print(f"   Got {len(response.json().get('recommended_assessments', []))} recommendations")
    print()
    
    print("🎉 All tests completed!")

if __name__ == "__main__":
    test_api()