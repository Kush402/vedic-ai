# Vedic AI

A Vedic astrology application with AI-powered chart analysis.

## Environment Variables

### Frontend (Vercel)

Set these environment variables in your Vercel project settings:

- `VITE_API_URL`: Backend API URL (e.g., `https://vedic-backend.onrender.com/api/v1`)

### Backend (Render)

Set these environment variables in your Render project settings:

- `GEMINI_API_KEY`: Your Google Gemini API key
- `SWEPH_PATH`: Path to Swiss Ephemeris files (automatically set in Dockerfile)

## Project Structure

```
vedic-ai/
├── frontend/               # React + TypeScript frontend
│   ├── src/               # Source code
│   ├── public/            # Static assets
│   ├── package.json       # Frontend dependencies
│   ├── tsconfig.json      # TypeScript configuration
│   └── vite.config.ts     # Vite configuration
│
├── backend/               # Python FastAPI backend
│   ├── astrology/        # Astrology calculation modules
│   ├── requirements.txt   # Python dependencies
│   └── run_api.py        # API server entry point
│
├── ephe/                  # Ephemeris data files
│
└── setup.sh              # Project setup script
```

## Setup Instructions

### Prerequisites
- Node.js 18.x or later
- Python 3.8 or later
- Git

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start development server:
   ```bash
   npm run dev
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the API server:
   ```bash
   python run_api.py
   ```

## Development

- Frontend runs on `http://localhost:5173`
- Backend API runs on `http://localhost:8000`

## Deployment

### Frontend (Vercel)

1. Connect your GitHub repository to Vercel
2. Set environment variables in Vercel dashboard
3. Deploy

### Backend (Render)

1. Connect your GitHub repository to Render
2. Set environment variables in Render dashboard
3. Deploy

## API Endpoints

- `GET /api/v1/health`: Health check
- `POST /api/v1/charts`: Generate birth chart
- `POST /api/v1/generate-report`: Generate AI analysis report

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.