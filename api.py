# api/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import json
import pandas as pd
from typing import List, Dict
import re

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import our recommender (we'll create this)
try:
    from src.recommender import SHLRecommender
    print("✅ Recommender loaded successfully")
except ImportError as e:
    print(f"⚠️  Recommender import failed: {e}")
    # Create a fallback class
    class SHLRecommender:
        def __init__(self):
            self.assessments = self._load_assessments()
        
        def _load_assessments(self):
            try:
                with open('../data/assessments.json', 'r') as f:
                    return json.load(f)
            except:
                # Return sample data if file doesn't exist
                return [
                    {
                        "url": "https://www.shl.com/solutions/products/product-catalog/view/java-8-new/",
                        "name": "Java 8 Assessment",
                        "adaptive_support": "Yes",
                        "description": "Tests Java 8 programming skills",
                        "duration": 60,
                        "remote_support": "Yes",
                        "test_type": ["K"]
                    },
                    # Add more sample assessments...
                ]
        
        def recommend(self, query: str, k: int = 10) -> List[Dict]:
            # Simple keyword matching as fallback
            results = []
            query_lower = query.lower()
            
            for assessment in self.assessments:
                score = 0
                desc = assessment.get('description', '').lower()
                name = assessment.get('name', '').lower()
                
                # Check for keyword matches
                if 'java' in query_lower and ('java' in desc or 'java' in name):
                    score += 3
                if 'python' in query_lower and ('python' in desc or 'python' in name):
                    score += 3
                if 'sql' in query_lower and ('sql' in desc or 'sql' in name):
                    score += 3
                if 'developer' in query_lower and 'developer' in desc:
                    score += 2
                if 'collaborat' in query_lower and ('team' in desc or 'communication' in desc):
                    score += 2
                
                if score > 0:
                    results.append((score, assessment))
            
            # Sort by score and return
            results.sort(key=lambda x: x[0], reverse=True)
            return [r[1] for r in results[:k]]
        
        def balance_recommendations(self, recommendations: List[Dict], query: str) -> List[Dict]:
            return recommendations[:10]

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize recommender
recommender = SHLRecommender()

def extract_duration_constraint(query: str) -> tuple:
    """
    Extract duration constraints from query.
    Returns (min_duration, max_duration) or (None, None)
    """
    query_lower = query.lower()
    
    # Patterns for duration extraction
    patterns = [
        r'(\d+)[-\s]+(\d+)\s*minute',
        r'(\d+)[-\s]+(\d+)\s*min',
        r'(\d+)\s*minute',
        r'(\d+)\s*min',
        r'(\d+)[-\s]+(\d+)\s*hour',
        r'(\d+)\s*hour',
        r'about\s*an?\s*hour',
        r'less than\s*(\d+)',
        r'max\s*(\d+)',
        r'at most\s*(\d+)'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, query_lower)
        if matches:
            if isinstance(matches[0], tuple):
                # Range like "30-40 minutes"
                min_time, max_time = map(int, matches[0])
                return min_time, max_time
            else:
                # Single value like "60 minutes"
                time_val = int(matches[0])
                return time_val - 10, time_val + 10
    
    # Check for common phrases
    if 'short test' in query_lower or 'quick assessment' in query_lower:
        return 15, 30
    elif 'long assessment' in query_lower:
        return 90, 180
    
    return None, None

def filter_by_duration(assessments: List[Dict], min_time: int, max_time: int) -> List[Dict]:
    """Filter assessments by duration constraints"""
    filtered = []
    for assessment in assessments:
        duration = assessment.get('duration', 60)
        if min_time <= duration <= max_time:
            filtered.append(assessment)
    
    # If no matches, return closest matches
    if not filtered and assessments:
        # Sort by closeness to desired duration
        assessments.sort(key=lambda x: abs(x.get('duration', 60) - (min_time + max_time)/2))
        filtered = assessments[:min(10, len(assessments))]
    
    return filtered

@app.route('/')
def index():
    """API Documentation"""
    return jsonify({
        "name": "SHL Assessment Recommendation API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check endpoint",
            "POST /recommend": "Get assessment recommendations"
        },
        "example_request": {
            "method": "POST",
            "url": "/recommend",
            "body": {"query": "Java developer with collaboration skills"}
        },
        "example_response": {
            "recommended_assessments": [
                {
                    "url": "https://www.shl.com/...",
                    "name": "Assessment Name",
                    "adaptive_support": "Yes",
                    "description": "Assessment description",
                    "duration": 60,
                    "remote_support": "Yes",
                    "test_type": ["K", "P"]
                }
            ]
        }
    })

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint - required by specification"""
    return jsonify({
        "status": "healthy",
        "service": "SHL Assessment Recommender API",
        "timestamp": pd.Timestamp.now().isoformat()
    }), 200

@app.route('/recommend', methods=['POST', 'GET'])
def recommend():
    """
    Main recommendation endpoint.
    Accepts: POST with JSON body {"query": "text"}
    Also supports GET with query parameter: ?q=text
    """
    try:
        # Handle both POST and GET
        if request.method == 'GET':
            query = request.args.get('q', '')
        else:
            # POST request
            if not request.is_json:
                return jsonify({
                    "error": "Content-Type must be application/json"
                }), 400
            
            data = request.get_json()
            query = data.get('query', '')
        
        # Validate query
        if not query or not isinstance(query, str):
            return jsonify({
                "error": "Query must be a non-empty string",
                "example": {"query": "Java developer with collaboration skills"}
            }), 400
        
        # Clean and truncate query
        query = query.strip()
        if len(query) > 1000:
            query = query[:1000] + "..."
        
        print(f"📥 Received query: {query[:100]}...")
        
        # Extract duration constraints
        min_duration, max_duration = extract_duration_constraint(query)
        
        # Get recommendations
        raw_recommendations = recommender.recommend(query, k=15)
        
        # Apply duration filter if constraints exist
        if min_duration is not None and max_duration is not None:
            print(f"⏱️  Applying duration filter: {min_duration}-{max_duration} minutes")
            raw_recommendations = filter_by_duration(raw_recommendations, min_duration, max_duration)
        
        # Balance recommendations
        recommendations = recommender.balance_recommendations(raw_recommendations, query)
        
        # Ensure we have 5-10 recommendations
        if len(recommendations) < 5:
            # Try to get more recommendations
            additional = recommender.recommend(query, k=20)
            for rec in additional:
                if rec not in recommendations:
                    recommendations.append(rec)
                if len(recommendments) >= 10:
                    break
        
        # Trim to maximum 10
        recommendations = recommendations[:10]
        
        # Ensure minimum 1 (as per spec)
        if not recommendations:
            # Return some default assessments
            recommendations = recommender.assessments[:5]
        
        # Format response exactly as specified
        response = {
            "recommended_assessments": [
                {
                    "url": rec.get("url", ""),
                    "name": rec.get("name", "Unknown Assessment"),
                    "adaptive_support": rec.get("adaptive_support", "No"),
                    "description": rec.get("description", ""),
                    "duration": int(rec.get("duration", 60)),
                    "remote_support": rec.get("remote_support", "Yes"),
                    "test_type": rec.get("test_type", [])
                }
                for rec in recommendations
            ]
        }
        
        print(f"✅ Returning {len(recommendations)} recommendations")
        return jsonify(response), 200
    
    except Exception as e:
        print(f"❌ Error processing request: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Test endpoint with sample queries"""
    sample_queries = [
        "I am hiring for Java developers who can also collaborate effectively with my business teams",
        "Looking to hire mid-level professionals who are proficient in Python, SQL and JavaScript",
        "Need assessments for a sales role, about 30 minutes each",
        "Cognitive and personality tests for analyst position"
    ]
    
    return jsonify({
        "test_queries": sample_queries,
        "usage": "Use POST /recommend with JSON body: {\"query\": \"your text here\"}",
        "example": {
            "curl": "curl -X POST -H 'Content-Type: application/json' -d '{\"query\": \"Java developer\"}' http://localhost:5000/recommend"
        }
    })

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 SHL Assessment Recommendation API")
    print("=" * 60)
    print("\n📋 Available Endpoints:")
    print("  GET  /health     - Health check")
    print("  POST /recommend  - Get recommendations (main endpoint)")
    print("  GET  /recommend?q=query - Get recommendations via GET")
    print("  GET  /test       - Test queries and usage")
    print("\n⚡ Starting server on http://localhost:5000")
    print("📝 Press Ctrl+C to stop")
    print("=" * 60)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        threaded=True
    )