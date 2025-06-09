from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from astrology.api import router as astrology_router

app = FastAPI(title="Vedic AI API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local development
        "https://vedic-ai-snowy.vercel.app",  # Vercel frontend
        "https://vedic-ai.onrender.com",      # Render backend (self-calls)
        "https://*.vercel.app"  # Any Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(astrology_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False) 