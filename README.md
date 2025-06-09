# Vedic AI - Advanced Vedic Astrology Analysis Platform

A modern, AI-powered Vedic astrology platform that provides detailed astrological analysis using advanced calculations and AI-generated interpretations. This project demonstrates a practical implementation of Retrieval-Augmented Generation (RAG) for domain-specific AI applications.

## 🌟 Features

### AI-Powered Analysis (RAG Implementation)
- **Contextual Astrological Interpretation**
  - Retrieval of relevant astrological principles and rules
  - Structured prompt engineering for accurate interpretations
  - Domain-specific knowledge integration
  - Real-time analysis of planetary configurations

- **Intelligent Report Generation**
  - Dynamic content generation based on chart data
  - Contextual understanding of planetary relationships
  - Personalized life path analysis
  - Adaptive interpretation based on multiple factors

### Astrological Calculations
- **D1 (Rashi) Chart Generation**
  - Accurate planetary positions using Swiss Ephemeris
  - House placements with Whole Sign system
  - Detailed planetary aspects
  - Nakshatra and Pada calculations

### Planetary Analysis
- **Comprehensive Planet Strengths**
  - Dignity status (Exalted, Debilitated, Own Sign, Neutral)
  - Combustion detection
  - Retrograde status
  - Overall planetary condition assessment
  - Numerical strength indicators

### AI-Powered Reports
- **Detailed Life Analysis**
  - Personality and life path insights
  - Career and professional guidance
  - Relationship dynamics
  - Health and well-being
  - Current dasha period analysis
  - Personal growth recommendations

### Technical Features
- **Modern Tech Stack**
  - FastAPI backend with Python
  - React/TypeScript frontend
  - Google Gemini AI integration
  - Swiss Ephemeris for accurate calculations
  - RESTful API architecture

## 🤖 AI Implementation Details

### RAG Architecture
1. **Knowledge Base**
   - Vedic astrology principles and rules
   - Planetary relationships and significations
   - House and sign meanings
   - Dasha system interpretations

2. **Retrieval Process**
   - Chart data analysis
   - Planetary position evaluation
   - Aspect pattern recognition
   - Dignity and strength assessment

3. **Generation Process**
   - Context-aware prompt construction
   - Multi-factor analysis integration
   - Structured response formatting
   - Personalized interpretation generation

### AI Features
- **Smart Context Integration**
  - Combines multiple astrological factors
  - Weights different planetary influences
  - Considers temporal aspects (dashas)
  - Balances traditional and modern interpretations

- **Adaptive Learning**
  - Pattern recognition in planetary configurations
  - Dynamic interpretation adjustment
  - Contextual relevance assessment
  - Personalized insight generation

### Example RAG Flow
1. **Input Processing**
   ```python
   # Chart data analysis
   chart_data = calculate_d1_chart(name, dob, tob, latitude, longitude)
   ```

2. **Context Retrieval**
   ```python
   # Planetary strength analysis
   planet_strengths = calculate_planet_strengths(jd, latitude, longitude)
   
   # Aspect pattern analysis
   aspects = calculate_aspects(jd)
   ```

3. **Prompt Construction**
   ```python
   # Structured prompt with retrieved context
   prompt = f"""
   Based on the following Vedic astrology chart data:
   - Planetary positions and strengths
   - House placements and aspects
   - Current dasha period
   Provide a comprehensive analysis...
   """
   ```

4. **Response Generation**
   ```python
   # AI-powered interpretation
   report = generate_astrology_report(chart_data)
   ```

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- Google Gemini API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Kush402/vedic-ai.git
cd vedic-ai
```

2. Set up the backend:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Create a `.env` file in the backend directory:
```
GEMINI_API_KEY=your_gemini_api_key
```

5. Run the development servers:
```bash
# Backend (from backend directory)
uvicorn run_api:app --reload

# Frontend (from frontend directory)
npm run dev
```

## 📚 API Documentation

### Endpoints

#### 1. Generate Chart
```http
POST /api/v1/charts
```
Generates a complete D1 chart with planetary positions, aspects, and strengths.

**Request Body:**
```json
{
    "name": "string",
    "dob": "YYYY-MM-DD",
    "tob": "HH:MM",
    "location": "City, Country"
}
```

**Response:**
```json
{
    "name": "string",
    "ascendant": "string",
    "houses": [
        {
            "house": "string",
            "sign": "string",
            "planets": "string"
        }
    ],
    "nakshatra": {
        "nakshatra": "string",
        "pada": "integer"
    },
    "dasha": {
        "current_maha_dasha": "string",
        "years_remaining": "float",
        "sequence": [
            {
                "lord": "string",
                "start_year": "float",
                "end_year": "float"
            }
        ]
    },
    "planet_strengths": {
        "planet_name": {
            "sign": "string",
            "longitude": "float",
            "dignity": "string",
            "retrograde": "boolean",
            "combust": "boolean",
            "strength": "float",
            "condition": "string"
        }
    },
    "aspects": {
        "planet_name": ["aspecting_planets"]
    }
}
```

#### 2. Generate Report (RAG Implementation)
```http
POST /api/v1/generate-report
```
Generates a comprehensive astrological report using RAG-based AI analysis.

**Request Body:**
```json
{
    "name": "string",
    "dob": "YYYY-MM-DD",
    "tob": "HH:MM",
    "location": "City, Country"
}
```

**Response:**
```json
{
    "overall_analysis": "string",
    "chart_data": {
        // Chart calculations
    },
    "ai_analysis": {
        "personality_insights": "string",
        "life_path_analysis": "string",
        "career_guidance": "string",
        "relationship_dynamics": "string",
        "health_insights": "string",
        "dasha_analysis": "string",
        "recommendations": "string"
    }
}
```

## 🛠️ Project Structure

```
vedic-ai/
├── backend/
│   ├── astrology/
│   │   ├── api.py          # API endpoints
│   │   ├── charts.py       # Chart calculations
│   │   ├── llm_query.py    # RAG implementation
│   │   ├── models.py       # Data models
│   │   └── utils.py        # Utility functions
│   ├── run_api.py          # API server
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API services
│   │   └── App.tsx         # Main application
│   └── package.json        # Node dependencies
└── setup.sh               # Setup script
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Swiss Ephemeris for accurate astronomical calculations
- Google Gemini AI for intelligent report generation
- The Vedic astrology community for their knowledge and insights
- RAG architecture patterns and implementations