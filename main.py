# main.py
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, rooms, upload

# Create all database tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Large File Uploader API")

# --- CORS Middleware ---
# This allows your React frontend (running on a different port) to communicate with the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # The origin of your React app
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Create uploads directory if it doesn't exist ---
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# --- API Routers ---
# Include the routes from other files
app.include_router(auth.router, tags=["Authentication"])
app.include_router(rooms.router, tags=["Rooms"])
app.include_router(upload.router, tags=["Upload"])


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the FastAPI File Uploader!"}

