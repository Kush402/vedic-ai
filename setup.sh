#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting Vedic AI Project Setup...${NC}\n"

# Check if Python 3.8+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Node.js is required but not installed. Please install Node.js 16 or higher."
    exit 1
fi

# Create and activate virtual environment
echo -e "${BLUE}Setting up Python virtual environment...${NC}"
python3 -m venv .venv
source .venv/bin/activate

# Install backend dependencies
echo -e "${BLUE}Installing backend dependencies...${NC}"
pip install -r backend/requirements.txt

# Install frontend dependencies
echo -e "${BLUE}Installing frontend dependencies...${NC}"
cd frontend
npm install
cd ..

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${BLUE}Creating .env file...${NC}"
    cat > .env << EOL
# Backend Configuration
BACKEND_PORT=8000
BACKEND_HOST=localhost

# Frontend Configuration
VITE_API_URL=http://localhost:8000/api/v1

# Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
EOL
    echo -e "${GREEN}Created .env file. Please update it with your Gemini API key.${NC}"
fi

# Create a README.md if it doesn't exist
if [ ! -f README.md ]; then
    echo -e "${BLUE}Creating README.md...${NC}"
    cat > README.md << EOL
# Vedic AI - Vedic Astrology Analysis Platform

A modern web application that provides detailed Vedic astrology chart analysis using AI.

## Features

- Generate detailed Vedic astrology charts
- AI-powered chart analysis and predictions
- Interactive chart visualization
- Comprehensive birth chart analysis
- Dasha period calculations
- Nakshatra and planetary position analysis

## Setup

1. Clone the repository:
\`\`\`bash
git clone https://github.com/Kush402/vedic-ai.git
cd vedic-ai
\`\`\`

2. Run the setup script:
\`\`\`bash
chmod +x setup.sh
./setup.sh
\`\`\`

3. Update the \`.env\` file with your Gemini API key

4. Start the development servers:

Backend:
\`\`\`bash
cd backend
uvicorn main:app --reload
\`\`\`

Frontend:
\`\`\`bash
cd frontend
npm run dev
\`\`\`

## Environment Variables

- \`BACKEND_PORT\`: Port for the backend server (default: 8000)
- \`BACKEND_HOST\`: Host for the backend server (default: localhost)
- \`VITE_API_URL\`: API URL for the frontend (default: http://localhost:8000/api/v1)
- \`GEMINI_API_KEY\`: Your Gemini API key

## Technologies Used

- Backend: FastAPI, Python, Swiss Ephemeris
- Frontend: React, TypeScript, Vite
- AI: Google Gemini API
- Database: SQLite

## License

MIT License
EOL
fi

echo -e "\n${GREEN}Setup completed successfully!${NC}"
echo -e "\nTo start the development servers:"
echo -e "1. Backend: ${BLUE}cd backend && uvicorn main:app --reload${NC}"
echo -e "2. Frontend: ${BLUE}cd frontend && npm run dev${NC}"
echo -e "\nDon't forget to update the .env file with your Gemini API key!" 