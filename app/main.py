from fastapi import FastAPI
from app.routers import invoice_generation_routers, po, invoiceInput, warehouse, reportingDetails
from app.routers import auth, users
from app.routers import get_distys
from app.routers import common
from app.routers import client_onboard
from app.routers import password
from fastapi.middleware.cors import CORSMiddleware
from app.config import load_clients
from app.logging_config import setup_logging
import logging
from app.routers import client_onboard
from starlette.middleware.base import BaseHTTPMiddleware

# Setup logging
setup_logging()

# Define the FastAPI app instance at the module level
app = FastAPI()

class ContentSecurityPolicyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Allow Swagger UI to load over HTTP
        if request.url.path.startswith("/docs") or request.url.path.startswith("/openapi.json"):
            response = await call_next(request)
            response.headers[
                "Content-Security-Policy"
            ] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' http: https:;"
            return response

        # Default policy for other routes
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = "upgrade-insecure-requests;"
        return response


# Add the middleware
app.add_middleware(ContentSecurityPolicyMiddleware)

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
app.include_router(client_onboard.router)
app.include_router(common.router)
app.include_router(po.router)
app.include_router(invoiceInput.router)
app.include_router(warehouse.router)
app.include_router(reportingDetails.router)
app.include_router(invoice_generation_routers.router,tags=['Invoice Generation API'])
app.include_router(password.router)
logging.debug("Debugging initialized")



import uvicorn


if __name__=="__main__":
    uvicorn.run("app.main:app",port=8000,reload=True,debug=True)