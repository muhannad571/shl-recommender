import streamlit as st
import requests
import json

st.set_page_config(
    page_title="SHL Assessment Recommender",
    page_icon="📊",
    layout="wide"
)

# App title
st.title("🎯 SHL Assessment Recommendation System")
st.markdown("""
Enter a job description or query to get recommended SHL assessments.
The system uses AI to find the most relevant tests for your hiring needs.
""")

# API endpoint (change to your deployed URL)
API_URL = "http://localhost:8000"

# Sidebar for API configuration
with st.sidebar:
    st.header("API Configuration")
    api_url = st.text_input("API Endpoint", value=API_URL)
    st.markdown("---")
    st.markdown("### How to Use")
    st.markdown("""
    1. Enter job description in the text area
    2. Click 'Get Recommendations'
    3. View recommended assessments
    4. Click URLs to visit assessment pages
    """)

# Main content
query = st.text_area(
    "Job Description / Query",
    height=150,
    placeholder="Example: I am hiring for Java developers who can also collaborate effectively with my business teams. Looking for an assessment(s) that can be completed in 40 minutes."
)

col1, col2 = st.columns([1, 1])
with col1:
    max_results = st.slider("Number of recommendations", 5, 10, 10)
with col2:
    st.markdown("")
    get_recommendations = st.button("🚀 Get Recommendations", type="primary")

if get_recommendations and query:
    with st.spinner("Finding the best assessments for you..."):
        try:
            # Call API
            response = requests.post(
                f"{api_url}/recommend",
                json={"query": query},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("recommended_assessments", [])
                
                st.success(f"Found {len(recommendations)} assessments")
                st.markdown("---")
                
                # Display recommendations
                for i, rec in enumerate(recommendations, 1):
                    with st.expander(f"{i}. {rec['name']}", expanded=True):
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.markdown(f"**Description:** {rec['description']}")
                            st.markdown(f"**Test Type:** {', '.join(rec['test_type'])}")
                            st.markdown(f"**Duration:** {rec['duration']} minutes")
                            
                            # Show badges
                            badge_cols = st.columns(3)
                            with badge_cols[0]:
                                adaptive_color = "green" if rec['adaptive_support'] == "Yes" else "red"
                                st.markdown(f"<span style='color:{adaptive_color}'>🔄 Adaptive: {rec['adaptive_support']}</span>", 
                                          unsafe_allow_html=True)
                            with badge_cols[1]:
                                remote_color = "green" if rec['remote_support'] == "Yes" else "red"
                                st.markdown(f"<span style='color:{remote_color}'>🌐 Remote: {rec['remote_support']}</span>", 
                                          unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown(f"[Visit Assessment Page]({rec['url']})")
                
                # Show JSON response
                with st.expander("View Raw API Response"):
                    st.json(data)
                    
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure the API server is running at the specified endpoint.")

elif get_recommendations:
    st.warning("Please enter a job description first!")

# Footer
st.markdown("---")
st.markdown("""
### 📊 About This System
- **Model**: Uses Sentence Transformers for semantic search + Gemini for ranking
- **Data**: Scraped from SHL product catalog (377+ individual test solutions)
- **Balance**: Ensures mix of technical and behavioral assessments when needed
- **API**: Fully compatible with SHL's requirements
""")