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
from app.routers.utilities import convert_csv_to_json
from app.routers.utilities import ensure_directory_exists
from app.routers.utilities import calculate_sha256
from app.routers.utilities import get_file_path
from app.routers.utilities import save_file
from app.config.config import settings
from app.routers.utilities import convert_json_to_csv

# Initialize FastAPI router
router = APIRouter()
security_scheme = HTTPBearer()

# Base folder settings from config
base_folder = settings.base_folder
po_folder = settings.purchase_orders_folder
po_mapping = settings.po_mappings_folder
sample_po_folder = settings.sample_po
im_folder = settings.item_master_folder
im_mapping = settings.item_master_mappings_folder
cm_folder = settings.customer_master_folder
cm_mapping = settings.customer_master_mappings_folder

# Function to handle Purchase Order (PO) file uploads
def handle_po_file(db: Session, file: UploadFile, client_name: str, hash: str, page_id: str):
    # Determine the file extension
    file_extension = os.path.splitext(file.filename)[1]
    # Construct file names
    po_file_name = f"{client_name}-{sample_po_folder}{file_extension}"
    po_mappings_file_name = f"{client_name}-{po_mapping}.csv"

    # Construct file paths for PO and PO mappings
    # e-commerce-platform->clientname->purchase-orders->sample-po->clientname-sample-po.pdf
    file_path = get_file_path(client_name, po_folder, sample_po_folder, po_file_name)

    # e-commerce-platform->clientname->purchase-orders->po-mappings->clientname-po-mappings.csv
    po_mappings_folder_path = get_file_path(client_name, po_folder, po_mapping, po_mappings_file_name)

    # Save the uploaded file to the specified path
    save_file(file, file_path)
    # Calculate the hash of the uploaded file and verify its integrity
    uploaded_file_hash = calculate_sha256(file_path)
    if uploaded_file_hash != hash:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Integrity check failed.")

    # Process the CSV file and extract data
    try:
        extracted_data = convert_csv_to_json(page_id)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")
    
    # Process the json to csv 
    # try:
    #     data = convert_json_to_csv(extracted_data, po_mappings_folder_path, po_mappings_file_name)
    # except Exception as e:
    #         os.remove(file_path)
    #         raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "file_hash": uploaded_file_hash,
        "saved_path": file_path,
        "status": "File uploaded and processed successfully",
        "extracted_data": extracted_data,
        #"json_to_csv": data
    }

# Handle Item Master files
def handle_im_file(db: Session, file: UploadFile, client_name: str, hash: str, page_id: str):
    # Determine the file extension
    file_extension = os.path.splitext(file.filename)[1]
    # Construct file names
    im_file_name = f"{client_name}-{im_folder}{file_extension}"
    im_mappings_file_name = f"{client_name}-{im_mapping}.csv"

    # Construct file paths for Item Master and its mappings
    # e-commerce-platform->clientname->item-master->clientname-item-master.xlsx
    file_path = get_file_path(client_name, im_folder, "", im_file_name)

    # e-commerce-platform->clientname->item-master->item-master-mappings->clientname-item-master-mappings.csv
    im_mappings_folder_path = get_file_path(client_name, im_folder, im_mapping, "")

    # Save the uploaded file to the specified path
    save_file(file, file_path)
    # Calculate the hash of the uploaded file and verify its integrity
    uploaded_file_hash = calculate_sha256(file_path)
    if uploaded_file_hash != hash:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Integrity check failed.")

    # Process the CSV file and extract data
    try:
        extracted_data = convert_csv_to_json(page_id)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    #  Process the json to csv 
    # try:
    #     data = convert_json_to_csv(extracted_data, im_mappings_folder_path, im_mappings_file_name)
    # except Exception as e:
    #         os.remove(file_path)
    #         raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "file_hash": uploaded_file_hash,
        "saved_path": file_path,
        "status": "File uploaded and processed successfully",
        "extracted_data": extracted_data,
        #"json_to_excel": data
    }

# Handle Customer Master files
def handle_cm_file(db: Session, file: UploadFile, client_name: str, hash: str, page_id: str):
    # Determine the file extension
    file_extension = os.path.splitext(file.filename)[1]
    # Construct file names
    cm_file_name = f"{client_name}-{cm_folder}{file_extension}"
    cm_mappings_file_name = f"{client_name}-{cm_mapping}.csv"

    # Construct file paths for Customer Master and its mappings
    # e-commerce-platform->clientname->customer-master->clientname-customer-master.xlsx
    file_path = get_file_path(client_name, cm_folder, "", cm_file_name)

    # e-commerce-platform->clientname->customer-master->customer-master-mappings->clientname-customer-master-mappings.csv
    cm_mappings_folder_path = get_file_path(client_name, cm_folder, cm_mapping, "")

    # Save the uploaded file to the specified path
    save_file(file, file_path)
    uploaded_file_hash = calculate_sha256(file_path)
    if uploaded_file_hash != hash:
        os.remove(file_path)
        raise HTTPException(status_code=400, detail="Integrity check failed.")

     # Process the CSV file and extract data
    try:
        extracted_data = convert_csv_to_json(page_id)
    except Exception as e:
        os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")
    # Process the json to csv 
    # try:
    #     data = convert_json_to_csv(extracted_data, cm_mappings_folder_path, cm_mappings_file_name)
    # except Exception as e:
    #         os.remove(file_path)
    #         raise HTTPException(status_code=500, detail=f"File processing failed: {str(e)}")

    return {
        "filename": file.filename,
        "file_hash": uploaded_file_hash,
        "saved_path": file_path,
        "status": "File uploaded and processed successfully",
        "extracted_data": extracted_data,
        #"json_to_excel": data
    }
    
# Endpoint to handle file uploads
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
        "customer_master_page": handle_cm_file
    }

    # Validate page_id and invoke respective function
    if page_id not in handle_file_upload:
        raise HTTPException(status_code=400, detail="Invalid page_id.")

    return handle_file_upload[page_id](db, file, client_name, hash, page_id)