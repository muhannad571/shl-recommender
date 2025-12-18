from flask import Flask, request, jsonify
from flask_cors import CORS
import os

# Import recommendation engine
try:
    from recommendation_engine import recommendation_engine
    print("✅ Recommendation engine loaded")
except ImportError as e:
    print(f"⚠️ Error: {e}")
    print("Using fallback engine...")
    # Simple fallback engine
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
    recommendation_engine = DummyEngine()

app = Flask(__name__)
CORS(app)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

@app.route('/recommend', methods=['POST'])
def recommend():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
        
        query = data.get('query', '')
        max_results = data.get('max_results', 10)
        
        if not query:
            return jsonify({'error': 'Query parameter is required'}), 400
        
        results = recommendation_engine.recommend(query, max_results)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': 'API is working!'})

if __name__ == '__main__':
    print("Starting SHL Recommender API on http://0.0.0.0:5000")
    print("Available endpoints:")
    print("  GET  /health     - Health check")
    print("  GET  /test       - Test endpoint")
    print("  POST /recommend  - Get recommendations")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)