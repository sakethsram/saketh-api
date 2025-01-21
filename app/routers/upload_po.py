from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Form, Header, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os
import shutil
import hashlib
from typing import List
from datetime import datetime
from app.models import User
from app.schemas import UploadPoSchema
from app.routers.automationscript import po_to_json 
from app.security import validate_token 
from app.dependencies import get_db  


router = APIRouter()
security_scheme = HTTPBearer()

# Base folder for storing files
BASE_FOLDER = "e-Commerce-platform"
PURCHASE_ORDERS_FOLDER = "Purchase Orders"
PO_FOLDER = "Sample PO"
PO_MAPPINGS_FOLDER = "PO Mappings"

os.makedirs(BASE_FOLDER, exist_ok=True)

def calculate_sha256(file_path):
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


@router.post("/upload/", response_model=UploadPoSchema)
def upload_file(
    db: Session = Depends(get_db),
    client_name: str = Query(..., description="Name of the client uploading the file"),
    file: UploadFile = File(...),
    current_user: User = Depends(security_scheme),
    hash: str = Header(..., description="SHA-256 hash value provided by the client for integrity check"),
    page_id: str = Header(..., description="Page identifier for routing logic"),  
    authorization: str = Header(None, description="Bearer token for authentication"), 
):
    """
    Handle file uploads, validate hash, process the file, and authenticate using token.
    """

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")
    
    token = authorization.split(" ")[1]
    user = validate_token(token, db)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid token or user not found")

    # Check the page_id from header
    if page_id != "PO_Page": 
        raise HTTPException(status_code=400, detail="Invalid page_id.")

    # Define the base folder structure for the client
    client_base_folder = os.path.join(BASE_FOLDER, client_name, PURCHASE_ORDERS_FOLDER)
    po_folder = os.path.join(client_base_folder, PO_FOLDER)
    po_mappings_folder = os.path.join(client_base_folder, PO_MAPPINGS_FOLDER)

    # Create the folder structure if it doesn't exist
    os.makedirs(po_folder, exist_ok=True)
    os.makedirs(po_mappings_folder, exist_ok=True)

    # Generate a file name with the current date and timestamp
    today_date = datetime.utcnow().strftime("%d-%m-%Y")
    utc_timestamp = datetime.utcnow().strftime("%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        raise HTTPException(status_code=400, detail="File must have a valid extension.")

    file_path = os.path.join(po_folder, f"PO-{today_date} -{utc_timestamp}{file_extension}")

    # Save the uploaded file in the Sample PO folder
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Calculate the hash of the uploaded file
    uploaded_file_hash = calculate_sha256(file_path)

    # Compare the client's provided hash with the calculated hash
    if uploaded_file_hash != hash:
        os.remove(file_path) 
        raise HTTPException(status_code=400, detail="Integrity check failed.")

    # Process the file using the automation logic
    try:
        extracted_data = po_to_json(po_folder)
    except Exception as e:
        os.remove(file_path) 
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "file_hash": uploaded_file_hash,
        "saved_path": file_path,
        "status": "File uploaded and processed successfully",
        "extracted_data": extracted_data,
    }
