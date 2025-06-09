# Vedic AI

A modern web application for Vedic astrology calculations and predictions.

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
The frontend is configured for deployment on Vercel. The build process is handled automatically.

### Backend
The backend can be deployed on any Python-compatible hosting service.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.