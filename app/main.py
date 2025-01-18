from fastapi import FastAPI
from app.routers import auth, users
from app.routers import get_distys
from fastapi.middleware.cors import CORSMiddleware
from app.config import load_clients
from app.logging_config import setup_logging
import logging

# Setup logging
setup_logging()

# Define the FastAPI app instance at the module level
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Load client configurations
CONFIG_FILE = "app/config/clients.json"
clients = load_clients(CONFIG_FILE)

# Optional: Define a startup event to log clients or other initialization tasks
@app.on_event("startup")
async def startup_event():
    print(f"Loaded clients: {clients}")

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(get_distys.router)
logging.debug("Debugging initialized")
