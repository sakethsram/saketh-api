from fastapi import APIRouter, File, UploadFile
from fastapi import HTTPException, Query, Header, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
import os
from datetime import datetime
from app.models import User
from app.schemas import UploadPoSchema
from app.security import validate_token
from app.dependencies import get_db
from app.routers.utilities import po_to_json
from app.routers.utilities import ensure_directory_exists
from app.routers.utilities import calculate_sha256
from app.routers.utilities import get_file_path
from app.routers.utilities import save_file
from app.config.config import settings


router = APIRouter()
security_scheme = HTTPBearer()

po_folder = settings.purchase_orders_folder
base_folder = settings.base_folder
po_mapping = settings.po_mappings_folder
im_folder = settings.item_master_folder
im_mapping = settings.item_master_mappings_folder
cm_folder = settings.customer_master_folder
cm_mapping = settings.customer_master_mappings_folder

# Handle Purchase Orders
def handle_po_file(db: Session, file: UploadFile, client_name: str, hash: str):
    """Handle Purchase Order files."""
    utc_timestamp = datetime.now().strftime("%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        raise HTTPException(status_code=400, detail="File must have a valid extension.")
    
    file_name = f"purchase_order_{utc_timestamp}{file_extension}"
    # TODO: Show the example filename with path
    file_path = get_file_path(po_folder, client_name, po_folder, file_name)

    # Ensure PO Mappings folder exists
    # TODO: Show the example filename with path
    po_mappings = os.path.join(base_folder, po_folder, client_name, po_mapping)
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
    utc_timestamp = datetime.now().strftime("%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        raise HTTPException(status_code=400, detail="File must have a valid extension.")
    
    file_name = f"item_master_{utc_timestamp}{file_extension}"
    # TODO: Show the example filename with path
    file_path = get_file_path(im_folder, client_name, im_folder, file_name)

    # TODO: Show the example filename with path
    item_master_mappings = os.path.join(base_folder, im_folder, client_name, im_mapping)
    ensure_directory_exists(item_master_mappings)

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
    utc_timestamp = datetime.now().strftime("%H%M%S")
    file_extension = os.path.splitext(file.filename)[1]
    if not file_extension:
        raise HTTPException(status_code=400, detail="File must have a valid extension.")
    
    file_name = f"customer_master_{utc_timestamp}{file_extension}"
    # TODO: Show the example filename with path
    file_path = get_file_path(cm_folder, client_name, cm_folder, file_name)

    # Ensure Customer Master Mappings folder exists
    # TODO: Show the example filename with path
    customer_master_mappings = os.path.join(base_folder, cm_folder, client_name, cm_mapping)
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
