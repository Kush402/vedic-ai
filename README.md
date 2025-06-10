# Vedic AI

A Vedic astrology application with AI-powered chart analysis.

## Live Deployment

You can try the live app here:

- **Frontend:** [https://vedic-ai-iumc.vercel.app/](https://vedic-ai-iumc.vercel.app/)

## Project Overview

Vedic AI is a modern web application that generates Vedic astrology charts and provides AI-powered analysis. Users can enter their birth details to receive a detailed astrological chart and an AI-generated report.

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

## Development

- Frontend runs on `http://localhost:5173`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.