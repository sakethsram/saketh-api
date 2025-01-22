from fastapi import APIRouter, File, UploadFile, HTTPException, Query, Header, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os
import shutil
import hashlib
from datetime import datetime
from app.models import User
from app.schemas import UploadPoSchema
from app.routers.automationscript import po_to_json
from app.security import validate_token
from app.dependencies import get_db

router = APIRouter()
security_scheme = HTTPBearer()

# Base folder for storing files
base_folder = "e_commerce_platform"
purchase_orders_folder = "purchase_orders"
item_master_folder = "item_master"
customer_master_folder = "customer_master"

# Folder structure sub-categories
po_mappings_folder = "po_mappings"
item_master_mappings_folder = "item_master_mappings"
customer_master_mappings_folder = "customer_master_mappings"

def ensure_directory_exists(path: str):
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_sha256(file_path: str) -> str:
    """Calculate the SHA-256 hash of a file."""
    hash_sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def get_file_path(primary_folder: str, client_name: str, mappings_folder: str, file_name: str) -> str:
    """Generate a file path based on the folder structure."""
    today_date = datetime.utcnow().strftime("%d-%m-%Y")
    folder_path = os.path.join(base_folder, primary_folder, client_name, mappings_folder, today_date)
    ensure_directory_exists(folder_path)
    return os.path.join(folder_path, file_name)

def save_file(file: UploadFile, file_path: str):
    """Save the uploaded file to the specified path."""
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

# Handle Purchase Orders
def handle_po_file(db: Session, file: UploadFile, client_name: str, hash: str):
    """Handle Purchase Order files."""
    utc_timestamp = datetime.utcnow().strftime("%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        raise HTTPException(status_code=400, detail="File must have a valid extension.")
    
    file_name = f"purchase_order_{utc_timestamp}{file_extension}"
    file_path = get_file_path(purchase_orders_folder, client_name, purchase_orders_folder, file_name)

    # Ensure PO Mappings folder exists
    po_mappings = os.path.join(base_folder, purchase_orders_folder, client_name, po_mappings_folder)
    ensure_directory_exists(po_mappings)

    # Save file and validate hash
    save_file(file, file_path)
    uploaded_file_hash = calculate_sha256(file_path)
    if uploaded_file_hash != hash:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Integrity check failed.")

    # Process the file using the automation script (PO)
    try:
        extracted_data = po_to_json(file_path)
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

# Handle Item Master files
def handle_im_file(db: Session, file: UploadFile, client_name: str, hash: str):
    """Handle Item Master files."""
    utc_timestamp = datetime.utcnow().strftime("%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        raise HTTPException(status_code=400, detail="File must have a valid extension.")
    
    file_name = f"item_master_{utc_timestamp}{file_extension}"
    file_path = get_file_path(item_master_folder, client_name, item_master_folder, file_name)

    # Ensure Item Master Mappings folder exists
    item_master_mappings = os.path.join(base_folder, item_master_folder, client_name, item_master_mappings_folder)
    ensure_directory_exists(item_master_mappings)

    # Save file and validate hash
    save_file(file, file_path)
    uploaded_file_hash = calculate_sha256(file_path)
    if uploaded_file_hash != hash:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Integrity check failed.")

    # Process the file using the automation script (Item Master)
    try:
        extracted_data = po_to_json(file_path)
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

# Handle Customer Master files
def handle_cm_file(db: Session, file: UploadFile, client_name: str, hash: str):
    """Handle Customer Master files."""
    utc_timestamp = datetime.utcnow().strftime("%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        raise HTTPException(status_code=400, detail="File must have a valid extension.")
    
    file_name = f"customer_master_{utc_timestamp}{file_extension}"
    file_path = get_file_path(customer_master_folder, client_name, customer_master_folder, file_name)

    # Ensure Customer Master Mappings folder exists
    customer_master_mappings = os.path.join(base_folder, customer_master_folder, client_name, customer_master_mappings_folder)
    ensure_directory_exists(customer_master_mappings)

    # Save file and validate hash
    save_file(file, file_path)
    uploaded_file_hash = calculate_sha256(file_path)
    if uploaded_file_hash != hash:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Integrity check failed.")

    # Process the file using the automation script (Customer Master)
    try:
        extracted_data = po_to_json(file_path)
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

# Main upload route with page_id-based dynamic routing
@router.post("/upload/", response_model=UploadPoSchema)
def upload(
    db: Session = Depends(get_db),
    client_name: str = Query(..., description="Name of the client uploading the file"),
    file: UploadFile = File(...),
    current_user: User = Depends(security_scheme),
    hash: str = Header(..., description="SHA-256 hash value provided by the client for integrity check"),
    page_id: str = Header(..., description="Page identifier for routing logic"),
    authorization: str = Header(None, description="Bearer token for authentication"),
):
    """
    Handle file uploads, validate hash, and authenticate using token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Authorization header missing or invalid")

    token = authorization.split(" ")[1]
    user = validate_token(token, db)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid token or user not found")

    # Define function mapping based on page_id
    handle_file_upload = {
        "po_page": handle_po_file,
        "item_master_page": handle_im_file,
        "customer_master_page": handle_cm_file,
    }

    # Validate page_id and invoke respective function
    if page_id not in handle_file_upload:
        raise HTTPException(status_code=400, detail="Invalid page_id.")

    return handle_file_upload[page_id](db, file, client_name, hash)
