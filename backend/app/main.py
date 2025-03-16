import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="LUMA API", description="API for LUMA - Luminous AI Search")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://luma-zeta.vercel.app", "http://localhost:5173"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "Welcome to LUMA API. Go to /docs for API documentation."}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 