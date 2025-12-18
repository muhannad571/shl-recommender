#!/bin/bash
# deploy_api.sh

echo "🚀 Deploying SHL Recommendation API..."
echo "======================================="

# Check if in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Not in virtual environment. Creating one..."
    python -m venv venv
    source venv/bin/activate
fi

# Install requirements
echo "📦 Installing dependencies..."
pip install -r api/requirements.txt

# Check if assessments data exists
if [ ! -f "data/assessments.json" ]; then
    echo "📥 Creating sample assessment data..."
    python -c "
import json
sample_data = [
    {
        'url': 'https://www.shl.com/solutions/products/product-catalog/view/java-8-new/',
        'name': 'Java 8 Programming Assessment',
        'adaptive_support': 'Yes',
        'description': 'Tests Java 8 programming skills, object-oriented concepts',
        'duration': 60,
        'remote_support': 'Yes',
        'test_type': ['K']
    },
    {
        'url': 'https://www.shl.com/solutions/products/product-catalog/view/python-new/',
        'name': 'Python Programming Test',
        'adaptive_support': 'Yes',
        'description': 'Evaluates Python programming skills and problem-solving',
        'duration': 45,
        'remote_support': 'Yes',
        'test_type': ['K']
    },
    {
        'url': 'https://www.shl.com/products/product-catalog/view/interpersonal-communications/',
        'name': 'Interpersonal Communications',
        'adaptive_support': 'No',
        'description': 'Measures communication and collaboration skills',
        'duration': 30,
        'remote_support': 'Yes',
        'test_type': ['P']
    },
    {
        'url': 'https://www.shl.com/solutions/products/product-catalog/view/verify-verbal-ability-next-generation/',
        'name': 'Verbal Ability Assessment',
        'adaptive_support': 'Yes',
        'description': 'Tests verbal reasoning and comprehension',
        'duration': 35,
        'remote_support': 'Yes',
        'test_type': ['A']
    },
    {
        'url': 'https://www.shl.com/solutions/products/product-catalog/view/sql-server-new/',
        'name': 'SQL Server Assessment',
        'adaptive_support': 'Yes',
        'description': 'Tests SQL query writing and database knowledge',
        'duration': 50,
        'remote_support': 'Yes',
        'test_type': ['K']
    }
]
with open('data/assessments.json', 'w') as f:
    json.dump(sample_data, f, indent=2)
print('Created sample data with 5 assessments')
"
fi

echo "✅ Dependencies installed"
echo ""
echo "🌐 Starting API server..."
echo ""
echo "📋 API Endpoints:"
echo "   Health check:    http://localhost:5000/health"
echo "   Recommendations: http://localhost:5000/recommend"
echo "   Test endpoint:   http://localhost:5000/test"
echo ""
echo "📝 Example curl commands:"
echo "   curl http://localhost:5000/health"
echo "   curl -X POST -H 'Content-Type: application/json' \\"
echo "        -d '{\"query\": \"Java developer with team skills\"}' \\"
echo "        http://localhost:5000/recommend"
echo ""
echo "🎯 Web Interface: Open frontend/index.html in your browser"
echo ""

# Start the API
cd api
python app.py