# Vedic AI - Vedic Astrology Analysis Platform

A modern web application that provides detailed Vedic astrology analysis using Swiss Ephemeris calculations and AI-powered interpretations.

## Features

- **Accurate Planetary Calculations**: Uses Swiss Ephemeris for precise planetary positions
- **D1 Chart Analysis**: Complete birth chart calculation with house placements
- **Vimshottari Dasha**: Accurate dasha period calculations
- **AI-Powered Reports**: Detailed astrological interpretations using Gemini AI
- **Modern UI**: Clean and intuitive user interface built with React and TypeScript

## Tech Stack

### Backend
- Python 3.9+
- FastAPI
- Swiss Ephemeris
- Gemini AI API
- Pydantic for data validation

### Frontend
- React 18
- TypeScript
- Vite
- Tailwind CSS
- React Router

## Project Structure

```
vedic/
├── backend/
│   ├── astrology/
│   │   ├── api.py           # FastAPI routes
│   │   │   ├── charts.py        # Chart calculations
│   │   │   ├── llm_query.py     # AI report generation
│   │   │   └── models.py        # Data models
│   │   ├── ephe/                # Swiss Ephemeris files
│   │   └── run_api.py           # API server
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── charts.py          # Chart components
│   │   │   ├── pages/          # Page components
│   │   │   ├── services/       # API services
│   │   │   └── types/          # TypeScript types
│   │   └── package.json
└── setup.sh                 # Installation script
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Kush402/vedic-ai.git
cd vedic-ai
```

2. Run the setup script:
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment
- Install backend dependencies
- Download Swiss Ephemeris files
- Install frontend dependencies
- Set up environment variables

## Running the Application

1. Start the backend server:
```bash
cd backend
uvicorn run_api:app --reload --port 8001
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8001

## API Endpoints

### `/api/v1/charts`
- **Method**: POST
- **Description**: Calculate D1 chart
- **Request Body**:
  ```json
  {
    "name": "string",
    "dob": "YYYY-MM-DD",
    "tob": "HH:MM",
    "latitude": number,
    "longitude": number
  }
  ```

### `/api/v1/generate-report`
- **Method**: POST
- **Description**: Generate AI-powered astrological report
- **Request Body**: Same as charts endpoint

## Environment Variables

Create a `.env` file in the backend directory:

```env
GEMINI_API_KEY=your_gemini_api_key
SWEPH_PATH=path_to_ephemeris_files
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Swiss Ephemeris for accurate astronomical calculations
- Google Gemini AI for astrological interpretations
- FastAPI for the robust backend framework
- React and Vite for the modern frontend