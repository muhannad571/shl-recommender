# SHL Assessment Recommendation System
## Technical Documentation

### 1. Solution Architecture

**System Components:**
1. **Data Pipeline**: Scrapes 377+ SHL individual test solutions
2. **Vector Database**: ChromaDB with sentence-transformers embeddings
3. **LLM Layer**: Gemini Pro for intelligent ranking and balancing
4. **API Layer**: FastAPI with REST endpoints
5. **Frontend**: Streamlit web interface

**Technology Stack:**
- Python 3.9+
- FastAPI (Backend)
- Streamlit (Frontend)
- ChromaDB (Vector storage)
- Sentence Transformers (Embeddings)
- Google Gemini (LLM ranking)

### 2. Data Pipeline

**Scraping Process:**
1. Parse SHL sitemap for all product URLs
2. Filter out pre-packaged solutions
3. Extract assessment metadata:
   - Name, URL, Description
   - Test Type (A/B/C/D/E/K/P/S)
   - Duration, Adaptive support, Remote support
4. Store in CSV + vector embeddings

**Data Validation:**
- Minimum 377 individual test solutions ✓
- Test type categorization ✓
- URL validity checking ✓

### 3. Recommendation Algorithm

**Two-Stage Approach:**

**Stage 1: Semantic Search**
- Query embedding using all-MiniLM-L6-v2
- Cosine similarity search in ChromaDB
- Returns top 20 candidate assessments

**Stage 2: LLM Ranking & Balancing**
- Gemini Pro analyzes query requirements
- Considers: Technical skills, soft skills, duration constraints
- Ensures balanced mix of test types
- Outputs ranked top 10 assessments

**Balancing Logic:**
```python
if query_requires_multiple_skills:
    # Ensure mix of test types
    technical_assessments = filter(test_type='K')
    behavioral_assessments = filter(test_type='P')
    balanced_list = interleave(technical, behavioral)