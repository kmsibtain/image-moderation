from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import auth, moderation
from services.database import connect_to_mongo, close_mongo_connection
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="Image Moderation API",
    description="API for detecting and blocking harmful imagery.",
    version="1.0.0"
)

# Database connection events
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Include routers
app.include_router(auth.router)
app.include_router(moderation.router)

@app.get("/")
async def root():
    return {"message": "Image Moderation API is running!"}

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:80",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)