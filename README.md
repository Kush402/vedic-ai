# Vedic Astrology Report Generator

A web application that generates detailed Vedic astrology reports based on birth details. The application uses Python for the backend and React for the frontend.

## Features

- Input birth details (name, date of birth, time of birth, latitude, longitude)
- Generate comprehensive Vedic astrology reports
- Beautiful and responsive user interface
- Detailed analysis of planetary positions and their effects
- Career and life path insights
- Relationship dynamics analysis
- Current Dasha period analysis
- Personal growth recommendations

## Tech Stack

### Backend
- Python
- FastAPI
- Google Gemini AI for report generation
- Vedic astrology calculations

### Frontend
- React
- TypeScript
- Vite
- Axios for API calls
- Modern CSS styling

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vedic.git
cd vedic
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

4. Start the development servers:

Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
cd frontend
npm run dev
```

5. Open http://localhost:5173 in your browser

## Usage

1. Enter your birth details in the form:
   - Name
   - Date of Birth
   - Time of Birth
   - Latitude
   - Longitude

2. Click "Generate Report" to get your personalized Vedic astrology report

3. The report will include:
   - Planetary positions and their effects
   - Career and life path insights
   - Relationship dynamics
   - Current Dasha period analysis
   - Personal growth recommendations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.